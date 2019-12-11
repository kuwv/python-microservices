from typing import Any, Dict, Optional, List
from pydantic import BaseModel, ValidationError
from starlette.requests import Request
from fastapi.security import SecurityScopes
from fastapi import HTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN
)
import json
import base64

from authlib.jose import jwk
from authlib.jose import jwt

from authlib.oauth2.rfc6750 import BearerTokenValidator
from .logging import AuthAudit
from pprint import pprint


# https://tools.ietf.org/html/rfc7517#page-5
JWK = Dict[str, Any]

class JWKS(BaseModel):
    keys: List[JWK]

class JWTAuthorizationCredentials(BaseModel):
    token_string: str
    header: Dict[str, str]
    claims: Dict[str, Any]
    message: str
    signature: str

class AuthorizationCredentials(BaseModel):
    token_string: str
    header: Optional[Dict[str, str]]
    claims: Dict[str, Any]
    message: Optional[str]
    signature: Optional[str]

class JWTBearerTokenValidator(BearerTokenValidator):
    def __init__(
        self,
        jwks: JWKS,
        realm: str = None,
        headers: List[dict] = [],
        **config: Any
    ):
        self.jwks = jwks
        self.headers = headers
        self.config = config
        super().__init__(realm)

    # @AuthAudit()
    def authenticate_token(self, token_string: str) -> bool:
        # TODO: Handle JKU
        header,message,signature = token_string.split('.')
        padding = ("=" * ((4 - len(header) % 4) % 4))
        headers = json.loads(base64.b64decode(header+padding).decode('utf8'))
        matching_key = [k for k in self.jwks.keys if k['kid'] == headers['kid']][0]

        key = jwk.loads(matching_key)
        token = jwt.decode(token_string, key)
        token.validate()

        # TODO: deprecate this
        self.credentials = JWTAuthorizationCredentials(
            token_string=token_string,
            header=headers,
            claims=token,
            message=message,
            signature=signature
        )

        return token

    def request_invalid(self, request: Request) -> bool:
        """
        Check if the HTTP request is valid or not.
        """
        # TODO: Handle request to allow HBAC and audit
        # TODO: Can subject be a group or service account (impersonation)?
        if 'headers' in self.config:
            for h in self.headers['headers']:
                for k in h.keys():
                    if h[k] != self.credentials.claims[k]:
                        return True
        return False

    def token_revoked(self, token: str) -> bool:
        """
        Check if this token is revoked.
        Query introspection when:
          - if MAC based
          - if JWT lifetime (exp) is higher than config policy
          - if refresh token for client
        Requires client for RPT
        """
        return False

    def __call__(
        self,
        token_string: str,
        scope: str,
        request: Request,
        scope_operator: str = 'AND'
    ) -> Optional[JWTAuthorizationCredentials]:
        if self.request_invalid(request):
            raise InvalidRequestError()
        token = self.authenticate_token(token_string)
        if not token:
            raise InvalidTokenError(realm=self.realm)
        # TODO: JWTClaims does not implement get_expires_at()
        # if self.token_expired(token):
        #     raise InvalidTokenError(realm=self.realm)
        if self.token_revoked(token):
            raise InvalidTokenError(realm=self.realm)
        # TODO: JWTClaims does not implement get_scope()
        # if self.scope_insufficient(token, scope, scope_operator):
        #     raise InsufficientScopeError()
        return self.credentials
