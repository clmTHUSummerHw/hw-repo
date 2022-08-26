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
                    <a v-if="isLogin"> {{ userStore.username }} </a>
                    <a v-else> - </a>

                    <a>&emsp;登录状态: </a>
                    <el-tag class="ml-2" type="success" v-if="isLogin">已登录</el-tag>
                    <el-tag class="ml-2" type="danger" v-else>未登录</el-tag>
                </div>
                <!--TODO: 展示用户详细信息-->
            </el-header>

            <el-main>
                <!--展示项目包含项目列表的表格-->
                <el-table :data="userStore.projectList.value" style="width: 100%" height="80%">
                    <el-table-column label="项目名称">
                        <template #default="scope">
                            <span>{{ scope.row }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作">
                        <template #default="scope">
                            <el-button size="small" @click="handleOpenProject(scope.row)">打开</el-button>
                            <el-button size="small" type="danger" @click="handleDeleteProject(scope.row)">删除</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-main>

            <el-footer>
                <!--创建项目按钮区域-->
                <el-button type="primary" @click="handleCreateProject">创建项目</el-button>
                <el-button type="danger" @click="handleLogout">退出登录</el-button>
            </el-footer>
        </el-container>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import type ListProjectsResult from "@/utils/post-util/ListProjectsResult";
import { useEditorStore } from "@/stores/editor";
import type ListFilesResult from "@/utils/post-util/ListFilesResult";
import type CreateFileResult from "@/utils/post-util/CreateFileResult";
import { ElMessage, ElMessageBox } from "element-plus";

export default defineComponent({
    name: "ProjectList",
    computed: {
        userStore()
        {
            return useUserStore();
        },
        editorStore()
        {
            return useEditorStore();
        },
        isLogin()
        {
            return useUserStore().session != "";
        }
    },
    methods: {
        async updateProjects()
        {
            if(!this.isLogin)
                return;

            try
            {
                let result = await axios.post('/user/list-projects', {session: this.userStore.session});
                let data = result.data as ListProjectsResult;
                if(data.code != 0)
                {
                    console.log('Code: ' + data.code);
                    alert('未知错误');
                    return;
                }

                this.userStore.projectList.value = data.projects;
            }
            catch(e)
            {
                console.log(e);
                return;
            }
        },
        async handleOpenProject(name: string)
        {
            if(!this.isLogin)
                return;

            try
            {
                this.editorStore.project.name = name;
                let result = await axios.post('/project/list-files', {
                    session: this.userStore.session,
                    project: name
                });

                let data = result.data as ListFilesResult;
                if(data.code != 0)
                {
                    console.log('Code: ' + data.code);
                    alert('未知错误');
                    return;
                }
                this.editorStore.tree.data = [{
                    folder: 1,
                    name: name,
                    files: data.files
                }];

                this.$router.push('/editor');
                return;
            }
            catch(e)
            {
                console.log(e);
                return;
            }
        },
        async handleDeleteProject(name: string)
        {
            try
            {
                let result = await axios.post('/user/delete-project', {
                    session: this.userStore.session,
                    name: name
                });

                let data = result.data as CreateFileResult;
                if(data.code != 0)
                {
                    console.log('Code: ' + data.code);
                    alert('未知错误');
                    return;
                }

                await this.updateProjects();
                return;
            }
            catch(e)
            {
                console.log(e);
                return;
            }
        },
        async createProject(name: string)
        {
            try
            {
                let result = await axios.post('/user/new-project', {
                    session: this.userStore.session,
                    name: name
                });

                let data = result.data as CreateFileResult;

                if(data.code != 0)
                {
                    alert('未知错误');
                    console.log('Code: ' + data.code);
                    return;
                }

                await this.updateProjects();
                return;
            }
            catch(e)
            {
                console.log(e);
                return;
            }
        },
        handleCreateProject()
        {
            ElMessageBox.prompt("请输入项目名称", "新建项目", {
                confirmButtonText: "OK",
                cancelButtonText: "Cancel",
                inputPattern: /\w{1,256}/,
                inputErrorMessage: "项目名称只能由字母，数字和下划线组成",
            })
                .then(({ value }) =>
                {
                    this.createProject(value);
                })
                .catch(() =>
                {
                    ElMessage({
                        type: "info",
                        message: "Input canceled",
                    });
                });
        },
        async handleLogout()
        {
            try
            {
                let result = await axios.post('/user/logout', {
                    session: this.userStore.session
                });

                let data = result.data as CreateFileResult;
                if(data.code != 0)
                {
                    console.log('Code: ' + data.code);
                    alert('未知错误');
                    return;
                }

                this.userStore.session = '';
                this.$router.push('/');
                return;
            }
            catch(e)
            {
                console.log(e);
                return;
            }
        }
    },
    mounted()
    {
        this.updateProjects();
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