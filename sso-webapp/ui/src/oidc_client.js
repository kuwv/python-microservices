import { UserManager, WebStorageStateStore, User } from 'oidc-client';
import { oidc_config } from './config';

export class OIDCClient {
  constructor() {
    const config = {
      userStore: new WebStorageStateStore({ store: window.localStorage }),
      authority: oidc_config.auth_url,
      client_id: oidc_config.auth_ui_client_id,
      redirect_uri: oidc_config.callback_url,
      response_type: 'id_token token',
      scope: 'openid profile',
      post_logout_redirect_uri: oidc_config.auth_url,
      filterProtocolClaims: true,
      metadata: {
        issuer: oidc_config.auth_issuer,
        authorization_endpoint: oidc_config.auth_url,
        userinfo_endpoint: oidc_config.userinfo_url,
        end_session_endpoint: oidc_config.logout_url,
        jwks_uri: oidc_config.jwks_url,
      }
    };

    this.userManager = new UserManager(config);
  }

  getUser(): Promise<User | null> {
    return this.userManager.getUser();
  }

  login(): Promise<void> {
    return this.userManager.signinRedirect();
  }

  logout(): Promise<void> {
    return this.userManager.signoutRedirect();
  }
}
