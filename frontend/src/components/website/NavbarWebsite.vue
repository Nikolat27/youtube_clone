<script setup>
import { ref, reactive, onMounted, watch } from 'vue';
import { useToast } from 'vue-toastification';
import { useRouter } from 'vue-router';
import { sharedState } from '@/sharedState';
import { useRoute } from 'vue-router';

import axios from 'axios';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue';

// Icons
import plusIcon from '/src/assets/icons/svg-icons/plus-icon.svg'
import kebabMenuIcon from '/src/assets/icons/svg-icons/kebab-menu.svg'
import unAuthenticatedUserImg from '/src/assets/img/unauthenticated_user_img.png'

const route = useRoute()
const routeName = ref(null)
watch(route, () => {
    routeName.value = route.name
})

const toggleWebsiteSideBar = () => {
    if (routeName.value === 'video_detail') {
        sharedState.isSecondWebsiteSideBarOpen = !sharedState.isSecondWebsiteSideBarOpen
        return;
    }

    if (!sharedState.isWebsiteSideBarClosed) {
        sharedState.isWebsiteSideBarCollapsed = !sharedState.isWebsiteSideBarCollapsed
    } else {
        sharedState.isWebsiteSideBarCollapsed = true
        sharedState.isSecondWebsiteSideBarOpen = true
    }
}


// Handle Notification Container Expanding 
let isNotificationContainerExpanded = ref(false)
const toggleNotificationContainer = () => {
    isNotificationContainerExpanded.value = !isNotificationContainerExpanded.value
}

