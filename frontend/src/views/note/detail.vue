<template>
  <div class="text-xl">{{ note['title'] }}</div>
  <div class="mt-1 mb-3">
    <div class="flex text-xs" v-if="$route.meta.requiresAuth">
      <div class="mr-2">
        <router-link
            :to="{name:'EditNote',params: {noteId: $route.params.noteId}}"
            class="underline"
        >编辑
        </router-link>
      </div>
      <div class="mr-2">

        <a class="underline cursor-pointer"
           @click="deleteDialogRef.deleteDialog=true">删除</a>

        <DeleteDialog ref="deleteDialogRef"/>
      </div>
    </div>
    <div class="flex text-xs">
      <div class="text-gray-300">{{ formatDateStr(note['created_at']) }}</div>
      <div class="text-gray-500 ml-2 italic" v-if="$route.meta.requiresAuth">
        {{ note['display'] ? '显示' : '隐藏' }}
      </div>
    </div>
    <div class="divide-y divide-solid divide-slate-200">
      <div></div>
      <div></div>
    </div>
  </div>
  <div>
    <Editor ref="editorRef" notEditable/>
  </div>
</template>

<style scoped>
:deep(.ProseMirror) {
  @apply px-0
}

</style>

<script setup>
import DeleteDialog from './my/deleteDialog.vue'
import Editor from './my/editor.vue'
//
import {ref, watch} from "vue"
import {useRoute, useRouter} from "vue-router"
import {getNote, getNoteForOwn} from "~/api/note.js"
import {formatDateStr} from "~/composables/utils"

const route = useRoute()
const router = useRouter()
const note = ref({})
const editorRef = ref(null)
const deleteDialogRef = ref(null)


function getNoteReq() {
  let func = getNote
  if (route.meta.requiresAuth) {
    func = getNoteForOwn
  }
  func(route.params.noteId).then((res) => {
    if (res['code']) {
      router.push('/')
    } else {
      note.value = res
      //
      editorRef.value.editor
          .commands.insertContent(res['content'])
    }
  })
}

watch(
    () => route.path,
    () => {
      getNoteReq()
    },
    {immediate: true, flush: 'post'}
)

</script>
