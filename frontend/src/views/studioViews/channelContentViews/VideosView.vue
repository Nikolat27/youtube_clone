<script setup>
import { ref, reactive, onMounted, watch } from 'vue';
import axios from 'axios';
import { sharedState } from '@/sharedState';
import { useRoute } from 'vue-router';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';

// Icons
import youtubeIcon from '@/assets/icons/svg-icons/youtube-icon.svg'
import editIcon from '@/assets/icons/svg-icons/edit-icon.svg'
import kebabMenuIcon from '@/assets/icons/svg-icons/kebab-menu.svg'
import downloadIcon from '@/assets/icons/svg-icons/download-icon2.svg'
import uninstallIcon from '@/assets/icons/svg-icons/uninstall-icon.svg'
import { useToast } from 'vue-toastification';


const toggleVideoCreationVisibility = (video_id) => {
    sharedState.isVideoCreationOpen.open = !sharedState.isVideoCreationOpen.open;
    sharedState.isVideoCreationOpen.video_id = video_id
}

// Opening closing video options 
const videoOptionStates = ref({});
const toggleOptions = (video_id, option) => {
    if (!videoOptionStates.value[video_id]) {
        videoOptionStates.value = {};
        videoOptionStates.value[video_id] = { optionDiv: false, editDiv: false }
    }
    videoOptionStates.value[video_id][option] = !videoOptionStates.value[video_id][option]
}

const toggleVideoOptions = (video_id) => toggleOptions(video_id, 'optionDiv')
const toast = useToast()
const router = useRoute()
let videos = reactive([])
const isVideoRetrievingLoading = ref(false)


const downloadVideo = (video_id) => {
    axios.get(`${sharedState.websiteUrl}/videos/download/${video_id}`).then((response) => {
        toast.info("Your download started...")
        if (response.status == 200) {
            toast.success(response.data.data)
        }
    }).catch((error) => console.error(error))
}


const deleteVideo = (video_id) => {
    axios.delete(`${sharedState.websiteUrl}/videos/delete/${video_id}`).then((response) => {
        if (response.status == 204) {
            toast.success("Video have been deleted")
            retrieveAllVideos()
        }
    }).catch((error) => console.error(error))
}


watch(() => sharedState.refreshRetrieveVideos, () => {
    retrieveAllVideos()
})

watch(() => router.query, () => {
    retrieveAllVideos()
})


const retrieveAllVideos = async () => {
    isVideoRetrievingLoading.value = true
    await axios.get(`${sharedState.websiteUrl}/studio/list`, {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id"),
            queries: router.query,
            video_type: router.query.type ?? 'long_video'
        }
    }).then((response) => {
        videos = response.data.data;
        sharedState.refreshRetrieveVideos = false
    }).catch((error) => {
        toast.error(`Error: ${error}`)
    }).finally(() => {
        isVideoRetrievingLoading.value = false // Loading
    })
}

onMounted(() => {
    retrieveAllVideos();
})
</script>

<template>
    <div class="border-b font-roboto pl-[48px] w-full">
        <div v-if="!isVideoRetrievingLoading">
            <div v-for="video in videos" :key="video.id" class="table-itself border-b">
                <router-link :to="`/video/${video.unique_id}`">
                    <div class="video-thumbnail">
                        <img draggable="false" :src="video.thumbnail_url" alt="">
                        <span class="video-duration">{{ video.duration }}</span>
                    </div>
                </router-link>
                <div class="video-detail relative flex flex-col font-normal text-[13px] mt-2"
                    style="padding-left: 12px;">
                    <router-link :to="`/video/${video.unique_id}`">
                        <span>{{ video.title }}</span>
                    </router-link>
                    <span>{{ video.description }}</span>
                    <div class="flex flex-row justify-start items-center">
                        <router-link :to="`/video/${video.unique_id}`">
                            <button class="w-[39.2px] h-[39.2px] rounded-full hover:bg-[#eaeaea] flex items-center
                            justify-center">
                                <img class="w-[20px] h-[20px] center" :src="youtubeIcon" alt="">
                            </button>
                        </router-link>
                        <button @click="toggleVideoCreationVisibility(video.id)" class="w-[39.2px] h-[39.2px] rounded-full hover:bg-[#eaeaea] flex items-center
                            justify-center">
                            <img class="w-[17px] h-[17px] center" :src="editIcon" alt="">
                        </button>
                        <button @click="toggleVideoOptions(video.id)" class="w-[39.2px] h-[39.2px] rounded-full hover:bg-[#eaeaea] flex items-center
                            justify-center">
                            <img class="w-[17px] h-[17px] center" :src="kebabMenuIcon" alt="">
                        </button>
                        <div v-if="videoOptionStates[video.id]?.optionDiv" class="absolute left-40 top-0 video-edit-options w-[226px] h-auto rounded-xl bg-white flex flex-col
                            justify-start items-center py-4">
                            <div @click="downloadVideo(video.unique_id)" class="w-[226px] cursor-pointer z-50 h-[32px] hover:bg-[#f9f9f9] flex flex-row justify-start items-center
                                text-[15px] font-normal font-roboto">
                                <img class="w-[17px] h-[17px] mx-4" :src="downloadIcon" alt="">
                                <p>Download</p>
                            </div>
                            <div @click="deleteVideo(video.unique_id)" class="w-full cursor-pointer h-[32px] z-50 hover:bg-[#f9f9f9] flex flex-row justify-start items-center
                                text-[15px] font-normal font-roboto">
                                <img class="w-[17px] h-[17px] mx-4" :src="uninstallIcon" alt="">
                                <p>Delete forever</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="video-info w-[70%] relative h-full flex flex-row justify-end items-center text-[13px] font-normal
                    ml-auto mr-8">
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[355px]">{{ video.visibility ?
                        'public' : 'private' }}</p>
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[430px]">{{ video.restriction ? 'yes'
                        : 'no' }}</p>
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[525px]">{{ video.created_at }}</p>
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[635px]">{{ video.views }} </p>
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[710px]">{{ video.total_comments }}
                    </p>
                    <p class="ml-8 absolute top-1/3 transform translate-y-1/3 left-[775px]">{{ video.total_likes }}, {{
                        video.total_dislikes }}</p>
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