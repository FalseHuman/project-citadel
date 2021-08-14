<template>
  <v-app id="inspire">
    <router-view />
  </v-app>
</template>

<script>
import adapter from "webrtc-adapter";
import $ from "jquery";
export default {
  created() {
    if (localStorage.getItem("auth-token")) {
      $.ajaxSetup({
        headers: {
          Authorization: "Token " + localStorage.getItem("auth-token")
        }
      });
    }
    this.themeBrowser();
  },
  methods: {
    themeBrowser() {
      console.log(adapter.browserDetails.browser);
      if (window.matchMedia) {
        if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
          console.log("dark")
        } else {
          console.log("light")
        }
      }
    }
  }
};
</script>