// Handle the Notifications` options
const expandedNotification = reactive([])
const toggleNotificationOptions = (notificationId) => {
    const index = expandedNotification.indexOf(notificationId);
    if (index === -1) { // -1 means it doesnt exist!
        expandedNotification.splice(index, 1); // Close options
        expandedNotification.push(notificationId); // Open options
    } else {
        expandedNotification.splice(index, 1); // Close options
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


const hideNotification = async (notificationId) => {
    await axios.delete(`http://127.0.0.1:8000/users/notifications/delete/${notificationId}`, {
        params: {
            "user_session_id": sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 204) {
            isNotificationContainerExpanded.value = false
            retrieveNotifications()
            toast.info("You Hide the notification", {
                position: "top-center"
            })
        }
    }).catch((error) => toast.error("Error!"))
}


const markVisibleNotificationsAsRead = () => {
    if (unreadNotifications.value <= 0) return;
    axios.patch(`http://127.0.0.1:8000/users/notifications/read?user_session_id=${sessionStorage.getItem("user_session_id")}`).then((response) => {
        if (response.status == 204) {
            unreadNotifications.value = 0
        }
    }).catch((error) => console.error("Error: ", error))
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
            notifications.splice(0, notifications.length, ...response.data.data.detail)
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
    if (query.length <= 2) {
        toast.warning("You have to enter at least one word")
        return
    };

    shouldWatch = false;
    isAutoCompleteOpen.value = false
    searchBarText.value = query

    router.push({ name: 'search_results', query: { "query": query } })
    setTimeout(() => (shouldWatch = true), 0);
}


const channelId = ref(null)
const userId = ref(null)
const userProfileImgSrc = ref(null)
const retrieveUserProfileImg = async (user_session_id) => {
    await axios.get("http://127.0.0.1:8000/users/profile-picture", {
        params: {
            user_session_id: user_session_id
        }
    }).then((response) => {
        if (response.status == 200) {
            userProfileImgSrc.value = response.data.profile_picture
            userId.value = response.data.user_id
            channelId.value = response.data.channel_id
        }
    }).catch((error) => {
        toast.error(error)
    })
}


const deleteAllNotifications = () => {
    axios.delete("http://127.0.0.1:8000/users/notifications/delete-all", {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 204) {
            toast.info("All your Notifications have been removed", {
                position: "top-center"
            })
            isNotificationContainerExpanded.value = false
            retrieveNotifications()
        }
    })
}


onMounted(async () => {
    const user_session_id = sessionStorage.getItem("user_session_id")
    if (user_session_id) {
        await userAuthentication(user_session_id)
        if (isUserAuthenticated) {
            retrieveUserProfileImg(user_session_id)
            retrieveNotifications()
        }
    }
})
</script>

<template>
    <header class="header mx-auto font-roboto">
        <div class="left-div">
            <button @click="toggleWebsiteSideBar"
                class="w-[50px] shrink-0 h-[50px] bg-white hover:bg-[#f1f1f1] flex justify-center items-center rounded-full">
                <img class="shrink-0" src="@/assets/icons/header/hamburger-menu.svg" alt="">
            </button>
            <router-link to="/">
                <img class="youtube-logo-img min-w-[108px] w-[108px]" src="@/assets/icons/header/youtube-logo.svg"
                    alt="">
            </router-link>
        </div>
        <div class="center-div bg-transparent flex flex-col w-[60%] h-full justify-center items-center relative top-1">
            <div class="search-div">
                <div class="w-[60%] h-[40px] flex flex-row relative">
                    <input v-model="searchBarText" autocomplete="off" type="text" class="search-bar w-full h-full"
                        placeholder="Search">
                    <button @click="searchVideo(searchBarText)" class="search-btn active:border-black active:border-2ث">
                        <div class="w-[24px] h-[24px] flex justify-center items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" height="24" viewBox="0 0 24 24"
                                width="24" focusable="false" aria-hidden="true"
                                style="pointer-events: none; display: inherit; width: 100%; height: 100%;">
                                <path clip-rule="evenodd"
                                    d="M16.296 16.996a8 8 0 11.707-.708l3.909 3.91-.707.707-3.909-3.909zM18 11a7 7 0 00-14 0 7 7 0 1014 0z"
                                    fill-rule="evenodd"></path>
                            </svg>
                        </div>
                    </button>
                    <div v-if="searchBarText.length >= 3 && isAutoCompleteOpen"
                        class="autocomplete-bar absolute top-10 w-[543px] h-[540px] bg-white z-40 rounded-xl custom-shadow-inset">
                        <div v-if="!isSearchLoading"
                            class="flex flex-col justify-center items-center gap-y-1 py-4 h-full">
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
            </div>
        </div>
        <div class="right-div">
            <div class="flex flex-row gap-x-4 items-center">
                <router-link to="/studio/">
                    <button class="flex flex-row justify-center items-center px-2 ml-4 rounded-3xl bg-[#f2f2f2]
                     hover:bg-[#e5e5e5] w-[97px] h-[36px]">
                        <img class="w-[18px] h-[18px]" :src="plusIcon" alt="">
                        <span class="text-[14px] font-medium ml-2">Create</span>
                    </button>
                </router-link>
                <button @click="toggleNotificationContainer"
                    class="mx-auto w-9 min-w-[40px] h-9 min-h-[40px] rounded-full mr-2 relative hover:bg-[#e5e5e5] flex justify-center items-center">
                    <div class="w-[24px] h-[24px] flex justify-center items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" height="24" viewBox="0 0 24 24"
                            width="24" focusable="false" aria-hidden="true"
                            style="pointer-events: none; display: inherit; width: 100%; height: 100%;">
                            <path clip-rule="evenodd"
                                d="m13.497 4.898.053.8.694.4C15.596 6.878 16.5 8.334 16.5 10v2.892c0 .997.27 1.975.784 2.83L18.35 17.5H5.649l1.067-1.778c.513-.855.784-1.833.784-2.83V10c0-1.666.904-3.122 2.256-3.902l.694-.4.053-.8c.052-.78.703-1.398 1.497-1.398.794 0 1.445.618 1.497 1.398ZM6 10c0-2.224 1.21-4.165 3.007-5.201C9.11 3.236 10.41 2 12 2c1.59 0 2.89 1.236 2.993 2.799C16.79 5.835 18 7.776 18 10v2.892c0 .725.197 1.436.57 2.058l1.521 2.535c.4.667-.08 1.515-.857 1.515H15c0 .796-.316 1.559-.879 2.121-.562.563-1.325.879-2.121.879s-1.559-.316-2.121-.879C9.316 20.56 9 19.796 9 19H4.766c-.777 0-1.257-.848-.857-1.515L5.43 14.95c.373-.622.57-1.333.57-2.058V10Zm4.5 9c0 .398.158.78.44 1.06.28.282.662.44 1.06.44s.78-.158 1.06-.44c.282-.28.44-.662.44-1.06h-3Z"
                                fill-rule="evenodd"></path>
                        </svg>
                    </div>
                    <!-- <img src="@/assets/icons/header/notifications.svg" class="notification-img" alt=""> -->
                    <span v-if="unreadNotifications >= 1" class="w-[18px] h-[18px] absolute top-0 -right-[1px] bg-red-500 text-white text-medium text-[12px] 
                     rounded-full flex justify-center items-center">{{ unreadNotifications }}</span>
                </button>
                <div @vue:mounted="markVisibleNotificationsAsRead" v-if="isNotificationContainerExpanded"
                    class="notification-container custom-shadow-inset max-w-[480px]">
                    <div class="notification-title flex w-full items-center flex-row">
                        <p class="mb-1">Notifications</p>
                        <span v-if="notifications.length >= 1" @click="deleteAllNotifications"
                            class="cursor-pointer ml-auto w-auto mt-1 px-2 mr-4 text-[15px] text-blue-700 font-medium">
                            Delete All
                        </span>
                        <hr>
                    </div>
                    <div v-if="isUserAuthenticated && !isLoading">
                        <div v-for="notification in notifications" :key="notification.id"
                            class="notification z-1 relative">
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
                            </button>
                            <div @click.stop="hideNotification(notification.id)"
                                v-if="expandedNotification.includes(notification.id)" class="custom-shadow-inset flex flex-row w-[300px] rounded-lg p-2 h-[46px] items-center bg-white
                                hover:bg-[#f9f9f9] z-[999] absolute -bottom-4 right-0 cursor-pointer">
                                <div class="w-[24px] h-[24px] flex justify-center items-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24"
                                        height="24" viewBox="0 0 24 24" width="24" focusable="false" aria-hidden="true"
                                        style="pointer-events: none; display: inherit; width: 100%; height: 100%;">
                                        <path
                                            d="m3.85 3.15-.7.7L6.19 6.9C4.31 8.11 2.83 9.89 2 12c1.57 3.99 5.45 6.82 10 6.82 1.77 0 3.44-.43 4.92-1.2l3.23 3.23.71-.71L3.85 3.15zM13.8 14.5c-.51.37-1.13.59-1.8.59-1.7 0-3.09-1.39-3.09-3.09 0-.67.22-1.29.59-1.8l4.3 4.3zM12 17.82c-3.9 0-7.35-2.27-8.92-5.82.82-1.87 2.18-3.36 3.83-4.38L8.79 9.5c-.54.69-.88 1.56-.88 2.5 0 2.25 1.84 4.09 4.09 4.09.95 0 1.81-.34 2.5-.88l1.67 1.67c-1.27.61-2.69.94-4.17.94zm-.51-9.87c.17-.02.34-.05.51-.05 2.25 0 4.09 1.84 4.09 4.09 0 .17-.02.34-.05.51l-1.01-1.01c-.21-1.31-1.24-2.33-2.55-2.55l-.99-.99zM9.12 5.59c.92-.26 1.88-.41 2.88-.41 4.55 0 8.43 2.83 10 6.82-.58 1.47-1.48 2.78-2.61 3.85l-.72-.72c.93-.87 1.71-1.92 2.25-3.13C19.35 8.45 15.9 6.18 12 6.18c-.7 0-1.39.08-2.06.22l-.82-.81z">
                                        </path>
                                    </svg>
                                </div>
                                <p class="text-[14px] font-normal text-center">Hide
                                    this Notification</p>
                            </div>
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
            <router-link :to="isUserAuthenticated ? `/channel-page/${channelId}` : '/auth/'">
                <button class="channel-profile-btn w-[40px] h-[40px]">
                    <img :src="isUserAuthenticated ? userProfileImgSrc : unAuthenticatedUserImg"
                        class="rounded-full w-full h-full" alt="">
                </button>
            </router-link>
        </div>
    </header>
</template>
<style scoped>
@media screen and (max-width: 804px) {
    .center-div {
        display: none;
    }
}


@media screen and (min-width: 646px) {
    .notification-container {
        display: flex;
        position: absolute;
        flex-direction: column;
        top: 55px;
        right: 135px;
        height: auto;
        max-height: 450px;
        scrollbar-width: thin;
        overflow-y: auto;
        overflow-x: hidden;
        border-radius: 16px;
        z-index: 100;
        background-color: white;
    }
}


@media screen and (max-width: 645px) {
    .notification-container {
        display: flex;
        position: fixed;
        flex-direction: column;
        top: 55px;
        left: 0;
        height: auto;
        max-width: 100%;
        max-height: 450px;
        scrollbar-width: thin;
        overflow-y: auto;
        overflow-x: hidden;
        border-radius: 16px;
        z-index: 100;
        background-color: white;
    }
}



.custom-shadow-inset {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}
</style>