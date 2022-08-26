<template>
    <div id="admin-page">
        <el-container class="box-base">
            <el-header class="box-header"> <!--标题-->
                <el-button type="primary" @click="goAdmin" class="backButton" size="big">返回</el-button>
                <div class="title">日志页面</div>
                <div class="projectUserInfo">
                    <a>当前用户名：{{userName}}</a><br>
                    <a>当前项目名：{{projectName}}</a>
                </div>
            </el-header>

            <el-main>
                <!--展示项目包含项目列表的表格-->
                <el-table
                border
                table-layout="auto"
                empty-text="No Log"
                :data="logData"
                style="width: 100%">

                    <!--prop是logData中的键-->
                    <el-table-column prop="logDatetime" label="日期时间" sortable></el-table-column>
                    <el-table-column prop="logContent" label="具体内容"></el-table-column>
                    <el-table-column prop="logObject" label="操作对象"></el-table-column>

                </el-table>
            </el-main>
        </el-container>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import axios from "axios";

class Data {
    logData: {logDatetime: any; logContent: any; logObject: any;}[] = []
}

export default defineComponent({
    name: "LogPage",
    data()
    {
        return new Data()
    },

    methods: {
        goAdmin() {
            this.$router.push({name:'admin'});
        },
        async updateTable() {
            try
            {
                let username = this.$route.params.username;
                let projectName = this.$route.params.projectName;
                let jsonForm = {
                    'username': username,
                    'projectname': projectName
                }
                let result = await axios.post('/user/get-logs', jsonForm);
                let data = result.data.log;
                let result_list = [];
                function getLogType(logcode: Number) {
                    switch(logcode) {
                        case 0: return 'PROJECT BUILD'; break;
                        case 1: return 'NEW FILE'; break;
                        case 2: return 'NEW FOLDER'; break;
                        case 3: return 'DELETE FILE'; break;
                        case 4: return 'DELETE FOLDER'; break;
                        case 5: return 'FILE UPLOAD'; break;
                        case 6: return 'FILE DOWNLOAD'; break;
                        case 7: return 'RUN PROJECT'; break;
                        case 8: return 'DEBUG PROJECT'; break;
                        case 9: return 'DEPENDENCY ADDED'; break;
                        case 10: return 'DEPENDENCY REMOVED'; break;
                        case 11: return 'PACKED UP'; break;
                        default: break;
                    }
                }
                for (let i in data)
                {
                    let current_log = {
                        logDatetime: new Date(data[i].time),
                        logContent: getLogType(data[i].code),
                        logObject: data[i].extra_data
                    }
                    result_list.push(current_log);
                    console.log(current_log);
                }
                this.logData = result_list;
                return;
            }
            catch(e)
            {
                console.log(e);
                return;
            }
        }
    },
    computed: {
        userName() {
            return this.$route.params.username;
        },
        projectName() {
            return this.$route.params.projectName
        },
        getOperation() {
            //TODO: 根据相应中log[x].code输出字符串形式的操作内容
        }
    },
    mounted() {
        this.updateTable();
    }
})
</script>

<style lang="scss">
#admin-page
{
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;

    box-sizing: border-box;
    width: 100%;
    height: 800px;
    background-image: url(@/assets/small_logo_bg.png);

    .box-base
    {
        /* 整体框 */
        color: black;
        background-color: white;
        box-shadow: 1px 0 10px rgb(0 0 0 / 30%);

        margin: auto;
        width: 90%;
        height: 600px;

        position: relative;
        top: 7%;
    }

    .box-header
    {
        /* 顶部展示当前用户、项目信息 */
        padding: 0;

        display: flex;
        align-items: center;

        border-bottom: 1px solid grey;
    }

    .title
    {
        /* “日志页面” 字体设置 */
        font-size: 36px;
        height: 58px;
        flex-grow: 5;
    }

    .projectUserInfo
    {
        /* 展示用户名、项目名 */
        font-size: 18px;
        height: 58px;
        flex-grow: 1;
        text-align: left;
    }

    .backButton {
        margin-left: 20px;
    }
}
</style>