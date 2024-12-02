<script setup>
import { ref, reactive, onMounted } from 'vue';


const isChannelSubscribed = ref(false)


// Handle Channel`s options
const isChannelOptionsOpen = ref(false)
const toggleChannelOptions = () => isChannelOptionsOpen.value = !isChannelOptionsOpen.value


// Handle Search Bar
const isSearchBarOpen = ref(false)
const toggleSearchBar = () => isSearchBarOpen.value = !isSearchBarOpen.value


// Handle Channel Description
const isDescriptionOpen = ref(false)
const truncateChannelDescription = (description) => {
    return isDescriptionOpen.value ? description : description.substring(0, 40) + '...'
}
const toggleDescription = () => isDescriptionOpen.value = !isDescriptionOpen.value;


// Retrieving and assigning the Videos
const pinnedVideo = reactive({
    title: "Django Tutorial",
    channel_name: "Channel Name",
    views: "1.1M views",
    created_at: "2 years ago",
    description: "asdfasdfasdfadsf",
    duration: "12:29",
})


const regularVideos = []
for (let i = 0; i < 15; i++) {
    regularVideos.push({ title: `Regular Videos ${i + 1}`, created_at: `${i + 1} days ago` })
}


const popularVideos = []
for (let i = 0; i < 15; i++) {
    popularVideos.push({ title: `Popular Videos ${i + 1}`, created_at: `${i + 1} days ago` })
}


const famousPlaylistVideos1 = []
for (let i = 0; i < 15; i++) {
    famousPlaylistVideos1.push({ title: `Famous Playlist Videos 1 ${i + 1}`, created_at: `${i + 1} days ago` })
}


const famousPlaylistVideos2 = []
for (let i = 0; i < 15; i++) {
    famousPlaylistVideos2.push({ title: `Famous Playlist Videos 2 ${i + 1}`, created_at: `${i + 1} days ago` })
}

const updateSliderButtons = (container_id) => {
    const sliderContainer = document.getElementById(container_id)
    const prevButton = document.querySelector(`#${container_id}-prev-btn`)
    const nextButton = document.querySelector(`#${container_id}-next-btn`)
    const nextSlideCondition = sliderContainer.scrollLeft >= sliderContainer.scrollWidth - sliderContainer.clientWidth - 100

    prevButton.style.visibility = sliderContainer.scrollLeft <= 0 ? "hidden" : "visible";
    nextButton.style.visibility = nextSlideCondition ? "hidden" : "visible";
}

const regularVideosSliding = (container_id, direction) => {
    let slideAmount = 300;
    const sliderContainer = document.getElementById(container_id)
    sliderContainer.scrollLeft += direction === "prev" ? -slideAmount : slideAmount
    console.log(sliderContainer.scrollLeft)
    updateSliderButtons(container_id);
}

