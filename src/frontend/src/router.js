import Vue from 'vue'
import Router from 'vue-router'
import DashboardLayout from '@/layout/DashboardLayout'
import AuthLayout from '@/layout/AuthLayout'

Vue.use(Router);

export default new Router({
    linkExactActiveClass: 'active',
    routes: [
        {
            path: '/',
            redirect: 'dashboard',
            component: DashboardLayout,
            children: [
                {
                    path: '/dashboard',
                    name: 'dashboard',
                    // route level code-splitting
                    // this generates a separate chunk (about.[hash].js) for this route
                    // which is lazy-loaded when the route is visited.
                    component: () => import(/* webpackChunkName: "demo" */ './views/Dashboard.vue')
                },
                {
                    path: '/icons',
                    name: 'icons',
                    component: () => import(/* webpackChunkName: "demo" */ './views/Icons.vue')
                },
                {
                    path: '/settings',
                    name: 'settings',
                    component: () => import(/* webpackChunkName: "demo" */ './views/Settings.vue')
                },
                {
                    path: '/maps',
                    name: 'maps',
                    component: () => import(/* webpackChunkName: "demo" */ './views/Maps.vue')
                },
                {
                    path: '/tables',
                    name: 'tables',
                    component: () => import(/* webpackChunkName: "demo" */ './views/Tables.vue')
                },
                {
                    path: '/search',
                    name: 'search',
                    component: () => import(/* webpackChunkName: "demo" */ './views/Search.vue')
                },
                {
                    path: '/message',
                    name: 'message',
                    component: () => import(/* webpackChunkName: "demo" */ './views/Message.vue')
                },
                {
                    path: '/friends',
                    name: 'friends',
                    component: () => import(/* webpackChunkName: "demo" */ './views/Test.vue')
                }
            ]
        },
        {
            path: '/',
            redirect: 'login',
            component: AuthLayout,
            children: [
                {
                    path: '/login',
                    name: 'login',
                    component: () => import(/* webpackChunkName: "demo" */ './views/Login.vue')
                },
                {
                    path: '/register',
                    name: 'register',
                    component: () => import(/* webpackChunkName: "demo" */ './views/Register.vue')
                }
            ]
        },
        {
            path: '/test',
            name: 'test',
            component: () => import(/* webpackChunkName: "demo" */ './views/Test.vue')
        }
    ],
    scrollBehavior(to, from, saveTop) {
        if (saveTop) {
            return saveTop;
        } else {
            return {x: 0, y: 0}
        }
    }
})
