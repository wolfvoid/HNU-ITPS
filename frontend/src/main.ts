import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'reset-css'
import 'virtual:uno.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './routers'
import './style.css'
import locale from 'element-plus/dist/locale/zh-cn.mjs'

const app = createApp(App)

app.use(ElementPlus, { locale })
app.use(router)
app.mount('#app')

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
