<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import { useRoute, useRouter } from 'vue-router';

const toast = useToast()
const router1 = useRoute()
const router2 = useRouter()

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

onMounted(async () => {
    const user_session_id = sessionStorage.getItem("user_session_id")
    if (user_session_id) {
        await userAuthentication(user_session_id)
        if (isUserAuthenticated.value) {
            retrieveChannelSubscriptions(user_session_id)
        }
    }
})
</script>

<template>
    <aside class="side-bar-div">
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

        <!-- Show only the first 4 channels by default -->
        <transition-group name="slide-down">
            <div v-for="channel in subscriptionChannels.slice(0, maxChannelShownByDefault)" :key="channel.unique_id">
                <router-link :to="`/channel-page/${channel.unique_identifier}`"
                    class="side-bar-links subscriptions-div">
                    <img style="border-radius: 50%;" :src="channel.profile_picture_url" alt="">
                    <p>{{ channel.name }}</p>
                </router-link>
            </div>
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
        </transition-group>

        <div v-if="totalChannels > 4" class="side-bar-links">
            <img style="width: 18px; height: 18px;" :class="[isCollapsed ? 'rotate-180' : '']"
                src="@/assets/icons/svg-icons/line-angle-up-icon.svg" alt="">
            <button @click="toggleSubscriptionChannels" id="show-more-btn">
                {{ isCollapsed ? 'Show more' : 'Show less' }}
            </button>
        </div>
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