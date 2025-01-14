<script setup>
import { ref, onMounted, reactive, watch } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import { sharedState } from '@/sharedState';
import PlaylistCreation from '@/components/studio/video_creation/PlaylistCreation.vue';

const toast = useToast()
const router1 = useRoute()
const router2 = useRouter()

// Icons
import arrowDown from '/src/assets/icons/svg-icons/arrow-down-icon.svg'
import playIcon from '/src/assets/icons/video-player/play-icon.png'
import kebabMenuIcon from '/src/assets/icons/svg-icons/kebab-menu.svg'


const playlistOptionsOpen = reactive([])
const togglePlaylistOption = (playlistId) => {
    if (playlistOptionsOpen.includes(playlistId)) {
        playlistOptionsOpen.pop()
    } else {
        playlistOptionsOpen.pop()
        playlistOptionsOpen.push(playlistId)
    }
}

const playPlaylist = (playlistId) => {
    router2.push({ name: 'playlist-videos', params: { id: playlistId } })
}

const deletePlaylist = (playlistId) => {
    axios.delete(`http://127.0.0.1:8000/playlist/delete/${playlistId}`).then((response) => {
        if (response.status == 202) {
            const user_session_id = sessionStorage.getItem("user_session_id");
            retrievePlaylists(user_session_id, currentSortBy.value);
            toast.success(response.data.data);
        }
    }).catch(() => toast.error("Error!"))
}

watch(() => sharedState.refreshRetrievePlaylists, () => {
    playlistOptionsOpen.pop()
    const user_session_id = sessionStorage.getItem("user_session_id")
    retrievePlaylists(user_session_id, currentSortBy.value)
})

const openPlaylistCreation = (playlistId) => {
    sharedState.isPlaylistCreationOpen.open = true
    sharedState.isPlaylistCreationOpen.playlist_id = playlistId
}

const isFilterOpen = ref(false)
const isLoading = ref(false)
const toggleFilterOpening = () => {
    isFilterOpen.value = !isFilterOpen.value
}

const filterPlaylists = (sortBy) => {
    isFilterOpen.value = false
    retrievePlaylists(sessionStorage.getItem("user_session_id"), sortBy);
}

const currentSortBy = ref('latest')
let playlists = reactive([])
const retrievePlaylists = (user_session_id, sortBy) => {
    isLoading.value = true
    axios.get("http://127.0.0.1:8000/playlist/", {
        params: {
            user_session_id: user_session_id,
            sortBy: sortBy
        }
    }).then((response) => {
        if (response.status == 200) {
            playlists.length = 0; // Clear the array
            playlists.push(...response.data.data); // Add new data
            currentSortBy.value = sortBy
        }
    }).catch((error) => toast.error(error)).finally(() => isLoading.value = false)
}

onMounted(() => {
    const user_session_id = sessionStorage.getItem("user_session_id")
    if (user_session_id) {
        retrievePlaylists(user_session_id, "latest")
    } else {
        router2.push({ name: "auth" })
    }
})
</script>

<template>
    <Teleport v-if="sharedState.isPlaylistCreationOpen.open && sharedState.isPlaylistCreationOpen.playlist_id"
        to="body">
        <PlaylistCreation></PlaylistCreation>
    </Teleport>
    <div class="flex flex-col font-roboto left-[260px] top-[70px] relative gap-y-4">
        <div class="title">
            <p class="text-[36px] font-bold">Playlists</p>
        </div>
        <div class="filters">
            <button @click="toggleFilterOpening" class="bg-[#f2f2f2] w-auto px-2 min-w-[62.35px] h-[32px] rounded-lg flex flex-row justify-center
             items-center gap-x-2">
                <span class="font-medium text-[14px]">
                    {{ currentSortBy === 'a-z' ? 'A-Z' : "Date Added" }}
                </span>
                <img class="w-[12px] h-[12px]" :src="arrowDown" alt="">
            </button>
            <div v-if="isFilterOpen" class="w-[256px] h-[80px] rounded-lg flex flex-col text-[14px] font-normal bg-white
             custom-shadow-inner">
                <button @click="filterPlaylists('a-z')" :class="[currentSortBy === 'a-z' ? 'bg-gray-200' : '']"
                    class="w-full h-1/2 text-left pl-2 hover:bg-[#f2f2f2] rounded-tl-lg rounded-tr-lg">
                    A-Z
                </button>
                <button @click="filterPlaylists('latest')" :class="[currentSortBy === 'latest' ? 'bg-gray-200' : '']"
                    class="w-full h-1/2 text-left pl-2 hover:bg-[#f2f2f2] rounded-bl-lg rounded-br-lg">
                    Recently added
                </button>
            </div>
        </div>
        <div v-if="!isLoading" class="flex flex-row flex-wrap gap-x-4 gap-y-12">
            <div v-for="playlist in playlists" :key="playlist.id" class="playlist">
                <div class="playlist-thumbnail relative z-0 w-[295px] h-[166px]" :id="playlist.id">
                    <img class="w-full h-full object-fill rounded-lg z-0" :src="playlist.last_video_thumbnail" alt="">
                    <div @click="playPlaylist(playlist.id)"
                        class="cursor-pointer play-buttons hidden bg-black w-auto p-2 rounded-lg flex-row gap-x-4 absolute top-1/2 left-[83px]">
                        <img class="w-[20px] h-[20px]" :src="playIcon" alt="">
                        <span class="text-[14px] font-medium text-white">Play all</span>
                    </div>
                    <span class="absolute bottom-2 right-2 w-[63px] h-[20px] text-[12px] text-white
                        bg-[#474646] font-medium text-center rounded-md bg-opacity-80">
                        {{ playlist.total_videos }} videos</span>
                </div>
                <div class="flex flex-col mt-1">
                    <div class="relative flex flex-row justify-start items-center">
                        <p class="text-[14px] font-medium">{{ playlist.title }}</p>
                        <button class="justify-self-end ml-auto w-[36px] h-[36px] rounded-full flex justify-center items-center
                         hover:bg-[#e5e5e5]" @click="togglePlaylistOption(playlist.id)">
                            <img class="w-[14px] h-[14px]" :src="kebabMenuIcon" alt="">
                        </button>
                        <div v-if="playlistOptionsOpen.includes(playlist.id)" class="w-[200px] h-[80px] rounded-lg flex flex-col text-[14px] font-normal bg-white
                            custom-shadow-inner absolute top-10 right-0">
                            <button @click="openPlaylistCreation(playlist.id)"
                                class="w-full h-1/2 text-left pl-2 hover:bg-[#f2f2f2] rounded-tl-lg rounded-tr-lg">
                                Edit
                            </button>
                            <button @click="deletePlaylist(playlist.id)"
                                class="w-full h-1/2 text-left pl-2 hover:bg-[#f2f2f2] rounded-bl-lg rounded-br-lg">
                                Remove
                            </button>
                        </div>
                    </div>
                    <p class="text-[14px] font-normal text-gray-600">{{ playlist.visibility }}</p>
                    <p @click="playPlaylist(playlist.id)" class="cursor-pointer text-[14px] font-normal text-gray-700">
                        View full
                        playlist</p>
                </div>
            </div>
        </div>
        <div v-else class="w-[70%] mt-40 h-full flex justify-center items-center">
            <PulseLoader color="red" size="20px"></PulseLoader>
        </div>
    </div>
</template>
<style scoped>
.custom-shadow-inner {
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.5);
}

.playlist-thumbnail:hover .play-buttons {
    display: flex;
}
</style>