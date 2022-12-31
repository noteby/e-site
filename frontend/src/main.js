import {createApp} from 'vue'
//
import 'element-plus/dist/index.css'
//
import './style.css'
//

import App from './App.vue'
import router from './router'
import store from './store'

const app = createApp(App)
app.use(router)
app.use(store)

import './permission'

app.mount('#app')
