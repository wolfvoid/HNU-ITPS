import * as VueRouter from 'vue-router'
import FullPage from '../layouts/Adminlayout.vue'
import Home from '../pages/Home.vue'
import Userhome from '../pages/Userhome.vue'
import UserVue from '../pages/User.vue'
import userlayoutVue from '../layouts/userlayout.vue'
import LoginVue from '../pages/Login.vue'
import PreVue from '../pages/pre.vue'
import RealtimeVue from '../pages/Realtime.vue'
import VisionVue from '../pages/Vision.vue'
// 2. 定义一些路由
// 每个路由都需要映射到一个组件。
// 我们后面再讨论嵌套路由。
const routes:any = [
    {
        path: '/login',
        component: LoginVue,
        title: '登录界面',
    },
    {
        path: '/u',
        component: userlayoutVue,
        redirect: '/u/userhome',
        children: [
            {
                path: 'userhome',
                component: Userhome,
                title: '首页',
            },
            
            {
                path: 'pre',
                component: PreVue,
                title: '预测一览',
            },
            {
                path: 'realtime',
                component: RealtimeVue,
                title: '实时交通预测',
            },
            {
                path: 'vision',
                component: VisionVue,
                title: '可视化界面',
            },
        ],
    },
    {
        path: '/',
        component: FullPage,
        children: [
            {
                path: '',
                component: Home,
                title: '首页',
            },
            {
                path: 'User',
                component: UserVue,
                title: '用户管理'
            },
            {
                path: 'pre',
                component: PreVue,
                title: '预测一览',
            },
            {
                path: 'realtime',
                component: RealtimeVue,
                title: '实时交通预测',
            },
            {
                path: 'vision',
                component: VisionVue,
                title: '可视化界面',
            },
        ],
    },
]

// 3. 创建路由实例并传递 `routes` 配置
// 你可以在这里输入更多的配置，但我们在这里
// 暂时保持简单
const router = VueRouter.createRouter({
    // 4. 内部提供了 history 模式的实现。为了简单起见，我们在这里使用 hash 模式。
    history: VueRouter.createWebHashHistory(),
    routes, // `routes: routes` 的缩写
})

// 添加路由守卫
router.beforeEach((to, from, next) => {
    // console.log(to, from)
    if (to.path === '/login') {
        next()
    } else {
        const user: {
            id: number
            name: string
            type: 0 | 1 // 0: 管理员 1: 普通用户
        } = JSON.parse(localStorage.getItem('user') || null)

        // 如果用户信息不存在，跳转到登录页
        if (!user) {
            next('/login')
            return
        }
        // 管理员不能访问移动端页面
        if (user.type === 0 && to.path.startsWith('/u')) {
            next('/')
            return
        }
        // 普通用户不能访问管理端页面
        if (user.type === 1 && !to.path.startsWith('/u')) {
            next('/u')
            return
        }

        next()
    }
})
export default router
