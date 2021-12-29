<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="6" md="6">
        <v-select
          :items="temp"
          v-model="temps"
          label="Вставить данные из шаблона"
        ></v-select>
      </v-col>
      <v-col cols="12" sm="6" md="6">
        <v-btn color="blue darken-1" text @click="titleSend" style="margin-top:15px">Вставить</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
export default {
    props: ['temp'],
    data: () => ({
        temps: ''
    }),
    methods:{
        titleSend(){
            this.$emit('changeData', this.temps);
        }
    },
}
</script>