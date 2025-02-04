<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import PacmanLoader from 'vue-spinner/src/PacmanLoader.vue';
import { sharedState } from '@/sharedState';

const router = useRoute()

const isPlaylistSortOpen = ref(false)
const togglePlaylistSort = () => isPlaylistSortOpen.value = !isPlaylistSortOpen.value

// Handle infinite scrolling
let page = 1
let size = 12
let isLoading = ref(false)
let playlists = reactive([])
let total_pages = ref(0)

const retrievePlaylists = (channelId, page, sortBy) => {
    isLoading.value = true
    axios.get(`${sharedState.websiteUrl}/channel/${channelId}/playlists/`, {
        params: {
            page: page,
            size: size,
            sortBy: sortBy ?? null
        }
    }).then((response) => {
        if (response.status == 200) {
            if (!sortBy) {
                playlists = [...playlists, ...response.data.data]
            } else {
                Object.assign(playlists, response.data.data)
            }
            total_pages.value = response.data.total_pages
        }
    }).catch((error) => console.log(error)).finally(() => isLoading.value = false)
}


const scrollMore = () => {

}
const checkScroll = () => {
    const endOfPage = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 200
    if (endOfPage && !isLoading.value) {
        scrollMore()
    }
}

const filterPlaylists = (channelId, sortBy) => {
    retrievePlaylists(channelId, 1, sortBy);
}

onMounted(() => {
    const channelId = router.params.id
    retrievePlaylists(channelId, page)

    document.addEventListener("scroll", checkScroll);
})
</script>

<template>
    <div id="playlistsDivision">
        <div class="flex flex-row mt-7 relative">
            <span class="text-base font-normal left-0">Created playlists</span>
            <button @click="togglePlaylistSort" class="playlistSortingToggle flex flex-row absolute right-0">
                <img class="w-6 h-6" src="@/assets/icons/svg-icons/filter-filtering-icon.svg" alt="">
                <span class="ml-2">Sort by</span>
            </button>
            <div v-if="isPlaylistSortOpen" class="playlistSortingDiv my-shadow absolute right-0 top-10 w-[164px] h-[112px]
                 flex flex-col rounded-xl font-normal text-sm pt-2 bg-white">
                <button @click="filterPlaylists($route.params.id, 'latest')"
                    :class="[!$route.query.sortBy || $route.query.sortBy == 'latest' ? 'active' : '']"
                    class="w-[164px] h-[48px] flex flex-row justify-start items-center hover:bg-[#e5e5e5]">
                    <span class="pl-3">Date added (Newest)</span>
                </button>
                <button @click="filterPlaylists($route.params.id, 'oldest')"
                    :class="[$route.query.sortBy == 'oldest' ? 'active' : '']"
                    class="w-[164px] h-[48px] flex flex-row justify-start items-center hover:bg-[#e5e5e5]">
                    <span class="pl-3">Oldest</span>
                </button>
            </div>
        </div>

        <div class="flex flex-row flex-wrap mt-4 gap-x-1 gap-y-6">
            <div v-for="playlist in playlists" :key="playlist.id" class="cursor-pointer">
                <a href="#" class="flex flex-col">
                    <img class="w-[210px] h-[118px] rounded-2xl" src="@/assets/img/Django.png" alt="">
                    <p class="text-sm font-medium mt-2 mb-2">
                        {{ playlist.title }}
                    </p>
                    <span class="text-sm font-normal text-gray-600">View full playlist</span>
                </a>
            </div>
        </div>
        <div class="flex justify-center items-center my-6">
            <PacmanLoader v-if="isLoading" color="red"></PacmanLoader>
        </div>
    </div>
</template>