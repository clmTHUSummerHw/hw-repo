<template>
    <div id="admin-page">
        <el-container class="box-base">
            <el-header class="box-header"> <!--标题-->
                <div class="title">管理者页面</div>
            </el-header>

            <el-main>
                <!--展示项目包含项目列表的表格-->
                <el-table
                border
                table-layout="auto"
                :data="projectData"
                style="width: 100%">

                    <!--prop是projectData中的键-->
                    <el-table-column prop="projectUsername" label="项目发起人"></el-table-column>
                    <el-table-column prop="projectName" label="项目名称" sortable></el-table-column>
                    <el-table-column prop="projectCreateDate" label="项目创建日期"></el-table-column>
                    <el-table-column prop="projectDirectory" label="项目路径"></el-table-column>
                    <el-table-column> <!--搜索栏以及查看项目日志链接-->
                        <template #default="scope">
                            <el-button
                                @click="getLog(scope.row)"
                                link
                                type="primary"
                                size="small">查看项目日志
                            </el-button>
                        </template>
                    </el-table-column>

                </el-table>
            </el-main>
        </el-container>
    </div>
</template>

<script lang="ts">
import axios from "axios";
import { defineComponent } from "vue";

class Data {
    projectData: { projectUsername: any; projectName: any; projectCreateDate: any; projectDirectory: any; }[] = []
}

export default defineComponent({
    name: "AdminPage",
    data() {
        return new Data()
    },

    methods: {
        async getLog(row: any) {
            this.$router.push({
                name:"projectLog", 
                params: {
                    username:row.projectUsername, 
                    projectName: row.projectName
                }
            });
            
        },
        async updateTable() {
            try
            {
                let result = await axios.post('/user/get-all-project');
                let data = result.data.projects;
                this.projectData = data;
                return;
            }
            catch(e)
            {
                console.log(e);
                return;
            }
        }
    },
    mounted() {
        this.updateTable()
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
        /* 顶部展示当前用户信息 */
        padding: 0;

        display: flex;
        align-items: center;

        border-bottom: 1px solid grey;
    }

    .title
    {
        /* “项目列表” 字体设置 */
        font-size: 36px;
        height: 58px;
        flex-grow: 1;
    }

    .user-info
    {
        /* 调整用户信息栏的flex-grow */
        flex-grow: 4;

        h3
        {
            /* 调整用户信息栏标题上下margin */
            margin-top: 0;
            margin-bottom: 5px;
        }
    }
}
</style>