import * as Keycloak from 'keycloak-js'
import { auth_config } from '@/config'
import { fireLoginEvent, fireLogoutEvent } from '@/event-bus'


export class AuthService {
  constructor() {
    this._keycloak = new Keycloak({
      url: auth_config.url,
      realm: auth_config.realm,
      clientId: auth_config.client_id,
    });

    // TODO: optional init here
    this.init();
    this._keycloak.onAuthSuccess = (() => fireLoginEvent());
    this._keycloak.onAuthLogout = (() => fireLogoutEvent());
    // this._keycloak.onAuthError = (() => fireLoginEvent());
    this._keycloak.onTokenExpired = () => { console.log('expired'); };
  }

  init() {
    this._keycloak.init({
      onLoad: 'check-sso',
      flow: 'standard',
      checkLoginIframe: false,
      pkceMethod: 'S256',
      enableLogging: true
    }).then(function(authenticated) {
       console.log(authenticated ? 'authenticated' : 'unauthenticated');
    }).catch(function() {
       alert('failed to initialize');
    });
  }

  login() {
    this._keycloak.login({
      redirectUri: auth_config.redirect_url,
      scope: auth_config.scope,
    });
  }

  logout() {
    return this._keycloak.logout();
  }

  isUserAuthenticated() {
    return new Promise((resolve, reject) => {
      // console.log(Object.keys(this._keycloak));
      if (this._keycloak.authenticated !== undefined) {
        if (this._keycloak.authenticated) {
          console.log('authenticated');
          console.log(this.isTokenExpired());
          resolve(true);
        } else {
          console.log('unauthenticated');
          resolve(false);
        }
      } else {
        console.log('uninitialized')
        reject(false);
      }
    });
  }

  getProfile() {
    return this._keycloak.loadUserProfile();
  }

  getRoles() {
    return this._keycloak.realmAccess;
  }

  getAccessToken() {
    return this._keycloak.token;
  }

  isTokenExpired(validity=0) {
    return new Promise((resolve, reject) => {
      if (this._keycloak.token !== undefined) {
        if (this._keycloak.isTokenExpired(validity)) {
          console.log('expired');
          this.updateToken();
          resolve(true);
        } else {
          console.log('valid');
          resolve(false);
        }
      } else {
        console.log('uninitialized')
        reject(false);
      }
    });
  }

  updateToken(validity=5) {
    this._keycloak.updateToken(validity).then(function(refreshed) {
      if (refreshed) {
        console.log('refreshed');
      }
    }).catch(function() {
      console.log('Failed to refresh token');
    });
  }
}

export const authService = new AuthService();

export default {
  install: function (Vue) {
    Vue.prototype.$auth = authService;
  }
}
