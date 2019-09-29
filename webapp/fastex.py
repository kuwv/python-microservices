import logging

from fastapi import FastAPI
from starlette.responses import RedirectResponse
from starlette.testclient import TestClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI()


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}


subapi = FastAPI(openapi_prefix="/subapi")


@subapi.get("/sub")
async def read_sub():
    return {"message": "Hello World from sub API"}


@subapi.get("/redirect")
async def redirect():
    url = app.url_path_for("redirected")
    response = RedirectResponse(url=url)
    return response


@subapi.get("/redirected")
async def redirected():
    logger.debug("REDIRECTED")
    return {"message": "you've been redirected"}


app.mount("/subapi", subapi)


client = TestClient(app)


def test_redirect_subapi():
    url = app.url_path_for("redirect")
    response = client.get(url)
    assert response.json() == {"message": "you've been redirected"}
