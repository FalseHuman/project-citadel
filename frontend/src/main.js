import Vue from 'vue'
import store from './store'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import Meta from 'vue-meta';
import CKEditor from '@ckeditor/ckeditor5-vue2';
Vue.use(Meta);
Vue.use( CKEditor );
Vue.config.productionTip = false

new Vue({
  router,
  vuetify,
  store,
  render: h => h(App)
}).$mount('#app')
