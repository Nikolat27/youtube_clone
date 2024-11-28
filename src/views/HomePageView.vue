<script setup>
import { onMounted, ref, watch } from 'vue';
import { useInfiniteScroll } from '@vueuse/core'

const shortVideos = [
    { title: "Django Tutorial", view: "100K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
    { title: "Django Tutorial", view: "120K" },
]

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


onMounted(() => {
    const shortContainerDiv = document.getElementById("shortVideoScrollDiv");
    updateScrollState(shortContainerDiv);
});
</script>

<template>
    <div class="container">
        <div class="regular-videos">
            <div class="video-preview">
                <div class="video-thumbnail">
                    <img src="@/assets/img/Django.png" alt="">
                </div>
                <div class="video-info">
                    <div class="channel-logo">
                        <img src="@/assets/img/Django.png" alt="">
                    </div>
                    <div class="video-title-div">
                        <p class="video-title"><a href="">Django Tutorial</a></p>
                        <p class="video-channel-name">Channel name</p>
                        <p class="video-stats">409K views . 2 months ago</p>
                    </div>
                </div>
            </div>
            <div class="video-preview">
                <div class="video-thumbnail">
                    <img src="@/assets/img/Django.png" alt="">
                </div>
                <div class="video-info">
                    <div class="channel-logo">
                        <img src="@/assets/img/Django.png" alt="">
                    </div>
                    <div class="video-title-div">
                        <p class="video-title"><a href="">Django Tutorial</a></p>
                        <p class="video-channel-name">Channel name</p>
                        <p class="video-stats">409K views . 2 months ago</p>
                    </div>
                </div>
            </div>
            <div class="video-preview">
                <div class="video-thumbnail">
                    <img src="@/assets/img/Django.png" alt="">
                </div>
                <div class="video-info">
                    <div class="channel-logo">
                        <img src="@/assets/img/Django.png" alt="">
                    </div>
                    <div class="video-title-div">
                        <p class="video-title"><a href="">Django Tutorial</a></p>
                        <p class="video-channel-name">Channel name</p>
                        <p class="video-stats">409K views . 2 months ago</p>
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

            <div id="shortVideoScrollDiv" class="flex flex-row overflow-hidden gap-x-[30px]">
                <div v-for="(short, index) in shortVideos" :key="index" class=" select-none short-video-preview">
                    <div class="short-video-thumbnail">
                        <img src="@/assets/img/Django.png" alt="">
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

        <div class="video-preview">
            <div class="video-thumbnail">
                <img src="@/assets/img/Django.png" alt="">
            </div>
            <div class="video-info">
                <div class="channel-logo">
                    <img src="@/assets/img/Django.png" alt="">
                </div>
                <div class="video-title-div">
                    <p class="video-title"><a href="">Django Tutorial</a></p>
                    <p class="video-channel-name">Channel name</p>
                    <p class="video-stats">409K views . 2 months ago</p>
                </div>
            </div>
        </div>
        <div class="video-preview">
            <div class="video-thumbnail">
                <img src="@/assets/img/Django.png" alt="">
            </div>
            <div class="video-info">
                <div class="channel-logo">
                    <img src="@/assets/img/Django.png" alt="">
                </div>
                <div class="video-title-div">
                    <p class="video-title"><a href="">Django Tutorial</a></p>
                    <p class="video-channel-name">Channel name</p>
                    <p class="video-stats">409K views . 2 months ago</p>
                </div>
            </div>
        </div>

    </div>
</template>