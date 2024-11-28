import { createWebHistory, createRouter } from "vue-router";

import HomePageView from "@/views/HomePageView.vue";
import VideoDetail from "@/views/VideoDetail.vue";
import SubscriptionsView from "@/views/SubscriptionsView.vue";
import NotFoundView from "@/views/NotFoundView.vue";
import TestView from "@/views/TestView.vue";


const routes = [
    { path: "/", name: "home", component: HomePageView, },
    { path: "/video/:id", name: "video_detail", component: VideoDetail, },
    { path: "/subscriptions", name: "subscriptions", component: SubscriptionsView, },
    { path: "/test", name: "test", component: TestView, },
    { path: "/short/:id", name: "short_detail", component: null, },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFoundView },
]


const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;