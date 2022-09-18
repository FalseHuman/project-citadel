<template>
  <div  v-if="!$vuetify.breakpoint.mobile">
    <v-navigation-drawer v-model="drawer" :mini-variant.sync="mini" permanent app>
      <p style="text-align: center; margin: 0">
        <v-sheet color="light" class="pa-4">
          <div v-if="mini === false">
            <v-avatar
              v-if="user.photo !== null"
              class="mb-4"
              color="grey darken-1"
              size="64"
            >
              <img :src="`${user.photo}`" />
            </v-avatar>
            <v-avatar v-else class="mb-4" color="grey darken-1" size="64">
              <img src />
            </v-avatar>

            <div v-if="user.first_name === '' && user.last_name === ''" class="mb-2">
              {{ user.username }} ({{ user.email }})
            </div>
            <div v-else class="mb-2">{{ user.first_name }} {{ user.last_name }}</div>
            <v-btn color="primary" @click="logout" class="button-nav" title="Выход">
              <v-icon>mdi-exit-run</v-icon>
            </v-btn>
            <v-btn color="primary" @click="theme" class="button-nav" title="Сменить тему">
              <v-icon>mdi-theme-light-dark</v-icon>
            </v-btn>
            <v-btn
              color="primary"
              class="button-nav"
              title="Свернуть панель"
              @click.stop="mini = !mini"
            >
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
          </div>
          <div v-else style="margin-left: -10px">
            <v-avatar v-if="user.photo !== null" color="grey darken-1" size="44">
              <img
                :lazy-src="`${user.photo}`"
                :src="`${user.photo}`"
                :alt="`${user.photo}`"
              />
            </v-avatar>
            <v-avatar v-else color="grey darken-1" size="44">
              <img src />
            </v-avatar>
          </div>
        </v-sheet>
      </p>

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
  <div v-else>
  <footer class="footer">
    <v-bottom-navigation color="primary" fixed>
      <div v-for="[icon, link, text] in links">
      <v-btn :href="link">
        <span>{{text}}</span>

        <v-icon>{{icon}}</v-icon>
      </v-btn>
      </div>
      <!-- v-btn>
        <span>Recents</span>

        <v-icon>mdi-history</v-icon>
      </v-btn>

      <v-btn>
        <span>Favorites</span>

        <v-icon>mdi-heart</v-icon>
      </v-btn>

      <v-btn>
        <span>Nearby</span>

        <v-icon>mdi-map-marker</v-icon>
      </v-btn> -->
    </v-bottom-navigation>
    </footer>
  </div>
</template>

<script>
import $ from "jquery";

export default {
  data: () => ({
    drawer: null,
    links: [
      ["mdi-cash", "/", "Расходы/Доходы"],
      ["mdi-pen", "/notes", "Заметки"],
      ["mdi-account-cog", "/profile", "Настройки"]
    ],
    mini: true,
    user: []
  }),
  created() {
    //this.username = localStorage.getItem("username");
    this.token = localStorage.getItem("auth-token");
    $.ajaxSetup({
      headers: {
        Authorization: `Token ${localStorage.getItem("auth-token")}`,
      },
    });
    this.userinfo();
  },
  methods: {
    userinfo() {
      $.get(this.$store.state.backend_url + "api/user/", (data) => {
        this.user = data.results[0];
      });
    },
    logout() {
      $.post(
        this.$store.state.backend_url + "auth/token/logout/",
        this.token,
        (data) => {}
      );
      localStorage.removeItem("auth-token");
      localStorage.removeItem("username");
      window.location = "/login";
    },
    theme() {
      if (localStorage.getItem("theme") !== "true") {
        localStorage.setItem("theme", true);
      } else {
        localStorage.removeItem("theme");
      }
      location.reload();
    },
  },
};
</script>
<style scoped>
.button-nav {
  margin-left: 5px;
}
.footer {
position: absolute;
left: 0;
bottom: 0;
width: 100%;
}
.theme--dark.v-btn.v-btn--has-bg{
  background-color: transparent !important;
  margin-top: 5px !important;
  font-size: 15px !important
}
</style>
