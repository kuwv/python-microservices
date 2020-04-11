<template>
  <div>
    <h2>Profile</h2>
    <template v-if="profile !== null">
      <p>User: {{ profile.username }}</p>
      <p>Email: {{ profile.email }}</p>
      <p>Attributes: {{ profile.attributes }}</p>
      Roles:
      <!-- ul v-if="profile.realm_access" -->
        <li v-for="role in roles" :key="role">
          {{ role }}
        </li>
      <!-- /ul -->
    </template>
  </div>
</template>

<script>
export default {
  data () {
    return {
      profile: null,
      roles: null
    }
  },
  mounted () {
    this.$auth.getProfile()
      .then(profile => {
        this.profile = profile;
      })
      .catch(error => {
        console.log(error);
        this.profile = {};
      });
    this.roles = this.$auth.getRoles().roles;
  }
}
</script>

<style/>
