<template>
    <!--TODO: 把编辑器拆分为多个组件，使用vuex共享状态-->
    <div id="editor">
        <el-container id="BOX_BASE">
            <!--最高级容器-->
            <el-header>
                <!--放置-->
                <el-menu menu-trigger="click" mode="horizontal" unique-opened=true @select="handleMenuSelect">
                    <!--
                        menu-trigger设置打开子菜单的方式，可供选择还有"hover" /
                        mode属性设horizontal可使其元素水平摆放 / unique-opened=true表示同时只能打开一个子菜单
                        select函数在点击菜单选项时调用
                    -->
                    <!--文件栏目-->
                    <el-sub-menu index="1">
                        <template #title>文件</template>
                        <el-menu-item index="1-1">ele1-2</el-menu-item>
                        <el-menu-item index="1-2">ele1-2</el-menu-item>
                    </el-sub-menu>

                    <!--编辑栏目-->
                    <el-sub-menu index="2">
                        <template #title>编辑</template>
                        <el-menu-item index="2-1">ele2-1</el-menu-item>
                    </el-sub-menu>

                    <!--帮助栏目-->
                    <el-menu-item>
                        <el-link href="README.md">帮助</el-link>
                    </el-menu-item>

                </el-menu>
            </el-header>
            <el-container>
                <el-aside id="BOX_PROJECT_FILE_LIST">
                    <!--当前项目文件栏-->

                    <el-tree :data="treeData" :props="defaultProps" />
                    <!--展示项目文件夹结构的树形控件-->


                </el-aside>

                <el-main id="BOX_FILE_EDITOR">
                    <!--编辑器空间-->
                    <el-tabs v-model="active_name" type="border-card" editable @edit="handleTabsEdit" closable>
                        <!--editable提供添加tab的按钮 / closable提供可关闭tab的按钮-->

                        <!--默认打开的tab，展示向导文件-->
                        <el-tab-pane label="WELCOME" name="first">
                            WELCOME TAB TO show README DOC
                        </el-tab-pane>

                        <!--默认提供的编辑器tab-->
                        <el-tab-pane label="EDITOR_PAGE" name="second">
                            <el-input v-model="editorText" type="textarea" rows="20"></el-input>
                        </el-tab-pane>
                    </el-tabs>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script lang="ts">
//import Node from 'element-plus/es/components/tree/src/model/node' //引入结点类型

import { defineComponent } from "vue"

export default defineComponent({
    name: 'EditorView',

    //接受session
    props: {
        session: {
            type: String,
            required: false
        }
    },

    data()
    {
        return {
            active_index: '1', //目前展开的菜单选项index
            active_name: '', //目前展示的编辑器区域文件名
            treeData: [ //目前项目文件夹结构
                {
                    label: "project-file",
                    children: [
                        {
                            label: "src",
                            children: []
                        },
                        {
                            label: "doc",
                            children: []
                        },
                        {
                            label: "ext",
                            children: []
                        }
                    ]
                } //TODO: 抓取并引入项目文件夹结构
            ],
            editorText: "", //默认编辑器tab的输入内容
            defaultProps: {
            }
        }
    },

    methods: {
        handleMenuSelect()
        { //应对菜单选择

        },
        /*handleClick(tab, event) {
            //console.log(tab, event);
        },*/
        handleTabsEdit(targetName: string, action: 'add' | 'remove')
        { //应对动态添加/删除tabs，action: 'remove' | 'add'
            if (action === 'add')
            {
                console.log('add!')
            }
            else if (action === 'remove')
            {
                console.log('remove!')
            }
        } //TODO: 定义添加或删除tabs的函数
    }
})
</script>

<style lang="scss">
#editor
{
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;

    box-sizing: border-box;
    width: 100%;
    height: 800px;

    background-color: white;
    background-image: url(@/assets/small_logo_bg.png);
}


#BOX_BASE
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

#BOX_PROJECT_FILE_LIST
{
    /* 目前项目文件列表 */
    width: 200px;
    padding: 20px;
    border-right: 1px solid rgb(223, 223, 223);
}


#BOX_FILE_EDITOR
{
    /* 编辑器区域 */
    padding: 5px 18px;
}
</style>