import axios from 'axios';

export class RESTClient {
  constructor(
      url = process.env.WEBAPP_PUBLIC_URL,
      timeout = 1000,
      headers
  ) {
    this.instance = axios.create({
      baseURL: url,
      timeout: timeout,
      headers: headers
    });
  }
}
