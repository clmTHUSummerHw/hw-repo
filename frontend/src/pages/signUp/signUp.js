import { createApp } from 'vue'
import signUp from './signUp.vue'

//import element-plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

//import axios
import axios from 'axios'


const app = createApp(signUp)

app.use(ElementPlus) //Use element-plus
app.config.globalProperties.axios=axios //axios
app.mount('#app')