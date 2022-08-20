<template>
<!-- TODO: 填充内容 -->
</template>

<script lang="ts">
import { useEditorStore } from '@/stores/editor';
import { useRunningStore } from '@/stores/running';
import { useUserStore } from '@/stores/user';
import WSConnector from '@/utils/ws-util/WsConnector';
import { defineComponent } from 'vue';

export default defineComponent({
    computed:
    {
        userStore() //使用该属性获取用户session
        {
            return useUserStore();
        },
        editorStore() //使用该属性获取项目名
        {
            return useEditorStore();
        },
        runningStore()
        {
            return useRunningStore();
        }
    },
    mounted()
    {
        if(this.runningStore.runCommandTriggered)
        {
            this.runningStore.runCommandTriggered = false;
            this.runningStore.running = true;
            this.runningStore.wsConnectors.run = new WSConnector('/run', this.userStore.session);
            let ws = this.runningStore.wsConnectors.run;
            //TODO: 完成后续的初始化
        }
        else if(this.runningStore.debugCommandTriggered)
        {
            this.runningStore.debugCommandTriggered = false;
            this.runningStore.debugging = true;
            this.runningStore.wsConnectors.debug = new WSConnector('/debug', this.userStore.session);
            let ws = this.runningStore.wsConnectors.debug;
            //TODO: 完成后续的初始化
        }
    },
    //TODO: 填充内容
})
</script>