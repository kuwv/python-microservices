import os

import requests
from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from .token import JWKS, JWTBearerTokenValidator, JWTAuthorizationCredentials

jwks = JWKS.parse_obj(
    requests.get(
        "http://keycloak:8080/auth/realms/master/protocol/openid-connect/certs"
    ).json()
)
auth = JWTBearerTokenValidator(jwks)


async def get_current_user(
    credentials: JWTAuthorizationCredentials = Depends(auth)
) -> str:
    try:
        return credentials.claims["username"]
    except KeyError:
        HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="invalid_token: Username missing"
        )
