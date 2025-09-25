import {createRouter, createWebHashHistory} from "vue-router";
import UserHome from "../views/UserHome"

const routes = [
    {
        path: "/",
        name: "UserHome",
        component: UserHome,
        children: [
            {
                path: "/",
                name: "page1",
                meta: {
                    title: '1.加权计算功能'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Page1")
            },
            // {
            //     path: "/page1",
            //     name: "page1",
            //     meta: {
            //         title: '1.加权计算功能'
            //     },
            //     component: () => import ( /* webpackChunkName: "table" */ "../views/Page1")
            // },
            {
                path: "/page2",
                name: "page2",
                meta: {
                    title: '2.合并表格功能'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Page2")
            },
            {
                path: "/page3",
                name: "page3",
                meta: {
                    title: '3.折线图功能'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Page3")
            },
            {
                path: "/page4",
                name: "page4",
                meta: {
                    title: '4.柱状图功能'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Page4")
            },
            {
                path: "/page5",
                name: "page5",
                meta: {
                    title: '5.雨课堂功能'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Page5")
            },
            {
                path: "/page6",
                name: "page6",
                meta: {
                    title: '6.饼状图功能'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Page6")
            },
            {
                path: "/page7",
                name: "page7",
                meta: {
                    title: '7.归一化成绩功能'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Page7")
            },
            {
                path: "/page8",
                name: "page8",
                meta: {
                    title: '8.能力维度图功能'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Page8")
            },
            {
                path: "/page9",
                name: "page9",
                meta: {
                    title: '9.年得分率散点图功能'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Page9/index.vue")
            },
            {
                path: "/page10",
                name: "page10",
                meta: {
                    title: '10.SPOC雷达图'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Page10")
            },
            {
                path: "/page11",
                name: "page11",
                meta: {
                    title: '11.自定义SPOC雷达图'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Page11")
            },
            {
                path: "/page12",
                name: "page12",
                meta: {
                    title: '12.基础归一化图'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Page12")
            },
            {
                path: "/page13",
                name: "page13",
                meta: {
                    title: '13.升级归一化图'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Page13")
            },
            {
                path: "/page14",
                name: "page14",
                meta: {
                    title: '14.下一步升级方向'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Page11")
            },
            {
                path: "/page15",
                name: "page15",
                meta: {
                    title: '15.下一步升级方向'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Page11")
            },

            // 在网页上显示，然后在此处增加路由
            {
                path: "/charts",
                name: "basecharts",
                meta: {
                    title: '图表'
                },
                component: () => import ( /* webpackChunkName: "charts" */ "../views/old_views/BaseCharts.vue")
            },
            // {
            //     path: "/form",
            //     name: "baseform",
            //     meta: {
            //         title: '表单'
            //     },
            //     component: () => import ( /* webpackChunkName: "form" */ "../views/old_views/BaseForm.vue")
            // },
            // {
            //     path: "/tabs",
            //     name: "tabs",
            //     meta: {
            //         title: 'tab标签'
            //     },
            //     component: () => import ( /* webpackChunkName: "tabs" */ "../views/old_views/Tabs.vue")
            // }, {
            //     path: "/donate",
            //     name: "donate",
            //     meta: {
            //         title: '鼓励作者'
            //     },
            //     component: () => import ( /* webpackChunkName: "donate" */ "../views/old_views/Donate.vue")
            // }, {
            //     path: "/permission",
            //     name: "permission",
            //     meta: {
            //         title: '权限管理',
            //         permission: true
            //     },
            //     component: () => import ( /* webpackChunkName: "permission" */ "../views/old_views/Permission.vue")
            // }, {
            //     path: "/i18n",
            //     name: "i18n",
            //     meta: {
            //         title: '国际化语言'
            //     },
            //     component: () => import ( /* webpackChunkName: "i18n" */ "../views/old_views/I18n.vue")
            // },
            // {
            //     path: "/upload",
            //     name: "upload",
            //     meta: {
            //         title: '上传插件'
            //     },
            //     component: () => import ( /* webpackChunkName: "upload" */ "../views/Upload.vue")
            // },
            // {
            //     path: "/icon",
            //     name: "icon",
            //     meta: {
            //         title: '自定义图标'
            //     },
            //     component: () => import ( /* webpackChunkName: "icon" */ "../views/old_views/Icon.vue")
            // }, {
            //     path: '/404',
            //     name: '404',
            //     meta: {
            //         title: '找不到页面'
            //     },
            //     component: () => import (/* webpackChunkName: "404" */ '../views/old_views/404.vue')
            // }, {
            //     path: '/403',
            //     name: '403',
            //     meta: {
            //         title: '没有权限'
            //     },
            //     component: () => import (/* webpackChunkName: "403" */ '../views/old_views/403.vue')
            // },
            // {
            //     path: '/test',
            //     name: 'test',
            //     meta: {
            //         title: 'test'
            //     },
            //     component: () => import (/* webpackChunkName: "403" */ '../views/Test')
            // },
            // {
            //     path: '/user',
            //     name: 'user',
            //     meta: {
            //         title: '个人中心'
            //     },
            //     component: () => import (/* webpackChunkName: "user" */ '../views/old_views/User.vue')
            // },
            // {
            //     path: '/editor',
            //     name: 'editor',
            //     meta: {
            //         title: '富文本编辑器'
            //     },
            //     component: () => import (/* webpackChunkName: "editor" */ '../views/Editor.vue')
            // }
        ]
    },
    // {
    //     path: "/login",
    //     name: "Login",

    //     meta: {
    //         title: '登录'
    //     },
    //     component: () => import ( /* webpackChunkName: "login" */ "../views/Login.vue")
    // },

];

const router = createRouter({
    history: createWebHashHistory(),
    // history:_emscripten_glMatrixMode(),
    // history:createRouter(),
    // mode:'history',
    routes
});


export default router;
