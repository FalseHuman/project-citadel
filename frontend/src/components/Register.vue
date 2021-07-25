<template>
     <main>
       <v-container fluid fill-height class="loginOverlay">
          <v-layout flex align-center justify-center>
            <v-flex xs12 sm4 elevation-6>
              <v-toolbar class="pt-5 blue darken-4">
                <v-toolbar-title class="white--text"><h4>Регистрация в Цитадель</h4></v-toolbar-title>
              </v-toolbar>
              <v-card>
                <v-card-text class="pt-4">
                  <div>
                      <v-form ref="form"><!-- Login-->
                        <v-text-field
                          label="E-mail"
                          v-model="email"
                          required
                        ></v-text-field>
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
                            <v-btn @click="signUp">Регистрация</v-btn>
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
      title: 'Регистрация',
    },
    data () {
      return {
        email: '',
        username: '',
        password: '',
        errors: {},
      }
    },
    methods: {
      signUp () {
        const credentials = {
          email: this.email,
          username: this.username,
          password: this.password
        }
        window.jQuery.post('https://powerful-castle-67781.herokuapp.com/auth/users/', credentials,  (data) => {
          this.$router.push('/login')
        }).fail((response) => {
          
          alert(response.responseText)
        })
      },
    }
  }
</script>