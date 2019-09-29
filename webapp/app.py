import logging
import os
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from urllib.parse import urlencode
from starlette.responses import PlainTextResponse, RedirectResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


@app.get("/api")
async def root():
    return {"message": "Hello World"}

@app.get("/api/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.put("/api/items/{item_id}")
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
