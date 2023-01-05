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
                <div v-if="isWideScreen">
                  <el-icon @click="toCollapse">
                    <Expand v-if="isCollapse"/>
                    <Fold v-else/>
                  </el-icon>
                </div>
                <div v-else>
                  <DropdownMenu/>
                </div>
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
import {ref, onMounted} from 'vue'
import {Expand, Fold} from '@element-plus/icons-vue'
import Menu from '~/views/index/menu.vue'
import Breadcrumb from '~/views/index/breadcrumb.vue'
import DropdownMenu from '~/views/index/dropdownMenu.vue'
import Copyright from '~/views/copyright.vue'

const isCollapse = ref(false)
const isWideScreen = ref(true)

function displayAside(i) {
  let aside = document.getElementById('e-aside')
  aside.style.display = i ? 'block' : 'none'
}

function toCollapse() {
  isCollapse.value = !isCollapse.value
  displayAside(!isCollapse.value)
}

function onResize() {
  if (document.body.clientWidth > 640) {
    isWideScreen.value = true
    displayAside(true)
  } else {
    isWideScreen.value = false
    displayAside(false)
  }
}

onMounted(() => {
  onResize()
})

window.addEventListener('resize', onResize)


</script>

<style scoped>
.el-aside {
  @apply w-24
}

.el-main {
  @apply py-0
  px-2.5 sm:px-5
}

</style>