<template>
  <v-main>
    <div v-if="load === true">
      <loading />
    </div>
    <div v-else>
      <NavAndFooter />
      <v-container class="py-8 px-6" fluid>
        <div>
          <v-row justify="center">
            <v-dialog
              v-model="dialog"
              persistent
              max-width="600px"
              :fullscreen="$vuetify.breakpoint.mobile"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="primary"
                  dark
                  small
                  fab
                  v-bind="attrs"
                  @click="createPays()"
                  v-on="on"
                  style="margin-top: -10px; margin-left: 5px;"
                  title="Добавить"
                >
                  <v-icon dark>mdi-plus</v-icon>
                </v-btn>
                <v-btn
                  color="primary"
                  dark
                  small
                  fab
                  style="margin-top: -10px; margin-left: 5px;"
                  title="Обновить"
                  @click="userpays(month)"
                >
                  <v-icon dark>mdi-refresh</v-icon>
                </v-btn>
              </template>
              <v-card>
                <v-banner single-line v-if="error!==''">
                  <v-icon slot="icon" color="red" size="36">mdi-comment-alert</v-icon>Заполните все поля!
                  <template v-slot:actions>
                    <v-btn color="primary" text @click="error=''">Закрыть</v-btn>
                  </template>
                </v-banner>
                <v-card-title>
                  <span class="text-h5">Добавить платеж</span>
                </v-card-title>
                <v-card-text>
                  <v-container>
                    <v-row>
                      <!--<p v-for="i in createData">{{i}}</p>-->
                      <formfield
                        v-for="i in Object.keys(createData)"
                        type_input="input"
                        :key_label="i"
                        :labels="createData[i].label"
                        :error="error"
                        @changeInput="changeInput"
                        :model="template_form[i]"
                        :cols="12"
                        v-show="i =='title' || i =='body'"
                      />
                      <formfield
                        type_input="input"
                        key_label="cost"
                        :labels="createData.cost.label"
                        @changeInput="changeInput"
                        :error="error"
                        :cols="10"
                        :model="template_form.cost"
                        :sm="6"
                        :md="6"
                      />
                      <formfield
                        type_input="select"
                        :labels="createData.type_of_pays.label"
                        key_label="type_of_pays"
                        :arr_select="arr_select"
                        :error="error"
                        :cols="12"
                        :model="template_form.type_of_pays"
                        :sm="6" 
                        :md="6"
                        @changeInput="changeInput"
                      />
                      <templates :temp="templates_title" @changeData="changeData" />
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="dialog = false">Закрыть</v-btn>
                  <v-btn color="blue darken-1" text @click="paysSend">Сохранить</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-row>
        </div>
        <v-col cols="12" style="margin-bottom: -25px;"><v-text-field type='month' v-model='month'></v-text-field></v-col>
        <p  class="text-center centered" v-if="pays.length ===0">Тут пока нет ни одного платежа:(</p>
        <v-row v-else>
          <v-col cols="12">
            <v-col
            >
              <v-card >
                <v-subheader>Данные за этот месяц - Потрачено: {{date_month.expense}} руб. Получено: {{date_month.income}} руб. Итог: {{date_month.total}} руб.</v-subheader>
                <!--<v-tabs>
                <v-tab>Список</v-tab>
                <v-tab>График</v-tab>
              </v-tabs>

              <v-card-text>
                <v-sheet color="rgba(0, 0, 0, .12)">
                  <v-sparkline
                    :value="value"
                    color="rgba(255, 255, 255, .7)"
                    height="100"
                    padding="24"
                    stroke-linecap="round"
                    smooth
                  >
                    <template v-slot:label="item">${{ item.value }}</template>
                  </v-sparkline>
                </v-sheet>
                </v-card-text>-->
                <v-list two-line>
                  <template v-for="n in pays">
                    <div :key="n.id">
                      <v-list-item>
                        <v-list-item-icon>
                          <v-icon v-if="n.type_of_pays=='наличные'">mdi-cash</v-icon>
                          <v-icon v-else-if="n.type_of_pays=='карта'">mdi-credit-card</v-icon>
                          <v-icon v-else>mdi-help</v-icon>
                        </v-list-item-icon>

                        <v-list-item-content>
                          <v-list-item-title>{{ n.title }}</v-list-item-title>

                          <v-list-item-subtitle
                            xs12
                            sm4
                            elevation-6
                          >{{n.cost}} руб., {{formatDate(n.data)}}</v-list-item-subtitle>
                        </v-list-item-content>
                        <v-col cols="auto" class="d-flex">
                          <v-dialog transition="dialog-bottom-transition" max-width="600">
                            <template v-slot:activator="{ on, attrs }">
                              <div v-if="$vuetify.breakpoint.mobile">
                                <v-menu>
                                  <template v-slot:activator="{ on, attrs }">
                                    <v-btn color="success" v-bind="attrs" v-on="on">
                                      <v-icon>mdi-eye</v-icon>
                                    </v-btn>
                                  </template>

                                  <v-list>
                                    <v-btn color="primary" v-bind="attrs" v-on="on">
                                      <v-icon>mdi-information</v-icon>
                                    </v-btn>
                                    <v-btn color="error" @click="deletePays(n.id)" class="ml-2">
                                      <v-icon>mdi-delete</v-icon>
                                    </v-btn>
                                  </v-list>
                                </v-menu>
                              </div>
                              <div v-else>
                                <v-btn color="primary" v-bind="attrs" v-on="on">
                                  <v-icon>mdi-information</v-icon>
                                </v-btn>
                                <v-btn color="error" @click="deletePays(n.id)" class="ml-2">
                                  <v-icon>mdi-delete</v-icon>
                                </v-btn>
                              </div>
                            </template>
                            <template v-slot:default="dialog">
                              <v-card>
                                <v-card-title dark>
                                  <span class="text-h5">
                                    {{n.title}}
                                  </span>
                                </v-card-title>
                                <v-card-text>
                                  <div class="text-h5 pa-5" v-for="key in Object.keys(labels)" :key="key">
                                    <a v-if="key !='type_of_pays' && key != 'data'">{{labels[key]}}: {{n[key]}}</a>
                                    <a v-else-if="key==='data'">Дата платежа: {{ formatDate(n[key])}}</a>
                                    <a v-else>{{labels[key]}}: {{ firstUpperWord(n[key])}}</a>
                                  </div>
                                </v-card-text>
                                <v-card-actions class="justify-end">
                                  <v-btn text @click="templatesSend(n)">Добавить в шаблон</v-btn>
                                  <v-btn text @click="dialog.value = false">Закрыть</v-btn>
                                </v-card-actions>
                              </v-card>
                            </template>
                          </v-dialog>
                        </v-col>
                      </v-list-item>
                    </div>
                  </template>
                </v-list>
              </v-card>
            </v-col>
              <div class="text-center">
                <v-btn title="Предыдущая" @click="paramsPagination(previous)"  v-show="previous !== null"><v-icon>mdi-menu-left</v-icon></v-btn>
                <v-btn title="Следующая"  @click="paramsPagination(next)" v-show="next !== null"><v-icon>mdi-menu-right</v-icon></v-btn>
              </div>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </v-main>
</template>

<script>
import $ from "jquery";
import formfield from "../components/FormField";
import NavAndFooter from "../components/NavAndFooter";
import Templates from "../components/Templates";
import Loading from "../components/Loading";
import EventBus from '../event/event-bus'
export default {
  components: { formfield, NavAndFooter, Loading, Templates },
  metaInfo: {
    title: "Расходы/Доходы - Цитадель"
  },
  name: "Cash",
  data: () => ({
    loading: null,
    load: null,
    arr_select: [],
    error: "",
    month: '',
    labels: [],
    value: [],
    dialog: false,
    pays: [],
    months: [],
    template_form: {},
    templates: [],
    templates_title: [],
    payData: {},
    createData: {},
    next: null,
    previous: null,
    date_month: null
  }),
  created() {
    let new_data = this.monthString(new Date()).split('.')
    this.month = new_data[1] + '-' + new_data[0]
    this.userpays(this.month);
    this.template_pays()
  },
  methods: {
    template_pays() {
      $.get(this.$store.state.backend_url + "api/templates/", data => {
        //console.log(data);
        this.templates = data.results;
        //console.log(this.templates)
        for (let i = 0; i < this.templates.length; i++) {
          this.templates_title.push(this.templates[i].body_template.title);
        }
      });
    },
    userpays(month, params=null) {
      this.load = true;
      let url = params === null? this.$store.state.backend_url + "api/pays/?date=" + month : this.$store.state.backend_url + "api/pays/?" +params
      //console.log(url)
      $.get(url, data => {
        document.cookie = "auth_token=; max-age=-1";
        this.date_month = data
        this.next = data.next;
        this.previous = data.previous;
        this.pays = data.results;
        if(this.pays.length>0){
          this.labels = this.pays[this.pays.length-1].labels;
        }
        this.createPays();
        this.payData = {};
        this.load = false;
      });
    },
    firstUpperWord(word) {
      return word[0].toUpperCase() + word.substr(1).toLowerCase();
    },
    changeInput(key, value) {
      let month = new Date().toLocaleString("ru", { month: "long" });
      if (key === "type_of_pays") {
        value = value.toLowerCase();
      }
      this.payData[key] = value;
      this.payData["month"] =
        month[0].toUpperCase() + month.substr(1).toLowerCase();
    },
    changeData(value) {
      this.templatesPaste(value);
    },
    createPays(id) {
      var self = this 
      $.ajax({
        url: this.$store.state.backend_url + "api/pays/",
        type: "OPTIONS",
        success: function(data) {
          self.createData = data.actions.POST
          let arr  = data.actions.POST.type_of_pays.choices
          let month = data.actions.POST.month.choices
          if(self.months.length === 0){
            for (let i in month){
              self.months.unshift(month[i].value)
            }
          }
          for(let i in arr){
            self.arr_select.push(arr[i].value)
          }
          //self.months = self.months.reverse()
          //console.log(self.months.reverse())
        },
        error: function(response) {
          alert(response.responseJSON);
        }
      });
    },
    deletePays(id) {
      $.ajax({
        url: this.$store.state.backend_url + "api/pays/" + id + "/delete_pays/",
        type: "DELETE",
        success: function(data) {
        },
        error: function(response) {
          alert(response.responseJSON);
        }
      });
      setTimeout(this.userpays(this.month), 1500); //this.userpays();
    },
    paysSend(dict) {
      //console.log(this.payData)
      $.post(this.$store.state.backend_url + "api/pays/", this.payData, data => {})
      .done(response => {
         var self = this;
         self.dialog = false
         self.userpays(self.month)
      }
      )
      .fail(
        response => {
            this.error = response.responseJSON;
            //console.log(this.error);
        }
      );
    },
    templatesPaste(value) {
      let obj = this.templates[this.templates_title.indexOf(value)]
        .body_template;
        //console.log(obj)
      //this.template_form = obj
      EventBus.$emit("modelPaste", obj);
    },
    templatesSend(dict) {
      //console.log(dict)
      let body = {};
      for (let i in dict){
        body[i] = dict[i]
      }
      const templatesData = {
        body_template: JSON.stringify(body)
      };
      $.post(
        this.$store.state.backend_url + "api/templates/",
        templatesData,
        data => {}
      ).fail(response => {
        alert(response.responseText);
      });
    },
    formatDate(date) {
      const options = {
        year: "numeric",
        month: "numeric",
        day: "numeric",
        hour: "numeric",
        minute: "numeric"
      };
      return new Date(date).toLocaleDateString("ru", options);
    },
    monthString(date) {
      const options = {
        year: "numeric",
        month: 'numeric'      
        };
      return new Date(date).toLocaleDateString("ru", options);
    },
    paramsPagination(url){
      this.userpays(this.month, url.split('?')[1] )
    }
  }
};
</script>
<style>
.centered {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 50%;
    left: 0;
    overflow: auto;
}
</style>