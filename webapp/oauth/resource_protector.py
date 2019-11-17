import json
import functools
from contextlib import contextmanager
from typing import Any, Dict, Optional, List

from starlette.requests import Request

from authlib.oauth2 import ResourceProtector as _ResourceProtector
from authlib.oauth2.rfc6749 import MissingAuthorizationError
from .logging import audit
from .models import OAuth2AuthorizationCodeBearer
import traceback
import logging


class ResourceProtector(_ResourceProtector, OAuth2AuthorizationCodeBearer):
    """A protecting method for resource servers. Creating a ``require_oauth``
    decorator easily with ResourceProtector
    """
    def __init__(
        self,
        authorization_url: str,
        token_url: str,
        scopes: dict = None,
        auto_error: bool = True
    ):
        _ResourceProtector.__init__(self)
        OAuth2AuthorizationCodeBearer.__init__(
            self, authorization_url, token_url, scopes, auto_error
        )

    # @audit
    async def acquire_token(
        self, request: Request, scope: str = None, operator: str = 'AND'
    ):
        """A method to acquire current valid token with the given scope.

        :param request: FastAPI HTTP request instance
        :param scope: string of space delimted scope values
        :param operator: value of "AND" or "OR"
        :return: token object
        """
        if not callable(operator):
            operator = operator.upper()
        token = self.validate_request(scope, request, operator)
        return token

    async def __call__(
        self,
        request: Request,
        scope: str = None,
        operator: str = 'AND',
        optional: bool = False
    ):
        return await self.acquire_token(request, scope, operator)
