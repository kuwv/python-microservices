from typing import Any, Dict, Optional, List
from pydantic import BaseModel, ValidationError
from starlette.requests import Request
from fastapi.security import (
    SecurityScopes
)
import json
import jwt

# TODO: Issue with KeyCloak decode :(
# from authlib.jose import JsonWebKey
# from authlib.jose import JWK_ALGORITHMS
# from authlib.jose import jwk

from authlib.oauth2.rfc6750 import BearerTokenValidator
from .logging import JWTAuditAuthentication


# https://tools.ietf.org/html/rfc7517#page-5
JWK = Dict[str, Any]

class JWKS(BaseModel):
    keys: List[JWK]

class JWTAuthorizationCredentials(BaseModel):
    token_string: str
    header: Dict[str, str]
    claims: Dict[str, str]
    signature: str
    message: str


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

    @JWTAuditAuthentication()
    def authenticate_token(self, token_string: str) -> bool:
        # TODO: Handle JKU
        kid = self.credentials.header['kid']
        jwk = [k for k in self.jwks.keys if k['kid'] == kid][0]

        # TODO: Check for HASH (oct)
        if jwk['kty'] == 'RSA':
            key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
        if jwk['kty'] == 'EC':
            key = jwt.algorithms.ECAlgorithm.from_jwk(json.dumps(jwk))

        return jwt.decode(
            self.credentials.token_string, key=key, algorithms=[jwk['alg']],
            **self.config
        )

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
        message, signature = token_string.rsplit('.', 1)
        self.credentials = JWTAuthorizationCredentials(
            token_string=token_string,
            header=jwt.get_unverified_header(token_string),
            claims=jwt.decode(token_string, verify=False),
            signature=signature,
            message=message
        )
        self.request_invalid(request)
        self.authenticate_token(token_string)
        return self.credentials
