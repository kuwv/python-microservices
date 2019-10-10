from typing import Any, Dict, Optional, List

from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
import json
import jwt
from jwt.exceptions import (
    DecodeError, ExpiredSignatureError, ImmatureSignatureError, InvalidIssuerError,
)


# https://tools.ietf.org/html/rfc7517#page-5
JWK = Dict[str, Any]


class JWKS(BaseModel):
    keys: List[JWK]


class JWTAuthorizationCredentials(BaseModel):
    jwt_token: str
    header: Dict[str, str]
    claims: Dict[str, str]
    signature: str
    message: str


class JWTBearer(HTTPBearer):
    def __init__(self, jwks: JWKS, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.jwks = jwks

    def verify_jwk_token(self, jwt_credentials: JWTAuthorizationCredentials) -> bool:
        try:
            kid = jwt_credentials.header["kid"]
            public_key = [k for k in self.jwks.keys if k['kid'] == kid][0]
        except KeyError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="JWK public key not found"
            )

        key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(public_key))

        try:
            return jwt.decode(jwt_credentials.jwt_token,
                              key=key,
                              algorithms=[public_key['alg']])
        except DecodeError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Authorization token cannot be decoded"
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Authorization token has expired"
            )
        except ImmatureSignatureError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Authorization token immature"
            )
        except InvalidIssuerError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Authorization token from unrecognized issuer"
            )


    async def __call__(self, request: Request) -> Optional[JWTAuthorizationCredentials]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="No supported authorization token scheme found"
                )

            jwt_token = credentials.credentials
            message, signature = jwt_token.rsplit(".", 1)

            try:
                jwt_credentials = JWTAuthorizationCredentials(
                    jwt_token=jwt_token,
                    header=jwt.get_unverified_header(jwt_token),
                    claims=jwt.decode(jwt_token, verify=False),
                    signature=signature,
                    message=message,
                )
            except JWTError:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="JWK invalid")

            if not self.verify_jwk_token(jwt_credentials):
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="JWK invalid")

            return jwt_credentials
