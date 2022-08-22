import type WSConnector from '@/utils/ws-util/WsConnector'
import { defineStore } from 'pinia'

class WSConnectors
{
    run: WSConnector | undefined = undefined;
    debug: WSConnector | undefined = undefined;
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
            consoleText: ""
        }
    }
})
