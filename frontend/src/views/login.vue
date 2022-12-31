<template>
  <div class="flex justify-center">
    <el-form :model="form"
             :rules="rules"
             ref="formRef"
             inline-message
             class="e-form">

      <el-form-item prop="email" required>
        <el-input v-model="form.email"
                  class="h-9"
                  placeholder="邮箱"/>
      </el-form-item>

      <el-form-item prop="password">
        <el-input v-model="form.password"
                  class="h-9"
                  type="password" show-password
                  placeholder="密码"/>
      </el-form-item>

      <el-form-item>
        <el-button class="mx-auto w-60"
                   :loading='loading'
                   @click="onSubmit">
          登 录
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.e-form {
  @apply w-60 mt-52 mb-10
}
</style>

<script setup>
import {reactive, ref} from 'vue'
import {useRouter} from 'vue-router'
//
import {useUserStore} from "~/store/user.js"

const userStore = useUserStore()
const router = useRouter()
const form = reactive({
  email: '',
  password: '',
})
const rules = {
  email: [
    {required: true, trigger: 'blur', message: '邮箱必填'},
    {type: 'email', trigger: ['blur', 'change'], message: '请输入有效的邮箱'}
  ],
  password: [
    {required: true, trigger: 'blur', message: '密码必填'}
  ],
}
const formRef = ref(null)
const loading = ref(false)
const onSubmit = () => {
  formRef.value.validate((valid) => {
    if (valid) {
      loading.value = true
      userStore.login(form.email, form.password)
          .then(res => {
            router.push('/')
          })
          .catch(err => {
            // Clear password
            form.password = null
          })
          .finally(() => {
            loading.value = false
          })
    }
  })
}

</script>
