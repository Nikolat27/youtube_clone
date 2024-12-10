<script setup>
import { ref, reactive, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

// Icons
import arrowBottomIcon from '@/assets/icons/svg-icons/arrow-bottom-icon.svg'
import youtubeIcon from '@/assets/icons/svg-icons/youtube-icon.svg'
import editIcon from '@/assets/icons/svg-icons/edit-icon.svg'
import kebabMenuIcon from '@/assets/icons/svg-icons/kebab-menu.svg'
import downloadIcon from '@/assets/icons/svg-icons/download-icon2.svg'
import uninstallIcon from '@/assets/icons/svg-icons/uninstall-icon.svg'

// Router
const router1 = useRoute()
const router2 = useRouter()

// Filter options Management
const isFilterOptionsOpen = ref(false)
const toggleFilterOptions = () => isFilterOptionsOpen.value = !isFilterOptionsOpen.value


// Generate some fake videos
const videos = reactive([])
for (let i = 1; i <= 3; i++) {
    videos.push({ id: i, title: `${i} video title`, description: `${i} video description` })
}

// Edit Video Title Management
const videoTitle = ref('')
const videoTitleLength = computed(() => videoTitle.value.length)

const videoTitleEdit = (event) => {
    videoTitle.value = event.target.value;
}
const userAbleToSave = computed(() => { // User can only save the information if the title`s length is equal or greater than 0
    return (videoTitle.value.length > 0 ? true : false)
})

// Edit Video Description Management
const videoDescription = ref('')
const videoDescriptionLength = computed(() => videoDescription.value.length)
const videoDescriptionEdit = (event) => {
    videoDescription.value = event.target.value;
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


// Filtering Videos Management
const filterVideos = (filter) => {
    router2.push({ name: 'channel-content', query: { ...router1.query, 'filter': filter } })
}

// Sorting Videos Management
const sortState = ref('DESC')
const sortVideos = (sortByType) => {
    sortState.value = sortState.value === 'ASC' ? 'DESC' : 'ASC'
    router2.push({ name: 'channel-content', query: { ...router1.query, 'sortByType': sortByType, 'sortByOrder': sortState.value } })
}

watch(() => router1.query.sortBy, () => {

})
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
        <div class="border-b font-roboto pl-[48px] w-full">
            <div v-for="video in videos" :key="video.id" class="table-itself border-b">
                <div class="video-thumbnail">
                    <img draggable="false" src="@/assets/img/Django.png" alt="">
                    <span class="video-duration">2:28</span>
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
                        <button class="w-[39.2px] h-[39.2px] rounded-full hover:bg-[#eaeaea] flex items-center
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
                        <div v-if="videoOptionStates[video.id]?.editDiv" class="edit-title-description bg-white z-40 w-[488px] h-[368px] rounded-lg
                         flex flex-col justify-start pt-2 items-center gap-y-4 absolute left-2 top-6">
                            <div class="w-[464px] h-[91px] rounded-lg border border-solid box-border border-[#d6d6d6] hover:border-black hover:border-2
                             focus:border-2 relative pl-2 pt-2"
                                :style="{ borderColor: userAbleToSave ? 'black' : 'red', borderWidth: !userAbleToSave ? '2px' : '1px' }">
                                <span class="text-[12px] font-medium text-gray-600">Title (required)</span>
                                <textarea @input="videoTitleEdit" v-model="videoTitle"
                                    class="mt-1 edit-title-input w-[440px] h-[41px] outline-none text-[15px] font-normal overflow-hidden leading-4"
                                    placeholder="Add title" minlength="1" required maxlength="100"></textarea>
                                <span class="text-[12px] font-normal absolute right-1 bottom-1 text-gray-700"><span
                                        class="title-char-counter">{{ videoTitleLength }}</span>/100</span>
                            </div>
                            <div
                                class="w-[464px] relative max-w-[464px] h-[201px] max-h-[201px] rounded-lg border border-[#d6d6d6] pl-2 pt-2 hover:border-black hover:border-2">
                                <span class="text-[12px] font-medium text-gray-600">Description</span>
                                <textarea style="scrollbar-width: thin;" @input="videoDescriptionEdit"
                                    v-model="videoDescription"
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
                        </div>
                    </div>
                </div>
                <div class="video-info w-[70%] relative h-full flex flex-row justify-end items-center text-[13px] font-normal
                 ml-auto mr-8">
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[355px]">Draft</p>
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[430px]">None</p>
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[525px]">1/1/2024</p>
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[635px]">101K </p>
                    <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[710px]">2k</p>
                    <p class="ml-8 absolute top-1/3 transform translate-y-1/3 left-[775px]">2k, 3k</p>
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