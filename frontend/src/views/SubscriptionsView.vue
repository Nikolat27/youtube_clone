<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue';
import { sharedState } from '@/sharedState';

const toast = useToast()
const router1 = useRoute()
const router2 = useRouter()

const isLoading = ref(false)
const longVideos = reactive([])
const shortVideos = reactive([])

const MountPage = (user_session_id) => {
    axios.get(`${sharedState.websiteUrl}/videos/subscriptions-list`, {
        params: {
            user_session_id: user_session_id
        }
    }).then((response) => {
        if (response.status == 200) {
            longVideos.splice(0, longVideos.length, ...response.data.long_videos)
            shortVideos.splice(0, shortVideos.length, ...response.data.short_videos)
        }
    }).catch((error) => console.log("Error: ", error))
}

let atStart = ref(null)
let atEnd = ref(null)
let scrollAmount = 180
const scrollShortVideos = (direction) => {
    const shortsContainer = document.getElementById("short-videos-container")
    shortsContainer.scrollLeft += (direction === 'next' ? scrollAmount : -scrollAmount)
    updateScrollButtons(shortsContainer.scrollWidth - shortsContainer.clientWidth, shortsContainer.scrollLeft)
}
const updateScrollButtons = (maxWidth, currentScrolled) => {
    if (currentScrolled <= 0) {
        atStart.value = true;
        atEnd.value = false;
    }
    else if (currentScrolled >= maxWidth) {
        atStart.value = false;
        atEnd.value = true;
    }
    else {
        atStart.value = false;
        atEnd.value = false;
    }
};

const isUserAuthenticated = ref(false)
const userAuthentication = async (user_session_id) => {
    await axios.get(`${sharedState.websiteUrl}/users/is_authenticated`, {
        params: {
            user_session_id: user_session_id
        }
    }).then((response) => {
        if (response.status == 200) {
            isUserAuthenticated.value = true
        }
    }).catch((error) => {
        toast.error(error)
    })
}

onMounted(async () => {
    const user_session_id = sessionStorage.getItem("user_session_id")
    if (!user_session_id) {
        router2.push({ name: "auth" })
    }

    await userAuthentication(user_session_id)
    if (!isUserAuthenticated) {
        router2.push({ name: "auth" })
    }

    MountPage(user_session_id)
    setTimeout(() => {
        const shortsContainer = document.getElementById("short-videos-container");
        if (shortsContainer) {
            updateScrollButtons(
                shortsContainer.scrollWidth - shortsContainer.clientWidth,
                shortsContainer.scrollLeft
            );
        }
    }, 0); // Use a small delay to ensure the DOM is fully rendered
});
</script>

