<template>
  <p>secure: {{ secure_state }}</p>
  <!-- p>unsecure: {{ unsecure_state }}</p -->
</template>

<script>
import RESTClient from '@/services/rest'

const client = new RESTClient().instance;

export default {
  data () {
    return {
      secure_state: '',
      unsecure_state: null
    }
  },
  mounted () {
    client.get('/secure')
      .then(response => {
        this.secure_state = response.data;
      })
      .catch((error) => {
        if (error.response.status === 403) {
          this.secure_state = 'access denied';
        } else {
          this.secure_state = 'access error';
        }
      });
  }
}
</script>

<style/>
