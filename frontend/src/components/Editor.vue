<template>
    <el-container id="BOX_BASE"> <!--最高级容器-->
        <el-header id="BOX_TOOLBAR"> <!--工具栏-->
            <el-menu id="" 
            mode="horizontal" 
            unique-opened="true" 
            menu-trigger="click"
            :default-active="active_index"
            >
                <el-menu-item index="1">文件</el-menu-item>
                <el-menu-item index="2">编辑</el-menu-item>
                <el-menu-item index="3">帮助</el-menu-item>
            </el-menu>
        </el-header>
        <el-container>
            <el-aside id="BOX_PROJECT_FILE_LIST"> <!--当前项目文件栏-->
                <el-tree :data="data"> <!--展示项目文件结构的树形控件-->

                </el-tree>
            </el-aside>
            <el-main id="BOX_FILE_EDITOR"> <!--编辑器空间-->
                <el-tabs v-model="active_name" type="border-card" closable>
                    <el-tab-pane label="WELCOME" name="first">
                        WELCOME TAB TO show README DOC
                    </el-tab-pane>
                </el-tabs>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
    export default {
        name: 'EditorPage',

        props: {

        },

        data() {
            return {
                active_index: '', //目前展开的菜单选项index
                active_name: '' //目前展示的编辑器区域文件名
                
            }
        },

        methods: {
            /*handleClick(tab, event) {
                //console.log(tab, event);
            }*/
        },

        computed: {

        }
    }
</script>

<style scoped>

    #BOX_BASE {
        color: black;

        border: 1px black solid; /* todelete */

        height: 600px;
    }

    #BOX_TOOLBAR {
        border: 1px black solid; /* todelete */
        height: 30px;
        
        z-index: 2;
    }

    

    #BOX_PROJECT_FILE_LIST { /* 目前项目文件列表 */
        width: 200px;
        border: 1px black solid; /* todelete */
    }

    
    #BOX_FILE_EDTIOR { /* 编辑器区域 */
        border: 1px black solid; /* todelete */
    }
    

</style>