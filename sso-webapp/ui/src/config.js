var auth_scheme = process.env.WEBAPP_AUTH_SCHEME || 'http';
var auth_host = process.env.WEBAPP_AUTH_HOST || 'localhost';
var auth_port = process.env.WEBAPP_AUTH_PORT || '8080';
var auth_realm = process.env.WEBAPP_AUTH_REALM || 'master';
var auth_url_base = process.env.WEBAPP_AUTH_URL_BASE ||
  `${auth_scheme}://${auth_host}:${auth_port}/auth/realms/${auth_realm}`;

export const oidc_settings = {
  // TODO: Provide OpenID-Connect alternative
  // TODO: Provide convention for client/secret or new  iables
  auth_url_base_base: auth_url_base,
  authorization_url: process.env.WEBAPP_AUTH_URL ||
    `${auth_url_base}/protocol/openid-connect/auth`,
  token_url: process.env.WEBAPP_TOKEN_URL ||
    `${auth_url_base}/protocol/openid-connect/token`,
  refresh_url: process.env.WEBAPP_REFRESH_URL ||
    `${auth_url_base}/protocol/openid-connect/token`,
  auth_ui_client_id: process.env.WEBAPP_AUTH_UI_CLIENT_ID ||
    `${process.env.WEBAPP_AUTH_CLIENT_ID}-ui`,
  auth_jwks_url: process.env.WEBAPP_AUTH_JWKS_URL,
  auth_introspect_url: process.env.WEBAPP_AUTH_INTROSPECT_URL,
  uri_prefix: process.env.WEBAPP_URI_PREFIX,
};
