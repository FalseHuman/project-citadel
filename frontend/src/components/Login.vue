<template>
     <main>
       <v-container fluid fill-height class="loginOverlay">
          <v-layout flex align-center justify-center>
            <v-flex xs12 sm4 elevation-6>
              <v-toolbar class="pt-5 blue darken-4">
                <v-toolbar-title class="white--text"><h4>Вход в Цитадель</h4></v-toolbar-title>
              </v-toolbar>
              <v-card>
                <v-card-text class="pt-4">
                  <div>
                      <v-form  ref="form"> <!--v-model="valid"-->
                        <v-text-field
                          label="Логин"
                          v-model="username"
                          required
                        ></v-text-field>
                        <v-text-field
                          label="Пароль"
                          v-model="password"
                          type="password"
                          required
                        ></v-text-field>
                        <v-layout justify-space-between>
                            <v-btn @click="signIn">Войти</v-btn>
                            <a href="/registraitions">Регистрация</a>
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
      title: 'Вход в систему',
    },
    data(){
      return{
        username: '',
        password: '',
      }
    },
    methods:{
      signIn () {
        const credentials = {
          username: this.username,
          password: this.password
        }
        window.jQuery.post('https://powerful-castle-67781.herokuapp.com/auth/token/login/', credentials,
         (data) => {
           localStorage.setItem('auth-token', data.auth_token)
           localStorage.setItem('username', this.username)
           this.$router.push('/')
         })
        .fail((response) => {
          alert(response.responseText)
        })
      },
    }
}
</script>