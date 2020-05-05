import './set-public-path';
import Vue from 'vue';
import singleSpaVue from 'single-spa-vue';
import App from './App.vue';
import router from './router';
import { auth_config, rest_config } from './config';
import AuthService from './plugins/auth';
import RESTClient from './plugins/rest';

Vue.config.productionTip = false;
// Vue.use(auth);
// Vue.use(http);

const vueLifecycles = singleSpaVue({
  Vue,
  appOptions: {
    router,
    render: (h) => h(App),
  }
});

export const bootstrap = [
  async () => {
    // let config = await (await fetch('/api/webapp/config.json')).json();
    // console.log(config);
    Vue.use(Vue.prototype.$auth = new AuthService(auth_config));
    Vue.use(Vue.prototype.$http = new RESTClient(rest_config));
    Vue.use(router);
  },
  vueLifecycles.bootstrap
];
export const mount = vueLifecycles.mount;
export const unmount = vueLifecycles.unmount;
