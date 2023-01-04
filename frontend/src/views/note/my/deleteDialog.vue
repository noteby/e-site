<template>
  <el-dialog
      class="e-dialog"
      v-model="deleteDialog"
      :show-close="false"
      destroy-on-close>
    <span>要删除吗？</span>
    <template #footer>
      <el-button
          @click="noteStore.toDeleteNote($router, $route.params.noteId)" text>
        是的
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import {ref} from "vue"
import {useNoteStore} from "~/store/note.js"

const noteStore = useNoteStore()
const deleteDialog = ref(false)

defineExpose({
  deleteDialog
})

</script>

<style lang="scss">
.e-dialog {
  min-width: 200px;
  max-width: 360px;

  .el-dialog__header {
    @apply hidden
  }

  .el-dialog__body {
    @apply pt-5 pb-2.5
    font-medium italic
  }

  .el-dialog__footer {
    @apply pt-0 pb-2.5
  }
}

</style>