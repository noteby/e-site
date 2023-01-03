<template>
  <el-menu
      text-color="#000"
      active-text-color="#000"
      mode="horizontal"
      menu-trigger="click"
      :ellipsis="false"
      router>

    <el-sub-menu index="#1" class="e-dropdown-1">
      <el-menu-item index="/">首页</el-menu-item>
      <el-sub-menu index="#2" v-if="userStore.hasLoggedIn()">
        <template #title>管理</template>
        <el-menu-item index="/my/note/list">我的</el-menu-item>
        <el-menu-item index="/my/note/add">新增</el-menu-item>
        <el-menu-item index="/logout">退出</el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/login" v-else>登录</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script setup>
import {useUserStore} from "~/store/user.js"

const userStore = useUserStore()

</script>

<style lang="scss" scoped>
.el-menu-item {
  @apply text-sm
}

.el-menu--horizontal {
  @apply border-b-0 border-none
}

:deep(.el-sub-menu__title) {
  @apply border-b-0 border-none #{!important}
}

.e-dropdown-1 :deep(.el-icon) {
  @apply m-0
}

</style>