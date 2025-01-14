<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue';
import { useToast } from 'vue-toastification';
import { useRoute, useRouter } from 'vue-router';
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue';
import axios from 'axios';

const toast = useToast();
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

const playlistInfo = reactive([])
const retrievePlaylist = (playlistId, filter) => {
    isLoading.value = true
    axios.get(`http://127.0.0.1:8000/playlist/${playlistId}`, {
        params: {
            filter: filter
        }
    }).then((response) => {
        if (response.status == 200) {
            Object.assign(playlistInfo, response.data.data)
        }
    }).catch((error) => console.log(error)).finally(() => isLoading.value = false)
}

const currentFilter = ref('all')
const filterPlaylist = (playlistId, filter) => {
    currentFilter.value = filter
    retrievePlaylist(playlistId, currentFilter.value)

}


onMounted(() => {
    const playlistId = router.params.id
    if (playlistId) {
        retrievePlaylist(playlistId, currentFilter.value)
    }

    document.addEventListener("scroll", checkScroll)
})
</script>

<template>
    <div class="flex flex-row font-roboto">
        <div class="w-[360px] h-[650px] ml-[240px] mt-[55px] flex flex-col bg-[#967b69] bg-opacity-80
         pt-5 pl-5 rounded-2xl">
            <img class="w-[312px] h-[175px] rounded-2xl" :src="playlistInfo.last_video_thumbnail" alt="">
            <p class="text-[28px] font-bold mt-3 text-white">Liked
                videos</p>
            <p class="text-sm font-medium mt-4 text-white">{{ playlistInfo.username }}</p>
            <p class="text-gray-700 text-[12px] mt-2">{{ playlistInfo.total_videos }} videos</p>
            <div class="flex flex-row mt-6 gap-x-2 ml-1">
                <button class="w-[152px] h-[36px] flex flex-row justify-center items-center
                 bg-white rounded-2xl hover:bg-[#e6e6e6]">
                    <img class="w-[40px] h-[20px] ml-[-10px]" src="@/assets/icons/svg-icons/play-icon.svg" alt="">
                    <p class="text-sm font-medium">Play all</p>
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
                <button @click="filterPlaylist($route.params.id, 'all')"
                    :class="[currentFilter === 'all' ? 'active' : '']"
                    class="w-[40px] h-[32px] rounded-xl font-medium text-sm bg-[#f2f2f2] hover:bg-[#e5e5e5]">All</button>
                <button @click="filterPlaylist($route.params.id, 'videos')"
                    :class="[currentFilter === 'videos' ? 'active' : '']"
                    class="w-[67.5px] h-[32px] rounded-xl font-medium text-sm bg-[#f2f2f2] hover:bg-[#e5e5e5]">Videos</button>
                <button @click="filterPlaylist($route.params.id, 'shorts')"
                    :class="[currentFilter === 'shorts' ? 'active' : '']"
                    class="w-[67.5px] h-[32px] rounded-xl font-medium text-sm bg-[#f2f2f2] hover:bg-[#e5e5e5]">Shorts</button>
            </div>

            <div v-if="!isLoading" class="content-section">
                <div v-for="(video, index) in playlistInfo.videos" :key="index" class="z-auto pl-4 h-[129px] w-[827px] flex flex-row items-center
                 ml-[-36px] mt-4 gap-x-4 hover:bg-[#f2f2f2] hover:z-auto rounded-lg relative">
                    <a href="#" class="w-full h-full flex items-center">
                        <p class="text-[#796966] font-medium text-sm justify-self-start ml-[-5px]">{{ index + 1 }}</p>
                        <img class="w-[200px] h-[113px] rounded-lg ml-4" :src="video.thumbnail_url" alt="">
                        <div class="flex flex-col mt-[-67px] relative ml-4">
                            <router-link :to="`/video/${video.unique_id}`">
                                <p class="font-medium text-base mt-2 mb-2">{{ video.title }}</p>
                            </router-link>
                            <div class="flex flex-row text-[#898f90] text-xs font-normal">
                                <p class="hover:text-[#182c61]">{{ video.channel_name }} .&nbsp;</p>
                                <p class="hover:text-[#182c61]">25K views .&nbsp;</p>
                                <p class="hover:text-[#182c61]">{{ video.created_at }} days ago</p>
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
            <div v-else class="my-20 mx-auto flex justify-center items-center">
                <ScaleLoader color="red"></ScaleLoader>
            </div>
        </div>
    </div>
</template>