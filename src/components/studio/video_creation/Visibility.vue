<script setup>
import { ref, computed, watch } from 'vue';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import arrowIcon from '/src/assets/icons/svg-icons/thin-chevron-arrow-bottom-icon.svg'

const videoVisibility = ref('private')
const date = ref()

const openVisibility = ref(false)
const toggleOpenVisibility = () => openVisibility.value = !openVisibility.value

const format = (date) => {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hours = date.getHours()
    const minutes = date.getMinutes()
    return `Date: ${year}/${month}/${day} ${hours}:${minutes}`
}
</script>
<template>
    <div class="flex flex-col pl-[50px] mt-2 h-[415px] max-h-[415px] overflow-y-auto" style="scrollbar-width: thin;">
        <div class="flex flex-col">
            <h3 class="text-[25px] font-semibold">Visibility</h3>
            <p class="text-[13px] font-normal">Choose when to publish and who can see your video</p>
        </div>
        <div class="first-container flex-row w-[532px] rounded-lg flex mt-4 border-black border
         pl-4 pt-4" :style="{ height: openVisibility ? '220px' : '80px' }">
            <div class="flex flex-col gap-y-2">
                <div class="w-full flex flex-col">
                    <p class="text-[15px] font-medium">Save or publish</p>
                    <p class="text-[13px] font-normal">Make your video public or private</p>
                </div>
                <div v-if="openVisibility" @click="videoVisibility = 'private'"
                    class="flex flex-col pl-6 mt-4 cursor-pointer">
                    <div class="flex flex-row justify-start items-start">
                        <input v-model="videoVisibility" value="private" :checked="videoVisibility === 'private'"
                            name="visibility" class="w-[20px] h-[20px]" type="radio">
                        <div class="flex flex-col ml-2">
                            <p class="text-[15px] font-normal">Private</p>
                            <span class="text-[13px] font-normal">Only yourself can see the video</span>
                        </div>
                    </div>
                </div>
                <div v-if="openVisibility" @click="videoVisibility = 'public'"
                    class="flex flex-col pl-6 mt-4 cursor-pointer mb-10">
                    <div class="flex flex-row justify-start items-start">
                        <input v-model="videoVisibility" value="public" :checked="videoVisibility === 'public'"
                            name="visibility" class="w-[20px] h-[20px]" type="radio">
                        <div class="flex flex-col ml-2">
                            <p class="text-[15px] font-normal">Public</p>
                            <span class="text-[13px] font-normal">Everyone can see</span>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="!openVisibility" @click="toggleOpenVisibility"
                class="justify-self-end self-center ml-auto mr-4 mb-2">
                <button class="w-[39.2px] h-[39.2px] flex justify-center items-center rounded-full hover:bg-[#f9f9f9]">
                    <img class="w-[14px] h-[14px]" :src="arrowIcon" alt="">
                </button>
            </div>
        </div>
        <div class="second-container flex-row gap-y-2 w-[532px] rounded-lg flex mt-4 border-black border
         pl-4 pt-4" :style="{height: openVisibility ? '80px' : '239px'}">
            <div class="flex flex-col gap-y-2">
                <div class="w-full">
                    <p class="text-[15px] font-medium">Schedule</p>
                    <p class="text-[13px] font-normal">Select a date to make your video public.</p>
                </div>
                <div v-if="!openVisibility" class="flex flex-col">
                    <p class="text-[15px] font-normal">Schedule as public</p>
                    <div class="flex flex-row gap-x-2 items-center justify-start">
                        <div class="card flex justify-center my-2">
                            <VueDatePicker required autocomplete v-model="date" :format="format"></VueDatePicker>
                        </div>
                    </div>
                </div>
                <div v-if="!openVisibility">
                    <p class="text-[13px] font-normal text-gray-600 -mt-2 mb-1">Noticable: The date which you choose is
                        in your local timezone</p>
                    <p class="text-[13px] font-normal text-gray-600 mb-4">Video will be private before publishing</p>
                </div>
            </div>
            <div v-if="openVisibility" @click="toggleOpenVisibility"
                class="justify-self-end self-center ml-auto mr-4 mb-2">
                <button class="w-[39.2px] h-[39.2px] flex justify-center items-center rounded-full hover:bg-[#f9f9f9]">
                    <img class="w-[14px] h-[14px]" :src="arrowIcon" alt="">
                </button>
            </div>
        </div>
    </div>
</template>