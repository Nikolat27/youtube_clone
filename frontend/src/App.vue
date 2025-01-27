<script setup>
import { ref, onMounted, nextTick } from "vue";

// Components
import NavbarWebsite from "@/components/website/NavbarWebsite.vue"
import SidebarWebsite from "@/components/website/SidebarWebsite.vue";
import NavbarStudio from "./components/studio/NavbarStudio.vue";
import SidebarStudio from "./components/studio/SidebarStudio.vue";
import SecondSideBarWebsite from "./components/website/SecondSideBarWebsite.vue";
import { sharedState } from "./sharedState";

import { RouterView } from "vue-router";
import { useRoute } from "vue-router";
import { computed } from "vue";

const route = useRoute();
const isVideoDetailRoute = computed(() => route.name === "video_detail");
// const isStudioRoute = computed(() => route.name === 'studio');
const isStudioRoute = computed(() => route.path.startsWith("/studio/"));


let windowHeight = ref(null)
const updateWindowHeight = () => {
  windowHeight.value = document.body.offsetHeight + window.innerHeight
}


const checkSideBar = () => {
  const windowWidth = window.innerWidth
  if (windowWidth > 650) {
    sharedState.isWebsiteSideBarCollapsed = false
    sharedState.isWebsiteSideBarClosed = false
  } else if (windowWidth >= 553 && windowWidth <= 650) {
    sharedState.isWebsiteSideBarCollapsed = true
    sharedState.isWebsiteSideBarClosed = false
  } else if (windowWidth < 553) {
    sharedState.isWebsiteSideBarClosed = true
  }
}


onMounted(() => {
  nextTick(() => {
    updateWindowHeight();
  });
  window.addEventListener("resize", updateWindowHeight)
  checkSideBar()
})
</script>


<template>
  <!-- Studio Components-->
  <NavbarStudio v-if="isStudioRoute" />
  <SidebarStudio v-if="isStudioRoute" />

  <!-- Regular Website Components-->
  <NavbarWebsite v-if="!isStudioRoute" />
  <SidebarWebsite v-if="!isStudioRoute && !isVideoDetailRoute && !sharedState.isSecondWebsiteSideBarOpen" />
  <SecondSideBarWebsite v-if="!isStudioRoute && sharedState.isSecondWebsiteSideBarOpen"></SecondSideBarWebsite>

  <!-- Layer div -->
  <div @click="sharedState.isSecondWebsiteSideBarOpen = false"
    v-if="!isStudioRoute && sharedState.isSecondWebsiteSideBarOpen"
    class="bg-opacity-50 bg-gray-500 z-50 absolute top-0 right-0 left-0 button-0 w-full"
    :style="{ height: `${windowHeight}px` }">
  </div>
  <RouterView />
</template>
