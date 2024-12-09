<script setup>
// Icons
import hamburgerBtn from '/src/assets/icons/svg-icons/collapse-menu-icon.svg'
import ytLogo from '/src/assets/img/yt-studio-logo.svg'
import searchIcon from '/src/assets/icons/svg-icons/search-icon.svg'
import createVideo from '/src/assets/icons/svg-icons/create-video-icon.svg'
import channelProfile from '/src/assets/img/Ruby.png'
</script>

<template>
    <header class="font-roboto flex flex-row w-full h-[63.2px] mx-auto bg-white z-50 fixed shadow-lg
     justify-start items-center">
        <div class="left-section w-[20%] h-full flex flex-row justify-start items-center pl-5">
            <button
                class="w-[43.2px] h-[43.2px] rounded-full hover:bg-[#f0f0f0] flex justify-center items-center mr-[16px] flex-shrink-0 flex-grow-0">
                <img class="w-[22px] h-[22px] flex-shrink-0 flex-grow-0" :src="hamburgerBtn" alt="">
            </button>
            <img class="w-[98.4px] min-w-[98.4px] h-[24px] cursor-pointer" :src="ytLogo" alt="">
        </div>
        <div class="middle-section w-[60%] h-full flex justify-center items-center flex-row">
            <div style="width: 60%;"
                class="bg-[#f1f1f1] flex justify-start items-center flex-row rounded-[20px] border border-transparent hover:border-black transition duration-75">
                <img class="w-[20px] h-[20px] mx-4" :src="searchIcon" alt="">
                <input
                    class="bg-transparent w-full h-[40px] outline-none text-[15px] font-normal placeholder:font-normal placeholder:text-[15px] placeholder:text-[#757577]"
                    type="text" placeholder="Search across your channel">
            </div>
        </div>
        <div class="right-section w-[20%] h-full flex flex-row justify-self-end ml-auto justify-end
         items-center pr-6 gap-x-4">
            <button class="flex-grow-0 flex-shrink-0 hover:bg-[#e5e5e5] flex flex-row justify-center items-center pl-1 gap-x-2
             w-[95px] h-[34px] rounded-3xl border border-gray-200">
                <img class="w-[20px] h-[20px]" :src="createVideo" alt="">
                <p class="text-[14px] font-medium">Create</p>
            </button>
            <img class="w-[32px] h-[32px] rounded-full cursor-pointer" :src="channelProfile" alt="">
        </div>
    </header>
</template>
<style scoped>
@media (max-width: 740px) {
    .middle-section {
        display: none;
    }
}
</style>