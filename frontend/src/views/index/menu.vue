<template>
  <el-menu
      text-color="#000"
      active-text-color="#000"
      router>
    <el-menu-item index="/">
      <template #title>首页</template>
    </el-menu-item>

    <div v-if="userStore.hasLoggedIn()">
      <el-sub-menu index="1">
        <template #title>管理</template>

        <el-menu-item index="/my/note/list">
          <template #title>我的</template>
        </el-menu-item>
        <el-menu-item index="/my/note/add">
          <template #title>新增</template>
        </el-menu-item>
        <el-menu-item index="/logout">
          <template #title>退出</template>
        </el-menu-item>
      </el-sub-menu>
    </div>
    <div v-else>
      <el-menu-item index="/login">
        <template #title>登录</template>
      </el-menu-item>
    </div>
  </el-menu>

</template>

<script setup>
import {useUserStore} from "~/store/user.js"

const userStore = useUserStore()

</script>

<style scoped>
.el-menu {
  @apply mt-20
}

.el-menu-item {
  @apply text-sm
}

</style>