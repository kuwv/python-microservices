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
from oauth.resource_protector import ResourceProtector
import pprint

# JWT
from oauth.token import JWK, JWKS, JWTBearerTokenValidator, JWTAuthorizationCredentials

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

auth = ResourceProtector(
    authorization_url=config.authorization_url,
    token_url=config.token_url,
    refresh_url=None,
    scopes={"profile": "User information"},
    auto_error=False,
)
# TODO: check if URL exists
jwks = JWKS.parse_obj(requests.get(config.svc_jwks_url).json())
auth.register_token_validator(
    JWTBearerTokenValidator(
        jwks,
        # TODO: Should minimal scopes be handled here too
        headers=config.headers,
        realm=config.realm,
        audience=config.audience,
        issuer=config.issuer,
        leeway=config.leeway,
        options=config.options
    )
)

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

@app.get("/secure", dependencies=[Depends(auth)])
async def secure() -> bool:
    return True

@app.get("/not_secure")
async def not_secure() -> bool:
    return True

@app.get("/token", response_model=JWTAuthorizationCredentials)
async def get_credentials(
    token: JWTAuthorizationCredentials = Security(auth, scopes=['profile', 'email'])
):
    if token is None:
        return {"msg": "No token found"}
    return token

@app.get("/items", dependencies=[Depends(auth)])
async def read_items():
    return True

@app.get("/items/{item_id}", dependencies=[Depends(auth)])
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}", dependencies=[Depends(auth)])
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
