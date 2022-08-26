import { createApp } from 'vue';
import { createPinia } from 'pinia';
import piniaPersist from 'pinia-plugin-persist';

import App from './App.vue';
import router from './router';
import axios from 'axios';
import setupAll from './languages/setupAll';

import '@/assets/main.css';
import 'font-awesome/css/font-awesome.css';
import 'element-plus/es/components/message-box/style/index';

axios.defaults.baseURL = '/api/';

const app = createApp(App);
const pinia = createPinia();

pinia.use(piniaPersist);
app.use(pinia);
app.use(router);

setupAll.setup();

app.mount('#app')
