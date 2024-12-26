<script setup>
import { ref, reactive, onMounted } from 'vue';
import PacmanLoader from 'vue-spinner/src/PacmanLoader.vue';


const isPlaylistSortOpen = ref(false)
const togglePlaylistSort = () => isPlaylistSortOpen.value = !isPlaylistSortOpen.value

// Handle infinite scrolling
let page = ref(1)
let isLoading = ref(false)
const playlists = reactive([])

const generateTestPlaylists = (page_number) => {
    for (let i = page_number * 10 - 9; i <= page_number * 10; i++) {
        playlists.push({ id: i, title: `${i} Playlist title` })
    }
}

const scrollMore = () => {
    isLoading.value = true
    setTimeout(() => {
        page.value += 1
        generateTestPlaylists(page.value)
        isLoading.value = false
    }, 2000)
}

const checkScroll = () => {
    const endOfPage = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 200
    if (endOfPage && !isLoading.value) {
        scrollMore()
    }
}

onMounted(() => {
    generateTestPlaylists(page.value);
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
                 flex flex-col rounded-xl font-normal text-sm pt-2">
                <router-link :to="'/channel-page/playlists?sortBy=latest'"
                    :class="[!$route.query.sortBy || $route.query.sortBy == 'latest' ? 'active' : '']"
                    class="w-[164px] h-[48px] flex flex-row justify-start items-center hover:bg-[#e5e5e5]">
                    <span class="pl-3">Date added (Newest)</span>
                </router-link>
                <router-link :to="'/channel-page/playlists?sortBy=oldest'"
                    :class="[$route.query.sortBy == 'oldest' ? 'active' : '']"
                    class="w-[164px] h-[48px] flex flex-row justify-start items-center hover:bg-[#e5e5e5]">
                    <span class="pl-3">Oldest</span>
                </router-link>
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