import os
from pydantic import BaseModel
from typing import Any, Dict, Optional, List


title: tuple = "WebApp"
description: str = "This is a web application"
version: str = "2.5.0"

uri_prefix: str = os.getenv('WEBAPP_URI_PREFIX', '')

# OpenAPI URI
oapi_prefix: str = os.getenv('WEBAPP_OAPI_PREFIX', uri_prefix)
oapi_url: str = os.getenv('WEBAPP_OAPI_URL', f"{oapi_prefix}/openapi.json")
oapi_redirect_url: str = f"{oapi_prefix}/docs/oauth2-redirect"

# Docs URI
docs_url: str = os.getenv('WEBAPP_DOCS_URI', f"{uri_prefix}/docs")

# ReDoc URI
redoc_url: str = os.getenv('WEBAPP_REDOC_URI', f"{uri_prefix}/redoc")

# Static URI
static_url: str = os.getenv('WEBAP_STATIC_URI', uri_prefix)

# TODO: Provide OpenID-Connect alternative
auth_connection: str = os.getenv('WEBAPP_AUTH_CONNECTION', 'http')
auth_host: str = os.getenv('WEBAPP_AUTH_HOST', 'localhost')
auth_port: int = os.getenv('WEBAPP_AUTH_PORT', '8080')
auth_realm: str = os.getenv('WEBAPP_AUTH_REALM', 'master')
auth_url_base: str = os.getenv(
    'WEBAPP_AUTH_URL_BASE',
    f"{auth_connection}://{auth_host}:{auth_port}/auth/realms/{auth_realm}"
)
authorization_url: str = os.getenv(
    'WEBAPP_AUTH_URL',
    f"{auth_url_base}/protocol/openid-connect/auth"
)
token_url: str = os.getenv(
    'WEBAPP_TOKEN_URL',
    f"{auth_url_base}/protocol/openid-connect/token"
)
refresh_url: str = os.getenv(
    'WEBAPP_REFRESH_URL',
    f"{auth_url_base}/protocol/openid-connect/token"
)

# Connection between SSO and APP
svc_auth_client_id: str = os.getenv('WEBAPP_SVC_AUTH_CLIENT_ID')
svc_auth_client_secret: str = os.getenv('WEBAPP_SVC_AUTH_CLIENT_SECRET')
svc_auth_connection: str = os.getenv(
    'WEBAPP_SVC_AUTH_CONNECTION', auth_connection
)
svc_auth_host: str = os.getenv('WEBAPP_SVC_AUTH_HOST', auth_host)
svc_auth_port: int = os.getenv('WEBAPP_SVC_AUTH_PORT', auth_port)
svc_auth_url_base: str = os.getenv(
    'WEBAPP_SVC_AUTH_URL_BASE',
    f"{svc_auth_connection}://{svc_auth_host}:{svc_auth_port}/auth/realms/{auth_realm}"
)
svc_jwks_url: str = os.getenv(
    'WEBAPP_SVC_JWKS_URL',
    f'{svc_auth_url_base}/protocol/openid-connect/certs'
)
svc_introspect_url: str = os.getenv(
    'WEBAPP_SVC_INTROSPECT_URL',
    f"{svc_auth_url_base}/protocol/openid-connect/token/introspect"
)

# authlib configuration
realm: str = auth_realm
headers: List[Dict] = [{'email_verified': True}]
