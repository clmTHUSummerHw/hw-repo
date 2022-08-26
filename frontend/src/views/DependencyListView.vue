<template>
    <div id="dependency-list">
        <el-container class="box-base">
            <el-header class="box-header" height="64px">
                <el-row>
                    <el-col class="title" :span="12">依赖列表</el-col>
                    <el-col :span="12">
                        <span>用户：</span>
                        <span>{{ userStore.username }}</span>
                        <span>项目：</span>
                        <span>{{ editorStore.project.name }}</span>
                    </el-col>
                </el-row>
            </el-header>
            <el-main class="view-main">
                <el-row class="full-height">
                    <el-col :span="12" class="full-height table-container">
                        <el-table height="calc(100% - 32px)" width="100%">
                            <!-- TODO: 设计表格，应包含依赖文件名与删除按钮 -->
                        </el-table>
                    </el-col>
                    <el-col :span="12" class="full-height">
                        <el-upload drag @change="onFileUpload"><!-- TODO: 处理上传操作 -->
                            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                            <div class="el-upload__text">
                                Drop file here or <em>click to upload</em>
                            </div>
                        </el-upload>
                        <el-row>
                            <el-button>返回编辑器</el-button>
                        </el-row>
                    </el-col>
                </el-row>
            </el-main>
        </el-container>
    </div>
</template>

<script lang="ts">
import { useEditorStore } from '@/stores/editor';
import { useUserStore } from '@/stores/user';
import { defineComponent } from 'vue';
import { UploadFilled } from '@element-plus/icons-vue';
import type { UploadFile, UploadFiles } from 'element-plus';
import axios from 'axios';

class Data
{
    dependencies: string[] = []
}

export default defineComponent({
    components: {
        UploadFilled
    },
    data()
    {
        return new Data();
    },
    computed: {
        userStore()
        {
            return useUserStore();
        },
        editorStore()
        {
            return useEditorStore();
        },
    },
    methods: {
        async onFileUpload(file: UploadFile, files: UploadFiles)
        {
            if(file.raw == null)
                return;
            try
            {
                let formData = new FormData();
                formData.append('session', this.userStore.session);
                formData.append('project', this.editorStore.project.name);
                formData.append('file', file.raw, file.name);
                let result = await axios.post('/project/add-dependency', formData);
            }
            catch(e)
            {
                console.log(e);
                return;
            }
        }
    }
})
</script>

<style lang="scss">
#dependency-list
{
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;

    box-sizing: border-box;
    width: 100vw;
    height: 100vh;

    margin: 0px;

    background-color: white;
    background-image: url(@/assets/small_logo_bg.png);

    .box-base
    {
        color: black;
        background-color: white;
        box-shadow: 1px 0 10px rgb(0 0 0 / 30%);

        margin: auto;
        width: 50vw;
        height: 75vh;

        position: relative;
        top: 12.5%;
    }

    .box-header
    {
        padding: 0;
        width: 100%;
        background-color: #A0D0FF;
        border-bottom: 1px solid var(--el-border-color);
        .el-row
        {
            line-height: var(--el-header-height);

            .title
            {
                font-size: 28px;
            }

            span
            {
                padding-left: 16px;
            }
        }
    }

    .view-main
    {
        height: calc(100% - 64px);
        padding: 0px;
        .el-col
        {
            padding: 16px;
        }
    }

    .full-height
    {
        height: 100%;
    }

    .table-container
    {
        border-right: 1px solid var(--el-border-color);
    }
}
</style>