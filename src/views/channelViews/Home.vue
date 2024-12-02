<script setup>
import { ref, reactive } from 'vue';
// Retrieving and assigning the Videos
const pinnedVideo = reactive({
    title: "Django Tutorial",
    channel_name: "Channel Name",
    views: "1.1M views",
    created_at: "2 years ago",
    description: "asdfasdfasdfadsf",
    duration: "12:29",
})


const regularVideos = []
for (let i = 0; i < 15; i++) {
    regularVideos.push({ title: `Regular Videos ${i + 1}`, created_at: `${i + 1} days ago` })
}


const popularVideos = []
for (let i = 0; i < 15; i++) {
    popularVideos.push({ title: `Popular Videos ${i + 1}`, created_at: `${i + 1} days ago` })
}


const famousPlaylistVideos1 = []
for (let i = 0; i < 15; i++) {
    famousPlaylistVideos1.push({ title: `Famous Playlist Videos 1 ${i + 1}`, created_at: `${i + 1} days ago` })
}


const famousPlaylistVideos2 = []
for (let i = 0; i < 15; i++) {
    famousPlaylistVideos2.push({ title: `Famous Playlist Videos 2 ${i + 1}`, created_at: `${i + 1} days ago` })
}

const updateSliderButtons = (container_id) => {
    const sliderContainer = document.getElementById(container_id)
    const prevButton = document.querySelector(`#${container_id}-prev-btn`)
    const nextButton = document.querySelector(`#${container_id}-next-btn`)
    const nextSlideCondition = sliderContainer.scrollLeft >= sliderContainer.scrollWidth - sliderContainer.clientWidth - 100

    prevButton.style.visibility = sliderContainer.scrollLeft <= 50 ? "hidden" : "visible";
    nextButton.style.visibility = nextSlideCondition ? "hidden" : "visible";
}

const VideosContainerSliding = (container_id, direction) => {
    let slideAmount = 300;
    const sliderContainer = document.getElementById(container_id)
    sliderContainer.scrollLeft += direction === "prev" ? -slideAmount : slideAmount
    updateSliderButtons(container_id);
}
</script>

