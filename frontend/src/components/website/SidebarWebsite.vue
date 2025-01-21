<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import { useRoute, useRouter } from 'vue-router';

const toast = useToast()
const router1 = useRoute()
const router2 = useRouter()

const items = reactive([{ title: "1" }, { title: "2" }, { title: "3" }, { title: "4" }])
let maxChannelShown = ref(1);
let isCollapsed = computed(() => maxChannelShown.value === 1) // if value == 1 then collapsed is True

const toggleSubscriptionChannels = () => {
    maxChannelShown.value = isCollapsed.value ? 10 : 1;
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

onMounted(async () => {
    const user_session_id = sessionStorage.getItem("user_session_id")
    if (!user_session_id) {
        router2.push({ name: "auth" })
    }

    await userAuthentication(user_session_id)
    if (!isUserAuthenticated) {
        router2.push({ name: "auth" })
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
        <div class="side-bar-links">
            <img src="@/assets/icons/svg-icons/video-playlist-icon.svg" alt="">
            <p>Subscriptions</p>
        </div>
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
            <div v-for="(channel, index) in items.slice(0, maxChannelShown)" :key="index"
                class="side-bar-links subscriptions-div">
                <img style="border-radius: 50%;" src="@/assets/img/Django.png" alt="">
                <p>{{ channel.title }}</p>
            </div>
        </transition-group>

        <div class="side-bar-links">
            <img style="width: 18px; height: 18px;" :class="[isCollapsed ? 'rotate-180' : '']"
                src="@/assets/icons/svg-icons/line-angle-up-icon.svg" alt="">
            <button @click="toggleSubscriptionChannels" id="show-more-btn">{{ isCollapsed ? 'Show more' : 'Show less'
                }}</button>
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