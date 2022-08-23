<template>
    <!--
        用法：在其他组件中嵌套该组件时，需要用v-model把编辑器内容和一个字符串绑定，
        同时，需要填写组件的file属性来允许组件添加/删除断点。

        示例：<MonacoEditor v-model="someStrVariable" file="some/file/name", language="java">

        所有断点被储存在@/stores/breakpoints.ts中。
    -->
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

//按照github页面上的指示配置monaco editor环境（我也不知道有什么用）
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

//editor不能是组件data的成员，否则，由于vue的某些自动化操作，editor将无法setValue
let editor: monaco.editor.IStandaloneCodeEditor | undefined = undefined;

export default defineComponent({
    props: {
        modelValue: String, //供v-model绑定的值
        file: String, //编辑器当前打开的文件名，留空代表未命名的临时文件
        language: String //编辑器的语言
    },
    emits: [
        'update:modelValue'
    ],
    data()
    {
        return {
            edited: false, //类似锁的变量，用于防止事件互相触发，引起死循环
            reloaded: false, //类似锁的变量
            inMount: false //类似锁的变量
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

        //创建editor实例
        let container = this.$refs['editor-container'] as HTMLElement;
        editor = monaco.editor.create(container, { language: this.language, glyphMargin: true });

        //监听鼠标事件和内容改变事件
        editor.onMouseUp(this.onEditorMouseUp, this);
        editor.onDidChangeModelContent(this.onModelContentChange, this);

        //为editor内容赋值
        if (this.modelValue != null)
            this.setEditorText(this.modelValue);

        //若文件有断点，显示所有的断点
        if(this.file != null)
            for(let i of this.breakpointsStore.breakpointsForFile(this.file))
                this.addBreakpoint(i, false);

        this.inMount = false;
    },
    unmounted()
    {
        //摧毁editor，为占据此位置的下一个组件初始化留出空间
        editor?.dispose();
    },
    methods: {
        //监听editor内容变化事件
        onModelContentChange(event: monaco.editor.IModelContentChangedEvent)
        {
            let text = this.modelValue;
            if (text == null)
                return;
            for (let change of event.changes)
            {
                //获取改变后的内容
                let t1 = text.substring(0, change.rangeOffset);
                let t2 = change.text;
                let t3 = text.substring(change.rangeOffset + change.rangeLength, text.length);

                //更新modelValue属性
                this.emitUpdate(t1 + t2 + t3);
            }
        },

        //监听鼠标事件，用于添加/删除断点
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

        //通过类似加锁的方式安全发出update信号
        emitUpdate(value: string)
        {
            if (this.inMount)
                return;

            if (!this.reloaded)
            {
                this.edited = true;
                this.$emit('update:modelValue', value);
            }
            else
                this.reloaded = false;
        },

        //通过类似加锁的方式安全设置editor值
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
                console.log(value);
                editor?.setValue(value);
            }
            else
                this.edited = false;
        },

        //添加断点，addToStore参数用于区分手动添加和从store加载的情况
        addBreakpoint(lineNumber: number, addToStore: boolean)
        {
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

        //移除断点
        removeBreakpoint(lineNumber: number)
        {
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
        //监视v-model改变，并更新editor值
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
        text-align: left; //不加这条会导致文字居中而光标不居中，效果极其鬼畜
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