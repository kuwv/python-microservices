import axios from 'axios';
import {rest_config} from './config';

export class RESTClient {
  constructor(
    url = rest_config.url,
    timeout = rest_config.timeout,
    headers = rest_config.headers
  ) {
    this.instance = axios.create({
      baseURL: url,
      timeout: timeout,
      headers: headers
    });
  }
}
