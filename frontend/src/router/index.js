import {
    createRouter,
    createWebHistory,
} from 'vue-router'
//
import NotFound from '~/views/404.vue'
import Login from '~/views/login.vue'
import Logout from '~/views/logout.vue'
// Index
import Index from '~/views/index/index.vue'
// Note
import NoteList from '~/views/note/list.vue'
import NoteDetail from '~/views/note/detail.vue'
import NoteEdit from '~/views/note/my/edit.vue'


const routes = [
    {path: '/:pathMatch(.*)*', component: NotFound, name: 'NotFound',},
    {path: '/login', component: Login, name: 'Login'},
    {path: '/logout', component: Logout},
    {
        path: '/', component: Index, name: 'Index',
        meta: {desc: '首页'},
        children: [{
            path: '/notes', children: [
                {path: '', component: NoteList, name: 'NoteList', alias: '/'},
                {
                    path: ':noteId(\\d+)', component: NoteDetail, name: 'NoteDetail',
                    meta: {desc: '查看详情'}
                },
                {
                    path: '/my/note', meta: {requiresAuth: true},
                    children: [
                        {
                            path: 'list', component: NoteList, name: 'MyNoteList',
                            meta: {desc: '我的'}
                        },
                        {
                            path: ':noteId(\\d+)', component: NoteDetail, name: 'MyNoteDetail',
                            meta: {desc: '查看详情'}
                        },
                        {
                            path: 'add', component: NoteEdit, name: 'AddNote',
                            meta: {desc: '新增'}
                        },
                        {
                            path: ':noteId(\\d+)/edit', component: NoteEdit, name: 'EditNote',
                            meta: {desc: '正在编辑'}
                        },
                    ]
                }]
        }]
    }]


const Router = createRouter({
    history: createWebHistory(),
    routes,
    strict: true,
})

export default Router