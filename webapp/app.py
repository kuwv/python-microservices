import logging
import os
import requests
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel
from urllib.parse import urlencode
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse
from oauth.resource_protector import ResourceProtector

# JWT
from oauth.token import JWK, JWKS, JWTBearer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
app = FastAPI()

auth_protocol=os.getenv("AUTH_PROTOCOL", "http")
auth_host=os.getenv("AUTH_HOST", "localhost")
auth_port=os.getenv("AUTH_PORT", "8180")
auth_url=os.getenv(
    "AUTH_URL",
    f"{auth_protocol}://{auth_host}:{auth_port}/auth"
)
authorization_url=os.getenv(
    "WEBAPP_AUTH_URL",
    f"{auth_url}/realms/master/protocol/openid-connect/auth"
)
token_url=os.getenv(
    "WEBAPP_TOKEN_URL",
    f"{auth_url}/realms/master/protocol/openid-connect/token"
)
jwks_uri=os.getenv(
    "WEBAPP_JWKS_URI",
    f"{auth_url}/realms/master/protocol/openid-connect/certs"
)

oauth2_scheme = ResourceProtector(
    authorization_url=authorization_url,
    token_url=token_url,
    auto_error=False
)
jwks = JWKS.parse_obj(requests.get(jwks_uri).json())
oauth2_scheme.register_token_validator(JWTBearer(jwks))

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

@app.get("/secure", dependencies=[Depends(oauth2_scheme)])
async def secure() -> bool:
    return True

@app.get("/not_secure")
async def not_secure() -> bool:
    return True

@app.get("/token", response_model=JWK)
async def read_items(token: str = Depends(oauth2_scheme)):
    if token is None:
        return {"msg": "No token found"}
    return {"token": token}

@app.get("/items", dependencies=[Depends(oauth2_scheme)])
async def read_items():
    return True

@app.get("/items/{item_id}", dependencies=[Depends(oauth2_scheme)])
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}", dependencies=[Depends(oauth2_scheme)])
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
