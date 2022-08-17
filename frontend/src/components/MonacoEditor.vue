<template>
    <div class="editor-container" ref="editor-container"></div>
</template>

<script lang="ts">
import * as monaco from "monaco-editor";
import { defineComponent } from "vue";

class Data
{
    editor: monaco.editor.IStandaloneCodeEditor | undefined = undefined;
}

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
        return new Data();
    },
    mounted()
    {
        console.log("mounted");
        let container = this.$refs['editor-container'] as HTMLElement;
        this.editor = monaco.editor.create(container, {language: this.language, value: "-"});

        this.editor.onDidChangeModelContent(this.onModelContentChange, this);

        if(this.modelValue != null)
        {
            console.log(this.modelValue);
            //this.editor.setValue(this.modelValue);
            console.log('setValue');
        }
    },
    methods: {
        onModelContentChange(event: monaco.editor.IModelContentChangedEvent)
        {
            console.log("onModelContentChange");
            let text = this.modelValue;
            if(text == null)
                return;
            for(let change of event.changes)
            {
                let t1 = text.substring(0, change.rangeOffset);
                let t2 = change.text;
                let t3 = text.substring(change.rangeOffset + change.rangeLength + 1, text.length);
                this.$emit('update:modelValue', t1 + t2 + t3);
            }
        }
    },
    watch: {
        modelValue(newValue: string, oldValue: string)
        {
            console.log("watchModelValue");
            if(newValue != oldValue)
            {
                console.log(newValue);
                this.editor?.setValue(newValue);
                console.log('setValue');
            }
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