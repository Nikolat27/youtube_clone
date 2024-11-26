<script setup>
import Navbar from "@/components/Navbar.vue"
import Sidebar from "./components/Sidebar.vue";
import { RouterView } from "vue-router";
</script>


<template>
  <Navbar />
  <Sidebar />
  <RouterView />
</template>

