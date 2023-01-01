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
        <span class="text-gray-500 italic">{{ note['display'] ? '显示' : '隐藏' }}</span>
      </div>
    </div>
    <div class="text-xs text-gray-500">{{ note['created_at'] }}</div>
    <div class="divide-y divide-solid divide-slate-200">
      <div></div>
      <div></div>
    </div>
  </div>
  <div>
    <Editor ref="editorRef" notEditable/>
  </div>
</template>

<script setup>
import {ref, watch} from "vue"
import {useRoute, useRouter} from "vue-router"
import Editor from './my/editor.vue'
import {getNote, getNoteForOwn} from "~/api/note.js"

const route = useRoute()
const router = useRouter()
const note = ref({})
const editorRef = ref(null)

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
