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
      <v-row>
        <v-col cols="12">
          <v-card v-for="n in notes" :key="n.id" v-show="notes.length > 0">
            <v-list  two-line>
              <template>
                <v-list-item>
                  <v-list-item-avatar>
                    <v-icon>mdi-pen</v-icon>
                  </v-list-item-avatar>

                  <v-list-item-content>
                    <v-list-item-title>{{ n.title }}</v-list-item-title>

                    <v-list-item-subtitle v-html="n.body"></v-list-item-subtitle>
                  </v-list-item-content>
                  <v-col cols="auto">
                    <v-dialog transition="dialog-bottom-transition" max-width="600">
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn color="success" v-bind="attrs" v-on="on">
                          <v-icon>mdi-pen</v-icon>
                        </v-btn>
                        <v-btn color="error" class="ml-2" @click="deleteNotes(n.id)">
                          <v-icon>mdi-delete</v-icon>
                        </v-btn>
                      </template>
                      <template v-slot:default="dialog">
                        <v-card>
                          <v-card-title>
                            <span class="text-h5">Редактировать заметку</span>
                          </v-card-title>
                          <v-container>
                            <v-row>
                              <v-col cols="12">
                                <v-text-field label="Название" v-model="n.title" required></v-text-field>
                              </v-col>
                              <v-col cols="12">
                                <ckeditor :editor="editor" v-model="n.body" :config="editorConfig"></ckeditor>
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
  </v-main>
</template>

<script>
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import $ from "jquery";
import NavAndFooter from "../components/NavAndFooter";
export default {
  components: { NavAndFooter },
  metaInfo: {
    title: "Заметки - Цитадель"
  },
  name: "Notes",
  data: () => ({
    editor: ClassicEditor,
    editorConfig: {
      // The configuration of the rich-text editor.
    },
    dialog: false,
    notes: [],
    person_name: "",
    title: "",
    body: ""
  }),
  created() {
    this.username = localStorage.getItem("username");
    this.userNotes();
  },
  methods: {
    userNotes() {
      $.get("http://localhost:8002/api/user/" + this.username + "/", data => {
        this.notes = data.notes;
      });
    },
    notesSend() {
      const notesData = {
        person_name: localStorage.getItem("username"),
        title: this.title,
        body: this.body
      };
      $.post("http://localhost:8002/api/notes/", notesData, data => {}).fail(
        response => {
          alert(response.responseText);
        }
      );
      this.dialog = false;

      setTimeout(this.userNotes, 1500);
    },
    deleteNotes(id) {
      $.ajax({
        url: "http://localhost:8002/api/notes/" + id + "/delete_notes/",
        type: "DELETE",
        success: function(data) {
          alert("Удалено");
        },
        error: function(response) {
          alert(response.responseJSON);
        }
      });
      this.userNotes();
    },
    editNotes(id, title, body) {
      const notesData = {
        id: id,
        person_name: localStorage.getItem("username"),
        title: title,
        body: body
      };
      $.post(
        "http://localhost:8002/api/notes/" + id + "/edit_notes/",
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