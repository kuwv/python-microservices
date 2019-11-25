import os
from pydantic import BaseModel
from typing import Any, Dict, Optional, List


# TODO: Provide OpenID-Connect alternative
auth_connection: str = os.getenv("WEBAPP_AUTH_CONNECTION", "http")
auth_host: str = os.getenv("WEBAPP_AUTH_HOST", "localhost")
auth_port: int = os.getenv("WEBAPP_AUTH_PORT", "8080")
auth_realm: str = os.getenv("WEBAPP_AUTH_REALM", "master")
auth_url_base: str = os.getenv(
    "WEBAPP_AUTH_URL_BASE",
    f"{auth_connection}://{auth_host}:{auth_port}/auth/realms/{auth_realm}"
)
authorization_url: str = os.getenv(
    "WEBAPP_AUTH_URL",
    f"{auth_url_base}/protocol/openid-connect/auth"
)
token_url: str = os.getenv(
    "WEBAPP_TOKEN_URL",
    f"{auth_url_base}/protocol/openid-connect/token"
)
refresh_url: str = os.getenv(
    "WEBAPP_REFRESH_URL",
    f"{auth_url_base}/protocol/openid-connect/token"
)

svc_auth_connection: str = os.getenv(
    "WEBAPP_SVC_AUTH_CONNECTION", auth_connection
)
svc_auth_host: str = os.getenv("WEBAPP_SVC_AUTH_HOST", auth_host)
svc_auth_port: int = os.getenv("WEBAPP_SVC_AUTH_PORT", auth_port)
svc_auth_url_base: str = os.getenv(
    "WEBAPP_SVC_AUTH_URL_BASE",
    f"{svc_auth_connection}://{svc_auth_host}:{svc_auth_port}/auth/realms/{auth_realm}"
)
svc_jwks_url: str = os.getenv(
    "WEBAPP_SVC_JWKS_URL",
    f"{svc_auth_url_base}/protocol/openid-connect/certs"
)
svc_introspect_url: str = os.getenv(
    "WEBAPP_SVC_INTROSPECT_URL",
    f"{svc_auth_url_base}/protocol/openid-connect/token/introspect"
)

# authlib configuration
realm: str = auth_realm
headers: List[Dict] = [{'email_verified': True}]

# PyJWT configuration
audience: str = [f"{auth_realm}-realm"]
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
