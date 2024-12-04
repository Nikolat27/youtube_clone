<script setup>
import { ref, reactive, watch } from 'vue';
import { useRoute } from 'vue-router';

const router = useRoute();


// Pinned Video
const pinnedVideo = reactive({
    title: "Django Tutorial",
    channel_name: "Channel Name",
    views: "1.1M views",
    created_at: "2 years ago",
    description: "asdfasdfasdfadsf",
    duration: "12:29",
    currentSrc: '/src/assets/img/Django.png',
    thumbnail: '/src/assets/img/Django.png',
    gif: "/src/assets/img/gif-image1.webp",
});

let hoverTimeout;
const hoverImage = (video) => {
    hoverTimeout = setTimeout(() => {
        video.currentSrc = video.gif;
    }, 1000)

};

const resetImage = (video) => {
    clearTimeout(hoverTimeout);
    video.currentSrc = video.thumbnail;
};

watch(() => router.query.query, () => {

})
</script>

<template>
    <div class="flex flex-col">
        <!-- Pinned Video Section -->
        <div class="flex flex-row mt-6 border-b-[1px] pb-6">
            <a href="#" class="relative">
                <img @mouseover="hoverImage(pinnedVideo)" @mouseleave="resetImage(pinnedVideo)"
                    class="pinned-video-img w-[246px] h-[145px] rounded-2xl" :src="pinnedVideo.currentSrc" alt="">
                <button
                    class="w-[40px] h-[18px] bg-black text-white font-medium text-xs absolute right-2 bottom-1 rounded-md">
                    {{ pinnedVideo.duration }}
                </button>
            </a>
            <div class="flex flex-col ml-4 mt-2">
                <a href="#" class="text-lg font-normal">{{ pinnedVideo.title }}</a>
                <div class="flex flex-row gap-x-2" style="font-size: 12px; font-weight: 400; color: #69696a;">
                    <a href="#">{{ pinnedVideo.channel_name }}</a>
                    <span>{{ pinnedVideo.views }} views</span>
                    <span>{{ pinnedVideo.created_at }}</span>
                </div>
                <p style="margin-top: 5px; font-size: 12px; font-weight: 400; color: #69696a;">{{
                    pinnedVideo.description }}</p>
            </div>
        </div>
        <div class="flex flex-row mt-6 border-b-[1px] pb-6">
            <a href="#" class="relative">
                <img @mouseover="hoverImage(pinnedVideo)" @mouseleave="resetImage(pinnedVideo)"
                    class="pinned-video-img w-[246px] h-[145px] rounded-2xl" :src="pinnedVideo.currentSrc" alt="">
                <button
                    class="w-[40px] h-[18px] bg-black text-white font-medium text-xs absolute right-2 bottom-1 rounded-md">
                    {{ pinnedVideo.duration }}
                </button>
            </a>
            <div class="flex flex-col ml-4 mt-2">
                <a href="#" class="text-lg font-normal">{{ pinnedVideo.title }}</a>
                <div class="flex flex-row gap-x-2" style="font-size: 12px; font-weight: 400; color: #69696a;">
                    <a href="#">{{ pinnedVideo.channel_name }}</a>
                    <span>{{ pinnedVideo.views }} views</span>
                    <span>{{ pinnedVideo.created_at }}</span>
                </div>
                <p style="margin-top: 5px; font-size: 12px; font-weight: 400; color: #69696a;">{{
                    pinnedVideo.description }}</p>
            </div>
        </div>
    </div>
</template>