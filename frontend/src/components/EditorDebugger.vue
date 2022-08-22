<template>
    <el-container id="editor-debugger">
        <el-header class="no-padding" height="var(--el-button-size)">
            <el-row>
                <el-button circle size="small" @click="handleContinue">
                    <span class="fa fa-play"></span>
                </el-button>
                <el-button circle size="small" @click="handleStepPass">
                    <span class="fa fa-step-forward"></span>
                </el-button>
                <el-button circle size="small" @click="handleStepIn">
                    <span class="fa fa-arrow-down"></span>
                </el-button>
                <el-button circle size="small" @click="handleStepOut">
                    <span class="fa fa-arrow-up"></span>
                </el-button>
            </el-row>
        </el-header>
        <el-main class="no-padding debugger-main">
            Stopped at:
            <el-row>
                <el-col :span="6">File</el-col>
                <el-col :span="18">{{ currentFile }}</el-col>
            </el-row>
            <el-row>
                <el-col :span="6">Line</el-col>
                <el-col :span="18">{{ currentLine }}</el-col>
            </el-row>
            <div>监视的变量：</div>
            <el-table :data="runningStore.debuggerStatus.variables" height="70%">
                <el-table-column label="变量">
                    <template #default="scope">
                        <el-popover effect="light" trigger="hover" placement="top" width="auto">
                            <template #default>
                                <div>{{ scope.row.value }}</div>
                            </template>
                            <template #reference>
                                <el-tag>{{ scope.row.name }}</el-tag>
                            </template>
                        </el-popover>
                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button size="small" type="danger" @click="() => handleRemoveVar(scope.row)">移除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div>添加监视变量：</div>
            <el-input v-model="inputtingVar"></el-input>
            <el-button size="small" @click="handleAddVar">添加</el-button>
        </el-main>
    </el-container>
</template>

<script lang="ts">
import { useRunningStore } from '@/stores/running';
import { defineComponent } from 'vue';
import type { VariableData } from '@/stores/running';
import type WSConnector from '@/utils/ws-util/WsConnector';
import type PauseResult from '@/utils/post-util/PauseResult';

class Data
{
    inputtingVar: string = ''
    ws: WSConnector | undefined = undefined
}

export default defineComponent({
    data()
    {
        return new Data();
    },
    computed: {
        runningStore()
        {
            return useRunningStore();
        },
        currentFile()
        {
            let out = useRunningStore().debuggerStatus.currentFile;
            return out == '' ? '-' : out;
        },
        currentLine()
        {
            let out = useRunningStore().debuggerStatus.currentLine;
            return out < 0 ? '-' : out.toString();
        }
    },
    methods: {
        handleAddVar()
        {
            let hasVar = false;
            for(let i of this.runningStore.debuggerStatus.variables)
                if(i.name == this.inputtingVar)
                    hasVar = true;

            if(hasVar)
                this.inputtingVar = '';
            else
            {
                this.runningStore.debuggerStatus.variables.push({name: this.inputtingVar, value: ''});
                this.inputtingVar = '';
            }
        },
        handleRemoveVar(variable: VariableData)
        {
            let index = this.runningStore.debuggerStatus.variables.indexOf(variable);
            if(index != -1)
                this.runningStore.debuggerStatus.variables.splice(index, 1);
        },
        handleContinue()
        {
            this.ws?.emit('continue_running', {});
        },
        handleStepPass()
        {
            this.ws?.emit('step_pass', {});
        },
        handleStepIn()
        {
            this.ws?.emit('step_in', {});
        },
        handleStepOut()
        {
            this.ws?.emit('step_out', {});
        },
        onPause(data: PauseResult)
        {
            this.runningStore.debuggerStatus.currentFile = data.file;
            this.runningStore.debuggerStatus.currentLine = data.line;
        },
        onVarValue(data: any)
        {
        }
    },
    mounted()
    {
        this.runningStore.$onAction(({name, store, args, after, onError}) => {
            if(name == 'setDebugWS')
                after(() => {
                    this.ws = this.runningStore.wsConnectors.debug;
                    if(this.ws != null)
                    {
                        this.ws?.on('pause', (data) => this.onPause(data));
                        this.ws.on('var_value', (data) => this.onVarValue(data));
                    }
                });
        });
    }
})
</script>

<style lang="scss">
#editor-debugger
{
    height: 100%;
    .no-padding
    {
        padding: 0px;
    }

    .debugger-main
    {
        text-align: left;
        overflow-x: visible;
        overflow-y: hidden;
    }

    .cell
    {
        padding: 0px;
    }
}
</style>