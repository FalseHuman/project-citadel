<template>
  <v-main>
    <NavAndFooter />
    <v-container class="py-8 px-6" fluid>
      <div>
        <v-row justify="center">
          <v-dialog v-model="dialog" persistent max-width="600px">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="primary"
                dark
                small
                fab
                v-bind="attrs"
                v-on="on"
                style="margin-bottom: 10px; margin-top: 0; margin-left: 5px;"
                title="Добавить"
              >
                <v-icon dark>mdi-plus</v-icon>
              </v-btn>
              <v-btn
                color="primary"
                dark
                small
                fab
                style="margin-bottom: 10px; margin-top: 0; margin-left: 5px;"
                title="Обновить"
              >
                <v-icon dark @click="userpays">mdi-refresh</v-icon>
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="text-h5">Добавить платеж</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        label="Назначение платежа*"
                        hint="Например, 'На молоко'"
                        v-model="title"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field v-model="body" label="Описание платежа"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="6">
                      <v-text-field
                        label="Сумма списания/пополнения*"
                        v-model="cost"
                        hint="Например, '200' для пополнения и '-200' для списания"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="6">
                      <v-select
                        :items="['Карта','Наличные']"
                        v-model="type_of_pays"
                        label="Тип платежа:*"
                        required
                      ></v-select>
                    </v-col>
                  </v-row>
                </v-container>
                <small>*Обязательные поля</small>
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
      <v-row>
        <v-col v-for="year in years" :key="year" cols="12">
          <p>{{year}} год</p>
          <v-col v-for="month in months" :key="month" cols="12" v-show="monthes(month, pays) !== 0">
            <v-card>
              <v-subheader>{{ month }} - {{ monthsPays(month, year) }}</v-subheader>

              <v-list two-line>
                <template v-for="n in pays">
                  <v-list-item :key="n.id" v-if="n.month === month && year === yearDate(n.data)">
                    <v-list-item-icon>
                      <v-icon v-if="n.type_of_pays=='наличные'">mdi-cash</v-icon>
                      <v-icon v-else-if="n.type_of_pays=='карта'">mdi-credit-card</v-icon>
                      <v-icon v-else>mdi-help</v-icon>
                    </v-list-item-icon>

                    <v-list-item-content>
                      <v-list-item-title>{{ n.title }}</v-list-item-title>

                      <v-list-item-subtitle>{{n.cost}} руб., {{formatDate(n.data)}}</v-list-item-subtitle>
                    </v-list-item-content>
                    <v-col cols="auto">
                      <v-dialog transition="dialog-bottom-transition" max-width="600">
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn color="primary" v-bind="attrs" v-on="on">
                            <v-icon>mdi-information</v-icon>
                          </v-btn>
                        </template>
                        <template v-slot:default="dialog">
                          <v-card>
                            <v-toolbar color="primary" dark>{{n.title}}</v-toolbar>
                            <v-card-text>
                              <div class="text-h5 pa-5">Назначение платежа: {{n.title}}</div>
                              <div class="text-h5 pa-5">Сумма платежа: {{n.cost}} руб.</div>
                              <div class="text-h5 pa-5">Тип платежа: {{n.type_of_pays}}</div>
                              <div class="text-h5 pa-5">Описание платежа: {{n.body}}</div>
                              <div class="text-h5 pa-5">Дата платежа: {{formatDate(n.data)}}</div>
                            </v-card-text>
                            <v-card-actions class="justify-end">
                              <v-btn text @click="dialog.value = false">Закрыть</v-btn>
                            </v-card-actions>
                          </v-card>
                        </template>
                      </v-dialog>
                    </v-col>
                  </v-list-item>
                </template>
              </v-list>
            </v-card>
          </v-col>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import $ from "jquery";
import NavAndFooter from "../components/NavAndFooter";
export default {
  components: { NavAndFooter },
  metaInfo: {
    title: "Расходы/Доходы - Цитадель"
  },
  name: "Cash",
  data: () => ({
    loading: null,
    years: [],
    months: [
      "Декабрь",
      "Ноябрь",
      "Октябрь",
      "Сентябрь",
      "Август",
      "Июль",
      "Июнь",
      "Май",
      "Апрель",
      "Март",
      "Февраль",
      "Январь"
    ],
    months_pays: [],
    dialog: false,
    pays: [],
    author_name: "",
    title: "",
    body: "",
    cost: "",
    type_of_pays: "",
    data: "",
    month: ""
  }),
  created() {
    this.username = localStorage.getItem("username");
    this.userpays();
    this.monthes();
  },
  methods: {
    userpays() {
      $.get(
        "http://localhost:8002/api/user/" +
          this.username +
          "/",
        data => {
          this.pays = data.pays;
          //this.monthes(data.pays)
          let year = [];
          for (let i = 0; i < this.pays.length; i++) {
            year.push(this.yearDate(this.pays[i].data));
          }
          this.years = Array.from(new Set(year));
        }
      );
    },
    monthes(mon, array) {
      let count = 0;
      for (let i = 0; i < array.length; i++) {
        if (array[i].month === mon) {
          count += 1;
        }
      }
      return count;
    },
    monthsPays(month, year) {
      let sum = 0;
      let minussum = 0;
      for (let i = 0; i < this.pays.length; i++) {
        //console.log('pays', Number(this.pays[i].cost))
        let num = Number(this.pays[i].cost);
        if (
          this.pays[i].month === month &&
          this.yearDate(this.pays[i].data) === year
        ) {
          if (num > 0) {
            sum += num;
          } else {
            minussum += num;
          }
        }
      }
      return (
        "Потрачено: " +
        minussum.toString() +
        " руб. " +
        "Получено: " +
        sum.toString() +
        " руб."
      );
    },
    paysSend() {
      let month = new Date().toLocaleString("ru", { month: "long" });
      const payData = {
        author_name: localStorage.getItem("username"),
        title: this.title,
        body: this.body,
        type_of_pays: this.type_of_pays.toLowerCase(),
        cost: this.cost,
        month: month[0].toUpperCase() + month.substr(1).toLowerCase()
      };
      $.post(
        "http://localhost:8002/api/pays/",
        payData,
        data => {}
      ).fail(response => {
        alert(response.responseText);
      });
      this.dialog = false;

      setTimeout(this.userpays, 1500);
    },
    formatDate(date) {
      const options = {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "numeric"
      };
      return new Date(date).toLocaleDateString("ru", options);
    },
    yearDate(date) {
      const options = { year: "numeric" };
      return new Date(date).toLocaleDateString("ru", options);
    },
  }
};
</script>