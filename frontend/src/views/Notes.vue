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
                  @click="userNotes"
                >
                  <v-icon dark>mdi-refresh</v-icon>
                </v-btn>
              </template>
              <v-card>
                <v-card-title>
                  <span class="text-h5">Добавить заметку</span>
                </v-card-title>
                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field label="Название" v-model="title" required></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <ckeditor :editor="editor" v-model="body" :config="editorConfig"></ckeditor>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="dialog = false">Закрыть</v-btn>
                  <v-btn color="blue darken-1" text @click="notesSend">Сохранить</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-row>
        </div>
        <p  class="text-center centered" v-if="notes.length ===0">Тут пока нет ни одной заметки:(</p>
        <v-row>
          <v-col cols="12">
            <v-card v-for="n in notes" :key="n.id" v-show="notes.length > 0">
              <v-list two-line>
                <template>
                  <v-list-item>
                    <v-list-item-avatar>
                      <v-icon>mdi-pen</v-icon>
                    </v-list-item-avatar>

                    <v-list-item-content>
                      <v-list-item-title>{{ n.title }}</v-list-item-title>
                    </v-list-item-content>
                    <v-col cols="auto">
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
                                <v-btn color="success" v-bind="attrs" v-on="on">
                                  <v-icon>mdi-pen</v-icon>
                                </v-btn>
                                <v-btn color="error" @click="deleteNotes(n.id)" class="ml-2">
                                  <v-icon>mdi-delete</v-icon>
                                </v-btn>
                              </v-list>
                            </v-menu>
                          </div>
                          <div v-else>
                            <v-btn color="success" v-bind="attrs" v-on="on">
                              <v-icon>mdi-pen</v-icon>
                            </v-btn>
                            <v-btn color="error" @click="deleteNotes(n.id)" class="ml-2">
                              <v-icon>mdi-delete</v-icon>
                            </v-btn>
                          </div>
                        </template>
                        <template v-slot:default="dialog">
                          <v-card>
                            <v-card-title>
                              <span class="text-h5">Редактировать заметку</span>
                            </v-card-title>
                            <v-container>
                              <v-row>
                                <v-col cols="12">
                                  <v-text-field label="Название" v-model="n.title"></v-text-field>
                                </v-col>
                                <v-col cols="12">
                                  <ckeditor
                                    :editor="editor"
                                    v-model="n.body"
                                    :config="editorConfig"
                                    style="backround: red;"
                                  ></ckeditor>
                                </v-col>
                              </v-row>
                            </v-container>
                            <v-card-text></v-card-text>
                            <v-card-actions class="justify-end">
                              <v-btn text @click="dialog.value = false">Закрыть</v-btn>
                              <v-btn text @click="editNotes(n.id, n.title, n.body)">Изменить</v-btn>
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
        </v-row>
      </v-container>
    </div>
  </v-main>
</template>

<script>
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import "@ckeditor/ckeditor5-build-classic/build/translations/ru";
import $ from "jquery";
import NavAndFooter from "../components/NavAndFooter";
import Loading from "../components/Loading";
export default {
  components: { NavAndFooter, Loading },
  metaInfo: {
    title: "Заметки - Цитадель"
  },
  name: "Notes",
  data: () => ({
    editor: ClassicEditor,
    editorConfig: {
      language: "ru"
    },
    load: null,
    dialog: false,
    notes: [],
    person_name: "",
    title: "",
    body: ""
  }),
  created() {
    this.userNotes();
  },
  methods: {
    userNotes() {
      this.load = true;
      $.get(this.$store.state.backend_url + "api/notes/", data => {
        //console.log(data)
        this.notes = data;
        //let link = this.notes[0].body
        this.load = false;
      });
    },
    findLink(body) {
      let link = body;
      link = link.match(/(https?:\/\/[^\s]+)/g);
      if (String(link)) {
        return '<a href="' + link + '">' + "Перейти по ссылке" + "</a>";
      }
    },
    notesSend() {
      const notesData = {
        title: this.title,
        body: this.body
      };
      //console.log(notesData)
      $.post(this.$store.state.backend_url + "api/notes/", notesData, data => {}).fail(
        response => {
          alert(response.responseText);
        }
      );
      this.dialog = false;
      setTimeout(this.userNotes, 1500);
    },
    deleteNotes(id) {
      $.ajax({
        url: this.$store.state.backend_url + "api/notes/" + id + "/delete_notes/",
        type: "DELETE",
        success: function(data) {
          //alert("Удалено");
        },
        error: function(response) {
          alert(response.responseJSON);
        }
      });
      setTimeout(this.userNotes, 1500);
    },
    editNotes(id, title, body) {
      const notesData = {
        id: id,
        title: title,
        body: body
      };
      $.post(
        this.$store.state.backend_url + "api/notes/" + id + "/edit_notes/",
        notesData,
        data => {}
      ).fail(response => {
        alert(response.responseText);
      });
      this.dialog = false;
      setTimeout(this.userNotes, 1500);
    }
  }
};
</script>