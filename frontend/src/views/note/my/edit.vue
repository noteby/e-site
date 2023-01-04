<template>
  <el-form
      :model="form"
      :rules="rules"
      ref="formRef"
      label-position="top"
      inline-message
  >
    <el-form-item size="large" prop="title" required>
      <el-input
          v-model="form.title"
          maxlength="36"
          show-word-limit
          placeholder="标题（必填）"
      />
    </el-form-item>

    <el-form-item size="small" prop="display">
      <el-switch
          v-model="form.display"
          inline-prompt
          active-text="显示"
          inactive-text="隐藏"
      />
    </el-form-item>

    <Editor ref="editorRef"/>

    <el-form-item size="default" class="e-buttons">
      <el-button class="e-button-delete"
                 @click="deleteDialogRef.deleteDialog=true" v-if="isUpdate" plain>删 除
      </el-button>
      <el-button @click="onSubmit" :loading='loading' plain>保 存</el-button>

      <DeleteDialog ref="deleteDialogRef"/>
    </el-form-item>

  </el-form>
</template>

<style lang="scss" scoped>
.e-editor > :deep(.ProseMirror) {
  margin-bottom: 18px;

  p {
    font-size: 14px;
  }
}

.e-buttons > :deep(div) {
  @apply justify-end
}

.e-button-delete {
  @apply text-gray-300
  hover:text-red-500
  hover:border-red-500
}
</style>

<script setup>
import DeleteDialog from './deleteDialog.vue'
import Editor from './editor.vue'
//
import {reactive, ref} from "vue"
import {useRouter} from "vue-router"
import {createNote, updateNote, getNoteForOwn} from "~/api/note.js"
import {useNoteStore} from "~/store/note.js"

const noteStore = useNoteStore()
const router = useRouter()
const form = reactive({
  title: '',
  display: false,
  content: '',
})
const rules = {
  title: [
    {required: true, trigger: 'blur', message: '标题必填'},
  ]
}
const editorRef = ref(null)
const deleteDialogRef = ref(null)
const isUpdate = ref(false)
const formRef = ref(null)
const loading = ref(false)
const deleteDialog = ref(false)

if (router.currentRoute.value.name === 'EditNote') {
  isUpdate.value = true
}

if (isUpdate.value) {
  getNoteForOwn(router.currentRoute.value.params.noteId)
      .then((res) => {
        if (res['code']) {
          router.push('/')
        } else {
          form.title = res['title']
          form.display = res['display']
          //
          editorRef.value.editor
              .commands.insertContent(res['content'])
        }
      })
}

function submitReq() {
  form.content = editorRef.value.editor.getHTML()
  if (!isUpdate.value) {
    return createNote(form.title, form.display, form.content)
  }
  return updateNote(
      router.currentRoute.value.params.noteId, form.title, form.display, form.content
  )
}

const onSubmit = () => {
  formRef.value.validate((valid) => {
        if (valid) {
          loading.value = true
          submitReq()
              .then((res) => {
                router.push({name: 'MyNoteDetail', params: {noteId: res['note_id']}})
              })
              .finally(() => {
                loading.value = false
              })
        }
      }
  )
}

</script>

