<script setup>
import Navbar from "@/components/Navbar.vue"
import Sidebar from "./components/Sidebar.vue";
import { RouterView } from "vue-router";
import { useRoute } from "vue-router";
import { computed } from "vue";

const route = useRoute();
const isVideoDetailRoute = computed(() => route.name === "video_detail")
</script>


<template>
  <Navbar />
  <Sidebar v-if="!isVideoDetailRoute" />
  <RouterView />
</template>
