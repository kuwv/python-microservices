import os
from pydantic import BaseModel
from typing import Any, Dict, Optional, List


headers: List[Dict] = [{'email_verified': True}]
audience: str = None
issuer: str = None
leeway: int = 0
options: Dict = {
    "verify_aud": True,
    "verify_exp": True,
    "verify_iat": True,
    "verify_iss": True,
    "verify_nbf": True,
    "verify_signature": True,
    "require_exp": True,
    "require_iat": True,
    "require_nbf": True
}

# TODO: Provide OpenID-Connect alternative
auth_protocol: str = os.getenv("AUTH_PROTOCOL", "http")
auth_host: str = os.getenv("AUTH_HOST", "localhost")
auth_port: int = os.getenv("AUTH_PORT", "8180")
auth_url: str = os.getenv(
    "AUTH_URL",
    f"{auth_protocol}://{auth_host}:{auth_port}/auth/realms/master"
)
authorization_url: str = os.getenv(
    "WEBAPP_AUTH_URL",
    f"{auth_url}/protocol/openid-connect/auth"
)
token_url: str = os.getenv(
    "WEBAPP_TOKEN_URL",
    f"{auth_url}/protocol/openid-connect/token"
)

private_auth_protocol: str = os.getenv("PRIVATE_AUTH_PROTOCOL", "http")
private_auth_host: str = os.getenv("PRIVATE_AUTH_HOST", "localhost")
private_auth_port: int = os.getenv("PRIVATE_AUTH_PORT", "8180")
private_auth_url: str = os.getenv(
    "PRIVATE_AUTH_URL",
    f"{private_auth_protocol}://{private_auth_host}:{private_auth_port}/auth/realms/master"
)

jwks_uri: str = os.getenv(
    "WEBAPP_JWKS_URI",
    f"{private_auth_url}/protocol/openid-connect/certs"
)
