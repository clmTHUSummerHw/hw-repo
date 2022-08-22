import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios';
import setupAll from './languages/setupAll';

import '@/assets/main.css'
import 'font-awesome/css/font-awesome.css'

axios.defaults.baseURL = '/api/'

const app = createApp(App)

app.use(createPinia())
app.use(router)

setupAll.setup();

app.mount('#app')
