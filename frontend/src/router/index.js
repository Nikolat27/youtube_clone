import { createWebHistory, createRouter } from "vue-router";
import NProgress from 'nprogress'
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
import createPostsView from "@/views/createPostsView.vue";

// Studio Children routes
import channelContentView from "@/views/studioViews/channelContentView.vue";
import dashboardView from "@/views/studioViews/dashboardView.vue";
import customizationView from "@/views/studioViews/customizationView.vue";

// Channel Content Children routes
import VideosView from "@/views/studioViews/channelContentViews/VideosView.vue";
import channelContentShortsView from "@/views/studioViews/channelContentViews/ShortsView.vue";
import LiveView from "@/views/studioViews/channelContentViews/LiveView.vue";
import PostsView from "@/views/studioViews/channelContentViews/PostsView.vue";
import PlaylistsView from "@/views/studioViews/channelContentViews/PlaylistsView.vue";
import SearchVideosView from "@/views/SearchVideosView.vue";

const routes = [
    { path: "/", name: "home", component: HomePageView, },
    { path: "/video/:id", name: "video_detail", component: VideoDetail, },
    { path: "/videos/results", name: "search_results", component: SearchVideosView, },
    { path: "/subscriptions", name: "subscriptions", component: SubscriptionsView, },
    { path: "/short/:id", name: "short_detail", component: ShortsView, },
    { path: "/auth", name: "auth", component: AuthView, },
    { path: "/history", name: "history", component: HistoryView, },
    { path: "/playlist", name: "playlist-videos", component: PlaylistVideosView, },
    { path: "/posts", name: "create-posts", component: createPostsView, },
    {
        path: "/channel-page/:id", name: "channel_detail", component: ChannelPageView, children: [
            { path: '', name: 'channel-home', component: Home, },
            { path: 'videos', name: 'videos', component: Video, },
            { path: 'playlists', name: 'playlists', component: Playlists, },
            { path: 'community', name: 'community', component: Community, },
            { path: 'search', name: 'search', component: Search, },
        ]
    },
    {
        path: "/studio/", name: "studio", redirect: '/studio/channel-content/videos', component: null, children: [
            {
                path: "channel-content", name: 'channel-content', redirect: '/studio/channel-content/videos', component: channelContentView, children: [
                    { path: "videos", name: 'videos', component: VideosView },
                    { path: "shorts", name: 'shorts', component: channelContentShortsView },
                    { path: "lives", name: 'lives', component: LiveView },
                    { path: "posts", name: 'posts', component: PostsView },
                    { path: "playlists", name: 'playlists', component: PlaylistsView },
                ]
            },
            { path: "dashboard", name: 'dashboard', component: dashboardView },
            { path: "analytics", name: 'analytics', component: null },
            { path: "community", name: 'community', component: null },
            { path: "earn", name: 'earn', component: null },
            { path: "customization", name: 'customization', component: customizationView },
        ]
    },
    { path: "/test", name: "test", component: TestView, },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFoundView },
]


const router = createRouter({
    history: createWebHistory(),
    routes,
})

// Loading Indicator 
router.beforeEach((To, From, next) => {
    NProgress.start()
    next()
})
router.afterEach(() => {
    NProgress.done()
})

export default router;