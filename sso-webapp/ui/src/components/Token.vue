<template>
  <div class="container">
    <h3>Token:</h3>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Insecure</th>
        </tr>
      </thead>
      <tbody>
        <tr> 
          <th scope="row">{{ insecure_endpoint }}</th>
        </tr>
      </tbody>
    </table> 
  </div> 
</template>

<script>
  import {RESTClient} from '../rest_client';

  const restClient = new RESTClient();

  export default {
    name: 'Token',
    data() {
      return {
        insecure_endpoint: false,
      };
    },
    created: function() {
      restClient.instance
        .get('/api/insecure')
        .then(res => {
          this.insecure_endpoint = res.data;
        })
    }
  }
</script>

<style>
  h3 {
    margin-bottom: 5%;
  }
</style>
