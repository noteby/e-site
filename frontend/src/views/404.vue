<template>
  <div class="pt-32"></div>

  <el-result title="页面不存在" sub-title="">
    <template #icon>
      <el-image/>
    </template>

    <template #extra>
      <router-link class="e-back" to="/">回到首页</router-link>
    </template>

  </el-result>
</template>

<style scoped>
.e-back {
  @apply cursor-pointer text-gray-500 text-sm underline
}
</style>
