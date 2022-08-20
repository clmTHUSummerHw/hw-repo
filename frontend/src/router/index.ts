import { createRouter, createWebHashHistory } from 'vue-router'
import IndexView from '@/views/IndexView.vue'
import SignUpView from '@/views/SignUpView.vue'
import ProjectListView from '@/views/ProjectListView.vue'
import EditorView from '@/views/EditorView.vue'
import TestEditorView from '@/views/TestEditorView.vue'

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: '/',
            name: 'index',
            component: IndexView
        },
        {
            path: '/sign-up',
            name: 'sign_up',
            component: SignUpView
        },
        {
            path: '/project-list',
            name: 'project_list',
            component: ProjectListView
        },
        {
            path: '/editor',
            name: 'editor',
            component: EditorView
        },
        {
            path: '/test',
            name: 'test_editor',
            component: TestEditorView
        }
    ]
})

export default router
