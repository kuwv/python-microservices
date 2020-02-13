import {UserManager, WebStorageStateStore, User} from 'oidc-client';

// Auth
// TODO: Provide OpenID-Connect alternative
// TODO: Provide convention for client/secret or new const variables
const auth_connection = process.env.WEBAPP_AUTH_CONNECTION || 'http';
const auth_host = process.env.WEBAPP_AUTH_HOST || 'localhost';
const auth_port = process.env.WEBAPP_AUTH_PORT || '8080';
const auth_realm = process.env.WEBAPP_AUTH_REALM || 'master';
const auth_url_base = process.env.WEBAPP_AUTH_URL_BASE
  || `${auth_connection}://${auth_host}:${auth_port}/auth/realms/${auth_realm}`;
const authorization_url = process.env.WEBAPP_AUTH_URL
  || `${auth_url_base}/protocol/openid-connect/auth`;
const token_url = process.env.WEBAPP_AUTH_TOKEN_URL
  || `${auth_url_base}/protocol/openid-connect/token`;
const userinfo_url = process.env.WEBAPP_AUTH_USERINFO_URL
  || `${auth_url_base}/protocol/openid-connect/userinfo`;
const logout_url = process.env.WEBAPP_LOGOUT_URL
  || `${auth_url_base}/protocol/openid-connect/logout`;
const jwks_url = process.env.WEBAPP_AUTH_JWKS_URL
  || `${auth_url_base}/protocol/openid-connect/certs`;
const auth_ui_client_id = process.env.WEBAPP_AUTH_UI_CLIENT_ID
  || `${process.env.WEBAPP_AUTH_CLIENT_ID}-ui`;

// Client
const uri_prefix = process.env.WEBAPP_URI_PREFIX || '';
const public_url = process.env.WEBAPP_PUBLIC_URL
  || `http://localhost:3000${uri_prefix}`;
const callback_url = process.env.WEBAPP_CALLBACK_URL
  || `${public_url}/callback.html`;

export class OIDCClient {
  constructor() {
    const settings = {
      userStore: new WebStorageStateStore({ store: window.localStorage }),
      authority: authorization_url,
      client_id: auth_ui_client_id,
      redirect_uri: callback_url,
      response_type: 'id_token token',
      scope: 'openid profile',
      post_logout_redirect_uri: authorization_url,
      filterProtocolClaims: true,
      metadata: {
        issuer: auth_url_base,
        authorization_endpoint: authorization_url,
        userinfo_endpoint: userinfo_url,
        end_session_endpoint: logout_url,
        jwks_uri: jwks.url,
      }
    };

    this.userManager = new UserManager(settings);
  }

  public getUser(): Promise<User | null> {
    return this.userManager.getUser();
  }

  public login(): Promise<void> {
    return this.userManager.signinRedirect();
  }

  public logout(): Promise<void> {
    return this.userManager.signoutRedirect();
  }
}
