import os

import requests
from fastapi import Depends, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from .token import JWKS, JWTBearer, JWTAuthorizationCredentials

jwks = JWKS.parse_obj(
    requests.get(
        "http://localhost:8180/auth/realms/master/protocol/openid-connect/certs"
    ).json()
)
authorization_url="http://localhost:8180/auth/realms/master/protocol/openid-connect/auth"
token_url="http://localhost:8180/auth/realms/master/protocol/openid-connect/token"
auth = JWTBearer(authorization_url, token_url, jwks)


async def get_current_user(
    credentials: JWTAuthorizationCredentials = Depends(auth)
) -> str:
    try:
        return credentials.claims["username"]
    except KeyError:
        HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Username missing")
