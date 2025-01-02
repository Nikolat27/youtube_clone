<script setup>
import { onMounted, reactive, ref } from 'vue';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue';
import axios from 'axios';

const isAtStart = ref(true);
const isAtEnd = ref(false);
let scrolledAmount = ref(0);
const itemWidth = 300;

const updateScrollState = (shortContainerDiv) => {
    const scrollLeft = shortContainerDiv.scrollLeft;
    const maxScrollWidth = shortContainerDiv.scrollWidth - shortContainerDiv.clientWidth;
    isAtStart.value = scrollLeft <= 0;
    isAtEnd.value = scrollLeft >= maxScrollWidth;
};

const handleScrollLeft = () => {
    const shortContainerDiv = document.getElementById("shortVideoScrollDiv");
    scrolledAmount.value -= itemWidth;
    shortContainerDiv.scrollLeft = scrolledAmount.value;
    updateScrollState(shortContainerDiv);
};

const handleScrollRight = () => {
    const shortContainerDiv = document.getElementById("shortVideoScrollDiv");
    scrolledAmount.value += itemWidth;
    shortContainerDiv.scrollLeft = scrolledAmount.value;
    updateScrollState(shortContainerDiv);
};


// Infinite scrolling Management
const infiniteIsLoading = ref(false)
const page = ref(1)
const size = ref(12)
const checkScroll = () => {
    const endOfPage = window.innerHeight + window.pageYOffset >= document.documentElement.scrollHeight - 150
    const lastPage = page.value == totalPages.value
    if (!lastPage && endOfPage && !infiniteIsLoading.value) {
        console.log("hi")
        loadMoreVideos()
    }
}

const isLoading = ref(false)
const shortVideos = reactive([])
const longVideos = reactive([])
const totalPages = ref(null)
const retrieveVideos = () => {
    isLoading.value = true
    axios.get("http://127.0.0.1:8000/videos/", {
        params: {
            size: size.value,
            page: page.value
        }
    }).then((response) => {
        if (response.status == 200) {
            totalPages.value = response.data.data.long_videos.pages
            shortVideos.splice(0, shortVideos.length, ...response.data.data.short_videos)
            longVideos.splice(0, longVideos.length, ...response.data.data.long_videos.items)
        }
    }).catch((error) => {
        console.log(error)
    }).finally(() => isLoading.value = false)
}

const loadMoreVideos = async () => {
    infiniteIsLoading.value = true
    page.value += 1
    await axios.get("http://127.0.0.1:8000/videos/load-more", {
        params: {
            page: page.value,
            size: size.value,
        }
    }).then((response) => {
        longVideos.splice(longVideos.length, 0, ...response.data.data.long_videos.items)
    }).catch((error) => console.log(error))
        .finally(() => infiniteIsLoading.value = false)

    console.log(page.value)
}

onMounted(() => {
    const shortContainerDiv = document.getElementById("shortVideoScrollDiv");
    updateScrollState(shortContainerDiv);
    retrieveVideos()

    document.addEventListener("scroll", checkScroll)
});
</script>

<template>
    <div v-if="!isLoading" class="container mb-10">
        <div class="regular-videos">
            <div v-for="video in longVideos.slice(0, 3)" :key="video.id" class="video-preview">
                <div class="video-thumbnail">
                    <img loading="lazy" :src="video.thumbnail_url" alt="">
                </div>
                <div class="video-info">
                    <div class="channel-logo">
                        <img loading="lazy" src="@/assets/img/Django.png" alt="">
                    </div>
                    <div class="video-title-div ml-2">
                        <router-link :to="`/video/${video.id}`">
                            <p class="video-title">{{ video.title }}</p>
                        </router-link>
                        <p class="video-channel-name">Channel name</p>
                        <p class="video-stats">409K views . {{ video.created_at }}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="short-videos-div">
            <img class="youtube-short-icon-videos" src="@/assets/icons/side-bar/youtube-shorts.jpg" alt="">
            <button @click="handleScrollLeft"
                :class="[isAtStart ? 'invisible' : '', 'navigate-btn', 'justify-center', 'items-center', 'ml-12']">
                <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" shape-rendering="geometricPrecision"
                    text-rendering="geometricPrecision" image-rendering="optimizeQuality" fill-rule="evenodd"
                    clip-rule="evenodd" viewBox="0 0 267 512.43">
                    <path fill-rule="nonzero"
                        d="M263.78 18.9c4.28-4.3 4.3-11.31.04-15.64a10.865 10.865 0 0 0-15.48-.04L3.22 248.38c-4.28 4.3-4.3 11.31-.04 15.64l245.16 245.2c4.28 4.3 11.22 4.28 15.48-.05s4.24-11.33-.04-15.63L26.5 256.22 263.78 18.9z" />
                </svg>
            </button>

            <div id="shortVideoScrollDiv" class="flex flex-row overflow-hidden gap-x-[30px] scroll-smooth">
                <div v-for='short in shortVideos' :key="short.id" class=" select-none short-video-preview">
                    <div class="short-video-thumbnail">
                        <img loading="lazy" src="@/assets/img/Django.png" alt="">
                    </div>
                    <div class="short-video-title-div">
                        <p class="short-video-title"><a href="">{{ short.title }}</a></p>
                        <p class="short-video-views">{{ short.view }} view</p>
                    </div>
                </div>
            </div>

            <button @click="handleScrollRight"
                :class="[isAtEnd ? 'invisible' : '', 'navigate-btn', 'justify-center', 'items-center', 'mr-10']">
                <svg class=" w-5 h-5 rotate-180" xmlns="http://www.w3.org/2000/svg" shape-rendering="geometricPrecision"
                    text-rendering="geometricPrecision" image-rendering="optimizeQuality" fill-rule="evenodd"
                    clip-rule="evenodd" viewBox="0 0 267 512.43">
                    <path fill-rule="nonzero"
                        d="M263.78 18.9c4.28-4.3 4.3-11.31.04-15.64a10.865 10.865 0 0 0-15.48-.04L3.22 248.38c-4.28 4.3-4.3 11.31-.04 15.64l245.16 245.2c4.28 4.3 11.22 4.28 15.48-.05s4.24-11.33-.04-15.63L26.5 256.22 263.78 18.9z" />
                </svg>
            </button>
        </div>

        <div v-for="video in longVideos.slice(3)" :key="video.id" class="video-preview">
            <div class="video-thumbnail">
                <img :src="video.thumbnail_url" alt="">
            </div>
            <div class="video-info">
                <div class="channel-logo">
                    <img loading="lazy" src="@/assets/img/Django.png" alt="">
                </div>
                <div class="video-title-div">
                    <router-link :to="`/video/${video.id}`">
                        <p class="video-title">{{ video.title }}</p>
                    </router-link>
                    <p class="video-channel-name">Channel name</p>
                    <p class="video-stats">409K views . {{ video.created_at }}</p>
                </div>
            </div>
        </div>

        <!-- <div v-if="infiniteIsLoading" class="w-full flex justify-center items-center mr-[300px] my-16">
            <ClipLoader size="45px" color="red"></ClipLoader>
        </div> -->
        <div v-if="infiniteIsLoading" class="skeleton-loaders flex flex-row">
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
        </div>
    </div>
    <div v-else class="w-full h-[100vh] flex justify-center items-center">
        <PulseLoader color="red" size="20px"></PulseLoader>
    </div>
</template>