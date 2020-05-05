import json
import os
from pydantic import BaseModel
from typing import Any, Dict, Optional, List


def init():
    # template = Template("""{%- for k, v in variables %}
    # {{ k }}={{ v }}
    # {%- endfor %}
    # """)
    # variables = [e for e in os.environ.items() if e[0].startswith('WEBAPP_')]
    # t = template.render(variables=variables)
    # with open('./static/config.json', 'w') as f:
    #     f.write(t)
    pass

title: tuple = 'webapp'
description: str = 'This is a web application'
version: str = '2.1.3'

origins: str = os.getenv('WEBAPP_ORIGINS', '').split(',')

path_prefix: str = os.getenv('WEBAPP_PATH_PREFIX', '')

# Static URI
static_url: str = os.getenv('WEBAP_PATH_STATIC', '/')

# OpenAPI URI
oapi_prefix: str = os.getenv('WEBAPP_OAPI_PREFIX', path_prefix)
oapi_url: str = os.getenv('WEBAPP_OAPI_URL', f"{oapi_prefix}/openapi.json")
oapi_redirect_url: str = f"{oapi_prefix}/docs/oauth2-redirect"

# Docs URI
docs_url: str = os.getenv('WEBAPP_PATH_DOCS', '/docs')

# ReDoc URI
redoc_url: str = os.getenv('WEBAPP_PATH_REDOC', '/redoc')

# TODO: Provide OpenID-Connect alternative
auth_protocol: str = os.getenv('WEBAPP_AUTH_PROTOCOL', 'http')
auth_host: str = os.getenv('WEBAPP_AUTH_HOST', 'localhost')
auth_port: int = os.getenv('WEBAPP_AUTH_PORT', '8080')
auth_realm: str = os.getenv('WEBAPP_AUTH_REALM', 'master')
auth_baseurl: str = os.getenv(
    'WEBAPP_AUTH_BASEURL',
    f"{auth_protocol}://{auth_host}:{auth_port}"
)
authorization_url: str = os.getenv(
    'WEBAPP_AUTH_URL',
    f"{auth_baseurl}/auth/realms/{auth_realm}/protocol/openid-connect/auth"
)
token_url: str = os.getenv(
    'WEBAPP_TOKEN_ENDPOINT',
    f"{auth_baseurl}/auth/realms/{auth_realm}/protocol/openid-connect/token"
)
refresh_url: str = os.getenv(
    'WEBAPP_REFRESH_URL',
    f"{auth_baseurl}/auth/realms/{auth_realm}/protocol/openid-connect/token"
)

# Connection between SSO and APP
svc_auth_client_id: str = os.getenv('WEBAPP_SVC_AUTH_CLIENT_ID')
svc_auth_client_secret: str = os.getenv('WEBAPP_SVC_AUTH_CLIENT_SECRET')
svc_auth_protocol: str = os.getenv(
    'WEBAPP_SVC_AUTH_PROTOCOL', auth_protocol
)
svc_auth_host: str = os.getenv('WEBAPP_SVC_AUTH_HOST', auth_host)
svc_auth_port: int = os.getenv('WEBAPP_SVC_AUTH_PORT', auth_port)
svc_auth_url_base: str = os.getenv(
    'WEBAPP_SVC_AUTH_BASEURL',
    f"{svc_auth_protocol}://{svc_auth_host}:{svc_auth_port}"
)
svc_auth_jwks_url: str = os.getenv(
    'WEBAPP_SVC_AUTH_JWKS_URL',
    f'{svc_auth_url_base}/auth/realms/{auth_realm}/protocol/openid-connect/certs'
)
svc_auth_introspect_url: str = os.getenv(
    'WEBAPP_SVC_AUTH_INTROSPECT_URL',
    f"{svc_auth_url_base}/auth/realms/{auth_realm}/protocol/openid-connect/token/introspect"
)

# authlib configuration
realm: str = auth_realm
headers: List[Dict] = [{'email_verified': True}]
