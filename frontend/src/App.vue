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
    this.tokenGet();
  },
  methods: {
    themeBrowser() {
      //console.log(adapter.browserDetails.browser);
      if (window.matchMedia) {
        if (window.matchMedia("(prefers-color-scheme: dark)").matches && localStorage.getItem('theme') !== 'true') {
          localStorage.setItem('theme', true)
        } else if (localStorage.getItem('theme') !== 'true') {
          localStorage.removeItem('theme')
        }
      }
    },
    tokenGet(){
        $.post("http://localhost:8002/api/token/", {'auth-token': localStorage.getItem("auth-token")}, data => {}).fail(
        response => {
           if (localStorage.getItem('auth-token')){
              localStorage.removeItem('auth-token')
              this.$router.push("/login");
            }
        }
      );
    }
  }
};
</script>
 <style>
.ck.ck-editor__main>.ck-editor__editable {
  background: none !important;
  border-radius: 0;
}
 </style>