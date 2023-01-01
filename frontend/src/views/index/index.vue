<template>
  <el-container class="h-screen">
    <el-aside class="relative">
      <div class="absolute inset-x-0 top-0">
        <Menu/>
      </div>
    </el-aside>

    <el-container>
      <el-main>
        <div class="h-full flex flex-col">
          <div class="sticky top-0 pt-6 bg-white z-10">
            <Breadcrumb/>
            <el-divider/>
          </div>

          <div class="grow flex flex-col justify-between">
            <div>
              <router-view></router-view>
            </div>

            <div class="leading-none text-center">
              <span class="text-xs text-slate-300">
                Copyright &copy; 2023 Formeta
              </span>
            </div>
          </div>
        </div>
      </el-main>

    </el-container>
  </el-container>
</template>

<script setup>
import Menu from '~/views/index/menu.vue'
import Breadcrumb from '~/views/index/breadcrumb.vue'

</script>

<style scoped>
.el-aside {
  @apply w-24
}

.el-main {
  @apply py-0
}

::-webkit-scrollbar {
  /*滚动条整体样式，定义滚动区域大小*/
  @apply w-1.5 h-1.5
}

::-webkit-scrollbar-thumb {
  /*滚动条滑块*/
  @apply rounded-none bg-gray-300
}

::-webkit-scrollbar-thumb:hover {
  /*滚动条滑块（鼠标悬停时）*/
  @apply bg-gray-500
}

::-webkit-scrollbar-track {
  /*滚动条轨道*/
  @apply rounded-none bg-gray-100
}

</style>