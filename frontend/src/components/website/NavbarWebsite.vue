<script setup>
import { ref, reactive, onMounted, watch } from 'vue';
import { useToast } from 'vue-toastification';
import { useRouter } from 'vue-router';

import axios from 'axios';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue';

import kebabMenuIcon from '@/assets/icons/svg-icons/kebab-menu.svg'


// Handle Notification Container Expanding 
let isNotificationExpanded = ref(false)
const toggleNotificationContainer = () => {
    isNotificationExpanded.value = !isNotificationExpanded.value
}

// Handle the Notifications` options
const expandedNotifications = ref([0])
const toggleNotificationOptions = (notificationId) => {
    const index = expandedNotifications.value.indexOf(notificationId);
    if (index === -1) {
        expandedNotifications.value.push(notificationId);
    } else {
        expandedNotifications.value.splice(index, 1);
    }
};

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

const toast = useToast();
const isLoading = ref(false)
const notifications = reactive([])
const unreadNotifications = ref(null)
const retrieveNotifications = () => {
    isLoading.value = true
    axios.get("http://127.0.0.1:8000/users/notifications", {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 200) {
            Object.assign(notifications, response.data.data.detail)
            unreadNotifications.value = response.data.data.unread_notifications
        }
    }).catch((error) => {
        toast.error(error)
    }).finally(() => isLoading.value = false)
}

const searchBarText = ref('')
const isAutoCompleteOpen = ref(false)
const autoCompletes = reactive([])
const isSearchLoading = ref(false)
let shouldWatch = true;

watch(() => searchBarText.value, () => {
    if (searchBarText.value.length < 3) return;
    if (!shouldWatch) return;

    isSearchLoading.value = true
    isAutoCompleteOpen.value = true
    axios.get("http://127.0.0.1:8000/videos/search/autocomplete", {
        params: {
            query: searchBarText.value
        }
    }).then((response) => {
        Object.assign(autoCompletes, response.data)
    }).catch((error) => toast.error(error)).finally(() => {
        isSearchLoading.value = false
    })

})

const router = useRouter()
const searchVideo = (query) => {
    shouldWatch = false;
    isAutoCompleteOpen.value = false
    searchBarText.value = query
    
    router.push({ name: 'search_results', query: { "query": query } })
    setTimeout(() => (shouldWatch = true), 0);
}

onMounted(async () => {
    const user_session_id = sessionStorage.getItem("user_session_id")
    if (user_session_id) {
        await userAuthentication(user_session_id)
        if (isUserAuthenticated) {
            retrieveNotifications()
        }
    }
})
</script>

<template>
    <header class="header">
        <div class="left-div">
            <img class="hamburger-img" src="@/assets/icons/header/hamburger-menu.svg" alt="">
            <img class="youtube-logo-img" src="@/assets/icons/header/youtube-logo.svg" alt="">
        </div>
        <div class="flex flex-col w-[60%] h-full justify-center items-center relative top-1">
            <div class="flex flex-row search-div">
                <input v-model="searchBarText" autocomplete="off" type="text" class="search-bar" placeholder="Search">
                <button @click="searchVideo(searchBarText)" class="search-btn">
                    <img src="@/assets/icons/header/search.svg" alt="">
                </button>
                <button class="audio-search-btn">
                    <img src="@/assets/icons/header/voice-search-icon.svg" alt="">
                </button>
            </div>
            <div v-if="searchBarText.length >= 3 && isAutoCompleteOpen"
                class="autocomplete-bar absolute top-[50px] left-[118px] w-[543px] h-[540px] bg-white z-40 rounded-xl custom-shadow-inset">
                <div v-if="!isSearchLoading" class="flex flex-col justify-center items-center gap-y-1 py-4 h-full">
                    <div @click="searchVideo(text)" v-for="(text, index) in autoCompletes" :key="index" class="w-full h-[32px] px-2 flex flex-row justify-start items-center
                    hover:bg-[#f2f2f2]">
                        <img class="w-[20px] h-[20px] mr-2" src="@/assets/icons/header/search.svg" alt="">
                        <p>{{ text }}</p>
                        <span
                            class="text-[13px] font-medium text-blue-600 justify-self-end ml-auto mr-2 cursor-pointer">Remove</span>
                    </div>
                </div>
                <div v-if="isSearchLoading" class="flex h-full w-full justify-center items-center">
                    <ClipLoader color="red" size="45px"></ClipLoader>
                </div>
            </div>
        </div>
        <div class="right-div">
            <div class="right-div-buttons">
                <router-link to="/studio">
                    <button class="upload-video-btn" data-tooltip="Upload">
                        <img src="@/assets/icons/header/upload.svg" class="create-video-img" alt="">
                    </button>
                </router-link>
                <button @click="toggleNotificationContainer" class="notification-btn" data-tooltip="Notifications">
                    <img src="@/assets/icons/header/notifications.svg" class="notification-img" alt="">
                    <span class="icon-button--badge">{{ unreadNotifications ?? 0 }}</span>
                </button>
                <div v-if="isNotificationExpanded" class="notification-container">
                    <div class="notification-title">
                        <p>Notifications</p>
                        <hr>
                    </div>
                    <div v-if="isUserAuthenticated && !isLoading">
                        <div v-for="notification in notifications" :key="notification.id" class="notification">
                            <div class="notification-channel-img">
                                <img :src="notification.sender_profile_picture" alt="">
                            </div>
                            <div class="notification-info">
                                <router-link :to="`/video/${notification.video_id}/`">
                                    <p class="notification-message">
                                        {{ notification.text }}
                                    </p>
                                </router-link>
                                <span>{{ notification.created_at }} days ago</span>
                            </div>
                            <router-link :to="`/video/${notification.video_id}`">
                                <div class="notification-video-img">
                                    <img :src="notification.video_thumbnail" alt="">
                                </div>
                            </router-link>
                            <button @click="toggleNotificationOptions(notification.id)" class="kebab-menu-btn">
                                <img :src="kebabMenuIcon" loading="lazy" alt="">
                                <div v-if="expandedNotifications.includes(notification.id)"
                                    class="notification-options">
                                    <a href="#"><img src="@/assets/icons/svg-icons/hide-notification-icon.svg"
                                            alt="">Hide
                                        this notification</a>
                                    <a href="#" class="mute-notification-button"><img
                                            src="@/assets/icons/svg-icons/mute-notification-icon.svg"
                                            alt="">Mute&nbsp;<span>@{{ notification.channel_name }}</span></a>
                                </div>
                            </button>
                        </div>
                    </div>
                    <div v-if="isLoading && isUserAuthenticated" class="flex justify-center items-center m-auto my-20">
                        <PulseLoader size="20px" color="red"></PulseLoader>
                    </div>
                    <div v-if="!isUserAuthenticated">
                        <router-link to="/auth/">
                            <div class="pl-4 my-6 font-medium">
                                <h2>For seeing the notifications you have to login first <span
                                        class="text-blue-600 text-[16px] underline">Click Here</span></h2>
                            </div>
                        </router-link>
                    </div>
                </div>
            </div>
            <button class="channel-profile-btn">
                <img src="@/assets/img/Django.png" class="channel-profile-img" alt="">
            </button>
        </div>
    </header>
</template>
<style scoped>
.custom-shadow-inset {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
}
</style>