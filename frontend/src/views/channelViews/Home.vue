<script setup>
import { ref, reactive } from 'vue';

// Factory function to create video objects
const createVideo = (title, index) => ({
    title,
    created_at: `${index + 1} days ago`,
    currentSrc: '/src/assets/img/Django.png',
    thumbnail: '/src/assets/img/Django.png',
    gif: "/src/assets/img/gif-image1.webp",
});

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

// Generate video arrays
const generateVideos = (prefix) => Array.from({ length: 15 }, (_, index) => createVideo(`${prefix} ${index + 1}`, index));

// Video arrays
const regularVideos = reactive(generateVideos('Regular Videos'));
const popularVideos = reactive(generateVideos('Popular Videos'));
const famousPlaylistVideos1 = reactive(generateVideos('Famous Playlist Videos 1'));
const famousPlaylistVideos2 = reactive(generateVideos('Famous Playlist Videos 2'));

// Slider Functions
const updateSliderButtons = (container_id) => {
    const sliderContainer = document.getElementById(container_id);
    const prevButton = document.querySelector(`#${container_id}-prev-btn`);
    const nextButton = document.querySelector(`#${container_id}-next-btn`);
    const nextSlideCondition = sliderContainer.scrollLeft >= sliderContainer.scrollWidth - sliderContainer.clientWidth - 100;

    prevButton.style.visibility = sliderContainer.scrollLeft <= 50 ? "hidden" : "visible";
    nextButton.style.visibility = nextSlideCondition ? "hidden" : "visible";
};

const slideVideos = (container_id, direction) => {
    // container_id is sliderId
    const sliderContainer = document.getElementById(container_id);
    const slideAmount = 300;
    sliderContainer.scrollLeft += direction === "prev" ? -slideAmount : slideAmount;
    updateSliderButtons(container_id);
};

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

// Reusable Slider Component (to be used in template)
const VideoSlider = {
    props: ['videos', 'sliderId', 'title', 'hoverImage', 'resetImage'],
    // $emit = first we pass the function which is for our even handling, then the arguments (in order)
    template: `
        <div class="flex flex-col mt-4 relative border-b-[1px]">
            <span class="font-bold text-xl mb-4">{{ title }}</span>
            <button @click="$emit('slide', sliderId, 'prev')" :id="\`\${sliderId}-prev-btn\`" class="invisible w-9 h-9 absolute top-[91px] left-[-20px] z-20 shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                <img class="w-[100%] h-[100%]" src="/src/assets/icons/svg-icons/thin-chevron-round-left-icon.svg" alt="Previous">
            </button>
            <div :id="sliderId" class="flex flex-row h-[204px] max-w-[1284px] gap-x-1 overflow-hidden">
                <div v-for="(video, index) in videos" :key="index" class="grow-0 shrink-0 basis-auto">
                    <a href="#" class="flex flex-col gap-y-2">
                        <img @mouseover="hoverImage(video)" @mouseleave="resetImage(video)" class="w-[210px] h-[118px] rounded-lg" :src="video.currentSrc" alt="">
                        <a href="#" class="text-sm font-medium text-black">{{ video.title }}</a>
                        <div class="flex flex-row text-xs font-normal text-[#69696a]">
                            <span>73K views&nbsp;</span>
                            <span>{{ video.created_at }}</span>
                        </div>
                    </a>
                </div>
            </div>
            <button @click="$emit('slide', sliderId, 'next')" :id="\`\${sliderId}-next-btn\`" class="w-9 h-9 absolute top-[91px] right-[-18px] shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                <img class="w-[100%] h-[100%]" src="/src/assets/icons/svg-icons/thin-chevron-round-right-icon.svg" alt="Next">
            </button>
        </div>
    `
};
</script>

<template>
    <div class="flex flex-col" id="homeDivision">
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

        <!-- Video Sliders -->
        <VideoSlider :videos="regularVideos" sliderId="slider1" title="Videos" @slide="slideVideos"
            :hoverImage="hoverImage" :resetImage="resetImage" />
        <VideoSlider :videos="popularVideos" sliderId="slider2" title="Popular Videos" @slide="slideVideos"
            :hoverImage="hoverImage" :resetImage="resetImage" />
        <VideoSlider :videos="famousPlaylistVideos1" sliderId="slider3" title="Famous Playlist Videos 1"
            @slide="slideVideos" :hoverImage="hoverImage" :resetImage="resetImage" />
        <VideoSlider :videos="famousPlaylistVideos2" sliderId="slider4" title="Famous Playlist Videos 2"
            @slide="slideVideos" :hoverImage="hoverImage" :resetImage="resetImage" />
    </div>
</template>
