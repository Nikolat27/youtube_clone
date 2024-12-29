<script setup>
import { ref, reactive, watch } from 'vue'
import axios from 'axios';
import DetailStep from './video_creation/DetailStep.vue';
import VideoElements from './video_creation/VideoElements.vue';
import Visibility from './video_creation/Visibility.vue';
import { sharedState } from '@/sharedState';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import PlaylistCreation from './video_creation/PlaylistCreation.vue';

const router = useRouter();

// Icons
import hamburgerBtn from '/src/assets/icons/svg-icons/collapse-menu-icon.svg'
import ytLogo from '/src/assets/img/yt-studio-logo.svg'
import searchIcon from '/src/assets/icons/svg-icons/search-icon.svg'
import createVideo from '/src/assets/icons/svg-icons/create-video-icon.svg'
import channelProfile from '/src/assets/img/Ruby.png'
import uploadIcon from '/src/assets/icons/svg-icons/upload-icon.svg'
import postIcon from '/src/assets/icons/svg-icons/post-icon.svg'
import playlistIcon from '/src/assets/icons/svg-icons/playlist-icon-2.svg'
import closeIcon from '/src/assets/icons/svg-icons/close-icon2.svg'
import checkMarkIcon from '/src/assets/icons/svg-icons/check-mark-icon.svg'
import shortVideoIcon from '/src/assets/icons/svg-icons/shorts-icon.svg'


const isVideoListboxOpen = ref(false)
const toggleVideoList = () => isVideoListboxOpen.value = !isVideoListboxOpen.value

const toggleVideoCreationVisibility = () => sharedState.isVideoCreationOpen.open = !sharedState.isVideoCreationOpen.open

const toggleFileUploadBox = (video_type) => {
    sharedState.isVideoUploadingOpen.open = !sharedState.isVideoUploadingOpen.open
    sharedState.isVideoUploadingOpen.video_type = video_type
}

const togglePlaylistCreation = () => {
    sharedState.isPlaylistCreationOpen.open = !sharedState.isPlaylistCreationOpen.open;
    sharedState.isPlaylistCreationOpen.playlist_id = null;
}

const inputField = ref(null)
const openFileInput = () => {
    inputField.value.click()
}

const uploadFile = async (event) => {
    const videoFile = event.target.files[0]; // Get the selected file from the input
    formData.details.title = event.target.files[0].name;
    formData.video_type = sharedState.isVideoUploadingOpen.video_type

    if (!videoFile) {
        console.error("No file selected.");
        return;
    }

    const fileFormData = new FormData();
    fileFormData.append("file", videoFile);
    fileFormData.append("user_session_id", sessionStorage.getItem("user_session_id"));
    fileFormData.append("video_type", formData.video_type);
    try {
        await axios.post("http://localhost:8000/videos/upload", fileFormData, {
            headers: {
                "Content-Type": "multipart/form-data" // This type is necessary for sending files
            }
        }).then((response) => {
            sharedState.isVideoUploadingOpen.open = false
            sharedState.isVideoCreationOpen.open = true
            sharedState.isVideoCreationOpen.video_id = response.data.video_id
            formData.details.video_id = response.data.video_id
            sharedState.refreshRetrieveVideos = true
            toast.success("Your video uploaded successfully!");
        });
    } catch (error) {
        toast.error(`Error File uploading ${error}`);
    }
}

// Multi stepper form Management
const steps = reactive([
    { title: 'Details', completed: false },
    { title: 'Elements', completed: false },
    { title: 'Visibility', completed: false },
])

const currentStep = ref(0);
const nextStep = () => {
    if (currentStep.value < steps.length - 1) {
        steps[currentStep.value].completed = true;
        currentStep.value += 1;
    }
}

const prevStep = () => {
    if (currentStep.value > 0) {
        steps[currentStep.value].completed = false;
        currentStep.value--;
    }
}

