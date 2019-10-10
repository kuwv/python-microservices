import logging
import os
from fastapi import Depends, FastAPI, Header
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from urllib.parse import urlencode
from starlette.responses import PlainTextResponse, RedirectResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8180/auth/realms/master/tokens/login")

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

@app.get("/webapp")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@app.get("/items")
async def read_items(*,
                     x_userinfo: str = Header(None),
                     x_access_token: str = Header(None),
                     x_id_token: str = Header(None),
                     user_agent: str = Header(None)):
    return {"User-Agent": user_agent}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

# @app.route('/login')
# async def login():
#     self.client = get_client()
#     return Redirect(get_authorization())
#
# @app.route('/oidc-callback')
# def auth_callback():
#     self.client = get_client()
#     aresp = get_authorization_response(self.client)
#     session['user_info'] = self.client.get_userinfo(self.client, aresp)
#     return redirect(url_for('index'))
