<template>
    <el-container id="editor-console">
        <el-header class="no-padding" height="var(--title-height)">
            <el-row>
                <el-col :span="20">
                    <div class="console-title"></div>
                </el-col>
                <el-col :span="2">
                    <el-button size="small">Stop</el-button>
                </el-col>
            </el-row>
        </el-header>
        <el-main class="no-padding">
            <textarea class="console-text no-padding" v-model="runningStore.consoleText" disabled></textarea>
        </el-main>
        <el-footer class="no-padding" height="var(--input-height)">
            <input class="no-padding" v-model="inputtingText" @keyup.enter.native="handleInput">
        </el-footer>
    </el-container>
</template>

<script lang="ts">
import { useEditorStore } from '@/stores/editor';
import { useRunningStore } from '@/stores/running';
import { useUserStore } from '@/stores/user';
import type OutputResult from '@/utils/post-util/OutputResult';
import WSConnector from '@/utils/ws-util/WsConnector';
import { defineComponent } from 'vue';

class Data
{
    inputtingText: string = ''
    ws: WSConnector | undefined = undefined
}

export default defineComponent({
    data()
    {
        return new Data();
    },
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
        if (this.runningStore.runCommandTriggered)
        {
            this.runningStore.runCommandTriggered = false;
            this.runningStore.running = true;
            this.runningStore.wsConnectors.run = new WSConnector('/run', this.userStore.session);
            this.ws = this.runningStore.wsConnectors.run;
            this.ws.on('output', data => this.onOutput(data as OutputResult));
        }
        else if (this.runningStore.debugCommandTriggered)
        {
            this.runningStore.debugCommandTriggered = false;
            this.runningStore.debugging = true;
            this.runningStore.wsConnectors.debug = new WSConnector('/debug', this.userStore.session);
            this.ws = this.runningStore.wsConnectors.debug;
            this.ws.on('output', data => this.onOutput(data as OutputResult));
        }
        else if(this.runningStore.running)
        {
            this.ws = this.runningStore.wsConnectors.run;
        }
        else if(this.runningStore.debugging)
        {
            this.ws = this.runningStore.wsConnectors.debug;
        }
    },
    methods: {
        handleInput()
        {
            this.runningStore.consoleText += this.inputtingText + "\n";
            this.ws?.emit('input', {text: this.inputtingText});
            this.inputtingText = "";
        },

        onOutput(data: OutputResult)
        {
            this.runningStore.consoleText += data.text;
        }
    }
})
</script>

<style lang="scss">
#editor-console
{
    text-align: left;
    --title-height: 1.8em;
    --input-height: 18px;
    --input-font-size: 16px;
    height: 100%;
    padding: 2px;
    padding-top: 0px;

    .console-title
    {
        vertical-align: bottom;
    }

    .no-padding
    {
        padding: 0px;
    }

    main
    {
        overflow: visible;
        height: calc(100% - var(--title-height) - var(--input-height));
    }

    .console-text
    {
        width: 100%;
        height: 100%;
        max-height: 100%;
        word-break: break-all;
        overflow-x: hidden;
        overflow-y: scroll;
        border: 1px solid;
        border-bottom: 0px;
        font-size: var(--input-font-size);
        font-family: consolas;
    }

    input
    {
        width: 100%;
        border: 1px solid;
        border-top: 0px;
        border-radius: 0px;
        font-size: var(--input-font-size);
        line-height: var(--input-height);
        height: var(--input-height);
        font-family: consolas;
        outline: none;
    }
}
</style>