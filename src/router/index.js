import { createWebHistory, createRouter } from "vue-router";

import HomePageView from "@/views/HomePageView.vue";
import VideoDetail from "@/views/VideoDetail.vue";

const routes = [
    { path: "/", name: "home", component: HomePageView, },
    { path: "/video/:id", name: "video_detail", component: VideoDetail, },
    { path: "/short/:id", name: "short_detail", component: null, },
]


const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;