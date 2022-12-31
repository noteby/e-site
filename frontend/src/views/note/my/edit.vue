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

    <el-form-item size="default">
      <el-button :loading='loading' @click="onSubmit">保 存</el-button>
    </el-form-item>

  </el-form>

</template>

<style lang="scss">
.e-editor {
  margin-bottom: 18px;

  p {
    font-size: 14px;
  }
}
</style>

<script setup>
import {reactive, ref} from "vue"
import {useRouter} from "vue-router"
import Editor from './editor.vue'
import {createNote, updateNote, getNoteForOwn} from "~/api/note.js"

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
const formRef = ref(null)
const editorRef = ref(null)
const loading = ref(false)

let isUpdate = false
if (router.currentRoute.value.name === 'EditNote') {
  isUpdate = true
}

if (isUpdate) {
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
  if (!isUpdate) {
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

