<template>
    <div id="editor-view">
        <el-container class="box-base">
            <el-header class="editor-header">
                <EditorMenu />
            </el-header>
            <el-container class="content">
                <el-aside class="editor-aside">
                    <EditorFileList />
                </el-aside>
                <EditorMain />
            </el-container>
        </el-container>
    </div>
</template>

<script lang="ts">
import EditorMenu from "@/components/EditorMenu.vue";
import { defineComponent } from "vue";
import EditorFileList from "@/components/EditorFileList.vue";
import EditorMain from "../components/EditorMain.vue";

export default defineComponent({
    components: {
    EditorMenu,
    EditorFileList,
    EditorMain
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
        padding: 20px;
        border-right: 1px solid rgb(223, 223, 223);
    }
}
</style>