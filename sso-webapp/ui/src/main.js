import '@/set-public-path';
import Vue from 'vue';
import singleSpaVue from 'single-spa-vue';
import App from '@/App.vue';
import router from '@/router';
import auth from '@/services/auth';
// import RESTClient as http from '@/services/rest';

Vue.config.productionTip = false;
Vue.use(auth);
// Vue.use(http);

const vueLifecycles = singleSpaVue({
  Vue,
  appOptions: {
    router,
    // created () {
    //   init()
    // },
    render: (h) => h(App),
  },
});

export const bootstrap = vueLifecycles.bootstrap;
export const mount = vueLifecycles.mount;
export const unmount = vueLifecycles.unmount;
