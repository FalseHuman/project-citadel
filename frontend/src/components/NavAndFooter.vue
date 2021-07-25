<template>
  <div>
    <v-navigation-drawer v-model="drawer" app>
      <v-sheet color="grey lighten-4" class="pa-4">
        <v-avatar class="mb-4" color="grey darken-1" size="64">
          <img :src="`${user.photo}`" />
        </v-avatar>

        <div v-if="user.first_name === '' && user.last_name === ''">{{username}} ({{user.email}})</div>
        <div v-else>{{user.first_name}} {{user.last_name}}</div>
        <v-btn color="primary" @click="logout">Выход</v-btn>
      </v-sheet>

      <v-divider></v-divider>

      <v-list>
        <v-list-item v-for="[icon, link, text] in links" :key="icon" link :to="link">
          <v-list-item-icon>
            <v-icon>{{ icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ text }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
export default {
  data: () => ({
    drawer: null,
    links: [
      ["mdi-cash", "/", "Расходы/Доходы"],
      ["mdi-account-cog", "/profile", "Настройки профиля"]
    ],
    user: []
  }),
  created() {
    this.username = localStorage.getItem("username");
    this.token = localStorage.getItem("auth-token");
    window.jQuery.ajaxSetup({
      headers: {
        Authorization: `Token ${localStorage.getItem("auth-token")}`
      }
    }),
      this.userinfo();
  },
  methods: {
    userinfo() {
      window.jQuery.get(
        "https://powerful-castle-67781.herokuapp.com/api/user/" + this.username + "/",
        data => {
          this.user = data;
        }
      );
    },
    logout() {
      window.jQuery.post(
        "https://powerful-castle-67781.herokuapp.com/auth/token/logout/",
        this.token,
        data => {}
      );
      localStorage.removeItem("auth-token");
      localStorage.removeItem("username");
      window.location = "/login";
    }
  }
  /* mounted: function(){
    this.$nextTick(this.userinfo)
}*/
};
</script>