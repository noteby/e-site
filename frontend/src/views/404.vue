<template>
  <div class="h-screen flex flex-col justify-between">
    <div class="pt-32">
      <el-result title="页面不存在" sub-title="">
        <template #icon>
          <el-image/>
        </template>

        <template #extra>
          <router-link class="e-back" to="/">回到首页</router-link>
        </template>

      </el-result>
    </div>
    
    <Copyright/>
  </div>
</template>

<style scoped>
.e-back {
  @apply cursor-pointer text-gray-500 text-sm underline
}
</style>

<script setup>
import Copyright from "~/views/copyright.vue"
</script>