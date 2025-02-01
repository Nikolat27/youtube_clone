<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import { useRoute } from 'vue-router';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';

import { sharedState } from '@/sharedState';
import kebabMenuSrc from '@/assets/icons/svg-icons/kebab-menu.svg'
import djangoIcon from '@/assets/img/Django.png'

const isKebabMenuOpen = ref(false)
const toggleKebabMenu = () => {
    isKebabMenuOpen.value = !isKebabMenuOpen.value
}

const router = useRoute()
const toast = useToast()
const videos = reactive([])
const isLoading = ref(false)
let size = 5

const retrieveSearchVideos = async (searchQuery) => {
    isLoading.value = true
    await axios.get("http://127.0.0.1:8000/videos/search", {
        params: {
            "query": searchQuery,
            "size": size
        }
    }).then((response) => {
        if (response.status == 200) {
            Object.assign(videos, response.data.data)
        }
    }).catch((error) => toast.error(error)).finally(() => {
        isLoading.value = false
    })
}

const downloadVideo = (videoId) => {
    axios.get(`http://127.0.0.1:8000/videos/download/${videoId}`).then((response) => {
        console.log(response.data.data)
    }).catch((error) => console.log(error))
}

const isSideBarCollapsed = ref(false)
watch(() => sharedState.isWebsiteSideBarCollapsed, (newVal) => {
    isSideBarCollapsed.value = newVal
})
const containerLeftPositionStyles = computed(() => {
    if (isSideBarCollapsed.value && !isSideBarClosed.value) {
        return '85px'
    } else if (!isSideBarCollapsed.value && !isSideBarClosed.value) {
        return '230px'
    } else if (isSideBarClosed.value) {
        return '8px'
    }
})


watch(() => router.query.query, () => {
    const searchQuery = router.query.query
    if (searchQuery) {
        retrieveSearchVideos(searchQuery)
    }
})


const isSideBarClosed = ref(false)
const resizeHandle = () => {
    const windowWidth = window.innerWidth
    if (windowWidth > 650) {
        sharedState.isWebsiteSideBarCollapsed = false
        sharedState.isWebsiteSideBarClosed = false
        isSideBarClosed.value = false
    } else if (windowWidth >= 553 && windowWidth <= 650) {
        sharedState.isWebsiteSideBarCollapsed = true
        sharedState.isWebsiteSideBarClosed = false
        isSideBarClosed.value = false
    } else if (windowWidth < 553) {
        sharedState.isWebsiteSideBarClosed = true
        isSideBarClosed.value = true
    }
}


onMounted(() => {
    resizeHandle()
    window.addEventListener("resize", resizeHandle)

    const searchQuery = router.query.query
    if (searchQuery) {
        retrieveSearchVideos(searchQuery)
    }
})
</script>
<template>
    <div v-if="!isLoading" class="flex flex-col w-full sm:w-[75%] gap-y-6 relative top-24 font-roboto"
        :style="{ left: containerLeftPositionStyles }">
        <div v-for="video in videos" :key="video.id" class="w-full h-[280px] flex flex-row">
            <router-link :to="`/video/${video.video_id}`"
                class="w-[40%] min-w-[240px] min-h-[130px] max-w-[500px] h-[281px]">
                <img loading="lazy" draggable="false" class="w-full h-full object-fit rounded-xl" :src="video.thumbnail"
                    alt="">
            </router-link>
            <div class="flex flex-col ml-4 w-[60%] gap-y-2">
                <div class="flex flex-row justify-start items-center">
                    <router-link @click="downloadVideo(video.video_id)" :to="`/video/${video.video_id}`">
                        <p class="text-[18px] font-normal">{{ video.title }}</p>
                    </router-link>
                    <div class="justify-self-end ml-auto mr-2 relative">
                        <button @click="toggleKebabMenu"
                            class="w-[40px] h-[40px] rounded-full hover:bg-[#e5e5e5] flex justify-center items-center">
                            <img class="w-[16px] h-[16px]" :src="kebabMenuSrc" alt="">
                        </button>
                        <div v-if="isKebabMenuOpen"
                            class="absolute flex flex-col w-[211px] h-auto rounded-xl top-10 right-0 py-4 bg-white z-20 custom-shadow-inset">
                            <div
                                class="w-[211px] h-[36px] flex flex-row justify-start items-center pl-4 hover:bg-[#e5e5e5]">
                                <img src="" alt="">
                                <p>Save to Watch later</p>
                            </div>
                            <div
                                class="w-[211px] h-[36px] flex flex-row justify-start items-center pl-4 hover:bg-[#e5e5e5]">
                                <img src="" alt="">
                                <p>Save to playlist</p>
                            </div>
                            <div
                                class="w-[211px] h-[36px] flex flex-row justify-start items-center pl-4 hover:bg-[#e5e5e5]">
                                <img src="" alt="">
                                <p>Share</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="text-gray-600 text-[12px] font-normal">
                    <span>{{ video.views ?? 0 }} views&nbsp;</span>.<span>&nbsp;{{ video.published_date }}</span>
                </div>
                <div
                    class="cursor-pointer flex flex-row gap-x-2 text-gray-600 text-[12px] font-normal justify-start items-center">
                    <img class="w-[24px] h-[24px] rounded-full" :src="djangoIcon" alt="">
                    <span>{{ video.channel }}</span>
                </div>
                <div class="metadata text-gray-600 text-[12px] font-normal mt-2 flex flex-row gap-x-1">
                    <p>{{ video.description }}</p>
                </div>
            </div>
        </div>
    </div>
    <div v-else class="relative top-[300px] left-[40px]">
        <PulseLoader color="red" size="25px"></PulseLoader>
    </div>
</template>
<style scoped>
.custom-shadow-inset {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
}
</style>