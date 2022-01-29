 <template>
  <v-main>
    <div v-if="load === true">
      <loading />
    </div>
    <div v-else>
      <NavAndFooter />
      <v-card class="mx-auto" max-width="100%" tile>
        <v-col>
          <p style="text-align: center; margin: 0;">
            <v-avatar size="100">
              <v-img :lazy-src="`${user.photo}`" :src="`${user.photo}`" :alt="`${user.photo}`"></v-img>
            </v-avatar>
          </p>
        </v-col>
        <v-list-item color="rgba(0, 0, 0, .4)">
          <v-list-item-content justify="center">
            <v-list-item-title
              class="title"
              style="text-align: center;"
              v-for="label in Object.keys(labels)"
              :key="label"
              v-show="label!=='photo' && label!=='email_send'"
            >{{firstUpperWord(labels[label])}}: {{user[label]}}</v-list-item-title>
            <div style="margin-top: 15px; margin-bottom: 10px;">
              <v-row justify="center">
                <v-dialog v-model="dialog" persistent max-width="600px">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn color="primary" dark v-bind="attrs" v-on="on">Pедактировать</v-btn>
                  </template>
                  <v-card>
                    <v-card-title>
                      <span class="text-h5">Редактировать профиль</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12">
                            <v-file-input
                              accept="image/*"
                              label="Фото"
                              prepend-icon="mdi-camera"
                              @change="onFileChange"
                            ></v-file-input>
                          </v-col>
                          <v-col cols="12" sm="6" md="6">
                            <v-text-field label="Имя пользователя*" v-model="login" required clearable></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="6">
                            <v-text-field label="Адрес электронной почты*" v-model="email" required clearable></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="6">
                            <v-text-field label="Имя*" v-model="name" required clearable></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="6">
                            <v-text-field label="Фамилия*" v-model="family" required clearable></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="10" md="10">
                            <v-radio-group v-model="row" row>
                              <template v-slot:label>
                                <div>
                                  Вы согласны получать копию расходов/доходов на
                                  <strong>е-mail</strong>?
                                </div>
                              </template>
                              <v-radio value="true">
                                <template v-slot:label>
                                  <div>
                                    <strong class="success--text">Да</strong>
                                  </div>
                                </template>
                              </v-radio>
                              <v-radio value="false">
                                <template v-slot:label>
                                  <div>
                                    <strong class="error--text">Нет</strong>
                                  </div>
                                </template>
                              </v-radio>
                            </v-radio-group>
                          </v-col>
                        </v-row>
                      </v-container>
                      <small>*Обязательные поля</small>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="dialog = false">Закрыть</v-btn>
                      <v-btn color="blue darken-1" type="submit" text @click="updateUser">Сохранить</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-row>
            </div>
          </v-list-item-content>
        </v-list-item>
      </v-card>
    </div>
  </v-main>
</template>
<script>
import $ from "jquery";
import NavAndFooter from "../components/NavAndFooter";
import Loading from "../components/Loading";
export default {
  components: { NavAndFooter, Loading },
  metaInfo: {
    title: "Профиль - Цитадель"
  },
  data() {
    return {
      load: null,
      user: [],
      dialog: false,
      link: "",
      login: "",
      email: "",
      name: "",
      family: "",
      labels: [],
      row: ""
    };
  },
  created() {
    this.users();
  },
  methods: {
    onFileChange(file) {
      this.link = file;
    },
    users() {
      this.load = true;
      $.get(this.$store.state.backend_url + "api/user/", data => {
        //console.log(data)
        //console.log(document.cookie)

        this.user = data[0];
        (this.labels = this.user.labels),
          //console.log(this.labels)
          (this.name = this.user.first_name),
          (this.login = this.user.username),
          (this.family = this.user.last_name),
          (this.email = this.user.email);
        //this.link = data.photo;
        //this.row = this.user.email_send.toString();
        this.load = false;
      });
    },
    firstUpperWord(word) {
      return word[0].toUpperCase() + word.substr(1).toLowerCase();
    },
    updateAvatar() {
      let formData = new FormData();
      formData.append("photo", this.link);

      $.ajax({
        url: this.$store.state.backend_url + "api/user-avatar/",
        data: formData,
        type: "POST",
        processData: false,
        contentType: false,
        success: function(data) {
          ////console.log('done')
        },
        error: function(response) {
          //console.log(this.data);
          let err = response.responseJSON;
          for (let key in err) {
            alert(key, err[key].toString());
          }
        }
      });
    },
    updateUser() {
      //console.log(this.row)
      $.ajax({
        url: this.$store.state.backend_url + "api/update_profile/",
        data: {
          username: this.login,
          first_name: this.name,
          last_name: this.family,
          email: this.email,
          email_send: this.row
        },
        type: "PUT",
        success: function(data) {
          location.reload();
        },
        error: function(response) {
          //console.log(this.data);
          let err = response.responseJSON;
          for (let key in err) {
            alert(key, err[key].toString());
          }
        }
      });
      if (this.link !== "") {
        this.updateAvatar();
      }
    }
  }
};
</script>