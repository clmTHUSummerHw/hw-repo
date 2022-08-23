<template>
    <!--编辑器空间-->
    <el-main id="editor-main">
        <div class="big-container">
            <el-tabs v-model="activeTab" class="editor-tabs" type="border-card" closable @tab-remove="onTabRemove">
                <el-tab-pane class="editor-pane" v-for="item in editorStore.tab.openedTabs" :key="item[1].name"
                    :label="item[1].title" :name="item[1].name">
                </el-tab-pane>
            </el-tabs>
            <div class="el-tabs text-editor-container">
                <MonacoEditor v-model="editorStore.tab.currentText" :file="activeFile" language="java" />
            </div>
        </div>
    </el-main>
</template>

<script lang="ts">
import { useEditorStore } from '@/stores/editor';
import { useUserStore } from '@/stores/user';
import type UploadFileResult from '@/utils/post-util/UploadFileResult';
import axios from 'axios';
import type { TabPanelName } from 'element-plus';
import { defineComponent } from 'vue';
import MonacoEditor from './MonacoEditor.vue';
import { Base64 } from 'js-base64';

export default defineComponent({
    components: {
        MonacoEditor
    },
    data()
    {
        return {
            activeTab: ""
        };
    },
    computed: {
        userStore()
        {
            return useUserStore();
        },
        editorStore()
        {
            return useEditorStore();
        },
        activeFile()
        {
            if (this.activeTab == '')
                return undefined;
            let tab = useEditorStore().tab.openedTabs.get(this.activeTab);
            if (tab == null)
                return undefined;
            return tab.isFile ? tab.name : undefined;
        }
    },
    mounted()
    {
        this.editorStore.tab.openedTabs.set("welcome", {
            active: false,
            isFile: false,
            title: "welcome",
            name: "welcome",
            content: "Welcome to Thide!"
        });

        setTimeout(() => {this.activeTab = 'welcome';}, 100);
    },
    methods: {
        async onTabRemove(name: TabPanelName)
        {
            let tab = this.editorStore.tab.openedTabs.get(name.toString());

            if(tab?.active)
            {
                tab.content = this.editorStore.tab.currentText;
                this.editorStore.tab.currentText = "";
                this.activeTab = "";
            }

            if (tab == null)
            {
                console.log("Unknown error");
                alert('Unknown error');
                return;
            }

            if(!tab.isFile)
            {
                this.editorStore.tab.openedTabs.delete(name.toString());
                return;
            }

            try
            {
                let result = await axios.post('/project/upload-file', {
                    session: this.userStore.session,
                    project: this.editorStore.project.name,
                    name: tab.name,
                    file: Base64.encode(tab.content)
                });

                if((result.data as UploadFileResult).code != 0)
                {
                    console.log(result.data);
                    alert('Unknown error');
                    return;
                }

                this.editorStore.tab.openedTabs.delete(name.toString());
                return;
            }
            catch(e)
            {
                console.log(e);
                alert('Unknown error');
                return;
            }
        }
    },
    watch: {
        activeTab(newValue: string, oldValue: string)
        {
            let newTab = this.editorStore.tab.openedTabs.get(newValue);
            let oldTab = this.editorStore.tab.openedTabs.get(oldValue);
            if (oldTab != null)
            {
                oldTab.content = this.editorStore.tab.currentText;
                oldTab.active = false;
            }
            if (newTab != null)
            {
                newTab.active = true;
                this.editorStore.tab.currentText = newTab.content;
            }
        }
    }
})
</script>

<style lang="scss">
#editor-main
{
    overflow: hidden;
    padding: 2px;

    .big-container
    {
        height: 100%;
    }

    .el-tabs__content
    {
        height: 0px;
        padding: 0px;
    }

    .editor-pane
    {
        height: 100%;
    }

    .text-editor-container
    {
        border: 1px solid var(--el-border-color);
        width: 100%;
        height: calc(100% - var(--el-tabs-header-height));
    }
}
</style>