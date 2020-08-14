import Vue from 'vue';
import axios from 'axios';


export default class RESTClient {
  // this.isHandlerEnabled = (config={}) => {
  //   return config.hasOwnProperty('handlerEnabled') && !config.handlerEnabled ? false : true
  // }

  constructor(config) {
    this.instance = axios.create({
      returnRejectedPromiseOnError: true,
      withCredentials: true,
      baseURL: config.url,
      timeout: config.timeout,
      headers: config.headers
    });

    this.instance.interceptors.request.use(async config => {
      let access_token = await Vue.prototype.$auth.getAccessToken();
      config.headers.common.Authorization = `Bearer ${access_token}`;
      return config;
    });

    this.instance.interceptors.response.use((response) => {
      return response;
    }, (error) => {
      console.log(error);
      return Promise.reject(error);
    });
  }

  getUri(config) {
    return this.instance.getUri(config);
  }

  request(config) {
    return this.instance.request(config);
  }
    
  get(path) {
    return this.instance.get(path);
  }

  delete(path, config) {
    return this.instance.delete(path, config);
  }

  head(path, config) {
    return this.instance.head(path, config);
  }

  post(path, data, config) {
    return this.instance.post(path, data, config);
  }

  put(path, data, config) {
    return this.instance.put(path, data, config);
  }

  patch(path, data, config) {
    return this.instance.patch(path, data, config);
  }
}

// export const restClient = new RESTClient(rest_config);
// 
// export default {
//   install: function (Vue) {
//     Vue.prototype.$http = restClient;
//   }
// }
