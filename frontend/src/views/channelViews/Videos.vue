<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import { sharedState } from '@/sharedState';

// Handling Infinite Scrolling

const router1 = useRoute()
const router2 = useRouter()

let total_pages = ref(null)
let videos = reactive([])
let page = 1
let size = 12
const isLoading = ref(false)
const currentSortBy = ref(null)

const retrieveVideos = (channelId, page, sortBy) => {
    isLoading.value = true
    axios.get(`${sharedState.websiteUrl}/channel/${channelId}/videos/`, {
        params: {
            page: page,
            size: size,
            sortBy: sortBy
        }
    }).then((response) => {
        if (response.status == 200) {
            if (!sortBy) {
                videos = [...videos, ...response.data.data]
            } else {
                Object.assign(videos, response.data.data)
            }
            total_pages.value = response.data.total_pages
        }
    }).catch((error) => console.log(error)).finally(() => isLoading.value = false)
}

const filterVideos = (channelId, sortBy) => {
    // When you sort the videos you go back to page 1
    currentSortBy.value = sortBy
    retrieveVideos(channelId, 1, sortBy)
}


const loadMore = () => {
    page += 1
}

const checkScroll = () => {
    const endOfPage = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 200
    if (endOfPage && !isLoading.value && page < total_pages.value) {
        loadMore()
    }
}


onMounted(() => {
    const channelId = router1.params.id
    retrieveVideos(channelId, page)
    document.addEventListener("scroll", checkScroll)
})
</script>

<template>
    <div id="videosDivision">
        <div class="flex flex-col mt-4">
            <div class="flex flex-row">
                <button @click="filterVideos($route.params.id, 'latest')"
                    :class="[!currentSortBy || currentSortBy === 'latest' ? 'active' : '', 'w-[63px]', 'h-[32px]']">Latest</button>
                <button @click="filterVideos($route.params.id, 'popular')"
                    :class="[currentSortBy === 'popular' ? 'active' : '', 'w-[63px]', 'h-[32px]']">Popular</button>
                <button @click="filterVideos($route.params.id, 'oldest')"
                    :class="[currentSortBy === 'oldest' ? 'active' : '', 'w-[63px]', 'h-[32px]']">Oldest</button>
            </div>
            <div id="infinite-scroll-division" class="flex flex-row flex-wrap mt-4 gap-x-4 gap-y-8">
                <div v-for="video in videos" :key="video.unique_id" class="flex flex-col">
                    <div class="relative">
                        <img loading="lazy" class="w-[251px] h-[141px] rounded-2xl" :src="video.thumbnail_url" alt="">
                        <span class="bg-opacity-80 w-10 h-4 rounded-md absolute bottom-2 right-2 font-medium text-xs bg-black
                         text-white flex justify-center items-center">
                            {{ video.duration }}
                        </span>
                    </div>
                    <router-link :to="`/video/${video.unique_id}`">
                        <p class="text-sm font-medium mt-3 mb-2">
                            {{ video.title }}
                        </p>
                    </router-link>
                    <div class="flex flex-row text-xs font-normal text-gray-600">
                        <span>1.2M views&nbsp;</span>
                        <span>{{ video.created_at }}&nbsp;</span>
                    </div>
                </div>
            </div>
            <PulseLoader v-if="isLoading" color="red" class="mt-10 mb-5" draggable="false"></PulseLoader>
        </div>
    </div>
</template>