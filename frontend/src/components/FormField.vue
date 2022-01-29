<template>
  <v-col :cols="cols" :sm="sm" :md="md">
    <v-text-field
      :label="`${labels}`"
      :hint="`Введите ${labels.toLowerCase()}`"
      v-model="input"
      :alert="true"
      @input="inputSend"
      v-if="type_input === 'input'"
      :error="error ? true : false"
      :messages="error ? error[key_label].toString(): null"
      required
      clearable
    ></v-text-field>
    <v-text-field
      :label="`${labels}`"
      :hint="`Введите ${labels.toLowerCase()}`"
      v-model="input"
      :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
      :type="showPassword ? 'text' : 'password'"
      required
      @input="inputSend"
      @click:append="showPassword = !showPassword "
      v-else-if="type_input === 'password'"
      :error="error ? true : false"
      :messages="error ? error[key_label].toString(): null"
      clearable
    ></v-text-field>
    <v-select
      v-else-if="type_input === 'select'"
      :items="arr_select"
      v-model="input"
      :label="`${labels}`"
      :hint="`Введите ${labels.toLowerCase()}`"
      :error="error ? true : false"
      @input="inputSend"
      :messages="error ? error[key_label].toString(): null"
      required
      clearable
    ></v-select>
    <ckeditor
      :editor="editor"
      v-model="input"
      :config="editorConfig"
      v-else-if="type_input === 'editor'"
    ></ckeditor>
  </v-col>
</template>
<script>
import EventBus from "../event/event-bus";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import "@ckeditor/ckeditor5-build-classic/build/translations/ru";
export default {
  props: [
    "type_input",
    "key_label",
    "labels",
    "arr_select",
    "sm",
    "md",
    "cols",
    "model",
    "error"
  ],
  data: () => ({
    input: "",
    rules: [],
    editor: ClassicEditor,
    editorConfig: {
      language: "ru"
    },
    showPassword: false
  }),
  mounted() {
    EventBus.$on("modelPaste", obj => {
      for (let i in obj) {
        if (this.key_label === i) {
          this.input = obj[i];
        }
      }
      this.inputSend();
    });
  },
  methods: {
    inputSend() {
      this.$emit("changeInput", this.key_label, this.input);
    }
  }
};
</script>