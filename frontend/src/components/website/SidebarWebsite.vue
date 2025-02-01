<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { RouterLink } from 'vue-router';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import { useRoute, useRouter } from 'vue-router';
import { sharedState } from '@/sharedState';

const toast = useToast()
const router1 = useRoute()
const router2 = useRouter()


const isSideBarCollapsed = ref(false)
watch(() => sharedState.isWebsiteSideBarCollapsed, (newVal) => {
    isSideBarCollapsed.value = newVal
    console.log(isSideBarClosed.value)
})

const isSideBarClosed = ref(false)
watch(() => sharedState.isWebsiteSideBarClosed, (newVal) => {
    isSideBarCollapsed.value = true
    isSideBarClosed.value = newVal
})


let maxChannelShownByDefault = ref(4);
let isCollapsed = computed(() => maxChannelShownByDefault.value === 1) // if value is 1 then collapsed is True
const toggleSubscriptionChannels = () => {
    if (isCollapsed.value === true) {
        maxChannelShownByDefault.value = 10
    } else {
        maxChannelShownByDefault.value = 1
    }
};

const watchLaterPlaylist = () => {
    axios.get("http://127.0.0.1:8000/playlist/watch/later", {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 200) {
            router2.push({ name: "playlist-videos", params: { id: response.data } })
        }
    }).catch((error) => { toast.error("Error: ", error) })
}

const likedVideosPlaylist = () => {
    axios.get("http://127.0.0.1:8000/playlist/liked/videos", {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 200) {
            router2.push({ name: "playlist-videos", params: { id: response.data } })
        }
    }).catch((error) => { toast.error("Error: ", error) })
}


