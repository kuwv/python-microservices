import json
import functools
from contextlib import contextmanager
from typing import Any, Dict, Optional, List

from starlette.requests import Request

from authlib.oauth2 import ResourceProtector as _ResourceProtector
from authlib.oauth2.rfc6749 import MissingAuthorizationError
from .errors import oauth_exception
from .models import OAuth2AuthorizationCodeBearer
import traceback
import logging


class ResourceProtector(_ResourceProtector, OAuth2AuthorizationCodeBearer):
    """A protecting method for resource servers. Creating a ``require_oauth``
    decorator easily with ResourceProtector::

        from authlib.integrations.flask_oauth2 import ResourceProtector

        require_oauth = ResourceProtector()

        # add bearer token validator
        from authlib.oauth2.rfc6750 import BearerTokenValidator
        from project.models import Token

        class MyBearerTokenValidator(BearerTokenValidator):
            def authenticate_token(self, token:str):
                return Token.query.filter_by(access_token=token).first()

            def request_invalid(self, request:Request) -> bool:
                return False

            def token_revoked(self, token:str) -> bool:
                return False

        require_oauth.register_token_validator(MyBearerTokenValidator())

        # protect resource with require_oauth
        @app.route('/user')
        @require_oauth('profile')
        def user_profile():
            user = User.query.get(current_token.user_id)
            return jsonify(user.to_dict())
    """
    def __init__(
        self,
        authorization_url: str,
        token_url: str,
        auto_error: bool = True
    ):
        _ResourceProtector.__init__(self)
        OAuth2AuthorizationCodeBearer.__init__(
            self,
            authorizationUrl=authorization_url,
            tokenUrl=token_url,
            auto_error=auto_error
        )

    @oauth_exception
    async def acquire_token(
         self,
         request: Request,
         scope: str = None,
         operator: str = 'AND'
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
