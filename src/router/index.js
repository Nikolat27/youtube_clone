import { createWebHistory, createRouter } from "vue-router";
import HomePageView from "@/views/HomePageView.vue";
import VideoDetail from "@/views/VideoDetail.vue";
import SubscriptionsView from "@/views/SubscriptionsView.vue";
import ShortsView from "@/views/ShortsView.vue";
import ChannelPageView from "@/views/ChannelPageView.vue";
import NotFoundView from "@/views/NotFoundView.vue";
import TestView from "@/views/TestView.vue";

// Children routes
import Home from "@/views/channelViews/Home.vue";
import Video from "@/views/channelViews/Videos.vue";
import Shorts from "@/views/channelViews/Shorts.vue";
import Playlists from "@/views/channelViews/Playlists.vue";
import Community from "@/views/channelViews/Community.vue";
import Search from "@/views/channelViews/Search.vue";

const routes = [
    { path: "/", name: "home", component: HomePageView, },
    { path: "/video/:id", name: "video_detail", component: VideoDetail, },
    { path: "/subscriptions", name: "subscriptions", component: SubscriptionsView, },
    { path: "/short/:id", name: "short_detail", component: ShortsView, },
    {
        path: "/channel-page", name: "channel_detail", component: ChannelPageView, children: [
            { path: '', name:'channel-home', component: Home, },
            { path: 'videos', name:'videos', component: Video, },
            { path: 'shorts', name:'shorts', component: Shorts, },
            { path: 'playlists',name:'playlists', component: Playlists, },
            { path: 'community', name:'community', component: Community, },
            { path: 'search', name:'search', component: Search, },
        ]
    },
    { path: "/test", name: "test", component: TestView, },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFoundView },
]


const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;