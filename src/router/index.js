import Vue from 'vue'
import VueRouter from 'vue-router';
import Home from "@/Home";
import home1 from "@/views/home1";
import home2 from "@/views/home2";
import file_home2 from "@/views/file_home2";
import file_home1 from "@/views/file_home1";
import Admin from "@/Admin.vue";
import alipay from "@/views/pay.vue";
import login from "@/views/login.vue";
import userInfo from "@/views/userInfo.vue";
import orderInfo from "@/views/orderInfo.vue";
import subInfo from "@/views/subInfo.vue";
import cSubInfo from "@/views/cSubInfo.vue";
import user_select from "@/views/admin/user_select.vue";
import user from "@/views/admin/user.vue";
import visit from "@/views/admin/visit.vue";
import register from "@/views/register.vue";
import publish_notify from "@/views/admin/publish_notify.vue";
import check_notify from "@/views/admin/check_notify.vue";
import discount from "@/views/admin/coupon.vue";
import used_coupons from "@/views/admin/used_coupons.vue";
import feedback from "@/views/feedback.vue";
import check_feedback from "@/views/admin/check_feedback.vue";
import notification from "@/views/notification.vue";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'login',
        meta: {showMenu: false},
        component: login
    },
    {
        path: '/register',
        name: 'register',
        meta: {showMenu: false},
        component: register
    },
    {
        path: '/Home',
        name: 'Home',
        meta: {showMenu: false},
        component: Home,
        children: [{
            path: '/home1',
            name: 'home1',
            meta: {showMenu: true},
            component: home1
        }, {
            path: '/home2',
            name: 'home2',
            meta: {showMenu: true},
            component: home2
        }, {
            path: '/file_home2',
            name: 'file_home2',
            meta: {showMenu: true},
            component: file_home2
        }, {
            path: '/file_home1',
            name: 'file_home1',
            meta: {showMenu: true},
            component: file_home1
        }, {
            path: '/pay',
            name: 'pay',
            meta: {showMenu: false},
            component: alipay,
        }, {
            path: '/userInfo',
            name: 'userInfo',
            meta: {showMenu: false},
            component: userInfo,
        }, {
            path: '/orderInfo',
            name: 'orderInfo',
            meta: {showMenu: false},
            component: orderInfo,
        }, {
            path: '/subInfo',
            name: 'subInfo',
            meta: {showMenu: false},
            component: subInfo,
        }, {
            path: '/cSubInfo',
            name: 'cSubInfo',
            meta: {showMenu: false},
            component: cSubInfo,
        }, {
            path: '/feedback',
            name: 'feedback',
            meta: {showMenu: false},
            component: feedback,
        }, {
            path: '/notification',
            name: 'notification',
            component: notification,
        }]
    },
    {
        path: '/Admin',
        name: 'Admin',
        component: Admin,
        children: [{
            path: '/user_test3',
            name: 'user',
            component: user
        }, {
            path: '/user_select',
            name: 'user_select',
            component: user_select
        }, {
            path: '/visit',
            name: 'visit',
            component: visit
        }, {
            path: '/publish_notify',
            name: 'publish_notify',
            component: publish_notify
        }, {
            path: '/check_notify',
            name: 'check_notify',
            component: check_notify
        }, {
            path: '/discount',
            name: 'discount',
            component: discount
        }, {
            path: '/used_coupons',
            name: 'used_coupons',
            component: used_coupons
        }, {
            path: '/check_feedback',
            name: 'check_feedback',
            component: check_feedback
        },]
    },

]

const router = new VueRouter({
    mode: "history",
    routes
})

export default router