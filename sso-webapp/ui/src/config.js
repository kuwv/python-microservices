const endpoint_name = process.env.WEBAPP_NAME || 'webapp';

// Auth
const auth_protocol = process.env.WEBAPP_AUTH_PROTOCOL || 'http';
const auth_host = process.env.WEBAPP_AUTH_HOST || 'localhost';
const auth_port = process.env.WEBAPP_AUTH_PORT || '8080';
const auth_realm = process.env.WEBAPP_AUTH_REALM || 'master';
const auth_url = process.env.WEBAPP_AUTH_URL || `${auth_protocol}://${auth_host}:${auth_port}/auth`;
const auth_url_base = process.env.WEBAPP_AUTH_URL_BASE || `${auth_url}/realms/${auth_realm}`;

// Client
const protocol = process.env.WEBAPP_PROTOCOL || 'http';
const host = process.env.WEBAPP_HOST || 'localhost';
const port = process.env.WEBAPP_PORT || '3000';
const path = process.env.WEBAPP_PATH || '';
const url = process.env.WEBAPP_URL || `${protocol}://${host}:${port}${path}`;

const public_url = process.env.WEBAPP_PUBLIC_URL || 'http://localhost:3001';

// OIDC Client Settings
// TODO: Provide OpenID-Connect alternative
// TODO: Provide convention for client/secret or new variable
const auth_config = {
  client_id: process.env.WEBAPP_AUTH_UI_CLIENT_ID || `${process.env.WEBAPP_AUTH_CLIENT_ID || endpoint_name}-ui`,
  redirect_uri: process.env.WEBAPP_AUTH_REDIRECT_URI || `${public_url}/login`,
  logout_redirect_uri: process.env.WEBAPP_AUTH_LOGOUT_REDIRECT_URI || `${public_url}/logout`,

  url: process.env.WEBAPP_AUTH_URL || auth_url,
  authority: process.env.WEBAPP_AUTH_URL_BASE || auth_url_base,
  realm: process.env.WEBAPP_AUTH_REALM || 'master',
  scope: process.env.WEBAPP_AUTH_SCOPE || 'openid profile',
  authorization_endpoint: process.env.WEBAPP_AUTH_ENDPOINT || `${auth_url_base}/protocol/openid-connect/auth`,

  jwks_uri: process.env.WEBAPP_AUTH_JWKS_URI || `${auth_url_base}/protocol/openid-connect/certs`,
  token_endpoint: process.env.WEBAPP_TOKEN_ENDPOINT || `${auth_url_base}/protocol/openid-connect/token`,
  refresh_url: process.env.WEBAPP_REFRESH_URL || `${auth_url_base}/protocol/openid-connect/token`,

  userinfo_endpoint: process.env.WEBAPP_AUTH_USERINFO_ENDPOINT || `${auth_url_base}/protocol/openid-connect/userinfo`,
  introspect_url: process.env.WEBAPP_AUTH_INTROSPECT_URL || `${auth_url_base}/protocol/openid-connect/token/introspect`,
  end_session_endpoint: process.env.WEBAPP_AUTH_END_SESSION_ENDPOINT || `${auth_url_base}/protocol/openid-connect/logout`,
};

// REST Client Settings
const rest_config = {
  url: url,
  timeout: 1000,
  headers: {
    common: {
      "Cache-Control": "no-cache, no-store, must-revalidate",
      Pragma: "no-cache",
      "Content-Type": "application/json",
      Accept: "application/json",
    }
  }
};

export { endpoint_name, auth_config, rest_config };
