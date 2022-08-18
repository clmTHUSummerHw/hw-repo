<template>
    <div class="editor-container" ref="editor-container"></div>
</template>

<script lang="ts">
import * as monaco from "monaco-editor";
import { defineComponent } from "vue";

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
    mounted()
    {
        this.inMount = true;

        let container = this.$refs['editor-container'] as HTMLElement;
        editor = monaco.editor.create(container, { language: this.language, value: "-" });

        editor.onDidChangeModelContent(this.onModelContentChange, this);

        if (this.modelValue != null)
        {
            this.setEditorText(this.modelValue);
        }

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

        emitUpdate(value: string)
        {
            if(this.inMount)
                return;

            if (!this.reloaded)
                this.edited = true;
            else
                this.reloaded = false;

            this.$emit('update:modelValue', value);
        },

        setEditorText(value: string)
        {
            if(this.inMount)
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
</style>