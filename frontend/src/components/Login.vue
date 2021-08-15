<template>
  <main>
    <v-container fluid fill-height class="loginOverlay">
      <v-layout flex align-center justify-center>
        <v-flex xs12 sm4 elevation-6>
          <v-alert dense outlined type="error" dismissible v-show="non_field_errors.length > 0">
            {{ non_field_errors }}
          </v-alert>
          <v-toolbar class="pt-5 blue darken-4 d-flex justify-space-around">
            <v-toolbar-title class="white--text mb-6">
              <h4>Вход в Цитадель</h4>
            </v-toolbar-title>
          </v-toolbar>
          <v-card>
            <v-card-text class="pt-4">
              <div>
                <v-form ref="form">
                  <v-text-field label="Логин" v-model="username" required></v-text-field>
                  <v-text-field label="Пароль" v-model="password" type="password" required></v-text-field>
                  <v-layout justify-space-between>
                    <v-btn  @click="signIn">Войти</v-btn>
                    <p><a href="/reset-password">Забыли пароль?</a> <a href="/registraitions">Регистрация</a></p>
                  </v-layout>
                </v-form>
              </div>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </main>
</template>

<script>
import $ from "jquery";
export default {
  metaInfo: {
    title: "Вход в систему"
  },
  data() {
    return {
      username: "",
      password: "",
      non_field_errors: ""
    };
  },
  methods: {
    signIn() {
      const credentials = {
        username: this.username,
        password: this.password
      };
      $.post(
        "http://localhost:8002/auth/token/login/",
        credentials,
        data => {
          localStorage.setItem("auth-token", data.auth_token);
          localStorage.setItem("username", this.username);
          this.$router.push("/");
          location.reload();
        }
      )
      .fail(response => {
        let json = response.responseJSON;
        this.non_field_errors = json.non_field_errors.toString()
      });
    }
  }
};
</script>