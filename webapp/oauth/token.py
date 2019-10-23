from typing import Any, Dict, Optional, List

from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
import json
import jwt
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidIssuerError,
)

from .authorization import OAuth2AuthorizationCodeBearer
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

    def authenticate_token(
        self, jwt_credentials: JWTAuthorizationCredentials
    ) -> bool:
        print("Authenticate token")
        try:
            kid = jwt_credentials.header["kid"]
            public_key = [k for k in self.jwks.keys if k['kid'] == kid][0]
        except KeyError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="JWK public key not found"
            )

        key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(public_key))

        try:
            return jwt.decode(
                jwt_credentials.token_string,
                key=key,
                algorithms=[public_key['alg']]
            )
        except DecodeError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Authorization token cannot be decoded"
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Authorization token has expired"
            )
        except ImmatureSignatureError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Authorization token immature"
            )
        except InvalidIssuerError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Authorization token from unrecognized issuer"
            )

    def request_invalid(self, request: Request) -> bool:
        print("Request invalid")
        return False

    def token_revoked(self, token: str) -> bool:
        print("Token revoked")
        return False

    def __call__(
        self, token_string: str, scope: str, request: Request, scope_operator: str
    ) -> Optional[JWTAuthorizationCredentials]:
        print("Here")
        if token_string:
            message, signature = token_string.rsplit(".", 1)

            try:
                print("Trying jwt")
                jwt_credentials = JWTAuthorizationCredentials(
                    token_string=token_string,
                    header=jwt.get_unverified_header(token_string),
                    claims=jwt.decode(token_string, verify=False),
                    signature=signature,
                    message=message,
                )
            except JWTError:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="JWK invalid"
                )

            if not self.authenticate_token(jwt_credentials):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="JWK invalid"
                )

            return jwt_credentials
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="No JWT Found"
            )
