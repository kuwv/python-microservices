from typing import Any, Dict, Optional, List

from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
import json
import jwt
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidIssuerError,
)

from .models import OAuth2AuthorizationCodeBearer
from .errors import token_exception
from authlib.oauth2.rfc6750 import BearerTokenValidator

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


class JWTBearer(BearerTokenValidator):
    def __init__(self, jwks: JWKS, realm: str=None):
        print("Token validator registered")
        self.jwks = jwks
        super().__init__(realm)

    @token_exception
    def get_credentials(self, token_string) -> JWTAuthorizationCredentials:
        message, signature = token_string.rsplit(".", 1)

        credentials = JWTAuthorizationCredentials(
            token_string=token_string,
            header=jwt.get_unverified_header(token_string),
            claims=jwt.decode(token_string, verify=False),
            signature=signature,
            message=message,
        )

        return credentials

    @token_exception
    def authenticate_token(
        self, credentials: JWTAuthorizationCredentials
    ) -> bool:
        kid = credentials.header["kid"]
        public_key = [k for k in self.jwks.keys if k['kid'] == kid][0]
        key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(public_key))

        return jwt.decode(
            credentials.token_string,
            key=key,
            algorithms=[public_key['alg']]
        )

    def request_invalid(self, request: Request) -> bool:
        return False

    def token_revoked(self, token: str) -> bool:
        return False

    def __call__(
        self, token_string: str, scope: str, request: Request, scope_operator: str
    ) -> Optional[JWTAuthorizationCredentials]:
        if token_string:
            credentials = self.get_credentials(token_string)

            if not self.authenticate_token(credentials):
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="invalid_token - JWK invalid"
                )
            return credentials
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="invalid_token - No JWT Found"
            )
