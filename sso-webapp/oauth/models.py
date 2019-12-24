from typing import List, Optional
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.security.oauth2 import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from starlette.requests import Request


class OAuth2AuthorizationCodeBearer(OAuth2):
    def __init__(
        self,
        authorization_url: str,
        token_url: str,
        refresh_url: str = None,
        scopes: dict = {},
        scheme_name: str = None,
        auto_error: bool = True,
    ):
        flows = OAuthFlowsModel(
            authorizationCode={
                "authorizationUrl": authorization_url,
                "tokenUrl": token_url,
                "refreshUrl": refresh_url,
                "scopes": scopes,
            })
        super().__init__(
            flows=flows, scheme_name=scheme_name, auto_error=auto_error
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
 
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param
