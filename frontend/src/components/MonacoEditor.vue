<template>
    <div class="editor-container" ref="editor-container"></div>
</template>

<script lang="ts">
import * as monaco from "monaco-editor";
import { defineComponent } from "vue";

class Data
{
    editor: monaco.editor.IStandaloneCodeEditor | undefined = undefined;
}

export default defineComponent({
    data()
    {
        return new Data();
    },
    mounted()
    {
        let container = this.$refs['editor-container'] as HTMLElement;
        this.editor = monaco.editor.create(container);
    }
})
</script>

<style lang="scss">
.editor-container
{
    width: 100%;
    height: 100%;

    *
    {
        text-align: left;
    }
}
</style>