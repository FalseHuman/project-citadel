import Vue from 'vue'
import Vuex from 'vuex'
//import parsing from './modules/parsing'

Vue.use(Vuex)

const store = new Vuex.Store({
    //modules: {
       // parsing
    //},
    state: {
        backend_url: 'http://92.255.107.252/',
        domain_url: 'http://92.255.107.252/'
    }
})

export default store