<template>
  <div v-for="(note, index) in noteList" :key="note.id">
    <div>
      <router-link class="block"
                   :to="{name: linkName, params: {noteId: note['note_id']}}"
      >{{ note['title'] }}
      </router-link>
    </div>
    <div class="mt-1 mb-3">
      <div class="flex text-xs" v-if="$route.meta.requiresAuth">
        <div class="mr-2">
          <router-link
              :to="{name: 'EditNote', params: {noteId: note['note_id']}}"
              class="underline">编辑
          </router-link>
        </div>
      </div>
      <div class="flex text-xs">
        <div class="text-gray-400">{{ formatDateStr(note['created_at']) }}</div>
        <div class="text-gray-500 ml-2 italic" v-if="$route.meta.requiresAuth">
          {{ note['display'] ? '显示' : '隐藏' }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, watch} from "vue"
import {useRoute} from "vue-router"
import {getNoteList, getNoteListForOwn} from "~/api/note.js"
import {formatDateStr} from "~/composables/utils"

const route = useRoute()
const noteList = ref([])
const linkName = ref(null)

function getNoteListReq() {
  let func = getNoteList
  linkName.value = 'NoteDetail'
  if (route.meta.requiresAuth) {
    func = getNoteListForOwn
    linkName.value = 'MyNoteDetail'
  }
  func().then((res) => {
    noteList.value = res.list
  })
}

watch(
    () => route.path,
    () => {
      getNoteListReq()
    },
    {immediate: true, flush: 'post'}
)
</script>

<style scoped>

</style>