</script>
<template>
    <div class="channel-container w-[1070px] h-100 absolute left-[345px] top-16">
        <div>
            <img class="h-[172px] rounded-2xl w-[100%]" src="@/assets/img/Django.png" alt="">
        </div>
        <div class="flex flex-row mt-8 gap-x-4">
            <img class="w-[160px] h-[160px] rounded-full" src="@/assets/img/Django.png" alt="">
            <div class="flex flex-col gap-y-3">
                <span class="text-4xl font-bold -mt-2">Channel name</span>
                <div class="flex flex-row text-sm font-normal text-[#9b97a5] gap-x-1 justify-start items-center">
                    <span>@Channel name &nbsp;.</span>
                    <span>1.35M subscribers &nbsp;.</span>
                    <span>@Channel name</span>
                </div>
                <div class="flex flex-row text-sm font-normal justify-start items-center">
                    <span class="text-[#9b97a5]">{{ truncateChannelDescription(`Lorem ipsum dolor sit amet consectetur
                        adipisicing elit.Nostrum earum quam, itaque unde nulla ratione nam qui eius odit omnis dolorum
                        aliquam necessitatibus, illo modi dolore perspiciatis fugit hic excepturi?`) }}<span
                            @click="toggleDescription" class="text-black font-bold cursor-pointer ml-2">{{
                                isDescriptionOpen ? "Show Less" : "Show More" }}</span></span>

                </div>
                <button v-if="isChannelSubscribed" @click="toggleChannelOptions" class="w-[150px] h-[36px] rounded-2xl bg-[#f2f2f2] hover:bg-[#e5e5e5]
                 flex justify-center items-center">
                    <img class="w-5 h-6" src="@/assets/icons/svg-icons/bell-line-icon.svg" alt="">
                    <span class="text-black text-sm font-medium ml-2">Subscribed</span>
                    <img class="w-3 h-3 ml-5" src="@/assets/icons/svg-icons/thin-chevron-arrow-bottom-icon.svg" alt="">
                </button>
                <button v-else class="w-[94px] h-[36px] rounded-3xl bg-black mt-2">
                    <span class="text-sm font-medium text-white">Subscribe</span>
                </button>

                <div v-if="isChannelSubscribed && isChannelOptionsOpen" class="channel-options w-[256px] h-[160px] flex flex-col my-shadow rounded-xl
                 text-sm font-normal -mt-3">
                    <a class="w-[100%] h-[40px] mt-2">
                        <img src="@/assets/icons/svg-icons/notification-alert-icon.svg" alt="">
                        <span>All</span>
                    </a>
                    <a class="w-[100%] h-[40px]">
                        <img src="@/assets/icons/svg-icons/bell-line-icon.svg" alt="">
                        <span>Personalized</span>
                    </a>
                    <a class="w-[100%] h-[40px]">
                        <img src="@/assets/icons/svg-icons/remove-bell-notification-icon.svg" alt="">
                        <span>None</span>
                    </a>
                    <a class="w-[100%] h-[40px] mb-2">
                        <img src="@/assets/icons/svg-icons/remove-male-user-icon.svg" alt="">
                        <span>Unsubscribe</span>
                    </a>
                </div>
            </div>
        </div>
        <div class="tabs-inner-container w-[1280px] h-[48px] bg-white ml-[-115px] mt-3 border-b">
            <div class="flex flex-row ml-[130px] items-center">
                <a href="#" class="active tab w-[48px]" data-section="videos">Home</a>
                <a href="#" class="tab w-[48px]" data-section="videos">Videos</a>
                <a href="#" class="tab w-[48px]" data-section="shorts">Shorts</a>
                <a href="#" class="tab w-[64px]" data-section="playlists">Playlists</a>
                <a href="#" class="tab w-[80px]" data-section="community">Community</a>
                <div class="flex flex-row h-[28px] gap-x-6 items-center">
                    <button @click="toggleSearchBar" class="mr-0 w-10 h-10 flex justify-center items-center">
                        <img class="w-5 h-5" src="@/assets/icons/svg-icons/search-line-icon.svg" alt="">
                    </button>
                    <input v-if="isSearchBarOpen" name="query" class="flex placeholder:font-normal text-sm w-[174px] ml-[-15px]
                     border-b-2 border-b-black outline-none pb-1" type="text" placeholder="Search">
                </div>
            </div>
        </div>

        <div id="content-container">
            <div class="flex flex-col" id="homeDivision">
                <div class="flex flex-row mt-6 border-b-[1px] pb-6">
                    <a href="#" class="relative">
                        <img class="w-[246px] h-[138px] rounded-2xl" src="@/assets/img/Django.png" alt="">
                        <button
                            class="w-[40px] h-[18px] bg-black text-white font-medium text-xs absolute right-2 bottom-1 rounded-md">
                            {{ pinnedVideo.duration }}
                        </button>
                    </a>
                    <div class="flex flex-col ml-4 mt-2">
                        <a href="#" class="text-lg font-normal">{{ pinnedVideo.title }}</a>
                        <div class="flex flex-row gap-x-2" style="font-size: 12px; font-weight: 400; color: #69696a;">
                            <a href="#">{{ pinnedVideo.channel_name }}</a>
                            <span>{{ pinnedVideo.views }} views</span>
                            <span>{{ pinnedVideo.created_at }}</span>
                        </div>
                        <p style="margin-top: 5px; font-size: 12px; font-weight: 400; color: #69696a;">{{
                            pinnedVideo.description }}</p>
                    </div>
                </div>
                <div class="flex flex-col mt-4 relative border-b-[1px]">
                    <span class="font-bold text-xl mb-4">Videos</span>
                    <button @click="regularVideosSliding('slider1', 'prev')" id="slider1-prev-btn"
                        class="w-9 h-9 absolute top-[91px] left-[-20px] z-20 shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                        <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-left-icon.svg"
                            alt="">
                    </button>
                    <div id="slider1" class="flex flex-row h-[204px] max-w-[1284px] gap-x-1 overflow-x-auto"
                        style="scrollbar-width: thin;">
                        <div v-for="(video, index) in regularVideos" :key="index" class="grow-0 shrink-0 basis-auto">
                            <a href="" class="flex flex-col gap-y-2">
                                <img class="w-[210px] h-[118px] rounded-lg" src="@/assets/img/Django.png" alt="">
                                <a href="#" class="text-sm font-medium text-black">{{ video.title }}</a>
                                <div class="flex flex-row text-xs font-normal text-[#69696a]">
                                    <span>73K views&nbsp;</span>
                                    <span>{{ video.created_at }}</span>
                                </div>
                            </a>
                        </div>
                    </div>
                    <button @click="regularVideosSliding('slider1', 'next')" id="slider1-next-btn"
                        class="w-9 h-9 absolute top-[91px] right-[-18px] shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                        <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-right-icon.svg"
                            alt="">
                    </button>
                </div>
                <div class="flex flex-col mt-4 relative border-b-[1px]">
                    <span class="font-bold text-xl mb-4">Popular Videos</span>
                    <button @click="regularVideosSliding('slider2', 'prev')" id="slider2-prev-btn"
                        class="w-9 h-9 absolute top-[91px] left-[-20px] z-2 shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                        <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-left-icon.svg"
                            alt="">
                    </button>
                    <div id="slider2" class="flex flex-row h-[204px] max-w-[1284px] gap-x-1 overflow-hidden">
                        <div v-for="(video, index) in popularVideos" :key="index" class="grow-0 shrink-0 basis-auto">
                            <a href="" class="flex flex-col gap-y-2">
                                <img class="w-[210px] h-[118px] rounded-lg" src="@/assets/img/Django.png" alt="">
                                <a href="#" class="text-sm font-medium text-black">{{ video.title }}</a>
                                <div class="flex flex-row text-xs font-normal text-[#69696a]">
                                    <span>73K views&nbsp;</span>
                                    <span>{{ video.created_at }}</span>
                                </div>
                            </a>
                        </div>
                    </div>
                    <button @click="regularVideosSliding('slider2', 'next')" id="slider2-next-btn"
                        class="w-9 h-9 absolute top-[91px] right-[-18px] shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                        <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-right-icon.svg"
                            alt="">
                    </button>
                </div>
                <div class="flex flex-col mt-4 relative border-b-[1px]">
                    <span class="font-bold text-xl mb-4">Famous playlist Videos 1 (maximum 15 videos)</span>
                    <a href="#"
                        class="w-[103px] h-[36px] rounded-3xl flex justify-center items-center gap-x-2 hover:bg-[#e5e5e5]">
                        <img class="w-4 h-4" src="@/assets/icons/svg-icons/play-icon.svg" alt="">
                        <span class="font-medium text-sm">Play all</span>
                    </a>
                    <button @click="regularVideosSliding('slider3', 'prev')" id="slider3-prev-btn"
                        class="w-9 h-9 absolute top-[122px] left-[-20px] z-20 shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                        <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-left-icon.svg"
                            alt="">
                    </button>
                    <div id="slider3" class="flex flex-row h-[204px] max-w-[1284px] gap-x-1 overflow-hidden">
                        <div v-for="(video, index) in famousPlaylistVideos1" :key="index"
                            class="grow-0 shrink-0 basis-auto">
                            <a href="" class="flex flex-col gap-y-2">
                                <img class="w-[210px] h-[118px] rounded-lg" src="@/assets/img/Django.png" alt="">
                                <a href="#" class="text-sm font-medium text-black">{{ video.title }}</a>
                                <div class="flex flex-row text-xs font-normal text-[#69696a]">
                                    <span>73K views&nbsp;</span>
                                    <span>{{ video.created_at }}</span>
                                </div>
                            </a>
                        </div>
                    </div>
                    <button @click="regularVideosSliding('slider3', 'next')" id="slider3-next-btn"
                        class="w-9 h-9 absolute top-[122px] right-[-18px] shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                        <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-right-icon.svg"
                            alt="">
                    </button>
                </div>
                <div class="flex flex-col mt-4 relative border-b-[1px]">
                    <span class="font-bold text-xl mb-4">Famous playlist Videos 2 (maximum 15 videos)</span>
                    <a href="#"
                        class="w-[103px] h-[36px] rounded-3xl flex justify-center items-center gap-x-2 hover:bg-[#e5e5e5]">
                        <img class="w-4 h-4" src="@/assets/icons/svg-icons/play-icon.svg" alt="">
                        <span class="font-medium text-sm">Play all</span>
                    </a>
                    <button @click="regularVideosSliding('slider4', 'prev')" id="slider4-prev-btn"
                        class="w-9 h-9 absolute top-[122px] left-[-20px] z-50 shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                        <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-left-icon.svg"
                            alt="">
                    </button>
                    <div id="slider4" class="flex flex-row h-[204px] max-w-[1284px] gap-x-1 overflow-hidden">
                        <div v-for="(video, index) in famousPlaylistVideos2" :key="index"
                            class="grow-0 shrink-0 basis-auto">
                            <a href="" class="flex flex-col gap-y-2">
                                <img class="w-[210px] h-[118px] rounded-lg" src="@/assets/img/Django.png" alt="">
                                <a href="#" class="text-sm font-medium text-black">{{ video.title }}</a>
                                <div class="flex flex-row text-xs font-normal text-[#69696a]">
                                    <span>73K views&nbsp;</span>
                                    <span>{{ video.created_at }}</span>
                                </div>
                            </a>
                        </div>
                    </div>
                    <button @click="regularVideosSliding('slider4', 'next')" id="slider4-next-btn"
                        class="w-9 h-9 absolute top-[122px] right-[-18px] shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                        <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-right-icon.svg"
                            alt="">
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>