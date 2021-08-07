<template>
  <v-app id="inspire">
    <router-view />
  </v-app>
</template>

<script>
import $ from 'jquery';
export default {
  created() {
    if (localStorage.getItem("auth-token")) {
      $.ajaxSetup({
        headers: {
          Authorization: "Token " + localStorage.getItem("auth-token")
        }
      });
    }
  }
};
</script>