const isLoading = ref(false)
watch(sharedState.isVideoCreationOpen, () => {
    currentStep.value = 0
    isLoading.value = true
    if (!sharedState.isVideoCreationOpen.open) return;
    axios.get("http://127.0.0.1:8000/videos/get", {
        params: {
            video_id: sharedState.isVideoCreationOpen.video_id
        }
    }).then((response) => {
        formData.video_type = response.data.data.video_type
        formData.details = response.data.data.details;
        formData.thumbnailFile = response.data.data.thumbnailFile;
        formData.subtitleFile = response.data.data.subtitleFile;
        formData.visibility = response.data.data.visibility;
    }).catch((error) => {
        console.log(error)
    }).finally(() => isLoading.value = false)
})

const formData = reactive({
    user_session_id: sessionStorage.getItem('user_session_id'),
    video_type: sharedState.isVideoUploadingOpen.video_type, // we have long_video (or regular) and short_video
    details: {
        video_id: sharedState.isVideoCreationOpen.video_id,
        title: '',
        description: '',
        playlists: [],
        audience: 'kids',
        ageRestriction: '',
        language: 'not-applicable',
        monetized: false,
    },
    thumbnailFile: null,
    subtitleFile: null,
    visibility: {
        scheduled: false,
        scheduledTime: '',
        publish: 'private',
    }
})

const toast = useToast()
const submitForm = async () => {
    isLoading.value = true
    const formDataToSend = new FormData();
    formDataToSend.append('video_type', formData.video_type);
    formDataToSend.append('user_session_id', formData.user_session_id);
    if (formData.thumbnailFile) {
        formDataToSend.append('thumbnailFile', formData.thumbnailFile);
    }
    if (formData.subtitleFile) {
        formDataToSend.append('subtitleFile', formData.subtitleFile);
    }
    formDataToSend.append('details', JSON.stringify(formData.details));
    formDataToSend.append('visibility', JSON.stringify(formData.visibility));
    await axios.post("http://127.0.0.1:8000/videos/update", formDataToSend, {
        headers: {
            'Content-Type': 'multipart/form-data' // Important for file uploads
        }
    }).then((response) => {
        toast.success("Your video Updated Successfully!")
        sharedState.refreshRetrieveVideos = true;
        sharedState.isVideoCreationOpen.open = false;
    }).catch((error) => {
        toast.error("Error!")
    }).finally(() => isLoading.value = false);
}

// Studio page is just for authenticated Users
axios.get("http://localhost:8000/users/is_authenticated", {
    params: {
        user_session_id: sessionStorage.getItem("user_session_id")
    }
}).then((response) => {
    if (!response.data) router.push({ name: 'auth' });
})
</script>

