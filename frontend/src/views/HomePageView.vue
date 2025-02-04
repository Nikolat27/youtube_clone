<script setup>
import { onMounted, reactive, ref, watch, computed } from 'vue';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue';
import axios from 'axios';
import { sharedState } from '@/sharedState';

const isSideBarCollapsed = ref(false)
watch(() => sharedState.isWebsiteSideBarCollapsed, (newVal) => {
    isSideBarCollapsed.value = newVal
})


const isAtStart = ref(true);
const isAtEnd = ref(false);


const updateScrollState = (shortContainerDiv) => {
    const scrollLeft = shortContainerDiv.scrollLeft;
    const maxScrollWidth = shortContainerDiv.scrollWidth - shortContainerDiv.clientWidth;
    isAtStart.value = scrollLeft <= 0;
    isAtEnd.value = scrollLeft >= maxScrollWidth;
};


// Infinite scrolling Management
const infiniteIsLoading = ref(false)
const page = ref(1)
const size = ref(12)

const checkScroll = () => {
    const endOfPage = window.innerHeight + window.pageYOffset >= document.documentElement.scrollHeight - 150
    const lastPage = page.value == totalPages.value
    if (!lastPage && endOfPage && !infiniteIsLoading.value) {
        loadMoreVideos()
    }
}

const isLoading = ref(false)
const shortVideos = reactive([])
const longVideos = reactive([])
const totalPages = ref(null)

const retrieveVideos = () => {
    isLoading.value = true
    axios.get(`${sharedState.websiteUrl}/videos/`, {
        params: {
            size: size.value,
            page: page.value,
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 200) {
            totalPages.value = response.data.data.long_videos.pages
            shortVideos.splice(0, shortVideos.length, ...response.data.data.short_videos)
            longVideos.splice(0, longVideos.length, ...response.data.data.long_videos.items)
        }
    }).catch((error) => {
        console.error(error)
    }).finally(() => isLoading.value = false)
}

const loadMoreVideos = async () => {
    infiniteIsLoading.value = true
    page.value += 1
    await axios.get(`${sharedState.websiteUrl}/videos/load-more`, {
        params: {
            page: page.value,
            size: size.value,
        }
    }).then((response) => {
        longVideos.splice(longVideos.length, 0, ...response.data.data.long_videos.items)
    }).catch((error) => console.error(error))
        .finally(() => infiniteIsLoading.value = false)
}


const isSideBarClosed = ref(false)
const resizeHandle = () => {
    const windowWidth = window.innerWidth
    if (windowWidth > 650) {
        sharedState.isWebsiteSideBarCollapsed = false
        sharedState.isWebsiteSideBarClosed = false
        isSideBarClosed.value = false
    } else if (windowWidth >= 553 && windowWidth <= 650) {
        sharedState.isWebsiteSideBarCollapsed = true
        sharedState.isWebsiteSideBarClosed = false
        isSideBarClosed.value = false
    } else if (windowWidth < 553) {
        sharedState.isWebsiteSideBarClosed = true
        isSideBarClosed.value = true
    }
}


const containerLeftPositionStyles = computed(() => {
    if (isSideBarCollapsed.value && !isSideBarClosed.value) {
        return '85px'
    } else if (!isSideBarCollapsed.value && !isSideBarClosed.value) {
        return '230px'
    } else if (isSideBarClosed.value) {
        return '8px'
    }
})


let maxRegularVideoWidth = 400
let maxShortVideoWidth = 233
let totalRegularVideos
let totalShortVideos
const calculateDivSizes = () => {
    // This func is for calculating how many videos should i place in each row.
    const homeContainer = document.querySelector('.home-page-container')
    let containerInnerWidth = homeContainer.clientWidth
    totalRegularVideos = Math.floor(containerInnerWidth / maxRegularVideoWidth)
    totalShortVideos = Math.floor(containerInnerWidth / maxShortVideoWidth)
}

const isVideoDeleted = ref(false)
onMounted(() => {
    const shortContainerDiv = document.getElementById("shortVideoScrollDiv");
    updateScrollState(shortContainerDiv);
    retrieveVideos()
    resizeHandle()

    calculateDivSizes()
    document.addEventListener("scroll", checkScroll)
    window.addEventListener("resize", resizeHandle)
});
</script>

