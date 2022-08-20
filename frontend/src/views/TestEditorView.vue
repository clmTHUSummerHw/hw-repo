<template>
    <div class="test-editor-view">
        <MonacoEditor v-model="text" file="test" language="java"></MonacoEditor>
    </div>
    <div>
        <input type="text" v-model="text">
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import MonacoEditor from '@/components/MonacoEditor.vue';

export default defineComponent({
    components: {
        MonacoEditor
    },
    data()
    {
        return {
            text: "Test text"
        }
    },
})
</script>

<style lang="scss">
.test-editor-view
{
    width: 75vw;
    height: 75vh;
}
</style>