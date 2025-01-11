<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
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


// Edit Video Title Management
const videoTitle = ref('')

const toggleVideoCreationVisibility = (video_id) => {
    sharedState.isVideoCreationOpen.open = !sharedState.isVideoCreationOpen.open;
    sharedState.isVideoCreationOpen.video_id = video_id
}


// Opening closing video options 
const videoOptionStates = ref({});
const toggleOptions = (video_id, video_title = '', video_description = '', option) => {
    if (!videoOptionStates.value[video_id]) {
        videoOptionStates.value = {};
        videoOptionStates.value[video_id] = { optionDiv: false, editDiv: false }
    }
    videoOptionStates.value[video_id][option] = !videoOptionStates.value[video_id][option]

    videoTitle.value = video_title; // Puting the video title and desc in their inputs
    videoDescription.value = video_description;
}

const toggleVideoOptions = (video_id, video_title, video_description) => toggleOptions(video_id, video_title, video_description, 'optionDiv')
const toggleVideoEdit = (video_id, video_title, video_description) => toggleOptions(video_id, video_title, video_description, 'editDiv')

const toast = useToast()
const router = useRoute()
let videos = reactive([])
const isVideoRetrievingLoading = ref(false)

watch(() => sharedState.refreshRetrieveVideos, () => {
    retrieveAllVideos()
})

watch(() => router.query, () => {
    retrieveAllVideos()
})


const retrieveAllVideos = async () => {
    isVideoRetrievingLoading.value = true
    await axios.get(`http://127.0.0.1:8000/studio/list`, {
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
                <div class="video-thumbnail">
                    <img draggable="false" :src="video.thumbnail_url" alt="">
                    <span class="video-duration">{{ video.duration }}</span>
                </div>
                <div class="video-detail relative flex flex-col font-normal text-[13px] mt-2"
                    style="padding-left: 12px;">
                    <span>{{ video.title }}</span>
                    <span>{{ video.description }}</span>
                    <div class="flex flex-row justify-start items-center">
                        <button class="w-[39.2px] h-[39.2px] rounded-full hover:bg-[#eaeaea] flex items-center
                    justify-center">
                            <img class="w-[20px] h-[20px] center" :src="youtubeIcon" alt="">
                        </button>
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
                            <div @click="toggleVideoEdit(video.id, video.title, video.description)" class="cursor-pointer w-full h-[32px] hover:bg-[#f9f9f9] flex flex-row justify-start items-center
                        text-[15px] font-normal font-roboto">
                                <img class="w-[17px] h-[17px] mx-4" :src="editIcon" alt="">
                                <p>Edit title and description</p>
                            </div>
                            <div class="w-full h-[32px] hover:bg-[#f9f9f9] flex flex-row justify-start items-center
                        text-[15px] font-normal font-roboto">
                                <img class="w-[17px] h-[17px] mx-4" :src="downloadIcon" alt="">
                                <p>Download</p>
                            </div>
                            <div class="w-full h-[32px] hover:bg-[#f9f9f9] flex flex-row justify-start items-center
                        text-[15px] font-normal font-roboto">
                                <img class="w-[17px] h-[17px] mx-4" :src="uninstallIcon" alt="">
                                <p>Delete forever</p>
                            </div>
                        </div>
                        <!-- <div v-if="videoOptionStates[video.id]?.editDiv" class="edit-title-description bg-white z-40 w-[488px] h-[368px] rounded-lg
                        flex flex-col justify-start pt-2 items-center gap-y-4 absolute left-2 top-6">
                            <div class="w-[464px] h-[91px] rounded-lg border border-solid box-border border-[#d6d6d6] hover:border-black hover:border-2
                        focus:border-2 relative pl-2 pt-2"
                                :style="{ borderColor: userAbleToSave ? 'black' : 'red', borderWidth: !userAbleToSave ? '2px' : '1px' }">
                                <span class="text-[12px] font-medium text-gray-600">Title (required)</span>
                                <textarea @input="videoTitleEdit" v-model="video.title"
                                    class="mt-1 edit-title-input w-[440px] h-[41px] outline-none text-[15px] font-normal overflow-hidden leading-4"
                                    placeholder="Add title" minlength="1" required maxlength="100"></textarea>
                                <span class="text-[12px] font-normal absolute right-1 bottom-1 text-gray-700"><span
                                        class="title-char-counter">{{ videoTitleLength }}</span>/100</span>
                            </div>
                            <div
                                class="w-[464px] relative max-w-[464px] h-[201px] max-h-[201px] rounded-lg border border-[#d6d6d6] pl-2 pt-2 hover:border-black hover:border-2">
                                <span class="text-[12px] font-medium text-gray-600">Description</span>
                                <textarea style="scrollbar-width: thin;" @input="videoDescriptionEdit"
                                    v-model="video.description"
                                    class="mt-1 edit-title-input w-[440px] h-[151px] outline-none text-[15px] font-normal overflow-y-auto leading-4"
                                    placeholder="Add description" maxlength="5000"></textarea>
                                <span class="text-[12px] font-normal absolute right-1 bottom-1 text-gray-700"><span
                                        class="title-char-counter">{{ videoDescriptionLength }}</span>/5000</span>
                            </div>
                            <div class="flex flex-row w-full self-end justify-end items-center font-roboto 
                     gap-x-2 pr-2 pb-2">
                                <span v-if="!userAbleToSave" class="text-[12px] font-normal text-red-800">Your
                                    video needs a title</span>
                                <button @click="toggleVideoEdit(video.id)" class="w-[74.9px] h-[36px] rounded-3xl text-[14px] font-medium
                         items-center text-black bg-[#f2f2f2] hover:bg-[#e5e5e5]">Cancel</button>
                                <button :disabled="!userAbleToSave" class="w-[62.2px] h-[36px] rounded-3xl text-[14px] font-medium
                         items-center text-white hover:bg-[#272727]"
                                    :style="{ backgroundColor: userAbleToSave ? 'black' : 'gray' }">Save</button>
                            </div>
                        </div> -->
                    </div>
                </div>
                <div class="video-info w-[70%] relative h-full flex flex-row justify-end items-center text-[13px] font-normal
                    ml-auto mr-8">
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[355px]">{{ video.visibility ?
                        'public' : 'private' }}</p>
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[430px]">{{ video.restriction ? 'yes'
                        : 'no' }}</p>
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[525px]">{{ video.created_at }}</p>
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[635px]">101K </p>
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[710px]">2k</p>
                    <p class="ml-8 absolute top-1/3 transform translate-y-1/3 left-[775px]">2k, 3k</p>
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