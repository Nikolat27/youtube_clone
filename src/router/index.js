import { createWebHistory, createRouter } from "vue-router";

import HomePageView from "@/views/HomePageView.vue";

const routes = [
    {
        path: "/",
        name: "home",
        component: HomePageView,
    },
]


const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;