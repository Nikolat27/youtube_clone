<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue';

const router = useRoute();
const router2 = useRouter();

const isVideoOptionsOpen = ref([])
const toggleVideoOptions = (video_id) => {
    if (!isVideoOptionsOpen.value.includes(video_id)) {
        isVideoOptionsOpen.value.pop()
        isVideoOptionsOpen.value.push(video_id)
    } else {
        isVideoOptionsOpen.value.pop()
    }
}


const isShortVideoOptionsOpen = ref([])
const toggleShortVideoOptions = (short_id) => {
    if (!isShortVideoOptionsOpen.value.includes(short_id)) {
        isShortVideoOptionsOpen.value.pop()
        isShortVideoOptionsOpen.value.push(short_id)
    } else {
        isShortVideoOptionsOpen.value.pop()
    }
}

let page = ref(1)
let isLoading = ref(false)
const totalItemsShown = { all: 20, videos: 20, shorts: 12 }
const videosData = reactive({
    all: [],
    videos: [],
    shorts: [],
})

const generateTestData = (type, page_number) => {
    const totalItem = totalItemsShown[type]
    let startIndex = page_number * totalItem - (totalItem - 1)
    let lastIndex = page_number * totalItem
    for (let i = startIndex; i <= lastIndex; i++) {
        if (type === 'all') {
            videosData.all.push({ id: i, title: `All Video title` })
        } else if (type === 'videos') {
            videosData.videos.push({ id: i, title: `Regular Video title` })
        } else if (type === 'shorts') {
            videosData.shorts.push({ id: i, title: `Short Video title` })
        }

    }
}


// Generating Test videos for 'all, videos and shorts'
// const all_videos = reactive([])
// const generateTestAllVideos = (page_number) => {
//     let totalItemShown = 20
//     // Minus 1 for starting from the index 1
//     let startIndex = page_number * totalItemShown - (totalItemShown - 1)
//     let lastIndex = page_number * totalItemShown

//     for (let i = startIndex; i <= lastIndex; i++) {
//         if (i % 2 == 0) {
//             all_videos.push({ id: i, title: `${i} Regular Video title` })
//         } else {
//             all_videos.push({ id: i, title: `${i} Short Video title` })
//         }
//     }
// }

// const videos = reactive([])
// const generateTestVideos = (page_number) => {
//     let totalItemShown = 20
//     // Minus 1 for starting from the index 1
//     let startIndex = page_number * totalItemShown - (totalItemShown - 1)
//     let lastIndex = page_number * totalItemShown
//     for (let i = startIndex; i <= lastIndex; i++) {
//         videos.push({ id: i, title: `${i} Video title` })
//     }
// }

// const shorts = reactive([])
// const generateTestShorts = (page_number) => {
//     let totalItemShown = 12
//     // Minus 1 for starting from the index 1
//     let startIndex = page_number * totalItemShown - (totalItemShown - 1)
//     let lastIndex = page_number * totalItemShown
//     for (let i = startIndex; i <= lastIndex; i++) {
//         shorts.push({ id: i, title: `${i} Short Video title` })
//     }
// }

// Handle infinite scrolling
const scrollMore = (type) => {
    isLoading.value = true
    setTimeout(() => {
        page.value += 1
        generateTestData(type, page.value)
        isLoading.value = false
    }, 1500)
}

const checkScroll = () => {
    const endOfPage = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 200
    if (endOfPage && !isLoading.value) {
        scrollMore(router.query.type || 'all')
    }
}


// Handle filtering
watch(() => router.query.type, () => {
    page.value = 1
    videosData.all = [] // Reset data on type change
    videosData.videos = []
    videosData.shorts = []
    generateTestData(router.query.type || 'all', page.value)
})

onMounted(() => {
    document.addEventListener("scroll", checkScroll)
    generateTestData(router.query.type || 'all', page.value) // Default 'type' handling
})
</script>

