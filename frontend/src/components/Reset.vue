<template>
  <main>
    <v-container fluid fill-height class="loginOverlay">
      <v-layout flex align-center justify-center>
        <v-flex xs12 sm4 elevation-6>
        <v-alert dense outlined type="error" dismissible v-show="non_field.length > 0">
            {{ non_field }}
          </v-alert>
          <v-toolbar class="pt-5 blue darken-4 d-flex justify-space-around">
            <v-toolbar-title class="white--text mb-6">
              <h4>Восстановление</h4>
            </v-toolbar-title>
          </v-toolbar>
          <v-card>
            <v-card-text class="pt-4" v-if="click === true">
              <div>
                <v-form ref="form">
                  <v-text-field label="Пароль" v-model="password" type="password" required></v-text-field>
                  <v-text-field
                    label="Повторите пароль"
                    v-model="new_password"
                    type="password"
                    required
                  ></v-text-field>
                  <v-layout justify-space-between>
                    <v-btn color="primary"  @click="sendNewPassword">Обновить</v-btn>
                    <a @click="click=false">Вернуться назад</a>
                  </v-layout>
                </v-form>
              </div>
            </v-card-text>
            <v-card-text class="pt-4" v-else>
              <div>
                <h3 style="text-align: center;">
                  <strong>Укажите логин</strong>
                </h3>
                <p>Пожалуйста, укажите логин, который вы использовали для входа на сайт.</p>
                <v-form ref="form">
                  <v-text-field label="Логин" v-model="username" required></v-text-field>
                  <v-layout justify-space-between>
                    <v-btn color="primary" @click="click=true">Далее</v-btn>
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
export default {
  metaInfo: {
    title: "Восстановление"
  },
  data() {
    return {
      non_field: "",
      username: "",
      password: "",
      new_password: "",
      click: false
    };
  },
  methods: {
    sendNewPassword() {
      const data_user = {
        login: this.username,
        password_1: this.password,
        password_2: this.new_password
      };
      $.post(
        "http://localhost:8002/api/password/change_password/change_password/",
        data_user,
        data => {
          this.$router.push("/login");
        }
      ).fail(response => {
        let json = response.responseJSON;
        this.non_field = json.toString()
      });
    }
  }
};
</script>
