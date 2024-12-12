<script setup>
import { ref, reactive } from 'vue'
import DetailStep from './video_creation/DetailStep.vue';
import VideoElements from './video_creation/VideoElements.vue';
import Visibility from './video_creation/Visibility.vue';

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


const isVideoListboxOpen = ref(false)
const toggleVideoList = () => isVideoListboxOpen.value = !isVideoListboxOpen.value

const isFileUploadBoxOpen = ref(false)
const toggleFileUploadBox = () => isFileUploadBoxOpen.value = !isFileUploadBoxOpen.value

const inputField = ref(null)
const openFileInput = () => {
    inputField.value.click()
}

const uploadFile = (event) => {
    console.log(event.target.value)
}


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
    console.log(`Current Step after next: ${currentStep.value}`);
}

const prevStep = () => {
    if (currentStep.value > 0) {
        steps[currentStep.value].completed = false;
        currentStep.value--;
    }
}

const isStepCompleted = (index) => {
    return steps[index].completed;
}

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
            <div v-if="isVideoListboxOpen" class="video-listbox absolute gap-y-1 py-4 top-[49px] right-[74px] w-[182px] h-auto rounded-xl
             bg-white flex flex-col justify-start items-center">
                <div @click="toggleFileUploadBox"
                    class="cursor-pointer w-full h-[32px] flex justify-start items-center hover:bg-[#f9f9f9]">
                    <img class="w-[20px] h-[20px] mr-4 ml-4" :src="uploadIcon" alt="">
                    <span>Upload videos</span>
                </div>
                <div class="cursor-pointer w-full h-[32px] flex justify-start items-center hover:bg-[#f9f9f9]">
                    <img class="w-[20px] h-[20px] mr-4 ml-4" :src="postIcon" alt="">
                    <span>Create post</span>
                </div>
                <div class="cursor-pointer w-full h-[32px] flex justify-start items-center hover:bg-[#f9f9f9]">
                    <img class="w-[20px] h-[20px] mr-4 ml-4" :src="playlistIcon" alt="">
                    <span>New playlist</span>
                </div>
            </div>
            <img class="w-[32px] h-[32px] rounded-full cursor-pointer" :src="channelProfile" alt="">
        </div>
    </header>
    <!-- <div v-if="isFileUploadBoxOpen" class="upload-div font-roboto w-[960px] h-[634px] flex flex-col absolute top-[75px] right-[250px] bg-white z-50
     rounded-3xl">
        <div class="title-section flex flex-row items-center border-b w-full h-[60.8px]">
            <div class="justify-self-start mr-auto pl-8">
                <p class="title text-[20px] font-medium">Upload videos</p>
            </div>
            <div class="justify-self-end ml-auto pr-4">
                <button @click="toggleFileUploadBox"
                    class="w-[39.2px] h-[39.2px] rounded-full hover:bg-[#dfdfdf] flex justify-center items-center">
                    <img draggable="false" class="w-[15px] h-[15px]" :src="closeIcon" alt="">
                </button>
            </div>
        </div>
        <div class="upload-section flex flex-col justify-center items-center w-full h-[558.4px]">
            <button @click="openFileInput"
                class="w-[136px] h-[136px] rounded-full flex justify-center items-center bg-[#f9f9f9]">
                <img draggable="false" class="w-[40%] h-[40%]" :src="uploadIcon" alt="">
            </button>
            <input @change="uploadFile" ref="inputField" class="hidden" type="file">
            <p class="text-[15px] font-normal mt-8">Drag and drop video files to upload</p>
            <span class="text-[13px] font-normal mt-1 text-[#5f5d5d]">Your videos will be private until you publish
                them.</span>
            <button @click="openFileInput" class="cursor-pointer w-[101px] h-[36px] rounded-3xl mt-6 bg-black text-white text-[14px]
             font-medium hover:bg-opacity-80">Select files</button>
        </div>
    </div> -->
    <div class="upload-div font-roboto w-[960px] h-auto min-h-[634px] flex flex-col absolute top-[75px] right-[250px] bg-white z-50
     rounded-3xl">
        <div class="title-section flex flex-row items-center border-b w-full h-[60.8px]">
            <div class="justify-self-start mr-auto pl-8">
                <p class="title text-[20px] font-medium">video title</p>
            </div>
            <div class="justify-self-end items-center flex flex-row justify-end ml-auto pr-4">
                <div class="w-[105px] h-[20px] rounded-md text-[12px] font-medium px-2 bg-[#e5e5e5] text-black mr-2">
                    <p>Saved as private</p>
                </div>
                <button @click="toggleFileUploadBox"
                    class="w-[39.2px] h-[39.2px] rounded-full hover:bg-[#dfdfdf] flex justify-center items-center">
                    <img draggable="false" class="w-[15px] h-[15px]" :src="closeIcon" alt="">
                </button>
            </div>
        </div>
        <div class="stepper-div flex flex-row justify-center items-center w-full h-[80px] border-b">
            <button
                class="w-[128px] h-[64px] rounded-lg bg-white hover:bg-[#e5e5e5] flex justify-center items-start pt-2">
                <span class="font-medium text-[15px]">Details</span>
            </button>
            <button
                class="w-[128px] h-[64px] rounded-lg bg-white hover:bg-[#e5e5e5] flex justify-center items-start pt-2">
                <span class="font-medium text-[15px] text-[#69666a]">Video elements</span>
            </button>
            <button
                class="w-[128px] h-[64px] rounded-lg bg-white hover:bg-[#e5e5e5] flex justify-center items-start pt-2">
                <span class="font-medium text-[15px] text-[#69666a]">Visibility</span>
            </button>
        </div>

        <!-- Showing Step Componenets -->
        <DetailStep v-if="currentStep === 0"></DetailStep>
        <VideoElements v-else-if="currentStep === 1"></VideoElements>
        <Visibility v-else-if="currentStep === 2"></Visibility>
        <!-- End Components-->

        <div class="flex flex-row absolute bottom-0 items-center justify-end pr-4 w-full h-[68.8px] border-t">
            <button @click="nextStep" class="w-[61px] h-[36px] rounded-3xl text-[14px] font-medium hover:bg-opacity-80
             text-white bg-black">Next
            </button>
            <h1>{{ currentStep }}</h1>
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

.stepper-div button {
    margin-right: 45px;
}

.video-listbox {
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.13);
}

.upload-div {
    box-shadow: 0 0 14px rgba(0, 0, 0, 0.15);
}
</style>