<template>
    <div class="flex flex-col absolute left-[240px] top-[80px] font-roboto">
        <p class="text-lg font-bold mb-4">Latest</p>
        <div class="videoContainer flex flex-row flex-wrap gap-x-4 gap-y-12 pb-10">
            <div v-for="video in longVideos.slice(0, 6)" :key="video.unique_id"
                class="subscription-video flex flex-col gap-y-4 cursor-pointer">
                <div class="video-tag w-[400px] h-[224px] relative">
                    <router-link :to="`/video/${video.unique_id}`">
                        <img class="w-[100%] h-[100%] object-fill rounded-2xl" :src="video.thumbnail_url" />
                        <div
                            class="video-duration bg-black h-6 w-12 flex justify-center items-center rounded-md absolute bottom-2 right-2">
                            <p class="text-white text-center font-[650] text-[12px]">{{ video.duration }}</p>
                        </div>
                    </router-link>
                </div>
                <div class="flex flex-row gap-x-4">
                    <router-link :to="`/channel-page/${video.channel_unique_identifier}`">
                        <div class="w-9 h-9">
                            <img class="w-[100%] h-[100%] rounded-full" :src="video.channel_profile" alt="">
                        </div>
                    </router-link>
                    <router-link :to="`/video/${video.unique_id}`">
                        <div class="flex flex-col">
                            <p class="text-base font-medium">{{ video.title }}</p>
                            <p class="text-sm font-normal text-[#99a4a5]">{{ video.channel_id }}</p>
                            <p class="text-sm font-normal text-[#99a4a5]">{{ video.views }} views . {{ video.created_at
                                }}
                                days ago</p>
                        </div>
                    </router-link>
                </div>
            </div>
            <div class="relative flex flex-col w-[1229px] h-[550px]">
                <div class="header-div flex flex-row gap-x-2 justify-start items-center">
                    <div class="w-[24px] h-[24px] flex justify-center items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                            focusable="false" aria-hidden="true"
                            style="pointer-events: none; display: inherit; width: 100%; height: 100%;">
                            <path
                                d="m19.45,3.88c1.12,1.82.48,4.15-1.42,5.22l-1.32.74.94.41c1.36.58,2.27,1.85,2.35,3.27.08,1.43-.68,2.77-1.97,3.49l-8,4.47c-1.91,1.06-4.35.46-5.48-1.35-1.12-1.82-.48-4.15,1.42-5.22l1.33-.74-.94-.41c-1.36-.58-2.27-1.85-2.35-3.27-.08-1.43.68-2.77,1.97-3.49l8-4.47c1.91-1.06,4.35-.46,5.48,1.35Z"
                                fill="#f03"></path>
                            <path d="m10,15l5-3-5-3v6Z" fill="#fff"></path>
                        </svg>
                    </div>
                    <p class="text-[20px] font-bold">Shorts</p>
                    <router-link class="ml-auto" to="/subscriptions/shorts">
                        <button class="w-[80.7px] h-[36px] text-[14px] font-medium
                         rounded-3xl text-blue-600 hover:bg-[#def1ff]">
                            View all
                        </button>
                    </router-link>
                </div>
                <div v-if="!atStart" @click="scrollShortVideos('previous')" class="z-50 absolute -left-6 top-[230px] w-[56px] h-[56px] rounded-full bg-[#f9f9f9] hover:bg-[#d9d9d9]
                     cursor-pointer">
                    <img draggable="false" class="w-[100%] h-[100%] -rotate-90"
                        src="@/assets/icons/svg-icons/angle-circle-up-icon.svg" alt="">
                </div>
                <div id="short-videos-container" class="flex flex-row w-full scroll-smooth overflow-hidden
                 gap-x-4 justify-start items-center mt-6">
                    <div v-for="video in shortVideos" :key="video.unique_id"
                        class="short-video min-w-[233px] w-[233px] h-[500px] flex-col">
                        <router-link :to="`/short/${video.unique_id}`">
                            <img class="w-full h-[414px] rounded-xl" :src="video.thumbnail_url" alt="">
                            <p class="mt-2 text-[16px] font-medium">{{ video.title }}</p>
                            <span class="text-[14px] font-normal text-gray-500">{{ video.views }} views</span>
                        </router-link>
                    </div>
                </div>
                <div v-if="!atEnd" @click="scrollShortVideos('next')" draggable="false" class="z-50 absolute -right-6 top-[230px] w-[56px] h-[56px] rounded-full bg-[#f9f9f9] hover:bg-[#d9d9d9]
                     cursor-pointer">
                    <img class="w-[100%] h-[100%] rotate-90" src="@/assets/icons/svg-icons/angle-circle-up-icon.svg"
                        alt="">
                </div>
            </div>
            <div v-for="video in longVideos.slice(6)" :key="video.unique_id"
                class="subscription-video flex flex-col gap-y-4 cursor-pointer">
                <div class="video-tag w-[400px] h-[224px] relative">
                    <router-link :to="`/video/${video.unique_id}`">
                        <img class="w-[100%] h-[100%] object-fill rounded-2xl" :src="video.thumbnail_url" />
                        <div
                            class="video-duration bg-black h-6 w-12 flex justify-center items-center rounded-md absolute bottom-2 right-2">
                            <p class="text-white text-center font-[650] text-[12px]">{{ video.duration }}</p>
                        </div>
                    </router-link>
                </div>
                <div class="flex flex-row gap-x-4">
                    <router-link :to="`/channel-page/${video.channel_unique_identifier}`">
                        <div class="w-9 h-9">
                            <img class="w-[100%] h-[100%] rounded-full" :src="video.channel_profile" alt="">
                        </div>
                    </router-link>
                    <router-link :to="`/video/${video.unique_id}`">
                        <div class="flex flex-col">
                            <p class="text-base font-medium">{{ video.title }}</p>
                            <p class="text-sm font-normal text-[#99a4a5]">{{ video.channel_id }}</p>
                            <p class="text-sm font-normal text-[#99a4a5]">{{ video.views }} views . {{ video.created_at
                                }}
                                days ago</p>
                        </div>
                    </router-link>
                </div>
            </div>
        </div>
        <div v-if="isLoading" class="mt-[40px] pb-20 text-center flex justify-center items-center">
            <ScaleLoader :color="['#df0d3b']" :width="['5px']" :height="['37.5px']" />
        </div>
    </div>
</template>