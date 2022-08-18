<template>
    <div class="editor-container" ref="editor-container"></div>
</template>

<script lang="ts">
import * as monaco from "monaco-editor";
import { defineComponent } from "vue";
import { useBreakpointsStore } from "@/stores/breakpoints";

import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker';
import jsonWorker from 'monaco-editor/esm/vs/language/json/json.worker?worker';
import cssWorker from 'monaco-editor/esm/vs/language/css/css.worker?worker';
import htmlWorker from 'monaco-editor/esm/vs/language/html/html.worker?worker';
import tsWorker from 'monaco-editor/esm/vs/language/typescript/ts.worker?worker';

self.MonacoEnvironment = {
    getWorker(_, label)
    {
        if (label === 'json')
        {
            return new jsonWorker()
        }
        if (label === 'css' || label === 'scss' || label === 'less')
        {
            return new cssWorker()
        }
        if (label === 'html' || label === 'handlebars' || label === 'razor')
        {
            return new htmlWorker()
        }
        if (label === 'typescript' || label === 'javascript')
        {
            return new tsWorker()
        }
        return new editorWorker()
    }
}

let editor: monaco.editor.IStandaloneCodeEditor | undefined = undefined;

export default defineComponent({
    props: {
        modelValue: String,
        file: String,
        language: String
    },
    emits: [
        'update:modelValue'
    ],
    data()
    {
        return {
            edited: false,
            reloaded: false,
            inMount: false
        }
    },
    computed: {
        breakpointsStore()
        {
            return useBreakpointsStore();
        }
    },
    mounted()
    {
        this.inMount = true;

        let container = this.$refs['editor-container'] as HTMLElement;
        editor = monaco.editor.create(container, { language: this.language, glyphMargin: true });

        editor.onMouseUp(this.onEditorMouseUp, this);
        editor.onDidChangeModelContent(this.onModelContentChange, this);

        if (this.modelValue != null)
            this.setEditorText(this.modelValue);

        if(this.file != null)
            for(let i of this.breakpointsStore.breakpointsForFile(this.file))
                this.addBreakpoint(i, false);

        this.inMount = false;
    },
    unmounted()
    {
        editor?.dispose();
    },
    methods: {
        onModelContentChange(event: monaco.editor.IModelContentChangedEvent)
        {
            console.log("onModelContentChange");
            let text = this.modelValue;
            if (text == null)
                return;
            for (let change of event.changes)
            {
                let t1 = text.substring(0, change.rangeOffset);
                let t2 = change.text;
                let t3 = text.substring(change.rangeOffset + change.rangeLength + 1, text.length);

                this.emitUpdate(t1 + t2 + t3);
            }
        },

        onEditorMouseUp(event: monaco.editor.IEditorMouseEvent)
        {
            if (this.file == null)
                return;

            if (event.target.type == 2)
            {
                let lineNumber = event.target.position.lineNumber
                if (this.breakpointsStore.hasBreakpoint(this.file, lineNumber))
                {
                    this.removeBreakpoint(lineNumber);
                }
                else
                {
                    this.addBreakpoint(lineNumber, true);
                }
            }
        },

        emitUpdate(value: string)
        {
            if (this.inMount)
                return;

            if (!this.reloaded)
                this.edited = true;
            else
                this.reloaded = false;

            this.$emit('update:modelValue', value);
        },

        setEditorText(value: string)
        {
            if (this.inMount)
            {
                editor?.setValue(value);
                return;
            }

            if (!this.edited)
            {
                this.reloaded = true;
                editor?.setValue(value);
            }
            else
                this.edited = false;
        },

        addBreakpoint(lineNumber: number, addToStore: boolean)
        {
            console.log("addBreakpoint");
            if(this.file == null)
                return;

            editor?.deltaDecorations([], [{
                range: new monaco.Range(lineNumber, 1, lineNumber, 1),
                options: {
                    isWholeLine: true,
                    linesDecorationsClassName: 'breakpoint'
                }
            }]);

            if(addToStore)
                this.breakpointsStore.addBreakpoint(this.file, lineNumber);
        },

        removeBreakpoint(lineNumber: number)
        {
            console.log("removeBreakpoint");
            if(this.file == null)
                return;

            let decorations = editor?.getLineDecorations(lineNumber);
            let breakpointDecorations: string[] = [];

            if (decorations != null)
                for (let i of decorations)
                    if (i.options.linesDecorationsClassName == "breakpoint")
                        breakpointDecorations.push(i.id);

            editor?.deltaDecorations(breakpointDecorations, []);
            this.breakpointsStore.removeBreakpoint(this.file, lineNumber);
        }
    },
    watch: {
        modelValue(newValue: string, _oldValue: string)
        {
            this.setEditorText(newValue);
        }
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

.breakpoint
{
    background: red;
    width: 10px !important;
    height: 10px !important;
    left: 0px !important;
    top: 3px;
    border-radius: 5px;
}
</style>