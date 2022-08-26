<template>
    <el-menu id="editor-menu" menu-trigger="click" mode="horizontal" unique-opened @select="handleMenuSelect">
        <!--
            menu-trigger设置打开子菜单的方式，可供选择还有"hover" /
            mode属性设horizontal可使其元素水平摆放 / unique-opened=true表示同时只能打开一个子菜单
            select函数在点击菜单选项时调用
        -->
        <!--文件栏目-->
        <el-sub-menu index="1">
            <template #title>文件</template>
            <el-menu-item index="1-1">上传文件</el-menu-item>
            <el-menu-item index="1-2">打包</el-menu-item>
        </el-sub-menu>

        <!--编辑栏目-->
        <el-sub-menu index="2">
            <template #title>编辑</template>
            <el-menu-item index="2-1">依赖管理</el-menu-item>
            <el-menu-item index="2-2">返回项目列表</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="3">
            <template #title>运行</template>
            <el-menu-item index="3-1">运行</el-menu-item>
            <el-menu-item index="3-2">调试</el-menu-item>
        </el-sub-menu>

        <!--帮助栏目-->
        <el-menu-item index="4">
            <el-link href="README.md">帮助</el-link>
        </el-menu-item>
    </el-menu>

    <!-- 上传文件对话框 -->
    <el-dialog id="upload-dialog" v-model="uploading">
        <div class="input-label">请填写要上传到的路径：</div>
        <el-input class="upload-to" v-model="uploadTo" />
        <el-upload class="file-to-upload" drag :auto-upload="false" @change="onFileUpload">
            <el-icon class="el-icon--upload">
                <UploadFilled />
            </el-icon>
            <div class="el-upload__text">
                Drop file here or <em>click to upload</em>
            </div>
        </el-upload>
        <el-button @click="uploadFiles">OK</el-button>
    </el-dialog>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { UploadFilled } from '@element-plus/icons-vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useEditorStore } from '@/stores/editor';
import type UploadFileResult from '@/utils/post-util/UploadFileResult';
import { Base64 } from 'js-base64';
import { useRunningStore } from '@/stores/running';

class Data
{
    filesToUpload: File[] = []
    uploadTo = '/'
    uploading = false
}

export default defineComponent({
    components: {
        UploadFilled
    },
    data()
    {
        return new Data();
    },
    computed:
    {
        userStore()
        {
            return useUserStore();
        },
        editorStore()
        {
            return useEditorStore();
        },
        runningStore()
        {
            return useRunningStore();
        }
    },
    methods: {
        handleMenuSelect(key: string, _keyPath: any)
        {
            if (key == '1-1')
                this.openUploadFileDialog();
            else if(key == '2-1')
                this.gotoDependencies();
            else if(key == '2-2')
                this.goProjectList();
            else if(key == '3-1')
                this.startRunning();
            else if(key == '3-2')
                this.startDebugging();
        },

        uploadFiles()
        {
            this.uploading = false;
            for(let file of this.filesToUpload)
            {
                this.uploadFile(file);
            }
            this.editorStore.updateTree();
        },

        async uploadFile(file: File)
        {
            try
            {
                let text = await file.text();
                if(text == null)
                {
                    alert("Not text!");
                    return;
                }

                let fullPath = this.uploadTo;
                if(fullPath[fullPath.length - 1] != '/')
                fullPath += '/';
                fullPath += file.name;

                let result = await axios.post('/project/upload-file', {
                    session: this.userStore.session,
                    project: this.editorStore.project.name,
                    name: fullPath,
                    file: Base64.encode(text)
                });

                let data = result.data as UploadFileResult;
                if(data.code != 0)
                {
                    alert("Upload error");
                    return;
                }
                return;
            }
            catch(e)
            {
                console.log(e);
                alert("Upload error");
                return;
            }
        },

        openUploadFileDialog()
        {
            this.uploading = true;
        },
        onFileUpload(_file: any, files: any[])
        {
            this.filesToUpload = [];
            for(let file of files)
            {
                let raw = file.raw as File;
                this.filesToUpload.push(raw);
            }
        },
        goProjectList()
        {
            this.editorStore.removeAllTabs();
            this.editorStore.project.name = "";
            this.$router.push('/project-list');
        },
        gotoDependencies()
        {
            this.$router.push('/dependency-list');
        },
        startRunning()
        {
            this.runningStore.runCommandTriggered = true;
        },
        startDebugging()
        {
            this.runningStore.debugCommandTriggered = true;
        }
    }
})
</script>

<style lang="scss">
.input-label
{
    text-align: left;
    width: 100%;
}
</style>