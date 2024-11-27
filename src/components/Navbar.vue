<script setup>
import { ref, reactive } from 'vue';


// Handle Notification Container Expanding 
let isNotificationExpanded = ref(false)
const toggleNotificationContainer = () => {
    isNotificationExpanded.value = !isNotificationExpanded.value
}


// Fetch the Notifications
const notifications = reactive([
    { id: 1, text: "hello World 1", },
    { id: 2, text: "hello World 2", },
    { id: 3, text: "hello World 3", },
])


// Handle the Notifications` options
const expandedNotifications = ref([0])
const togglingNotificationOptions = (notification_id) => {
    if (!expandedNotifications.value.includes(notification_id)) {
        expandedNotifications.value[0] = notification_id;
    } else {
        expandedNotifications.value.pop();
    }
}
</script>

<template>
    <header class="header">
        <div class="left-div">
            <img class="hamburger-img" src="@/assets/icons/header/hamburger-menu.svg" alt="">
            <img class="youtube-logo-img" src="@/assets/icons/header/youtube-logo.svg" alt="">
        </div>
        <div class="search-div">
            <input type="text" name="q" class="search-bar" placeholder="Search">
            <button class="search-btn">
                <img src="@/assets/icons/header/search.svg" alt="">
            </button>
            <button class="audio-search-btn">
                <img src="@/assets/icons/header/voice-search-icon.svg" alt="">
            </button>
        </div>
        <div class="right-div">
            <div class="right-div-buttons">
                <button class="upload-video-btn" data-tooltip="Upload">
                    <img src="@/assets/icons/header/upload.svg" class="create-video-img" alt="">
                </button>
                <button @click="toggleNotificationContainer" class="notification-btn" data-tooltip="Notifications">
                    <img src="@/assets/icons/header/notifications.svg" class="notification-img" alt="">
                    <!-- <img src="assets/icons/svg-icons/notification-fill-icon.svg" class="notification-img" alt=""> -->
                    <span class="icon-button--badge">2</span>
                </button>
                <div v-if="isNotificationExpanded" class="notification-container">
                    <div class="notification-title">
                        <p>Notifications</p>
                        <hr>
                    </div>
                    <div v-for="notification in notifications" :key="notification.id" class="notification">
                        <div class="notification-channel-img">
                            <img src="@/assets/img/Django.png" alt="">
                        </div>
                        <div class="notification-info">
                            <p class="notification-message">
                                <a href="#">{{ notification.text }}</a>
                            </p>
                            <span>15 hours ago</span>
                        </div>
                        <div class="notification-video-img">
                            <img src="@/assets/img/Django.png" alt="">
                        </div>
                        <button @click="togglingNotificationOptions(notification.id)" class="kebab-menu-btn">
                            <img src="@/assets/icons/svg-icons/kebab-menu.svg" class="kebab-menu-btn" alt="">
                            <div v-if="expandedNotifications.includes(notification.id)" class="notification-options">
                                <a href="#"><img src="@/assets/icons/svg-icons/hide-notification-icon.svg"
                                     alt="">Hide this notification</a>
                                <a href="#" class="mute-notification-button"><img
                                        src="@/assets/icons/svg-icons/mute-notification-icon.svg"
                                        alt="">Mute&nbsp;<span>@Channel name</span></a>
                            </div>
                        </button>
                    </div>
                </div>
            </div>
            <button class="channel-profile-btn">
                <img src="@/assets/img/Django.png" class="channel-profile-img" alt="">
            </button>
        </div>
    </header>
</template>