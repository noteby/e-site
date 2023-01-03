<template></template>
<style scoped></style>

<script setup>
import {onMounted} from "vue"
import {useRouter} from "vue-router"
import {useUserStore} from "~/store/user.js"

onMounted(() => {
  const router = useRouter()
  const userStore = useUserStore()

  userStore.logout()
  router.push('/')
})


</script>

