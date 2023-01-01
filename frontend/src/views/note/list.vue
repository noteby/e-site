<template>
  <div v-for="(note, index) in noteList" :key="note.id">
    <div>
      <router-link
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
        <div class="mr-2">
          <span class="text-gray-500 italic">{{ note['display'] ? '显示' : '隐藏' }}</span>
        </div>
      </div>
      <div class="text-xs text-gray-300">
        {{ note['created_at'] }}
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, watch} from "vue"
import {useRoute} from "vue-router"
import {getNoteList, getNoteListForOwn} from "~/api/note.js"

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