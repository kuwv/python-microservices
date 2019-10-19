import logging
import os
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel
from urllib.parse import urlencode
from starlette.responses import PlainTextResponse, RedirectResponse
from oauth.authorization import OAuth2AuthorizationCodeBearer
from oauth.resource_protector import ResourceProtector

# JWT
from oauth.token import JWTBearer
from oauth.auth import jwks

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
app = FastAPI()

authorization_url="http://localhost:8180/auth/realms/master/protocol/openid-connect/auth"
token_url="http://localhost:8180/auth/realms/master/protocol/openid-connect/token"
auth = JWTBearer(authorization_url, token_url, jwks)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=authorization_url,
    tokenUrl=token_url,
    auto_error=False
)

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

@app.get("/dao")
async def read_items(token: str = Depends(oauth2_scheme)):
    if token is None:
        return {"msg": "No token found"}
    return {"token": token}

@app.get("/items")
async def read_items(*,
                     x_userinfo: str = Header(None),
                     x_access_token: str = Header(None),
                     x_id_token: str = Header(None),
                     user_agent: str = Header(None)):
    return {
        "id_token": x_id_token,
        "User-Agent": user_agent
    }

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