<template>
    <header class="font-roboto flex flex-row w-full h-[63.2px] mx-auto bg-white z-50 fixed shadow-lg
     justify-start items-center">
        <div class="left-section w-[20%] h-full flex flex-row justify-start items-center pl-5">
            <button class="w-[43.2px] h-[43.2px] rounded-full hover:bg-[#f0f0f0] flex justify-center items-center mr-[16px]
             flex-shrink-0 flex-grow-0">
                <img class="w-[22px] h-[22px] flex-shrink-0 flex-grow-0" :src="hamburgerBtn" alt="">
            </button>
            <img class="w-[98.4px] min-w-[98.4px] h-[24px] cursor-pointer" :src="ytLogo" alt="">
        </div>
        <div class="middle-section w-[60%] h-full flex justify-center items-center flex-row">
            <div style="width: 60%;"
                class="bg-[#f1f1f1] flex justify-start items-center flex-row rounded-[20px] border border-transparent hover:border-black transition duration-75">
                <img class="w-[20px] h-[20px] mx-4" :src="searchIcon" alt="">
                <input class="bg-transparent w-full h-[40px] outline-none text-[15px] font-normal placeholder:font-normal placeholder:text-[15px]
                 placeholder:text-[#757577]" type="text" placeholder="Search across your channel">
            </div>
        </div>
        <div class="right-section relative w-[20%] h-full flex flex-row justify-self-end ml-auto justify-end
         items-center pr-6 gap-x-4">
            <button @click="toggleVideoList" class="flex-grow-0 flex-shrink-0 hover:bg-[#e5e5e5] flex flex-row justify-center items-center pl-1 gap-x-2
             w-[95px] h-[34px] rounded-3xl border border-gray-200">
                <img class="w-[20px] h-[20px]" :src="createVideo" alt="">
                <p class="text-[14px] font-medium">Create</p>
            </button>
            <div v-if="isVideoListboxOpen && !isVideoCreationOpen" class="video-listbox absolute gap-y-1 py-4 top-[49px] right-[74px] w-[182px] h-auto rounded-xl
             bg-white flex flex-col justify-start items-center">
                <div @click="toggleFileUploadBox('long_video')"
                    class="cursor-pointer w-full h-[32px] flex justify-start items-center hover:bg-[#f9f9f9]">
                    <img class="w-[20px] h-[20px] mr-4 ml-4" :src="uploadIcon" alt="">
                    <span>Upload videos</span>
                </div>
                <div @click="toggleFileUploadBox('short_video')"
                    class="cursor-pointer w-full h-[32px] flex justify-start items-center hover:bg-[#f9f9f9]">
                    <img class="w-[20px] h-[20px] mr-4 ml-4" :src="shortVideoIcon" alt="">
                    <span>Create shorts</span>
                </div>
                <router-link to="/posts"
                    class="cursor-pointer w-full h-[32px] flex justify-start items-center hover:bg-[#f9f9f9]">
                    <img class="w-[20px] h-[20px] mr-4 ml-4" :src="postIcon" alt="">
                    <span>Create post</span>
                </router-link>
                <div @click="togglePlaylistCreation"
                    class="cursor-pointer w-full h-[32px] flex justify-start items-center hover:bg-[#f9f9f9]">
                    <img class="w-[20px] h-[20px] mr-4 ml-4" :src="playlistIcon" alt="">
                    <span>New playlist</span>
                </div>
                <Teleport
                    v-if="sharedState.isPlaylistCreationOpen.open && !sharedState.isPlaylistCreationOpen.playlist_id"
                    to="body">
                    <PlaylistCreation></PlaylistCreation>
                </Teleport>
            </div>
            <img class="w-[32px] h-[32px] rounded-full cursor-pointer" :src="channelProfile" alt="">
        </div>
    </header>
    <div v-if="sharedState.isVideoUploadingOpen.open" class="upload-div shadow-outer font-roboto w-[960px] h-[634px] flex flex-col absolute top-[75px] right-[250px] bg-white z-50
     rounded-3xl">
        <div class="title-section flex flex-row items-center border-b w-full h-[60.8px]">
            <div class="justify-self-start mr-auto pl-8">
                <p class="title text-[20px] font-medium">Upload videos</p>
            </div>
            <div class="justify-self-end ml-auto pr-4">
                <button @click="toggleFileUploadBox(sharedState.isVideoUploadingOpen.video_type)"
                    class="w-[39.2px] h-[39.2px] rounded-full hover:bg-[#dfdfdf] flex justify-center items-center">
                    <img draggable="false" class="w-[15px] h-[15px]" :src="closeIcon" alt="">
                </button>
            </div>
        </div>
        <div class="upload-section flex flex-col justify-center items-center w-full h-[558.4px]">
            <h3 class="mb-6 select-none">Video Type: <span class="font-bold">{{
                sharedState.isVideoUploadingOpen.video_type }}</span></h3>
            <button @click="openFileInput"
                class="w-[136px] h-[136px] rounded-full flex justify-center items-center bg-[#f9f9f9]">
                <img draggable="false" class="w-[40%] h-[40%]" :src="uploadIcon" alt="">
            </button>
            <input @change="uploadFile" ref="inputField" accept="video/mp4" class="hidden" type="file">
            <p class="text-[15px] font-normal mt-8">Drag and drop video files to upload</p>
            <span class="text-[13px] font-normal mt-1 text-[#5f5d5d]">Your videos will be private until you publish
                them.</span>
            <button @click="openFileInput" class="cursor-pointer w-[101px] h-[36px] rounded-3xl mt-6 bg-black text-white text-[14px]
             font-medium hover:bg-opacity-80">Select files</button>
        </div>
    </div>
    <div v-if="sharedState.isVideoCreationOpen.open" class="video-creation shadow-outer font-roboto w-[960px]
     h-auto min-h-[634px] flex flex-col absolute top-[75px] right-[250px] bg-white z-50
     rounded-3xl">
        <div class="title-section flex flex-row items-center border-b w-full h-[60.8px]">
            <div class="justify-self-start mr-auto pl-8">
                <p class="title text-[20px] font-medium">video title</p>
            </div>
            <div class="justify-self-end items-center flex flex-row justify-end ml-auto pr-4">
                <div class="w-[105px] min-h-[20px] h-auto rounded-md text-[12px] font-medium px-2
                 bg-[#e5e5e5] text-black mr-2">
                    <p>Saved as {{ formData.visibility.scheduled ? 'scheduled' : formData.visibility.publish }}</p>
                </div>
                <button @click="toggleVideoCreationVisibility"
                    class="w-[39.2px] h-[39.2px] rounded-full hover:bg-[#dfdfdf] flex justify-center items-center">
                    <img draggable="false" class="w-[15px] h-[15px]" :src="closeIcon" alt="">
                </button>
            </div>
        </div>
        <div class="stepper-div flex flex-row justify-center items-center w-full h-[80px] border-b">
            <button @click="currentStep = 0" :style="{
                backgroundColor: currentStep === 0 ? '#e5e5e5' : '',
                color: currentStep === 0 ? 'black' : '#69666a'
            }" class="-ml-[64px] w-[128px] h-[64px] rounded-lg bg-white hover:bg-[#e5e5e5] flex
             flex-col justify-start items-center pt-2">
                <span class="font-medium text-[15px]">Details</span>
                <div v-if="currentStep === 0"
                    class="z-50 w-[24px] h-[24px] mb-2 rounded-full bg-black flex justify-center items-center">
                    <div class="w-[12px] h-[12px] bg-white rounded-full">
                    </div>
                </div>
                <div v-else-if="steps[0].completed === true"
                    class="z-50 w-[20px] h-[20px] mt-1 rounded-full flex justify-center items-center">
                    <img class="z-50 w-full h-full" :src="checkMarkIcon" alt="">
                </div>
                <div v-else class="z-50 w-[20px] h-[20px] mt-1 rounded-full bg-black flex justify-center items-center">
                    <div class="w-[10px] h-[10px] bg-white rounded-full">
                    </div>
                </div>
            </button>
            <div :class="[currentStep > 0 ? 'bg-black' : 'bg-gray-300']"
                class="step-separator mt-6 w-[222px] h-[2px] -ml-[56px] z-10 cursor-pointer"></div>
            <button :disabled="formData.details.title.length < 1" @click="currentStep = 1" :style="{
                backgroundColor: currentStep === 1 ? '#e5e5e5' : '',
                color: currentStep === 1 ? 'black' : '#69666a'
            }"
                class="-ml-[64px] w-[128px] h-[64px] rounded-lg bg-white hover:bg-[#e5e5e5] flex flex-col justify-start items-center pt-2">
                <span class="font-medium text-[15px]">Video elements</span>
                <div v-if="currentStep === 1"
                    class="m-auto z-50 w-[24px] h-[24px] mb-2 rounded-full bg-black flex justify-center items-center">
                    <div class="w-[12px] h-[12px] bg-white rounded-full">
                    </div>
                </div>
                <div v-else-if="steps[1].completed === true"
                    class="z-50 w-[20px] h-[20px] mt-1 rounded-full flex justify-center items-center">
                    <img class="z-50 w-full h-full" :src="checkMarkIcon" alt="">
                </div>
                <div v-else class="z-50 w-[20px] h-[20px] mt-1 rounded-full bg-black flex justify-center items-center">
                    <div class="w-[10px] h-[10px] bg-white rounded-full">
                    </div>
                </div>
            </button>
            <div :class="[currentStep > 1 ? 'bg-black' : 'bg-gray-300']"
                class="step-separator mt-6 w-[222px] h-[2px] -ml-[64px] z-10 cursor-pointer"></div>
            <button :disabled="formData.details.title.length < 1" @click="currentStep = 2" :style="{
                backgroundColor: currentStep === 2 ? '#e5e5e5' : '',
                color: currentStep === 2 ? 'black' : '#69666a'
            }"
                class="-ml-[64px] w-[128px] h-[64px] rounded-lg bg-white hover:bg-[#e5e5e5] flex flex-col justify-start items-center pt-2">
                <span class="font-medium text-[15px]">Visibility</span>
                <div v-if="currentStep === 2"
                    class="z-20 m-auto w-[24px] h-[24px] mb-2 relative rounded-full bg-black flex justify-center items-center">
                    <div class="w-[12px] h-[12px]
                     bg-white rounded-full">
                    </div>
                </div>
                <div v-else-if="steps[2].completed === true"
                    class="z-20 w-[20px] h-[20px] mt-1 rounded-full flex justify-center items-center">
                    <img class="z-30 w-full h-full" :src="checkMarkIcon" alt="">
                </div>
                <div v-else
                    class="z-20 w-[20px] h-[20px] relative mt-1 rounded-full bg-black flex justify-center items-center">
                    <div class="w-[10px] h-[10px] bg-white
                     rounded-full">
                    </div>
                </div>
            </button>
        </div>

        <!-- Showing Step Componenets -->
        <div v-if="!isLoading">
            <DetailStep v-if="currentStep === 0" :formData="formData"></DetailStep>
            <VideoElements v-else-if="currentStep === 1" :formData="formData"></VideoElements>
            <Visibility v-else-if="currentStep === 2" :formData="formData"></Visibility>
        </div>
        <div v-else class="m-auto justify-self-center self-center h-full flex justify-center items-center">
            <PulseLoader color="red" size="20px"></PulseLoader>
        </div>
        <!-- End Components-->

        <div class="flex flex-row absolute bottom-0 gap-x-2 items-center justify-end pr-4 w-full h-[68.8px] border-t">
            <button v-if="!(currentStep === 0)" @click="prevStep" class="w-[61px] h-[36px] rounded-3xl text-[14px] font-medium hover:bg-opacity-80
             text-black bg-[#f9f9f9] hover:bg-[#cccaca]">Back
            </button>
            <button v-if="currentStep < 2" @click="nextStep"
                :class="[formData.details.title.length >= 1 ? '' : 'opacity-40']"
                :disabled="formData.details.title.length < 1" class="w-[61px] h-[36px] rounded-3xl text-[14px] font-medium hover:bg-opacity-80
             text-white bg-black">Next
            </button>
            <button v-else @click="submitForm" class="w-[61px] h-[36px] disabled rounded-3xl text-[14px] font-medium hover:bg-opacity-80
             text-white bg-black" :disabled="formData.visibility.scheduled && !formData.visibility.scheduledTime"
                :class="[formData.visibility.scheduled && !formData.visibility.scheduledTime ? 'opacity-60' : '']">Save
            </button>
        </div>
    </div>
</template>
<style scoped>
.age-restriction-bar {
    visibility: hidden;
    max-height: 0px;
}

.age-restriction-container:hover .age-restriction-bar {
    visibility: visible;
    transition: opacity 0.1s ease-in-out;
    opacity: 1;
    max-height: 72px;
}

.video-time-tracker::-moz-range-progress {
    height: 5px;
    background-color: #ff0033;
}

.video-time-tracker::-moz-range-thumb {
    background-color: #ff0033;
    width: 14px;
    height: 14px;
}

.video-time-tracker::-moz-range-track {
    height: 5px;
    background-color: black;
}

.video-volume-input::-moz-range-thumb {
    width: 12px;
    height: 12px;
}

@media (max-width: 740px) {
    .middle-section {
        display: none;
    }
}

.playlist-creation {
    box-shadow: 0 0 14px rgba(0, 0, 0, 0.15);
}

textarea {
    resize: none;
}

.video-listbox {
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.13);
}
</style>