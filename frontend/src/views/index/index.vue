<template>
  <el-container class="h-screen">
    <el-aside id="e-aside">
      <div class="h-full flex flex-col">
        <div class="sticky top-0 py-16 bg-white z-10"></div>
        <div class="grow">
          <Menu/>
        </div>
      </div>
    </el-aside>

    <el-container>
      <el-main>
        <div class="h-full flex flex-col">
          <div class="sticky top-0 pt-6 bg-white z-10">
            <div class="flex justify-between">
              <Breadcrumb/>

              <div class="leading-none">
                <el-icon @click="toCollapse">
                  <Expand v-if="isCollapse"/>
                  <Fold v-else/>
                </el-icon>
              </div>
            </div>

            <el-divider/>
          </div>

          <div class="grow flex flex-col justify-between">
            <div>
              <router-view></router-view>
            </div>

            <Copyright/>
          </div>
        </div>
      </el-main>

    </el-container>
  </el-container>
</template>

<script setup>
import {ref} from 'vue'
import {Expand, Fold} from '@element-plus/icons-vue'
import Menu from '~/views/index/menu.vue'
import Breadcrumb from '~/views/index/breadcrumb.vue'
import Copyright from '~/views/copyright.vue'

const isCollapse = ref(false)

function toCollapse() {
  isCollapse.value = !isCollapse.value

  let aside = document.getElementById('e-aside')
  aside.style.display = isCollapse.value ? 'none' : 'block'
}


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