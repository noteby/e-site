<template>
  <el-container class="h-screen">

    <div v-if="!isCollapse">
      <div v-if="isWideScreen">
        <el-aside>
          <div class="sticky top-0 py-16 bg-white z-10"></div>
          <Menu/>
        </el-aside>
      </div>
      <div v-else>
        <div class="absolute h-screen left-0 bg-white z-10 overflow-auto">
          <Menu class="py-16"/>
        </div>
      </div>
    </div>

    <el-container>
      <el-header>
        <div class="pt-5 flex items-center">
          <el-icon @click="toCollapse" color="#6b7280" size="20" class="mr-3">
            <Expand v-if="isCollapse"/>
            <Fold v-else/>
          </el-icon>

          <Breadcrumb/>

        </div>

        <div class="divide-y-[1px] divide-solid divide-slate-200 pt-3">
          <div></div>
          <div></div>
        </div>

      </el-header>

      <el-main>
        <div class="absolute inset-0 backdrop-opacity-10 bg-white/50 z-[5]"
             v-if="!isCollapse && !isWideScreen"
             @click="onMaskLayer"
        ></div>

        <div class="h-full flex flex-col justify-between">
          <div>
            <router-view></router-view>
          </div>
          <Copyright/>
        </div>
      </el-main>

    </el-container>
  </el-container>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import {Expand, Fold} from '@element-plus/icons-vue'
import Menu from '~/views/index/menu.vue'
import Breadcrumb from '~/views/index/breadcrumb.vue'
// import DropdownMenu from '~/views/index/dropdownMenu.vue'
import Copyright from '~/views/copyright.vue'

const isCollapse = ref(false)
const isWideScreen = ref(true)

function toCollapse() {
  isCollapse.value = !isCollapse.value
}

function onResize() {
  if (document.body.clientWidth > 640) {
    isWideScreen.value = true
    isCollapse.value = false
  } else {
    isWideScreen.value = false
    isCollapse.value = true
  }
}


function onMaskLayer() {
  isCollapse.value = true
}

onMounted(() => {
  onResize()
})

window.addEventListener('resize', onResize)


</script>

<style scoped>
.el-header, .el-main {
  @apply px-2.5 sm:px-5
}

.el-header {
  @apply h-[70px]
}

.el-main {
  @apply py-0
}

.el-aside {
  @apply w-24
}

</style>