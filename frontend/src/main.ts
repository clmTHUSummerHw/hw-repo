import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios';
import setupAll from './languages/setupAll';

import WsConnector from './utils/ws-util/WsConnector';

import '@/assets/main.css'

axios.defaults.baseURL = '/api/'

const app = createApp(App)

app.use(createPinia())
app.use(router)

setupAll.setup();

app.mount('#app')

let testConnector = new WsConnector('/run');