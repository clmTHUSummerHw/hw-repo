<template>
    <div class="test-editor-view">
        <MonacoEditor></MonacoEditor>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import MonacoEditor from '@/components/MonacoEditor.vue';

export default defineComponent({
    components: {
        MonacoEditor
    }
})
</script>

<style lang="scss">
.test-editor-view
{
    width: 100vw;
    height: 100vh;
}
</style>