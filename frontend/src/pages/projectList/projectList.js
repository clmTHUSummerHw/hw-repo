import { createApp } from 'vue'
import projectList from './projectList.vue'

//import element-plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'



const app = createApp(projectList)
app.use(ElementPlus) //Use element-plus
app.mount('#app')