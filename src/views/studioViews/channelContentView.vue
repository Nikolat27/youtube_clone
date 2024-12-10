<script setup>
import { ref } from 'vue';

// Icons
import arrowBottomIcon from '@/assets/icons/svg-icons/arrow-bottom-icon.svg'
import youtubeIcon from '@/assets/icons/svg-icons/youtube-icon.svg'

// Filter options Management
const isFilterOptionsOpen = ref(false)
const toggleFilterOptions = () => isFilterOptionsOpen.value = !isFilterOptionsOpen.value
</script>

<template>
    <main id="channel-content" class="flex flex-col absolute w-[1270px] h-[100%] left-[82px] top-[90px]
     justify-start items-start">
        <div class="channel-main-content w-full">
            <div>
                <h1 class="text-[25px] font-semibold mb-7">Channel content</h1>
            </div>
            <div class="chnl-tab-content flex flex-row gap-x-6 border-b border-[#f1f1f1] w-[100%] h-[48px]">
                <router-link class="active" data-target="videos">Videos</router-link>
                <router-link class="" data-target="shorts">Shorts</router-link>
                <router-link class="" data-target="live">Live</router-link>
                <router-link class="" data-target="posts">Posts</router-link>
                <router-link class="" data-target="playlists" style="width: 56px;">Playlists</router-link>
            </div>
            <div class="chnl-filter-bar flex flex-row justify-start items-center gap-x-6
         border-b border-[#f1f1f1] w-[100%] h-[48px] mt-1 relative">
                <img @click="toggleFilterOptions" class="w-6 h-6 cursor-pointer"
                    src="@/assets/icons/svg-icons/filter-filtering-icon.svg" alt="">
                <input class="w-[70%] h-[48px] outline-none" type="text" placeholder="Filter">
                <div v-if="isFilterOptionsOpen" class="filter-options flex flex-col justify-center items-center w-[145px] h-[248px] bg-white
             rounded-lg text-[15px] font-normal font-roboto absolute top-[48px] left-[46px]">
                    <div>Age restriction</div>
                    <div>Copyright</div>
                    <div>Description</div>
                    <div>Made for kids</div>
                    <div>Title</div>
                    <div>Views</div>
                    <div>Visibility</div>
                </div>
            </div>
            <div class="table-header flex flex-row items-center w-full h-[47px]
         text-[12px] font-medium font-roboto text-[#767474] border-b" style="padding-left: 0px;">
                <div class="left-side w-[30%] h-[47px] flex flex-row justify-start items-center gap-x-4">
                    <input type="checkbox" class="w-[18px] h-[18px] rounded-md border-[#909090] cursor-pointer">
                    <span>Video</span>
                </div>
                <div class="right-side flex flex-row justify-end items-center w-[70%] h-[47px] gap-x-6 ml-8">
                    <span>Visiblity</span>
                    <span>Restrictions</span>
                    <button class="cursor-pointer mr-8 ml-8 text-black font-bold text-[14px] flex flex-row
                 justify-center items-center">
                        <span>Date</span>
                        <img class="w-[10px] h-[10px] ml-1" :src="arrowBottomIcon" alt="">
                    </button>
                    <span>Views</span>
                    <span>Comments</span>
                    <span>Likes (vs. dislikes)</span>
                </div>
            </div>
        </div>
        <div class="table-itself border-b font-roboto pl-[48px]">
            <div class="video-thumbnail">
                <img draggable="false" src="@/assets/img/Django.png" alt="">
                <span class="video-duration">2:28</span>
            </div>
            <div class="video-detail flex flex-col font-normal text-[13px] mt-2" style="padding-left: 12px;">
                <span>video title</span>
                <span>video description</span>
                <div class="flex flex-row justify-start items-center">
                    <button class="w-[39.2px] h-[39.2px] rounded-full hover:bg-[#eaeaea] flex items-center
                     justify-center">
                        <img class="w-[24px] h-[24px] center" :src="youtubeIcon" alt="">
                    </button>
                </div>
            </div>
        </div>
    </main>
</template>

<style scoped>
@media (min-width: 1200px) {
    #channel-content {
        left: 254px;
        top: 100px;
    }
}

.channel-main-content div {
    padding-left: 48px;
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

.right-side span {
    cursor: pointer;
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

.filter-options div:hover {
    background-color: #f9f9f9;
}
</style>