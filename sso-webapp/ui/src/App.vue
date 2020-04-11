<template>
  <div id="app">
    <!-- Token/ -->
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <!-- router-link to="/token">Token</router-link> | -->
      <!-- router-link to="/profile">Profile</router-link> | -->
      <router-link to="/about">About</router-link>
    </div>
    <router-view/>
  </div>
</template>

<script/>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
