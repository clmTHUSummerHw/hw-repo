<template>
    <div id="project-list">
        <el-container class="box-base">
            <el-header class="box-header">
                <!--顶部展示用户信息，flex容器-->
                <div class="title">项目列表</div>
                <!--用户信息展示栏-->
                <div class="user-info">
                    <h3>用户信息</h3>
                    <a>用户名: </a>
                    <!--若为已登录用户，则显示用户名，否则显示一条杠-->
                    <a v-if="isLogin"> {{ $store.state.username }} </a>
                    <a v-else> - </a>

                    <a>登录状态: </a>
                    <el-tag class="ml-2" type="success" v-if="isLogin">已登录</el-tag>
                    <el-tag class="ml-2" type="danger" v-else>未登录</el-tag>
                </div>
                <!--todo: 展示用户详细信息-->
            </el-header>

            <el-main>
                <!--展示项目包含项目列表的表格-->
                <el-table :data="projectData" style="width: 100%">

                    <el-table-column label="项目名称"></el-table-column>
                    <el-table-column label="项目创建时间"></el-table-column>
                    <el-table-column label="项目路径"></el-table-column>

                </el-table>
            </el-main>

            <el-footer>
                <!--创建项目按钮区域-->
                <el-button type="primary">创建远程项目</el-button>
                <el-button type="primary">创建本地项目</el-button>
            </el-footer>
        </el-container>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "ProjectList",
    data()
    {
        return {
            isLogin: false, //是否为注册过的用户
            projectData: [] //table中项目信息
        }
    },

    mounted()
    {
        //TODO: 加载用户信息及项目信息
    }
})
</script>

<style lang="scss">
#project-list
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