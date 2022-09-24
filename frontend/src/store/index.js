import Vue from 'vue'
import Vuex from 'vuex'
//import parsing from './modules/parsing'

Vue.use(Vuex)

const store = new Vuex.Store({
    //modules: {
       // parsing
    //},
    state: {
        backend_url: 'https://crm.khazieff.cf/',
        domain_url: 'https://crm.khazieff.cf/'
    }
})

export default store