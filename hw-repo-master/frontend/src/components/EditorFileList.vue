<template>
    <div id="editor-file-list">
        <div class="context-menu" ref="context-menu">
            <el-menu mode="vertical" v-show="menuVisible" @select="handleContextMenu">
                <el-menu-item index="1">新建文件</el-menu-item>
                <el-menu-item index="2">新建文件夹</el-menu-item>
                <!--包括删除文件和删除文件夹-->
                <el-menu-item index="3">删除</el-menu-item>
                <el-menu-item index="4">下载文件</el-menu-item>
                <el-menu-item index="5">取消</el-menu-item>
            </el-menu>
        </div>
        <!--当前项目文件栏-->
        <el-tree ref="tree" v-if="treeVisible" :data="editorStore.tree.data" :props="treeProps" node-key="id"
            :highlight-current="true" @node-click="handleNodeClick" @node-contextmenu="handleNodeContextMenu">
            <template #default="{ node, data }">
                <img src="~@/assets/icon-folder-close.svg" id="folder_close" v-if="!node.expanded && data.folder" />
                <img src="~@/assets/icon-folder-open.svg" id="folder_open" v-else-if="node.expanded && data.folder" />
                <img src="~@/assets/file_type_text.svg" id="file" v-else />
                <span id="label_text">{{ node.label }}</span>
            </template>
        </el-tree>
        <!--展示项目文件夹结构的树形控件-->
    </div>
</template>

<script lang="ts">
import { useEditorStore } from '@/stores/editor';
import type { TreeNode } from 'element-plus/es/components/tree-v2/src/types';
import { defineComponent } from 'vue';
import type { FileData } from '@/utils/post-util/ListFilesResult';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import type DownloadFileResult from '@/utils/post-util/DownloadFileResult';
import { ElMessage, ElMessageBox } from 'element-plus';
import type CreateFileResult from '@/utils/post-util/CreateFileResult';
import type ListFilesResult from '@/utils/post-util/ListFilesResult';
import { Base64 } from 'js-base64';

class Data
{
    treeProps = {
        label: "name",
        children: "files",
        isLeaf: "folder"
    }
    menuVisible = false
    nodeWithMenu: TreeNode | undefined = undefined
    maxTreeId = 0
    treeVisible = true
}

