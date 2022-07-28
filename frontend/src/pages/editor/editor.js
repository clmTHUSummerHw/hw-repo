import { createApp } from 'vue'
import Editor from './editor.vue'

//import element-ui
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'


//import axios
import axios from 'axios'

const app = createApp(Editor)

app.use(ElementPlus) //Use element-ui
app.config.globalProperties.axios=axios //将axios添加到app实例中的js模块
app.mount('#app')