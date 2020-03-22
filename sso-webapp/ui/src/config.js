export const endpoint_name = process.env.WEBAPP_NAME || 'webapp';

// Auth
const auth_protocol = process.env.WEBAPP_AUTH_PROTOCOL || 'http';
const auth_host = process.env.WEBAPP_AUTH_HOST || 'localhost';
const auth_port = process.env.WEBAPP_AUTH_PORT || '8080';
const auth_realm = process.env.WEBAPP_AUTH_REALM || 'master';
const auth_url_base = process.env.WEBAPP_AUTH_URL_BASE || `${auth_protocol}://${auth_host}:${auth_port}/auth/realms/${auth_realm}`;

// Client
const protocol = process.env.WEBAPP_PROTOCOL || 'http';
const host = process.env.WEBAPP_HOST || 'localhost';
const port = process.env.WEBAPP_PORT || '3000';
const path = process.env.WEBAPP_PATH || '';
const public_url = process.env.WEBAPP_PUBLIC_URL || `${protocol}://${host}:${port}${path}`;
const callback_url = process.env.WEBAPP_CALLBACK_URL || `${public_url}/callback.html`;

// OIDC Client Settings
// TODO: Provide OpenID-Connect alternative
// TODO: Provide convention for client/secret or new variable
export const oidc_config = {
  auth_issuer: auth_url_base,
  auth_url: process.env.WEBAPP_AUTH_URL || `${auth_url_base}/protocol/openid-connect/auth`,
  token_url: process.env.WEBAPP_TOKEN_URL || `${auth_url_base}/protocol/openid-connect/token`,
  refresh_url: process.env.WEBAPP_REFRESH_URL || `${auth_url_base}/protocol/openid-connect/token`,
  auth_ui_client_id: process.env.WEBAPP_AUTH_UI_CLIENT_ID || `${process.env.WEBAPP_AUTH_CLIENT_ID || endpoint_name}-ui`,
  auth_jwks_url: process.env.WEBAPP_AUTH_JWKS_URL,
  auth_introspect_url: process.env.WEBAPP_AUTH_INTROSPECT_URL
};

// REST Client Settings
export const rest_config = {
  timeout: 1000,
  url: public_url,
  headers: null
};
