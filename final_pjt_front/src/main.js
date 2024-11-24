import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'

import axios from 'axios'
axios.defaults.baseURL = 'http://localhost:8000'  // Django 서버 주소

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
// console.log('KAKAO API KEY:', import.meta.env.VITE_KAKAO_MAP_API_KEY)