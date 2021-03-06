import logging
import os
import requests
import config
from fastapi import Depends, FastAPI, Security
from fastapi.security import SecurityScopes
from pydantic import BaseModel
from urllib.parse import urlencode
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse
from security.resource_protector import ResourceProtector
from starlette.staticfiles import StaticFiles


# JWT
from security.token import (
    JWK, JWKS, JWTBearerTokenValidator, JWTAuthorizationCredentials
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

auth = ResourceProtector(
    authorization_url=config.authorization_url,
    token_url=config.token_url,
    refresh_url=None,
    auto_error=False,
)
# TODO: check if URL exists
jwks = JWKS.parse_obj(requests.get(config.svc_jwks_url).json())
auth.register_token_validator(
    JWTBearerTokenValidator(
        jwks,
        # TODO: Should minimal scopes be handled here too
        headers=config.headers,
        realm=config.realm
    )
)

app = FastAPI(
    title=config.title,
    description=config.description,
    version=config.version,
    openapi_url=config.oapi_url,
    docs_url=config.docs_url,
    redoc_url=config.redoc_url,
    swagger_ui_oauth2_redirect_url=config.oapi_redirect_url
)

@app.get("/secure", dependencies=[Depends(auth)])
async def secure() -> bool:
    return True

@app.get("/insecure")
async def insecure() -> bool:
    return True

@app.get("/token", response_model=JWTAuthorizationCredentials)
async def get_credentials(
    token: JWTAuthorizationCredentials = Security(auth, scopes=['profile', 'email'])
):
    if token is None:
        return {"msg": "No token found"}
    return token

app.mount(config.static_url, StaticFiles(directory='static/dist', html=True), name='static')
