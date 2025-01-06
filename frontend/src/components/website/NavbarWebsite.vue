<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useToast } from 'vue-toastification';

import axios from 'axios';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';

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
        <div class="search-div">
            <input autocomplete="off" type="text" name="q" class="search-bar" placeholder="Search">
            <button class="search-btn">
                <img src="@/assets/icons/header/search.svg" alt="">
            </button>
            <button class="audio-search-btn">
                <img src="@/assets/icons/header/voice-search-icon.svg" alt="">
            </button>
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