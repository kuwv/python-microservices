
const oidc_settings = {
  // TODO: Provide OpenID-Connect alternative
  // TODO: Provide convention for client/secret or new  iables
  auth_connection: process.env.WEBAPP_AUTH_CONNECTION || 'http',
  auth_host: process.env.WEBAPP_AUTH_HOST || 'localhost',
  auth_port: process.env.WEBAPP_AUTH_PORT || '8080',
  auth_realm: process.env.WEBAPP_AUTH_REALM || 'master',
  auth_url_base: process.env.WEBAPP_AUTH_URL_BASE
    || `${auth_connection}://${auth_host}:${auth_port}/auth/realms/${auth_realm}`,
  authorization_url: process.env.WEBAPP_AUTH_URL
    || `${auth_url_base}/protocol/openid-connect/auth`,
  token_url: process.env.WEBAPP_TOKEN_URL
    || `${auth_url_base}/protocol/openid-connect/token`,
  refresh_url: process.env.WEBAPP_REFRESH_URL
    || `${auth_url_base}/protocol/openid-connect/token`,
  auth_ui_client_id: process.env.WEBAPP_AUTH_UI_CLIENT_ID
    || `${process.env.WEBAPP_AUTH_CLIENT_ID}-ui`,
  auth_jwks_url: process.env.WEBAPP_AUTH_JWKS_URL,
  auth_introspect_url: process.env.WEBAPP_AUTH_INTROSPECT_URL,
  uri_prefix: process.env.WEBAPP_URI_PREFIX,
}
