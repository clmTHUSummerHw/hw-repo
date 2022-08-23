import type { FileData } from "@/utils/post-util/ListFilesResult";
import type { TreeNode } from "element-plus/es/components/tree-v2/src/types";
import { defineStore } from "pinia";

class ProjectStates
{
    name = ""
}

class TreeStates
{
    data: FileData[] = []
    currentNode: TreeNode | undefined = undefined
}

class Tab
{
    active = false
    isFile = false
    name = ""
    title = ""
    content = ""
}

class TabStates
{
    openedTabs: Map<string, Tab> = new Map()
    currentText = ""
}

export const useEditorStore = defineStore({
    id: "editor",
    state()
    {
        return {
            project: new ProjectStates(),
            tree: new TreeStates(),
            tab: new TabStates()
        }
    },
    actions: {
        updateTree()
        {
            console.log('Update Tree');
        }
    },
    persist: {
        enabled: true,
        strategies: [
            {
                storage: sessionStorage,
                paths: ['project']
            }
        ]
    }
})