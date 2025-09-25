import {createApp} from 'vue'
import App from './App.vue'

import router from './router'
import store from './store'

import installElementPlus from './plugins/element'
import './assets/css/icon.css'

import { VConsole } from "vconsole";

const app = createApp(App)
installElementPlus(app)



// app.$router = router
// app.$store = store

app
    .use(store)
    .use(router)
    .mount('#app')
// 添加JaChat
export default app
