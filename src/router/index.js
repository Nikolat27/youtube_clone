import { createWebHistory, createRouter } from "vue-router";
import HomePageView from "@/views/HomePageView.vue";
import VideoDetail from "@/views/VideoDetail.vue";
import SubscriptionsView from "@/views/SubscriptionsView.vue";
import ShortsView from "@/views/ShortsView.vue";
import ChannelPageView from "@/views/ChannelPageView.vue";
import AuthView from "@/views/AuthView.vue";
import HistoryView from "@/views/HistoryView.vue";
import NotFoundView from "@/views/NotFoundView.vue";
import TestView from "@/views/TestView.vue";

// Channel-page Children routes
import Home from "@/views/channelViews/Home.vue";
import Video from "@/views/channelViews/Videos.vue";
import Shorts from "@/views/channelViews/Shorts.vue";
import Playlists from "@/views/channelViews/Playlists.vue";
import Community from "@/views/channelViews/Community.vue";
import Search from "@/views/channelViews/Search.vue";
import PlaylistVideosView from "@/views/PlaylistVideosView.vue";

// Studio Children routes
import channelContentView from "@/views/studioViews/channelContentView.vue";


const routes = [
    { path: "/", name: "home", component: HomePageView, },
    { path: "/video/:id", name: "video_detail", component: VideoDetail, },
    { path: "/subscriptions", name: "subscriptions", component: SubscriptionsView, },
    { path: "/short/:id", name: "short_detail", component: ShortsView, },
    { path: "/auth", name: "auth", component: AuthView, },
    { path: "/history", name: "history", component: HistoryView, },
    { path: "/playlist", name: "playlist-videos", component: PlaylistVideosView, },
    {
        path: "/channel-page", name: "channel_detail", component: ChannelPageView, children: [
            { path: '', name: 'channel-home', component: Home, },
            { path: 'videos', name: 'videos', component: Video, },
            { path: 'shorts', name: 'shorts', component: Shorts, },
            { path: 'playlists', name: 'playlists', component: Playlists, },
            { path: 'community', name: 'community', component: Community, },
            { path: 'search', name: 'search', component: Search, },
        ]
    },
    {
        path: "/studio/", name: "studio", component: null, children: [
            { path: "channel-content", name: 'channel-content', component: channelContentView },
            { path: "dashboard", name: 'dashboard', component: null },
            { path: "analytics", name: 'analytics', component: null },
            { path: "community", name: 'community', component: null },
            { path: "earn", name: 'earn', component: null },
            { path: "customization", name: 'customization', component: null },
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