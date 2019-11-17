import logging
import os
import requests
from fastapi import Depends, FastAPI, Security
from pydantic import BaseModel
from urllib.parse import urlencode
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse
from oauth.resource_protector import ResourceProtector

# JWT
from oauth.token import JWK, JWKS, JWTBearerTokenValidator
import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

auth = ResourceProtector(
    config.authorization_url, config.token_url, auto_error=False
)
jwks = JWKS.parse_obj(requests.get(config.jwks_uri).json())
auth.register_token_validator(
    JWTBearerTokenValidator(jwks,
        headers=config.headers,
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

@app.get("/token", response_model=JWK)
async def read_items(token: str = Security(auth, scopes=['profile'])):
    if token is None:
        return {"msg": "No token found"}
    return {"token": token}

@app.get("/items", dependencies=[Depends(auth)])
async def read_items():
    return True

@app.get("/items/{item_id}", dependencies=[Depends(auth)])
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}", dependencies=[Depends(auth)])
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
