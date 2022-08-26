<template>
    <div id="editor-view">
        <el-container class="box-base">
            <el-header class="editor-header">
                <EditorMenu />
            </el-header>
            <el-container class="editor-content">
                <el-aside class="editor-aside">
                    <el-tabs class="aside-main">
                        <el-tab-pane label="文件列表">
                            <EditorFileList />
                        </el-tab-pane>
                        <el-tab-pane label="调试器" class="full-height">
                            <EditorDebugger />
                        </el-tab-pane>
                    </el-tabs>
                </el-aside>
                <el-container>
                    <EditorMain />
                    <el-footer height="30%" class="console-container">
                        <EditorConsole />
                    </el-footer>
                </el-container>
            </el-container>
        </el-container>
    </div>
</template>

<script lang="ts">
import EditorMenu from "@/components/EditorMenu.vue";
import { defineComponent } from "vue";
import EditorFileList from "@/components/EditorFileList.vue";
import EditorMain from "../components/EditorMain.vue";
import EditorConsole from "../components/EditorConsole.vue";
import EditorDebugger from "../components/EditorDebugger.vue";

export default defineComponent({
    components: {
        EditorMenu,
        EditorFileList,
        EditorMain,
        EditorConsole,
        EditorDebugger
    }
})
</script>

<style lang="scss">
#editor-view
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

    .editor-header
    {
        padding: 0px;
    }

    .box-base
    {
        /* 整体框 */
        color: black;
        background-color: white;
        box-shadow: 1px 0 10px rgb(0 0 0 / 30%);

        margin: auto;
        width: 95vw;
        height: 95vh;

        position: relative;
        top: 2.5%;
    }

    .editor-aside
    {
        width: 200px;
        padding: 2px;
        border-right: 1px solid rgb(223, 223, 223);
        overflow: hidden;

        .aside-main
        {
            height: 100%;

            .el-tabs__header
            {
                margin-bottom: 8px;
            }

            .el-tabs__content
            {
                height: calc(100% - var(--el-tabs-header-height) - 8px);
            }
        }

        .full-height
        {
            height: 100%;
        }
    }

    .editor-content
    {
        height: 100%;
    }

    .console-container
    {
        padding: 0px;
        border-top: 1px solid var(--el-border-color);
    }
}
</style>