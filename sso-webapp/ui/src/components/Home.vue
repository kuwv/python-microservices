<template>
  <div>
    <h1>Welcome!</h1>
    <div v-if="isAuthenticated">
      <router-link to="/protected">Protected</router-link>
      |
      <router-link to="/profile">Profile</router-link>
    </div>
    <br>
    <button v-if="!isAuthenticated" @click="onLogin()">Login</button>
    <button v-else @click="onLogout()">Logout</button>
  </div>
</template>

<script>
import { registerLoginEventListener, registerLogoutEventListener } from '@/event-bus';

export default {
  name: 'Home',
  data () {
    return {
      isAuthenticated: false
    };
  },
  mounted () {
    this.$auth.isUserAuthenticated()
      .then(isAuthenticated => {
        console.log('logged in: ' + isAuthenticated);
        this.isAuthenticated = isAuthenticated;
      })
      // If somehting goes wrong we assume no user is logged in
      .catch(err => {
        console.log(err);
        this.isAuthenticated = false;
      });
    registerLoginEventListener(() => { this.isAuthenticated = true });
    registerLogoutEventListener(() => { this.isAuthenticated = false });
  },
  methods: {
    onLogin () {
      console.log('Attempting login');
      this.$auth.login();
    },
    onLogout () {
      this.$auth.logout();
    }
  }
}
</script>
