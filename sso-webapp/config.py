import os
from pydantic import BaseModel
from typing import Any, Dict, Optional, List

title: tuple = 'webapp'
description: str = 'This is a web application'
version: str = '2.1.3'

uri_prefix: str = os.getenv('WEBAPP_URI_PREFIX', '')

# Static URI
static_url: str = os.getenv('WEBAP_URI_STATIC', '/')

# OpenAPI URI
oapi_prefix: str = os.getenv('WEBAPP_OAPI_PREFIX', uri_prefix)
oapi_url: str = os.getenv('WEBAPP_OAPI_URL', f"{oapi_prefix}/openapi.json")
oapi_redirect_url: str = f"{oapi_prefix}/docs/oauth2-redirect"

# Docs URI
docs_url: str = os.getenv('WEBAPP_URI_DOCS', '/docs')

# ReDoc URI
redoc_url: str = os.getenv('WEBAPP_URI_REDOC', '/redoc')

# TODO: Provide OpenID-Connect alternative
auth_protocol: str = os.getenv('WEBAPP_AUTH_PROTOCOL', 'http')
auth_host: str = os.getenv('WEBAPP_AUTH_HOST', 'localhost')
auth_port: int = os.getenv('WEBAPP_AUTH_PORT', '8080')
auth_realm: str = os.getenv('WEBAPP_AUTH_REALM', 'master')
auth_url_base: str = os.getenv(
    'WEBAPP_AUTH_URL_BASE',
    f"{auth_protocol}://{auth_host}:{auth_port}/auth/realms/{auth_realm}"
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
auth_svc_client_id: str = os.getenv('WEBAPP_AUTH_SVC_CLIENT_ID')
auth_svc_client_secret: str = os.getenv('WEBAPP_AUTH_SVC_CLIENT_SECRET')
auth_svc_protocol: str = os.getenv(
    'WEBAPP_AUTH_SVC_PROTOCOL', auth_protocol
)
auth_svc_host: str = os.getenv('WEBAPP_AUTH_SVC_HOST', auth_host)
auth_svc_port: int = os.getenv('WEBAPP_AUTH_SVC_PORT', auth_port)
auth_svc_url_base: str = os.getenv(
    'WEBAPP_AUTH_SVC_URL_BASE',
    f"{auth_svc_protocol}://{auth_svc_host}:{auth_svc_port}/auth/realms/{auth_realm}"
)
svc_jwks_url: str = os.getenv(
    'WEBAPP_SVC_JWKS_URL',
    f'{auth_svc_url_base}/protocol/openid-connect/certs'
)
svc_introspect_url: str = os.getenv(
    'WEBAPP_SVC_INTROSPECT_URL',
    f"{auth_svc_url_base}/protocol/openid-connect/token/introspect"
)

# authlib configuration
realm: str = auth_realm
headers: List[Dict] = [{'email_verified': True}]
