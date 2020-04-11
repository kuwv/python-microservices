import axios from 'axios'
import { rest_config } from '@/config'
import { authService } from '@/services/auth'


class RESTClient {
  // this.isHandlerEnabled = (config={}) => {
  //   return config.hasOwnProperty('handlerEnabled') && !config.handlerEnabled ? false : true
  // }

  constructor(config=rest_config) {
    this.instance = axios.create({
      returnRejectedPromiseOnError: true,
      withCredentials: true,
      baseURL: config.url,
      timeout: config.timeout,
      headers: config.headers
    });

    this.instance.interceptors.request.use(async config => {
      let access_token = await authService.getAccessToken();
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

  get(path) {
    return this.instance.get(path);
  }
}

export default RESTClient;