<template>
    <div class="flex flex-row">
        <div class="w-[360px] h-[650px] ml-[240px] mt-[55px] flex flex-col bg-[#846957] bg-opacity-80
         pt-5 pl-5 rounded-2xl">
            <img class="w-[312px] h-[175px] rounded-2xl" src="@/assets/img/Django.png" alt="">
            <p class="text-[28px] font-bold mt-3 text-white" style="font-family: 'YouTube Sans', sans-serif;">Liked
                videos</p>
            <p class="text-sm font-medium mt-4 text-white">Username</p>
            <p class="text-gray-700 text-xs mt-2">625 videos</p>
            <div class="flex flex-row mt-6 gap-x-2 ml-1">
                <button class="w-[152px] h-[36px] flex flex-row justify-center items-center
                 bg-white rounded-2xl hover:bg-[#e6e6e6]">
                    <img class="w-[40px] h-[20px] ml-[-10px]" src="@/assets/icons/svg-icons/play-icon.svg" alt="">
                    <p class="text-sm font-medium">Play&nbsp;all</p>
                </button>
                <button
                    class="w-[152px] h-[36px] flex flex-row justify-center items-center bg-[#766d65] bg-opacity-65 rounded-2xl">
                    <img class="w-[40px] h-[20px] ml-[-20px]" src="@/assets/icons/svg-icons/shuffle-icon.svg" alt="">
                    <p class="text-sm font-medium text-white">Shuffle</p>
                </button>
            </div>
        </div>
        <div class="w-[891px] flex flex-col mt-14 ml-10">
            <div class="flex flex-row liked-videos-buttons gap-x-2">
                <router-link to="/playlist?type=all"><button
                        :class="[!$route.query.type || $route.query.type === 'all' ? 'active' : '']"
                        class="w-[40px] h-[32px] rounded-xl font-medium text-sm bg-[#f2f2f2] hover:bg-[#e5e5e5]">All</button></router-link>
                <router-link to="/playlist?type=videos"><button
                        :class="[$route.query.type === 'videos' ? 'active' : '']"
                        class="w-[67.5px] h-[32px] rounded-xl font-medium text-sm bg-[#f2f2f2] hover:bg-[#e5e5e5]">Videos</button></router-link>
                <router-link to="/playlist?type=shorts"><button
                        :class="[$route.query.type === 'shorts' ? 'active' : '']"
                        class="w-[67.5px] h-[32px] rounded-xl font-medium text-sm bg-[#f2f2f2] hover:bg-[#e5e5e5]">Shorts</button></router-link>
            </div>

            <div v-if="!$route.query.type || $route.query.type === 'all'" id="all" class="content-section">
                <div v-for="video in videosData.all" :key="video.id" class="z-auto pl-4 h-[129px] w-[827px] flex flex-row items-center
                 ml-[-36px] mt-4 gap-x-4 hover:bg-[#f2f2f2] hover:z-auto rounded-lg relative">
                    <a href="#" class="w-full h-full flex items-center">
                        <p class="text-[#796966] font-medium text-sm justify-self-start ml-[-5px]">{{ video.id }}</p>
                        <img class="w-[200px] h-[113px] rounded-lg ml-4" src="@/assets/img/Django.png" alt="">
                        <div class="flex flex-col mt-[-67px] relative ml-4">
                            <p class="font-medium text-base mt-2 mb-2">{{ video.title }}</p>
                            <div class="flex flex-row text-[#898f90] text-xs font-normal">
                                <p class="hover:text-[#182c61]">Channel name .&nbsp;</p>
                                <p class="hover:text-[#182c61]">25K views .&nbsp;</p>
                                <p class="hover:text-[#182c61]">2 days ago</p>
                            </div>
                        </div>
                    </a>
                    <button @click="toggleVideoOptions(video.id)" class="absolute right-0 top-1/2 transform -translate-y-1/2 
                        w-10 h-10 rounded-full bg-transparent hover:bg-[#e5e5e5] flex justify-center items-center">
                        <img class="w-4 h-4" src="@/assets/icons/svg-icons/kebab-menu.svg" alt="">
                    </button>
                    <div v-if="isVideoOptionsOpen.includes(video.id)"
                        class="z-[100] bg-white rounded-lg flex flex-col w-[256.6px] h-[190px] absolute top-[85px] right-0 text-sm font-normal shadow-xl justify-center items-start">
                        <a href="#" class="flex flex-row h-[36px] gap-x-2 items-center hover:bg-[#e5e5e5] w-[256px]">
                            <img class="w-6 h-6 ml-4" src="@/assets/icons/svg-icons/clock-line-icon.svg" alt="">
                            <p>Save to watch later</p>
                        </a>
                        <a href="#" class="flex flex-row h-[36px] gap-x-2 items-center hover:bg-[#e5e5e5] w-[256px]">
                            <img class="w-6 h-6 ml-4" src="@/assets/icons/svg-icons/save-btn.svg" alt="">
                            <p>Save to playlist</p>
                        </a>
                        <a href="#" class="flex flex-row h-[36px] gap-x-2 items-center hover:bg-[#e5e5e5] w-[256px]">
                            <img class="w-6 h-6 ml-4" src="@/assets/icons/svg-icons/share-btn.svg" alt="">
                            <p>Share</p>
                        </a>
                        <hr style="width: 100%; border: 1px solid #ededed; margin: 10px 0;">
                        <a href="#" class="flex flex-row h-[36px] gap-x-2 items-center hover:bg-[#e5e5e5] w-[256px]">
                            <img class="w-6 h-6 ml-4" src="@/assets/icons/svg-icons/trash-can-icon.svg" alt="">
                            <p>Remove from Liked videos</p>
                        </a>
                    </div>
                </div>
            </div>

            <div v-if="$route.query.type === 'videos'" id="videos">
                <div v-for="video in videosData.videos" :key="video.id" class="z-auto pl-4 h-[129px] w-[827px] flex flex-row items-center
                 ml-[-36px] mt-4 gap-x-4 hover:bg-[#f2f2f2] hover:z-auto rounded-lg relative">
                    <a href="#" class="w-full h-full flex items-center">
                        <p class="text-[#796966] font-medium text-sm justify-self-start ml-[-5px]">{{ video.id }}</p>
                        <img class="w-[200px] h-[113px] rounded-lg ml-4" src="@/assets/img/Django.png" alt="">
                        <div class="flex flex-col mt-[-67px] relative ml-4">
                            <p class="font-medium text-base mt-2 mb-2">{{ video.title }}</p>
                            <div class="flex flex-row text-[#898f90] text-xs font-normal">
                                <p class="hover:text-[#182c61]">Channel name .&nbsp;</p>
                                <p class="hover:text-[#182c61]">25K views .&nbsp;</p>
                                <p class="hover:text-[#182c61]">2 days ago</p>
                            </div>
                        </div>
                    </a>
                    <button @click="toggleVideoOptions(video.id)" class="absolute right-0 top-1/2 transform -translate-y-1/2 
                        w-10 h-10 rounded-full bg-transparent hover:bg-[#e5e5e5] flex justify-center items-center">
                        <img class="w-4 h-4" src="@/assets/icons/svg-icons/kebab-menu.svg" alt="">
                    </button>
                    <div v-if="isVideoOptionsOpen.includes(video.id)"
                        class="z-[100] bg-white rounded-lg flex flex-col w-[256.6px] h-[190px] absolute top-[85px] right-0 text-sm font-normal shadow-xl justify-center items-start">
                        <a href="#" class="flex flex-row h-[36px] gap-x-2 items-center hover:bg-[#e5e5e5] w-[256px]">
                            <img class="w-6 h-6 ml-4" src="@/assets/icons/svg-icons/clock-line-icon.svg" alt="">
                            <p>Save to watch later</p>
                        </a>
                        <a href="#" class="flex flex-row h-[36px] gap-x-2 items-center hover:bg-[#e5e5e5] w-[256px]">
                            <img class="w-6 h-6 ml-4" src="@/assets/icons/svg-icons/save-btn.svg" alt="">
                            <p>Save to playlist</p>
                        </a>
                        <a href="#" class="flex flex-row h-[36px] gap-x-2 items-center hover:bg-[#e5e5e5] w-[256px]">
                            <img class="w-6 h-6 ml-4" src="@/assets/icons/svg-icons/share-btn.svg" alt="">
                            <p>Share</p>
                        </a>
                        <hr style="width: 100%; border: 1px solid #ededed; margin: 10px 0;">
                        <a href="#" class="flex flex-row h-[36px] gap-x-2 items-center hover:bg-[#e5e5e5] w-[256px]">
                            <img class="w-6 h-6 ml-4" src="@/assets/icons/svg-icons/trash-can-icon.svg" alt="">
                            <p>Remove from Liked videos</p>
                        </a>
                    </div>
                </div>
            </div>

            <div v-if="$route.query.type === 'shorts'" id="shorts" class="mt-6">
                <div id="shorts-container" class="flex flex-row flex-wrap gap-x-2 gap-y-8 min-h-[410px]">
                    <div v-for="short in videosData.shorts" :key="short.id"
                        class="short-video flex flex-col relative max-w-[200px] h-[400px] flex-grow-0 flex-shrink-0 basis-auto">
                        <a href="#" class="w-full">
                            <img class="w-[200px] h-[356px] rounded-lg" src="@/assets/img/Django.png" alt="">
                            <span class="text-base font-medium mt-2"
                                style="overflow-wrap: break-word; word-wrap: break-word;">
                                {{ short.title }}
                            </span>
                        </a>
                        <button @click="toggleShortVideoOptions(short.id)"
                            class="z-40 absolute right-0 bottom-0 w-9 h-9 rounded-full flex justify-center items-center">
                            <img class="w-4 h-4" src="@/assets/icons/svg-icons/kebab-menu.svg" alt="">
                        </button>
                        <div v-if="isShortVideoOptionsOpen.includes(short.id)" class="z-10 bg-white my-shadow rounded-2xl absolute bottom-12 left-0 flex flex-col
                         w-[256px] h-[150px] text-sm font-normal gap-y-1 pt-2 pb-2 justify-center">
                            <a class="pl-2 flex flex-row hover:bg-[#e5e5e5] cursor-pointer h-10
                             justify-start gap-x-1 items-center">
                                <img class="w-6 h-6 justify-start items-center"
                                    src="@/assets/icons/svg-icons/clock-line-icon.svg" alt="">
                                <p>Save to watch later</p>
                            </a>
                            <a class="pl-2 flex flex-row justify-start gap-x-1 items-center
                             hover:bg-[#e5e5e5] cursor-pointer h-10">
                                <img class="w-6 h-6" src="@/assets/icons/svg-icons/save-btn.svg" alt="">
                                <p>Save to playlist</p>
                            </a>
                            <a class="pl-2 flex flex-row gap-x-1 justify-start items-center
                             hover:bg-[#e5e5e5] cursor-pointer h-10">
                                <img class="w-6 h-6" src="@/assets/icons/svg-icons/trash-can-icon.svg" alt="">
                                <p>Remove from Liked videos</p>
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="isLoading" class="my-20 mx-auto flex justify-center items-center">
                <ScaleLoader color="red"></ScaleLoader>
            </div>
        </div>
    </div>
</template>