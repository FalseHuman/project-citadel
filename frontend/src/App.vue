<template>
  <v-app id="inspire">
    <router-view />
  </v-app>
</template>

<script>
export default {
  created() {
    if (localStorage.getItem("auth-token")) {
      window.jQuery.ajaxSetup({
        headers: {
          Authorization: "Token " + localStorage.getItem("auth-token")
        }
      });
    }
  }
};
</script>