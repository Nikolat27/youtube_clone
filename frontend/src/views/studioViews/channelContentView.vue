<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';

// Icons
import arrowBottomIcon from '@/assets/icons/svg-icons/arrow-bottom-icon.svg'

// Router
const router1 = useRoute()
const router2 = useRouter()

// Filter options Management
const isFilterOptionsOpen = ref(false)
const toggleFilterOptions = () => isFilterOptionsOpen.value = !isFilterOptionsOpen.value

// Filtering Videos Management
const filterVideos = (filter) => {
    router2.push({ name: router1.name, query: { ...router1.query, 'filter': filter } })
    isFilterOptionsOpen.value = false
}

// Sorting Videos Management
const sortState = ref('DESC')
const sortVideos = (sortByType) => {
    sortState.value = sortState.value === 'ASC' ? 'DESC' : 'ASC'
    router2.push({
        name: router1.name,
        query: { ...router1.query, 'sortByType': sortByType, 'sortByOrder': sortState.value }
    })
}
</script>

<template>
    <main id="channel-content" class="flex flex-col absolute w-[1270px] h-[100%] left-[82px] top-[90px]
     justify-start items-start">
        <div class="channel-main-content w-full">
            <div>
                <h1 class="text-[25px] font-semibold mb-7">Channel content</h1>
            </div>
            <div class="chnl-tab-content flex flex-row gap-x-6 border-b border-[#f1f1f1] w-[100%] h-[48px]">
                <router-link :class="$route.query.type === 'long_video' || ($route.name === 'videos' && !$route.query.type) ? 'active' : ''"
                    to="/studio/channel-content/videos?type=long_video">Videos</router-link>
                <router-link :class="$route.query.type === 'short_video' ? 'active' : ''"
                    to="/studio/channel-content/videos?type=short_video">Shorts</router-link>
                <!-- <router-link :class="$route.name === 'lives' ? 'active' : ''"
                    to="/studio/channel-content/lives">Lives</router-link> -->
                <router-link :class="$route.name === 'posts' ? 'active' : ''"
                    to="/studio/channel-content/posts">Posts</router-link>
                <router-link :class="$route.name === 'playlists' ? 'active' : ''" to="/studio/channel-content/playlists"
                    style="width: 56px;">Playlists</router-link>
            </div>
            <div class="chnl-filter-bar flex flex-row justify-start items-center gap-x-6
         border-b border-[#f1f1f1] w-[100%] h-[48px] mt-1 relative">
                <img @click="toggleFilterOptions" class="w-6 h-6 cursor-pointer"
                    src="@/assets/icons/svg-icons/filter-filtering-icon.svg" alt="">
                <input class="w-[70%] h-[48px] outline-none" type="text" placeholder="Filter">
                <div v-if="isFilterOptionsOpen" class="z-20 filter-options flex flex-col justify-center items-center w-[145px] h-[160px] bg-white
             rounded-lg text-[15px] font-normal font-roboto absolute top-[48px] left-[46px]"
                    style="padding-left: 0px;">
                    <div :class="[$route.query.filter == 'age-restriction' ? 'bg-gray-300 hover:bg-gray-300' : 'hover:bg-[#f9f9f9]']"
                        @click="filterVideos('age-restriction')">
                        Age restriction</div>
                    <div :class="[$route.query.filter == 'made-for-kids' ? 'bg-gray-300 hover:bg-gray-300' : 'hover:bg-[#f9f9f9]']"
                        @click="filterVideos('made-for-kids')">Made for kids</div>
                    <div :class="[$route.query.filter == 'views' ? 'bg-gray-300 hover:bg-gray-300' : 'hover:bg-[#f9f9f9]']"
                        @click="filterVideos('views')">
                        Views</div>
                    <div :class="[$route.query.filter == 'visibility' ? 'bg-gray-300' : 'hover:bg-[#f9f9f9]']"
                        @click="filterVideos('visibility')">Visibility</div>
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
                    <button v-if="!router1.query.sortByType || $route.query.sortByType === 'date'"
                        @click="sortVideos('date')" class="cursor-pointer mr-8 ml-8 text-black font-bold text-[14px] flex flex-row
                            justify-center items-center">
                        <span>Date</span>
                        <img :class="[(!router1.query.sortByType || $route.query.sortByType === 'date') && sortState === 'ASC' ? 'rotate-180' : '']"
                            class="w-[10px] h-[10px] ml-1" :src="arrowBottomIcon" alt="">
                    </button>
                    <span v-else @click="sortVideos('date')"
                        class="mr-8 ml-8 hover:text-black cursor-pointer">Date</span>
                    <button v-if="$route.query.sortByType === 'views'" @click="sortVideos('views')" class="cursor-pointer text-black font-bold text-[14px] flex flex-row
                        justify-center items-center">
                        <span>Views</span>
                        <img :class="[$route.query.sortByType === 'views' && sortState === 'ASC' ? 'rotate-180' : '']"
                            class="w-[10px] h-[10px] ml-1" :src="arrowBottomIcon" alt="">
                    </button>
                    <span v-else @click="sortVideos('views')" class="hover:text-black cursor-pointer">Views</span>
                    <span>Comments</span>
                    <span>Likes (vs. dislikes)</span>
                </div>
            </div>
        </div>

        <!-- View starts here -->
        <router-view></router-view>
        <!-- Views End here -->

    </main>
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