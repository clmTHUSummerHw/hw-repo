<template>
    <div id="admin-page">
        <el-container class="box-base">
            <el-header class="box-header"> <!--标题-->
                <el-button type="primary" @click="goAdmin" class="backButton" size="big">返回</el-button>
                <div class="title">日志页面</div>
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
                    <el-table-column prop="logMemo" label="备注"></el-table-column>

                </el-table>
            </el-main>
        </el-container>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "LogPage",
    data()
    {
        return {
            logData: [
                
            ] //table中项目信息
        }
    },

    methods: {
        goAdmin() {
            this.$router.push({name:'admin'});
        }
    },

    computed: {
        
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
    
    .backButton {
        margin-left: 20px;
    }
}
</style>