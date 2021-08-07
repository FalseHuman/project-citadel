<template>
     <main>
       <v-container fluid fill-height class="loginOverlay">
          <v-layout flex align-center justify-center>
            <v-flex xs12 sm4 elevation-6>
              <v-toolbar class="pt-5 blue darken-4 d-flex justify-space-around">
                <v-toolbar-title class="white--text mb-6"><h4>Регистрация в Цитадель</h4></v-toolbar-title>
              </v-toolbar>
              <v-card>
                <v-card-text class="pt-4">
                  <div>
                      <v-form ref="form" v-model="valid"><!-- Login-->
                        <v-text-field
                          label="E-mail"
                          v-model="email"
                          :rules="[rules.email]"
                          required
                        ></v-text-field>
                        <v-text-field
                          label="Логин"
                          v-model="username"
                          :rules="[rules.username]"
                          required
                        ></v-text-field>
                        <v-text-field
                          label="Пароль"
                          v-model="password"
                          :rules="[rules.password]"
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
import $ from 'jquery';
  export default {
    metaInfo: {
      title: 'Регистрация',
    },
    data () {
      return {
        valid: false,
        email: '',
        username: '',
        usernameError:'',
        emailError:'',
        passwordError:'',
        password: '',
        errors: {},
        rules:{
         username: value => {
           return this.usernameError.toString()
           },
          password: value =>{
            return this.passwordError
          },
          email: value => {
            const email = this.emailError.toString()
            return email 
            },
        }
      }
    },
    methods: {
      signUp () {
        const credentials = {
          email: this.email,
          username: this.username,
          password: this.password
        }
        $.post('http://localhost:8002/auth/users/', credentials,  (data) => {
          this.$router.push('/login')
        }).fail((response) => {
          
          let errors = response.responseJSON
          let passwordString = ''
          for(let i =0; i< errors.password.length; i++){
            passwordString += errors.password[i]
          }
            this.passwordError = passwordString
            this.usernameError = errors.username
            this.emailError = errors.email
        })
      },
    }
  }
</script>