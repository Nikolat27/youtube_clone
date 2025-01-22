<script setup>
import { ref, reactive, onMounted, watch } from 'vue';
import axios from 'axios';
import { sharedState } from '@/sharedState';
import { useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import PlaylistCreation from '@/components/studio/video_creation/PlaylistCreation.vue';

// Icons
import youtubeIcon from '@/assets/icons/svg-icons/youtube-icon.svg'
import editIcon from '@/assets/icons/svg-icons/edit-icon.svg'
import kebabMenuIcon from '@/assets/icons/svg-icons/kebab-menu.svg'
import uninstallIcon from '@/assets/icons/svg-icons/uninstall-icon.svg'
import playlistDefaultImg from '/src/assets/img/default-playlist-img.jpg'

// Opening closing video options 
const playlistOptionStates = ref({});
const toggleOptions = (playlist_id, option) => {
    if (!playlistOptionStates.value[playlist_id]) {
        playlistOptionStates.value = {};
        playlistOptionStates.value[playlist_id] = { optionDiv: false, editDiv: false }
    }
    playlistOptionStates.value[playlist_id][option] = !playlistOptionStates.value[playlist_id][option]
}

const togglePlaylistCreationOpen = (playlist_id) => {
    sharedState.isPlaylistCreationOpen.open = true
    sharedState.isPlaylistCreationOpen.playlist_id = playlist_id
}

const togglePlaylistOptions = (playlist_id) => toggleOptions(playlist_id, 'optionDiv')
const toast = useToast()

watch(() => sharedState.refreshRetrievePlaylists, () => {
    retrieveAllPlaylists()
    sharedState.refreshRetrievePlaylists = false
})

const isLoading = ref(false)

const deletePlaylist = async (playlist_id) => {
    isLoading.value = true
    await axios.delete(`http://127.0.0.1:8000/studio/playlist/delete/${playlist_id}`, {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 202) {
            toast.info("You Deleted your playlist.")
            retrieveAllPlaylists()
        }
    }).catch((error) => {
        toast.error(error)
    }).finally(() => isLoading.value = false)
}

const playlists = reactive([])
const retrieveAllPlaylists = async () => {
    isLoading.value = true
    await axios.get("http://127.0.0.1:8000/studio/playlist/list", {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 200) {
            playlists.splice(0, playlists.length, ...response.data.playlists)
        }
    }).catch((error) => {
        toast.error(error)
    }).finally(() => isLoading.value = false)
}

onMounted(() => {
    retrieveAllPlaylists()
})
</script>
<template>
    <div class="border-b font-roboto pl-[48px] w-full">
        <Teleport v-if="sharedState.isPlaylistCreationOpen.open && sharedState.isPlaylistCreationOpen.playlist_id"
            to="body">
            <PlaylistCreation></PlaylistCreation>
        </Teleport>
        <div v-if="!isLoading">
            <div v-for="playlist in playlists" :key="playlist.id" class="table-itself border-b">
                <router-link :to="`/playlist/${playlist.id}`">
                    <div class="video-thumbnail">
                        <img draggable="false" :src="playlist.last_video_thumbnail ?? playlistDefaultImg" alt="">
                        <span class="video-duration">{{ playlist.total_videos ?? 0 }}</span>
                    </div>
                </router-link>
                <div class="video-detail relative flex flex-col font-normal text-[13px] mt-2"
                    style="padding-left: 12px;">
                    <router-link :to="`/playlist/${playlist.id}`">
                        <span>{{ playlist.title }}</span>
                    </router-link>
                    <span>{{ playlist.description }}</span>
                    <div class="flex flex-row justify-start items-center">
                        <router-link :to="`/playlist/${playlist.id}`">
                            <button class="w-[39.2px] h-[39.2px] rounded-full hover:bg-[#eaeaea] flex items-center
                            justify-center">
                                <img class="w-[20px] h-[20px] center" :src="youtubeIcon" alt="">
                            </button>
                        </router-link>
                        <button v-if="!playlist.is_default" @click="togglePlaylistCreationOpen(playlist.id)" class="w-[39.2px] h-[39.2px] rounded-full hover:bg-[#eaeaea] flex items-center
                                justify-center">
                            <img class="w-[17px] h-[17px] center" :src="editIcon" alt="">
                        </button>
                        <button v-if="!playlist.is_default" @click="togglePlaylistOptions(playlist.id)" class="w-[39.2px] h-[39.2px] rounded-full hover:bg-[#eaeaea] flex items-center
                                justify-center">
                            <img class="w-[17px] h-[17px] center" :src="kebabMenuIcon" alt="">
                        </button>
                        <div v-if="playlistOptionStates[playlist.id]?.optionDiv" class="absolute left-36 top-0 video-edit-options w-[226px] h-auto rounded-xl bg-white flex flex-col
                                justify-start items-center py-4">
                            <div @click="deletePlaylist(playlist.id)" class="cursor-pointer w-full h-[32px] hover:bg-[#f9f9f9] flex flex-row justify-start items-center
                                text-[15px] font-normal font-roboto">
                                <img class="w-[17px] h-[17px] mx-4" :src="uninstallIcon" alt="">
                                <p>Delete forever</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="video-info w-[70%] relative h-full flex flex-row justify-end items-center text-[13px] font-normal
                        ml-auto mr-8">
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[430px]">{{ playlist.visibility }}</p>
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[525px]">{{ playlist.created_at }}</p>
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[635px]">Draft</p>
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[710px]">Draft</p>
                    <p class="ml-8 absolute top-1/3 transform translate-y-1/3 left-[775px]">Draft</p>
                </div>
            </div>
        </div>
        <div v-else class="h-[400px] flex justify-center items-center">
            <PulseLoader color="red" size="20px"></PulseLoader>
        </div>
    </div>
</template>
<style scoped>
@media (min-width: 1200px) {
    #channel-content {
        left: 254px;
        top: 100px;
    }
}

.filter-options div {
    cursor: pointer;
}

.edit-title-input {
    resize: none;
}

.edit-title-description {
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.15);
}

.channel-main-content div {
    padding-left: 48px;
}

.video-edit-options {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.13);
}

.table-itself {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    width: 100%;
    height: 83px;
}

.video-thumbnail {
    position: relative;
    display: flex;
    justify-content: center;
    align-content: center;
    width: auto;
    height: 83px;
    margin-bottom: 0px;
    align-items: center;
}

.video-thumbnail img {
    width: 120px !important;
    height: 68px !important;
    border-radius: 8px;
}

.video-duration {
    position: absolute;
    right: 3px;
    bottom: 10px;
    border-radius: 0.375rem;
    width: 2rem;
    height: 1rem;
    text-align: center;
    color: white;
    background-color: rgba(107, 114, 128, 0.85);
    font-size: 0.75rem;
    font-weight: 500;
}

.filter-options {
    box-shadow: 0 0 14px rgba(0, 0, 0, 0.13);
}

.filter-options div {
    user-select: none;
    width: 100%;
    height: 32px;
    display: flex;
    justify-content: start;
    align-items: center;
    padding-left: 16px;
}
</style>