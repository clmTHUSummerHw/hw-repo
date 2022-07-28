import { createApp } from 'vue'
import Index from './index.vue'

//import element-plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'


//import axios
import axios from 'axios'


const app = createApp(Index)
app.use(ElementPlus) //Use element-plus
app.config.globalProperties.axios=axios //将axios添加到app实例中的js模块
app.mount('#app')