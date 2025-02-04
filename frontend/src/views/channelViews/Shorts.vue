<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import { sharedState } from '@/sharedState';

const router1 = useRoute()
const router2 = useRouter()

let shorts = reactive([])
let page = 1
let size = 12
let total_pages = ref(null)
const isLoading = ref(false)
const currentSortBy = ref(null)

const retrieveVideos = (channelId, page, sortBy) => {
    isLoading.value = true
    axios.get(`${sharedState.websiteUrl}/channel/${channelId}/shorts/`, {
        params: {
            page: page,
            size: size,
            sortBy: sortBy
        }
    }).then((response) => {
        if (response.status == 200) {
            if (!sortBy) {
                shorts = [...shorts, ...response.data.data]
            } else {
                Object.assign(shorts, response.data.data)
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
    <div id="shortsDivision">
        <div class="flex flex-col mt-4">
            <div class="flex flex-row">
                <button @click="filterVideos($route.params.id, 'latest')"
                    :class="[!currentSortBy || currentSortBy === 'latest' ? 'active' : '', 'w-[63px]', 'h-[32px]']">Latest</button>
                <button @click="filterVideos($route.params.id, 'popular')"
                    :class="[currentSortBy === 'popular' ? 'active' : '', 'w-[63px]', 'h-[32px]']">Popular</button>
                <button @click="filterVideos($route.params.id, 'oldest')"
                    :class="[currentSortBy === 'oldest' ? 'active' : '', 'w-[63px]', 'h-[32px]']">Oldest</button>
            </div>
            <div class="flex flex-row flex-wrap mt-4 gap-y-5 gap-x-2 w-[1100px]">
                <div v-for="short in shorts" :key="short.unique_id" class="flex flex-col">
                    <img class="w-[209.98px] h-[372.37px] rounded-2xl" :src="short.thumbnail_url" alt="">
                    <router-link :to="`/short/${video.unique_id}`">
                        <p class="text-sm font-medium mt-3 mb-2">
                            {{ video.title }}
                        </p>
                    </router-link>
                    <span class="text-sm font-normal text-gray-600">73K views&nbsp;</span>
                </div>
                <div v-if="shorts == null" class="w-full h-full flex justify-center items-center">
                    <p class="text-[14px] font-normal">This channel dont have any short videos</p>
                </div>
            </div>
            <PulseLoader v-if="isLoading" color="red" class="mt-10"></PulseLoader>
        </div>
    </div>
</template>