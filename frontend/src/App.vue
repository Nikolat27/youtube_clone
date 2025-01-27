<script setup>
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
</script>


<template>
  <!-- Studio Components-->
  <NavbarStudio v-if="isStudioRoute" />
  <SidebarStudio v-if="isStudioRoute" />
  <div v-if="!isStudioRoute && sharedState.isSecondWebsiteSideBarOpen" class="bg z-50 absolute top-0 right-0 left-0 button-0 w-full h-full">
  </div>
  <!-- Regular Website Components-->
  <NavbarWebsite v-if="!isStudioRoute" />
  <SidebarWebsite v-if="!isStudioRoute && !isVideoDetailRoute && !sharedState.isSecondWebsiteSideBarOpen" />
  <SecondSideBarWebsite v-if="!isStudioRoute && sharedState.isSecondWebsiteSideBarOpen"></SecondSideBarWebsite>

  <RouterView />
</template>