const isUserAuthenticated = ref(false)
const userAuthentication = async (user_session_id) => {
    await axios.get("http://127.0.0.1:8000/users/is_authenticated", {
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

const openShortsPage = () => {
    axios.get("http://127.0.0.1:8000/videos/short-video").then((response) => {
        if (response.status == 200) {
            router2.push({
                name: "short_detail", params: { id: response.data.unique_id }, state: {
                    is_first: response.data.is_first,
                    is_last: response.data.is_last
                }
            })
        }
    }).catch(() => toast.error("Error!"))
}

let totalChannels = ref(null)
const subscriptionChannels = reactive([])
const retrieveChannelSubscriptions = (user_session_id) => {
    axios.get("http://127.0.0.1:8000/channel/subscriptions", {
        params: {
            user_session_id: user_session_id
        }
    }).then((response) => {
        if (response.status == 200) {
            subscriptionChannels.splice(0, subscriptionChannels.length, ...response.data.data)
            totalChannels.value = response.data.channel_count
        }
    }).catch((error) => console.error(error))
}


const checkSideBar = () => {
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


onMounted(async () => {
    checkSideBar()
    const user_session_id = sessionStorage.getItem("user_session_id")
    if (user_session_id) {
        await userAuthentication(user_session_id)
        if (isUserAuthenticated.value) {
            retrieveChannelSubscriptions(user_session_id)
        }
    }

    window.addEventListener("resize", () => {
        if (sharedState.isSecondWebsiteSideBarOpen) {
            sharedState.isSecondWebsiteSideBarOpen = false
        }
    })
})
</script>

<template>
    <aside v-if="!isSideBarCollapsed && !isSideBarClosed" class="side-bar-div">
        <router-link to="/">
            <div class="side-bar-links">
                <img src="@/assets/icons/svg-icons/home-icon.svg" alt="">
                <p>Home</p>
            </div>
        </router-link>
        <div @click="openShortsPage" class="side-bar-links">
            <img src="@/assets/icons/svg-icons/youtube-shorts-icon.svg" alt="">
            <p>Shorts</p>
        </div>
        <router-link to="/subscriptions">
            <div class="side-bar-links">
                <img src="@/assets/icons/svg-icons/video-playlist-icon.svg" alt="">
                <p>Subscriptions</p>
            </div>
        </router-link>
        <div class="side-bar-links">
            <p class="text-[16px] font-medium" style="margin-left: 0;">You</p>
            <img class="rotate-90" style="width: 14px; height: 14px; margin-left: 8px;"
                src="@/assets/icons/svg-icons/line-angle-up-icon.svg" alt="">
        </div>
        <router-link to="/history">
            <div class="side-bar-links">
                <img src="@/assets/icons/svg-icons/clockwise-icon.svg" alt="">
                <p>History</p>
            </div>
        </router-link>
        <router-link to="/feed/playlists">
            <div class="side-bar-links">
                <img src="@/assets/icons/svg-icons/playlist-videos-icon.svg" alt="">
                <p>Playlists</p>
            </div>
        </router-link>
        <router-link to="/studio/">
            <div class="side-bar-links">
                <img src="@/assets/icons/svg-icons/youtube-color-icon.svg" alt="">
                <p>Your videos</p>
            </div>
        </router-link>
        <div @click="watchLaterPlaylist" class="side-bar-links">
            <img src="@/assets/icons/side-bar/watch-later.webp" alt="">
            <p>Watch Later</p>
        </div>
        <div @click="likedVideosPlaylist" class="side-bar-links">
            <img src="@/assets\icons\svg-icons\like-empty.svg" alt="">
            <p>Liked</p>
        </div>

        <div class="side-bar-links">
            <p style="margin-left: 0;">Subscriptions</p>
        </div>

        <transition-group name="slide-down">
            <div v-for="channel in subscriptionChannels.slice(0, maxChannelShownByDefault)" :key="channel.unique_id">
                <router-link :to="`/channel-page/${channel.unique_identifier}`"
                    class="side-bar-links subscriptions-div">
                    <img style="border-radius: 50%;" :src="channel.profile_picture_url" alt="">
                    <p>{{ channel.name }}</p>
                </router-link>
            </div>
            <router-link to="/feed/channels" key="all-subscriptions">
                <div v-if="isCollapsed" class="side-bar-links subscriptions-div">
                    <div class="w-[24px] h-[24px]">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" height="24" viewBox="0 0 24 24"
                            width="24" focusable="false" aria-hidden="true"
                            style="pointer-events: none; display: inherit; width: 100%; height: 100%;">
                            <path clip-rule="evenodd"
                                d="M5 8.5c.828 0 1.5-.672 1.5-1.5S5.828 5.5 5 5.5 3.5 6.172 3.5 7 4.172 8.5 5 8.5ZM8 7c0-.414.336-.75.75-.75h11.5c.414 0 .75.336.75.75s-.336.75-.75.75H8.75C8.336 7.75 8 7.414 8 7Zm.75 4.25c-.414 0-.75.336-.75.75s.336.75.75.75h11.5c.414 0 .75-.336.75-.75s-.336-.75-.75-.75H8.75Zm0 5c-.414 0-.75.336-.75.75s.336.75.75.75h11.5c.414 0 .75-.336.75-.75s-.336-.75-.75-.75H8.75ZM6.5 12c0 .828-.672 1.5-1.5 1.5s-1.5-.672-1.5-1.5.672-1.5 1.5-1.5 1.5.672 1.5 1.5ZM5 18.5c.828 0 1.5-.672 1.5-1.5s-.672-1.5-1.5-1.5-1.5.672-1.5 1.5.672 1.5 1.5 1.5Z"
                                fill-rule="evenodd"></path>
                        </svg>
                    </div>
                    <p class="text-[14px] font-normal">All subscriptions</p>
                </div>
            </router-link>
        </transition-group>

        <div v-if="totalChannels > 4" class="side-bar-links">
            <img style="width: 18px; height: 18px;" :class="[isCollapsed ? 'rotate-180' : '']"
                src="@/assets/icons/svg-icons/line-angle-up-icon.svg" alt="">
            <button @click="toggleSubscriptionChannels" id="show-more-btn">
                {{ isCollapsed ? 'Show more' : 'Show less' }}
            </button>
        </div>
    </aside>
    <aside v-if="isSideBarCollapsed && !isSideBarClosed" class="flex flex-col side-bar-div gap-y-4">
        <router-link to="/" class="flex justify-center items-center w-[64px] h-[74px] hover:bg-[#f2f2f2] rounded-lg">
            <div class="flex flex-col justify-center items-center">
                <div class="w-[24px] h-[24px] flex justify-center items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" height="24" viewBox="0 0 24 24"
                        width="24" focusable="false" aria-hidden="true"
                        style="pointer-events: none; display: inherit; width: 100%; height: 100%;">
                        <path clip-rule="evenodd"
                            d="M22.146 11.146a.5.5 0 01-.353.854H20v7.5a1.5 1.5 0 01-1.5 1.5H14v-8h-4v8H5.5A1.5 1.5 0 014 19.5V12H2.207a.5.5 0 01-.353-.854L12 1l10.146 10.146Z"
                            fill-rule="evenodd"></path>
                    </svg>
                </div>
                <p class="text-[10px] font-normal mt-2" style="margin-left: 0;">Home</p>
            </div>
        </router-link>
        <router-link to="/short/"
            class="flex justify-center items-center w-[64px] h-[74px] hover:bg-[#f2f2f2] rounded-lg">
            <div class="flex flex-col justify-center items-center">
                <div class="w-[24px] h-[24px] flex justify-center items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" height="24" viewBox="0 0 24 24"
                        width="24" focusable="false" aria-hidden="true"
                        style="pointer-events: none; display: inherit; width: 100%; height: 100%;">
                        <path clip-rule="evenodd"
                            d="m7.61 15.719.392-.22v-2.24l-.534-.228-.942-.404c-.869-.372-1.4-1.15-1.446-1.974-.047-.823.39-1.642 1.203-2.097h.001L15.13 3.59c1.231-.689 2.785-.27 3.466.833.652 1.058.313 2.452-.879 3.118l-1.327.743-.388.217v2.243l.53.227.942.404c.869.372 1.4 1.15 1.446 1.974.047.823-.39 1.642-1.203 2.097l-.002.001-8.845 4.964-.001.001c-1.231.688-2.784.269-3.465-.834-.652-1.058-.313-2.451.879-3.118l1.327-.742Zm1.993 6.002c-1.905 1.066-4.356.46-5.475-1.355-1.057-1.713-.548-3.89 1.117-5.025a4.14 4.14 0 01.305-.189l1.327-.742-.942-.404a4.055 4.055 0 01-.709-.391c-.963-.666-1.578-1.718-1.644-2.877-.08-1.422.679-2.77 1.968-3.49l8.847-4.966c1.905-1.066 4.356-.46 5.475 1.355 1.057 1.713.548 3.89-1.117 5.025a4.074 4.074 0 01-.305.19l-1.327.742.942.403c.253.109.49.24.709.392.963.666 1.578 1.717 1.644 2.876.08 1.423-.679 2.77-1.968 3.491l-8.847 4.965ZM10 14.567a.25.25 0 00.374.217l4.45-2.567a.25.25 0 000-.433l-4.45-2.567a.25.25 0 00-.374.216v5.134Z"
                            fill-rule="evenodd"></path>
                    </svg>
                </div>
                <p class="text-[10px] font-normal mt-2" style="margin-left: 0;">Shorts</p>
            </div>
        </router-link>
        <router-link to="/subscriptions"
            class="flex justify-center items-center w-[64px] h-[74px] hover:bg-[#f2f2f2] rounded-lg">
            <div class="flex flex-col justify-center items-center">
                <div class="w-[24px] h-[24px] flex justify-center items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" height="24" viewBox="0 0 24 24"
                        width="24" focusable="false" aria-hidden="true"
                        style="pointer-events: none; display: inherit; width: 100%; height: 100%;">
                        <path clip-rule="evenodd"
                            d="M4 4.5A1.5 1.5 0 015.5 3h13A1.5 1.5 0 0120 4.5H4Zm16.5 3h-17v11h17v-11ZM3.5 6A1.5 1.5 0 002 7.5v11A1.5 1.5 0 003.5 20h17a1.5 1.5 0 001.5-1.5v-11A1.5 1.5 0 0020.5 6h-17Zm7.257 4.454a.5.5 0 00-.757.43v4.233a.5.5 0 00.757.429L15 13l-4.243-2.546Z"
                            fill-rule="evenodd"></path>
                    </svg>
                </div>
                <p class="text-[10px] font-normal mt-2" style="margin-left: 0;">Shorts</p>
            </div>
        </router-link>
    </aside>
</template>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
    transition: all 0.5s ease-in-out;
}

.slide-down-enter-from,
.slide-down-leave-to {
    opacity: 1;
    transform: translateY(-20px);
}
</style>