<template>
    <div class="flex flex-col" id="homeDivision">
        <div class="flex flex-row mt-6 border-b-[1px] pb-6">
            <a href="#" class="relative">
                <img class="w-[246px] h-[138px] rounded-2xl" src="@/assets/img/Django.png" alt="">
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
        <div class="flex flex-col mt-4 relative border-b-[1px]">
            <span class="font-bold text-xl mb-4">Videos</span>
            <button @click="VideosContainerSliding('slider1', 'prev')" id="slider1-prev-btn"
                class="invisible w-9 h-9 absolute top-[91px] left-[-20px] z-20 shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-left-icon.svg" alt="">
            </button>
            <div id="slider1" class="flex flex-row h-[204px] max-w-[1284px] gap-x-1 overflow-x-auto"
                style="scrollbar-width: thin;">
                <div v-for="(video, index) in regularVideos" :key="index" class="grow-0 shrink-0 basis-auto">
                    <a href="" class="flex flex-col gap-y-2">
                        <img class="w-[210px] h-[118px] rounded-lg" src="@/assets/img/Django.png" alt="">
                        <a href="#" class="text-sm font-medium text-black">{{ video.title }}</a>
                        <div class="flex flex-row text-xs font-normal text-[#69696a]">
                            <span>73K views&nbsp;</span>
                            <span>{{ video.created_at }}</span>
                        </div>
                    </a>
                </div>
            </div>
            <button @click="VideosContainerSliding('slider1', 'next')" id="slider1-next-btn"
                class="w-9 h-9 absolute top-[91px] right-[-18px] shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-right-icon.svg" alt="">
            </button>
        </div>
        <div class="flex flex-col mt-4 relative border-b-[1px]">
            <span class="font-bold text-xl mb-4">Popular Videos</span>
            <button @click="VideosContainerSliding('slider2', 'prev')" id="slider2-prev-btn"
                class="invisible w-9 h-9 absolute top-[91px] left-[-20px] z-2 shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-left-icon.svg" alt="">
            </button>
            <div id="slider2" class="flex flex-row h-[204px] max-w-[1284px] gap-x-1 overflow-hidden">
                <div v-for="(video, index) in popularVideos" :key="index" class="grow-0 shrink-0 basis-auto">
                    <a href="" class="flex flex-col gap-y-2">
                        <img class="w-[210px] h-[118px] rounded-lg" src="@/assets/img/Django.png" alt="">
                        <a href="#" class="text-sm font-medium text-black">{{ video.title }}</a>
                        <div class="flex flex-row text-xs font-normal text-[#69696a]">
                            <span>73K views&nbsp;</span>
                            <span>{{ video.created_at }}</span>
                        </div>
                    </a>
                </div>
            </div>
            <button @click="VideosContainerSliding('slider2', 'next')" id="slider2-next-btn"
                class="w-9 h-9 absolute top-[91px] right-[-18px] shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-right-icon.svg" alt="">
            </button>
        </div>
        <div class="flex flex-col mt-4 relative border-b-[1px]">
            <span class="font-bold text-xl mb-4">Famous playlist Videos 1 (maximum 15 videos)</span>
            <a href="#"
                class="w-[103px] h-[36px] rounded-3xl flex justify-center items-center gap-x-2 hover:bg-[#e5e5e5]">
                <img class="w-4 h-4" src="@/assets/icons/svg-icons/play-icon.svg" alt="">
                <span class="font-medium text-sm">Play all</span>
            </a>
            <button @click="VideosContainerSliding('slider3', 'prev')" id="slider3-prev-btn"
                class="invisible w-9 h-9 absolute top-[122px] left-[-20px] z-20 shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-left-icon.svg" alt="">
            </button>
            <div id="slider3" class="flex flex-row h-[204px] max-w-[1284px] gap-x-1 overflow-hidden">
                <div v-for="(video, index) in famousPlaylistVideos1" :key="index" class="grow-0 shrink-0 basis-auto">
                    <a href="" class="flex flex-col gap-y-2">
                        <img class="w-[210px] h-[118px] rounded-lg" src="@/assets/img/Django.png" alt="">
                        <a href="#" class="text-sm font-medium text-black">{{ video.title }}</a>
                        <div class="flex flex-row text-xs font-normal text-[#69696a]">
                            <span>73K views&nbsp;</span>
                            <span>{{ video.created_at }}</span>
                        </div>
                    </a>
                </div>
            </div>
            <button @click="VideosContainerSliding('slider3', 'next')" id="slider3-next-btn"
                class="w-9 h-9 absolute top-[122px] right-[-18px] shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-right-icon.svg" alt="">
            </button>
        </div>
        <div class="flex flex-col mt-4 relative border-b-[1px]">
            <span class="font-bold text-xl mb-4">Famous playlist Videos 2 (maximum 15 videos)</span>
            <a href="#"
                class="w-[103px] h-[36px] rounded-3xl flex justify-center items-center gap-x-2 hover:bg-[#e5e5e5]">
                <img class="w-4 h-4" src="@/assets/icons/svg-icons/play-icon.svg" alt="">
                <span class="font-medium text-sm">Play all</span>
            </a>
            <button @click="VideosContainerSliding('slider4', 'prev')" id="slider4-prev-btn"
                class="invisible w-9 h-9 absolute top-[122px] left-[-20px] z-50 shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-left-icon.svg" alt="">
            </button>
            <div id="slider4" class="flex flex-row h-[204px] max-w-[1284px] gap-x-1 overflow-hidden">
                <div v-for="(video, index) in famousPlaylistVideos2" :key="index" class="grow-0 shrink-0 basis-auto">
                    <a href="" class="flex flex-col gap-y-2">
                        <img class="w-[210px] h-[118px] rounded-lg" src="@/assets/img/Django.png" alt="">
                        <a href="#" class="text-sm font-medium text-black">{{ video.title }}</a>
                        <div class="flex flex-row text-xs font-normal text-[#69696a]">
                            <span>73K views&nbsp;</span>
                            <span>{{ video.created_at }}</span>
                        </div>
                    </a>
                </div>
            </div>
            <button @click="VideosContainerSliding('slider4', 'next')" id="slider4-next-btn"
                class="w-9 h-9 absolute top-[122px] right-[-18px] shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-right-icon.svg" alt="">
            </button>
        </div>
    </div>
</template>