export default defineComponent({
    data()
    {
        return new Data();
    },

    computed: {
        editorStore()
        {
            return useEditorStore();
        },
        userStore()
        {
            return useUserStore();
        }
    },

    methods: {
        handleNodeClick(data: FileData, node: TreeNode)
        {
            if (node != this.editorStore.tree.currentNode)
            {
                this.editorStore.tree.currentNode = node;
                return;
            }

            if (data.folder == 0)
            {
                let tab = this.editorStore.tab.openedTabs.get(this.getCurrentFilePath(node));
                if (tab == null)
                    this.openFile(node);
            }
        },

        //递归获取TreeNode对应的文件路径
        getCurrentFilePath(treeNode: TreeNode)
        {
            let result = '';
            if (treeNode.level > 1 && treeNode.parent != null)
            {
                let data = treeNode.data as FileData;
                let parentResult = this.getCurrentFilePath(treeNode.parent);

                if(parentResult[parentResult.length - 1] != '/')
                    result = parentResult + '/' + data.name;
                else
                    result = parentResult + data.name;
            }
            if (result[0] != '/')
                result = '/' + result;
            return result;
        },

        async openFile(node: TreeNode)
        {
            let path = this.getCurrentFilePath(node);
            try
            {
                let result = await axios.post('/project/download-file', {
                    session: this.userStore.session,
                    project: this.editorStore.project.name,
                    name: path
                });
                let data = result.data as DownloadFileResult;

                if (data.code == 0)
                {
                    let content = Base64.decode(data.file);
                    this.editorStore.tab.openedTabs.set(path, {
                        active: false,
                        isFile: true,
                        name: path,
                        title: (node.data as FileData).name,
                        content: content
                    });
                }
            }
            catch (e)
            {
                console.log(e);
                return;
            }
        },

        handleNodeContextMenu(event: MouseEvent, data: any, treenode: TreeNode)
        {
            //应对右键点击节点
            this.menuVisible = false; // 先把模态框关死，为了多次点击右键时菜单能随鼠标移动
            this.menuVisible = true; // 显示模态窗口，跳出自定义菜单栏
            this.nodeWithMenu = treenode;
            event.preventDefault(); //关闭浏览器右键默认事件
            let menu = this.$refs['context-menu'] as HTMLElement;
            /* 菜单定位基于鼠标点击位置 */
            menu.style.left = event.clientX - 100 + "px";
            menu.style.top = event.clientY - 60 + "px";
            document.addEventListener("click", this.hideContextMenu);
        },

        handleContextMenu(key: string, _keyPath: any)
        {
            if (this.nodeWithMenu == null)
                return;

            if (key == "1")
                this.createFileMessageBox(this.nodeWithMenu);

            else if (key == "2")
                this.createFolderMessageBox(this.nodeWithMenu);

            else if (key == "3")
            {
                if ((this.nodeWithMenu.data as FileData).folder == 1)
                    this.deleteFolder(this.nodeWithMenu);
                else
                    this.deleteFile(this.nodeWithMenu);
            }

            else if (key == "4")
                this.downloadFile(this.nodeWithMenu);
        },

        hideContextMenu()
        {
            // 取消鼠标监听事件 菜单栏
            this.menuVisible = false;
            this.nodeWithMenu = undefined;
            document.removeEventListener("click", this.hideContextMenu); // 关掉监听，
        },

        createFileMessageBox(currentTreeNode: TreeNode)
        {
            ElMessageBox.prompt("请输入文件名", "新建文件", {
                confirmButtonText: "OK",
                cancelButtonText: "Cancel",
                inputPattern: /([^/\\:\*\?"<>\|\f\n\r\t\v]*[^/\\:\*\?"<>\|\f\n\r\t\v\.])+/,
                inputErrorMessage: "请输入正确的文件名",
            })
                .then(({ value }) =>
                {
                    this.createFile(currentTreeNode, value);
                })
                .catch(() =>
                {
                    ElMessage({
                        type: "info",
                        message: "Input canceled",
                    });
                });
        },

        createFolderMessageBox(currentTreeNode: TreeNode)
        {
            ElMessageBox.prompt("请输入文件夹名", "新建文件夹", {
                confirmButtonText: "OK",
                cancelButtonText: "Cancel",
                inputPattern: /([^/\\:\*\?"<>\|\f\n\r\t\v]*[^/\\:\*\?"<>\|\f\n\r\t\v\.])+/,
                inputErrorMessage: "请输入正确的文件夹名",
            })
                .then(({ value }) =>
                {
                    this.createFolder(currentTreeNode, value);
                })
                .catch(() =>
                {
                    ElMessage({
                        type: "info",
                        message: "Input canceled",
                    });
                });
        },

        async createFile(treeNode: TreeNode, name: string)
        {
            let data = treeNode.data as FileData;
            if (data.folder == 0)
            {
                if (treeNode.parent == null)
                {
                    alert("Unknown error");
                    return;
                }
                treeNode = treeNode.parent;
            }

            let path = this.getCurrentFilePath(treeNode);
            if (path != '/')
                path += '/';
            path += name;

            try
            {
                let result = await axios.post("/project/new-file", {
                    session: this.userStore.session, //把props里接受session发送到后端
                    project: this.editorStore.project.name,
                    name: path,
                });

                let data = result.data as CreateFileResult;
                if (data.code == 0)
                {
                    await this.refreshTree();
                    return;
                }
                else if (data.code == 1)
                {
                    alert("session无效");
                    return;
                }
                else if (data.code == 2)
                {
                    alert("项目不存在");
                    return;
                }
                else if (data.code == 3)
                {
                    alert("文件名不符合规范");
                    return;
                }
                else if (data.code == 4)
                {
                    alert("文件已存在");
                    return;
                }
                else
                {
                    alert("未知错误");
                    return;
                }
            }
            catch (e)
            {
                console.log(e);
                alert('Create file failed');
                return;
            }
        },

        async createFolder(treeNode: TreeNode, name: string)
        {
            let data = treeNode.data as FileData;
            if (data.folder == 0)
            {
                if (treeNode.parent == null)
                {
                    alert("Unknown error");
                    return;
                }
                treeNode = treeNode.parent;
            }

            let path = this.getCurrentFilePath(treeNode);
            if (path != '/')
                path += '/';
            path += name;

            try
            {
                let result = await axios.post("/project/new-folder", {
                    session: this.userStore.session, //把props里接受session发送到后端
                    project: this.editorStore.project.name,
                    name: path,
                });

                let data = result.data as CreateFileResult;
                if (data.code == 0)
                {
                    await this.refreshTree();
                    return;
                }
                else if (data.code == 1)
                {
                    alert("session无效");
                    return;
                }
                else if (data.code == 2)
                {
                    alert("项目不存在");
                    return;
                }
                else if (data.code == 3)
                {
                    alert("文件夹名不符合规范");
                    return;
                }
                else if (data.code == 4)
                {
                    alert("文件夹已存在");
                    return;
                }
                else
                {
                    alert("未知错误");
                    return;
                }
            }
            catch (e)
            {
                console.log(e);
                alert('Create file failed');
                return;
            }
        },

        async deleteFile(treeNode: TreeNode)
        {
            let path = this.getCurrentFilePath(treeNode);

            try
            {
                let result = await axios.post("/project/delete-file", {
                    session: this.userStore.session,
                    project: this.editorStore.project.name,
                    name: path
                });

                let data = result.data as CreateFileResult;

                if (data.code == 0)
                {
                    await this.refreshTree();
                    return;
                }
                else if (data.code == 1)
                {
                    alert("session无效");
                    return;
                }
                else if (data.code == 2)
                {
                    alert("项目不存在");
                    return;
                }
                else if (data.code == 3)
                {
                    alert("文件不存在");
                    return;
                }
                else if (data.code == 4)
                {
                    alert("路径为文件夹而非文件");
                    return;
                }
                else
                {
                    alert("未知错误");
                    return;
                }
            }
            catch (e)
            {
                console.log(e);
                return;
            }
        },

        async deleteFolder(treeNode: TreeNode)
        {
            if (treeNode.level == 1)
            {
                alert("不可删除项目根目录");
            }

            let path = this.getCurrentFilePath(treeNode);

            try
            {
                let result = await axios.post("/project/delete-folder", {
                    session: this.userStore.session,
                    project: this.editorStore.project.name,
                    name: path
                });

                let data = result.data as CreateFileResult;

                if (data.code == 0)
                {
                    await this.refreshTree();
                    return;
                }
                else if (data.code == 1)
                {
                    alert("session无效");
                    return;
                }
                else if (data.code == 2)
                {
                    alert("项目不存在");
                    return;
                }
                else if (data.code == 3)
                {
                    alert("文件夹不存在");
                    return;
                }
                else if (data.code == 4)
                {
                    alert("路径为文件而非文件夹");
                    return;
                }
                else
                {
                    alert("未知错误");
                    return;
                }
            }
            catch (e)
            {
                console.log(e);
                return;
            }
        },

        async downloadFile(treeNode: TreeNode)
        {
            if ((treeNode.data as FileData).folder == 1)
            {
                alert("暂不支持下载文件夹");
                return;
            }
            else
            {
                let path = this.getCurrentFilePath(treeNode);
                try
                {
                    let result = await axios.post("/project/download-file", {
                        session: this.userStore.session, //把props里接受session发送到后端
                        project: this.editorStore.project.name,
                        name: path,
                    });

                    let data = result.data as DownloadFileResult;

                    if (data.code == 0)
                    {
                        var elementA = document.createElement("a"); // 创建a标签
                        elementA.download = treeNode["data"]["name"]; //文件的名称
                        elementA.style.display = "none";
                        var blob = new Blob([atob(data.file)]); //生成一个blob二进制数据，内容为从后端获得的文件内容
                        elementA.href = URL.createObjectURL(blob);
                        document.body.appendChild(elementA);
                        elementA.click();
                        document.body.removeChild(elementA);
                    }
                    else if (data.code == 1)
                    {
                        alert("session无效");
                        return;
                    }
                    else if (data.code == 2)
                    {
                        alert("项目不存在");
                        return;
                    }
                    else if (data.code == 3)
                    {
                        alert("文件不存在");
                        return;
                    }
                    else if (data.code == 4)
                    {
                        alert("路径为文件夹而非文件");
                        return;
                    }
                    else
                    {
                        alert("未知错误");
                        return;
                    }
                }
                catch (e)
                {
                    console.log(e);
                    return;
                }
            }
        },

        async refreshTree()
        {
            try
            {
                let result = await axios.post('/project/list-files', {
                    session: this.userStore.session,
                    project: this.editorStore.project.name
                });
                let data = result.data as ListFilesResult;

                if(data.code == 0)
                {
                    this.editorStore.tree.data = [{
                        name: "根目录",
                        folder: 1,
                        files: data.files
                    }];
                    this.treeVisible = false;

                    setTimeout(() => {
                        this.treeVisible = true;
                    }, 100);

                    return;
                }
                else
                {
                    alert('Unknown error');
                    return;
                }
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
        this.refreshTree();
        this.editorStore.$onAction(({name, store, args, after, onError}) => {
            if(name == 'updateTree')
                this.refreshTree();
        })
    },
    unmounted()
    {
        this.editorStore.tree.currentNode = undefined;
    }
})
</script>

<style lang="scss">
#folder_close
{
    width: 18px;
    height: 18px;
}

#folder_open
{
    width: 18px;
    height: 18px;
}

#file
{
    width: 18px;
    height: 18px;
}

#editor-file-list
{
    .el-menu
    {
        position: absolute;
        background-color: #fff;
        width: 120px;
        /*height: 106px;*/
        font-size: 10px;
        color: #444040;
        border-radius: 4px;
        -webkit-box-sizing: border-box;
        box-sizing: border-box;
        border-radius: 3px;
        border: 1px solid rgba(0, 0, 0, 0.15);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.175);
        white-space: nowrap;
        z-index: 1000;
    }
}
</style>