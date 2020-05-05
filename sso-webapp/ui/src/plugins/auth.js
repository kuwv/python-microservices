import * as Keycloak from 'keycloak-js'
// import { auth_config } from '@/config'
import { fireLoginEvent, fireLogoutEvent } from '@/event-bus'


export default class AuthService {
  constructor(config) {
    this._config = config;
    console.log(this._config);

    this._keycloak = new Keycloak({
      url: this._config.url,
      realm: this._config.realm,
      clientId: this._config.client_id,
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
      // auto or manual
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
      redirectUri: this._config.redirect_url,
      scope: this._config.scope,
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

// export const authService = new AuthService(auth_config);
// 
// export default {
//   install: function (Vue) {
//     Vue.prototype.$auth = authService;
//   }
// }
