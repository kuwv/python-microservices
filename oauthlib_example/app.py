from fastapi import Depends, FastAPI

from token import JWTBearer
from auth import jwks
from user import router as user_router

app = FastAPI()
auth = JWTBearer(jwks)


@app.get("/secure", dependencies=[Depends(auth)])
async def secure() -> bool:
    return True


@app.get("/not_secure")
async def not_secure() -> bool:
    return True


app.include_router(user_router, prefix="/user", dependencies=[Depends(auth)])
