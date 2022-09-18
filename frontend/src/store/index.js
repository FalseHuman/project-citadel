import Vue from 'vue'
import Vuex from 'vuex'
//import parsing from './modules/parsing'

Vue.use(Vuex)

const store = new Vuex.Store({
    //modules: {
       // parsing
    //},
    state: {
        backend_url: 'http://localhost:8000/',
        domain_url: 'http://localhost:8000/'
    }
})

export default store