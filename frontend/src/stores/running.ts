import type WSConnector from '@/utils/ws-util/WsConnector'
import { defineStore } from 'pinia'

class WSConnectors
{
    run: WSConnector | undefined = undefined;
    debug: WSConnector | undefined = undefined;
}

export class VariableData
{
    name: string = ''
    value: string = ''
}

class DebuggerStatus
{
    currentFile: string = ''
    currentLine: number = -1
    variables: VariableData[] = []
}

export const useRunningStore = defineStore({
    id: 'running',
    state()
    {
        return {
            runCommandTriggered: false,
            debugCommandTriggered: false,
            running: false,
            debugging: false,
            wsConnectors: new WSConnectors,
            consoleText: "",
            debuggerStatus: new DebuggerStatus
        }
    },
    actions: {
        setRunWS(ws: WSConnector)
        {
            this.wsConnectors.run = ws;
        },

        setDebugWS(ws: WSConnector)
        {
            this.wsConnectors.debug = ws;
        }
    }
})
