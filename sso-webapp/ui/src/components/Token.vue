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
          <th scope="row">{{insecure}}</th>
        </tr>
      </tbody>
    </table> 
  </div> 
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'Token',
    data() {
      return {
        insecure: false,
      };
    },
    created: function() {
      axios
        .get('http://localhost:3000/insecure')
        .then(res => {
          this.insecure = res.data;
        })
    }
  }
</script>

<style>
  h3 {
    margin-bottom: 5%;
  }
</style>