<template>
    <div v-if="!isLoading"
        class="home-page-container flex flex-row flex-wrap relative top-[85px] gap-x-[25px] gap-y-[18px] w-full pb-24"
        :style="{ left: containerLeftPositionStyles }">
        <div class="regular-videos flex-wrap w-[80%] gap-y-4">
            <div v-for="video in longVideos.slice(0, totalRegularVideos)" :key="video.id" class="regular-video"
                :class="[isSideBarCollapsed ? 'w-[33%] max-w-[450px]' : 'w-[29.5%] max-w-[400px]', isVideoDeleted ? 'w-[49%]' : 'w-[29.5%]']">
                <router-link :to="`/video/${video.unique_id}`">
                    <div class="video-thumbnail w-full h-[225px] mb-[10px] relative z-0">
                        <img class="w-full h-full" loading="lazy" :src="video.thumbnail_url" alt="">
                        <input v-if="video.watch_progress" type="range" :value="video.watch_progress" disabled
                            class="z-10 watch-progress-tracking w-full bg-transparent absolute -bottom-[8px] left-0">
                    </div>
                </router-link>
                <div class="video-info">
                    <router-link :to="`/channel-page/${video.channel_unique_identifier}`">
                        <div class="channel-logo">
                            <img loading="lazy" :src="video.channel_profile_picture" alt="">
                        </div>
                    </router-link>
                    <div class="video-title-div ml-2">
                        <router-link :to="`/video/${video.unique_id}`">
                            <p class="video-title">{{ video.title }}</p>
                        </router-link>
                        <router-link :to="`/channel-page/${video.channel_unique_identifier}`">
                            <p class="video-channel-name">{{ video.channel_name }}</p>
                        </router-link>
                        <p class="video-stats">{{ video.views }} views . {{ video.created_at }}</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="w-full h-[500px] gap-y-6 flex flex-col mt-14">
            <div class="justify-start items-center w-full">
                <img class="w-[45px] h-[35px]" src="/src/assets/icons/side-bar/youtube-shorts.jpg" alt="">
            </div>
            <div id="shortVideoScrollDiv" class="w-full">
                <div
                    class="flex flex-row w-[92%] overflow-hidden gap-x-[12px] scroll-smooth justify-start items-center">
                    <div v-for='short in shortVideos.slice(0, totalShortVideos)' :key="short.id"
                        class="flex flex-col gap-y-4 flex-shrink-0 w-[233px] h-[414px] max-h-[414px]">
                        <router-link :to="`/short/${short.unique_id}`">
                            <div class="w-full h-full">
                                <img style="height: 331px; max-height: 331px;"
                                    class="w-full h-full rounded-lg object-cover" loading="lazy"
                                    :src="short.thumbnail_url" alt="">
                            </div>
                        </router-link>
                        <div>
                            <p class="short-video-title">{{ short.title }}</p>
                            <p class="short-video-views">{{ short.views ?? 0 }} view</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="true" class="flex flex-row gap-y-4 flex-wrap gap-x-[15px] flex-grow w-[80%]">
            <div v-for="video in longVideos.slice(totalRegularVideos)" :key="video.id" class="regular-video"
                :class="[isSideBarCollapsed ? 'w-[33%] max-w-[450px]' : 'w-[29.5%] max-w-[400px]', isVideoDeleted ? 'w-[49%]' : 'w-[29.5%]']">
                <router-link :to="`/video/${video.unique_id}`">
                    <div class="video-thumbnail w-full h-[225px] mb-[10px] relative z-0">
                        <img class="w-full h-full" loading="lazy" :src="video.thumbnail_url" alt="">
                        <input v-if="video.watch_progress" type="range" :value="video.watch_progress" disabled
                            class="z-10 watch-progress-tracking w-[400px] bg-transparent absolute -bottom-[10px] left-0">
                    </div>
                </router-link>
                <div class="video-info">
                    <router-link :to="`/channel-page/${video.channel_unique_identifier}`">
                        <div class="channel-logo">
                            <img loading="lazy" :src="video.channel_profile_picture" alt="">
                        </div>
                    </router-link>
                    <div class="video-title-div ml-2">
                        <router-link :to="`/video/${video.unique_id}`">
                            <p class="video-title">{{ video.title }}</p>
                        </router-link>
                        <p class="video-channel-name">{{ video.channel_name }}</p>
                        <p class="video-stats">{{ video.views }} views . {{ video.created_at }}</p>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="infiniteIsLoading" class="w-full flex justify-center items-center md:mr-[300px] my-16">
            <ClipLoader size="45px" color="red"></ClipLoader>
        </div>
        <!-- <div v-if="infiniteIsLoading" class="skeleton-loaders flex flex-row">
            <div>
                <div class="video-preview">
                    <div class="video-thumbnail bg-gray-300 opacity-70 rounded-lg">
                    </div>
                    <div class="video-info flex flex-row">
                        <div class="channel-logo bg-gray-300 opacity-70 rounded-full">
                        </div>
                        <div class="video-title-div ml-2">
                            <p class="w-[280px] h-[16px] rounded-lg bg-gray-300 opacity-70"></p>
                            <p class="w-[140px] mt-2 h-[12px] rounded-lg bg-gray-300 opacity-70"></p>
                        </div>
                    </div>
                </div>
            </div>
            <div>
                <div class="video-preview">
                    <div class="video-thumbnail bg-gray-300 opacity-70 rounded-lg">
                    </div>
                    <div class="video-info">
                        <div class="channel-logo bg-gray-300 opacity-70 rounded-full">
                        </div>
                        <div class="video-title-div ml-2">
                            <p class="w-[280px] h-[16px] rounded-lg bg-gray-300 opacity-70"></p>
                            <p class="w-[140px] mt-2 h-[12px] rounded-lg bg-gray-300 opacity-70"></p>
                        </div>
                    </div>
                </div>
            </div>
            <div>
                <div class="video-preview">
                    <div class="video-thumbnail bg-gray-300 opacity-70 rounded-lg">
                    </div>
                    <div class="video-info">
                        <div class="channel-logo bg-gray-300 opacity-70 rounded-full">
                        </div>
                        <div class="video-title-div ml-2">
                            <p class="w-[280px] h-[16px] rounded-lg bg-gray-300 opacity-70"></p>
                            <p class="w-[140px] mt-2 h-[12px] rounded-lg bg-gray-300 opacity-70"></p>
                        </div>
                    </div>
                </div>
            </div>
        </div> -->
    </div>
    <div v-else class="w-full h-[100vh] flex justify-center items-center">
        <PulseLoader color="red" size="20px"></PulseLoader>
    </div>
</template>
<style scoped>
@media screen and (max-width: 740px) {
    .regular-video {
        width: 100%;
    }
}

@media screen and (max-width: 550px) {
    .short-video-preview {
        max-width: 70%;
    }
}

.watch-progress-tracking {
    cursor: default;
}

.watch-progress-tracking::-moz-range-progress {
    height: 4px;
    background: red;
}

.watch-progress-tracking::-moz-range-thumb {
    visibility: hidden;
}

.watch-progress-tracking::-moz-range-track {
    height: 4px;
    background: #909090;
}
</style>