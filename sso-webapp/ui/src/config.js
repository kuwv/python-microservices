const xhr = new XMLHttpRequest();
const config_url = '/api/webapp/config.json';

var json;
xhr.open("GET", config_url, false);
xhr.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    json = JSON.parse(this.responseText);
  }
};
xhr.send();

const endpoint_name = json.WEBAPP_NAME || 'webapp-ui';

// Auth
const auth_protocol = json.WEBAPP_AUTH_PROTOCOL || 'http';
const auth_host = json.WEBAPP_AUTH_HOST || 'localhost';
const auth_port = json.WEBAPP_AUTH_PORT || '8080';
const auth_realm = json.WEBAPP_AUTH_REALM || 'master';
const auth_url = json.WEBAPP_AUTH_URL || `${auth_protocol}://${auth_host}:${auth_port}/auth`;
const auth_baseurl = json.WEBAPP_AUTH_BASEURL || `${auth_url}/realms/${auth_realm}`;

// TODO: Move to webui
const public_url = json.WEBAPP_PUBLIC_URL || 'http://localhost:3001';

// OIDC Client Settings
// TODO: Provide OpenID-Connect alternative
// TODO: Provide convention for client/secret or new variable
const auth_config = {
  client_id: json.WEBAPP_AUTH_UI_CLIENT_ID || endpoint_name,
  redirect_uri: json.WEBAPP_REDIRECT_URI || `${public_url}/login`,
  logout_redirect_uri: json.WEBAPP_AUTH_LOGOUT_REDIRECT_URI || `${public_url}/logout`,

  url: json.WEBAPP_AUTH_URL || auth_url,
  authority: json.WEBAPP_AUTH_BASEURL || auth_baseurl,
  realm: json.WEBAPP_AUTH_REALM || 'master',
  scope: json.WEBAPP_AUTH_SCOPE || 'openid profile',
  authorization_endpoint: json.WEBAPP_AUTH_ENDPOINT || `${auth_baseurl}/protocol/openid-connect/auth`,

  // Public
  jwks_uri: json.WEBAPP_AUTH_JWKS_URI || `${auth_baseurl}/protocol/openid-connect/certs`,
  token_endpoint: json.WEBAPP_TOKEN_ENDPOINT || `${auth_baseurl}/protocol/openid-connect/token`,
  refresh_url: json.WEBAPP_REFRESH_URL || `${auth_baseurl}/protocol/openid-connect/token`,

  userinfo_endpoint: json.WEBAPP_AUTH_USERINFO_ENDPOINT || `${auth_baseurl}/protocol/openid-connect/userinfo`,
  introspect_url: json.WEBAPP_AUTH_INTROSPECT_URL || `${auth_baseurl}/protocol/openid-connect/token/introspect`,
  end_session_endpoint: json.WEBAPP_AUTH_END_SESSION_ENDPOINT || `${auth_baseurl}/protocol/openid-connect/logout`,
};

// Client
const protocol = json.WEBAPP_PROTOCOL || window.location.protocol;
const url = json.WEBAPP_URL || (protocol.includes(':') ? `${protocol}//` : `${protocol}://`)
  + (json.WEBAPP_HOST || window.location.hostname)
  + (json.WEBAPP_PORT !== undefined ? `:${json.WEBAPP_PORT}` : '')
  + (json.WEBAPP_PATH_PREFIX || '/api/webapp');

// REST Client Settings
const rest_config = {
  url: url,
  timeout: 1000,
  headers: {
    common: {
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      Pragma: 'no-cache',
      'Content-Type': 'application/json',
      Accept: 'application/json',
    }
  }
};

export { endpoint_name, auth_config, rest_config };
