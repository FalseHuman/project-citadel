import Vue from 'vue'
import VueRouter from 'vue-router'
import Cash from '../views/Cash.vue'
import Login from '../components/Login.vue'
import Profile from '../views/Profile.vue'
import Register from '../components/Register.vue'
import Reset from '../components/Reset.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Cash',
        component: Cash
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/reset-password',
        name: 'Reset',
        component: Reset
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile
    },
    {
        path: '/registraitions',
        name: 'Register',
        component: Register

    },
]

const router = new VueRouter({
    mode: 'history',
    routes
})

router.beforeEach((to, from, next) => {
    if (localStorage.getItem('auth-token') !== null || to.path === '/login' || to.path === '/registraitions' || to.path === '/reset-password') {
        next()
    } else {
        next('/login')
    }
})

export default router