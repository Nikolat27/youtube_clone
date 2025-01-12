<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import axios from 'axios';

const toast = useToast()
const router1 = useRoute()
const router2 = useRouter()

// Icons
import fillBellSrc from '/src/assets/icons/svg-icons/notification-alert-icon.svg'
import emptyBellSrc from '/src/assets/icons/svg-icons/bell-line-icon.svg'



// Handle Channel`s options
const isChannelOptionsOpen = ref(false)
const toggleChannelOptions = () => isChannelOptionsOpen.value = !isChannelOptionsOpen.value


// Handle Search Bar
const isSearchBarOpen = ref(false)
const toggleSearchBar = () => isSearchBarOpen.value = !isSearchBarOpen.value
const handleClickOutside = (event) => {
    const searchInputBar = document.getElementById("search-input")
    const searchButton = document.getElementById("search-button")
    if (searchInputBar && searchButton && !searchInputBar.contains(event.target) && !searchButton.contains(event.target)) {
        isSearchBarOpen.value = !isSearchBarOpen.value
    }
}

const submitSearch = (event) => {
    if (event.key !== "Enter") return;
    const query = event.target.value;
    router2.push({ path: '/channel-page/search', query: { 'query': query } })
}


// Handle Channel Description
const isDescriptionOpen = ref(false)
const truncateChannelDescription = (description) => {
    return isDescriptionOpen.value ? description : description.substring(0, 40) + '...'
}
const toggleDescription = () => isDescriptionOpen.value = !isDescriptionOpen.value;


const isUserAuthenticated = ref(false)
const isChannelSubscribed = ref(null)
const channelNotification = ref(null)

const channelInfo = reactive({})
const retrieveChannelInfo = (uniqueIdentifier) => {
    axios.get(`http://127.0.0.1:8000/channel/${uniqueIdentifier}`, {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 200) {
            Object.assign(channelInfo, response.data.data.details)
            isChannelSubscribed.value = response.data.data.is_sub
            channelNotification.value = response.data.data.channel_notification
        }
    }).catch((error) => toast.error(error))
}

const channelSubscribe = (channelId) => {
    if (!isUserAuthenticated.value) {
        toast.error("You have Login to subscribe a channel!")
        return;
    }
    axios.get(`http://127.0.0.1:8000/channel/subscribe/${channelId}`, {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 200) {
            toast.success(response.data.data)
            isChannelSubscribed.value = !isChannelSubscribed.value
        }
    }).catch((error) => toast.error(error))
}

const toggleChannelNotification = (channelId, notification) => {
    axios.get(`http://127.0.0.1:8000/channel/notification/${channelId}`, {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id"),
            notification: notification
        }
    }).then((response) => {
        if (response.status == 200) {
            toast.info(response.data.data)
        }
    }).catch((error) => {
        toast.error(error)
    }).finally(() => {
        channelNotification.value = !channelNotification.value
        toggleChannelOptions()
    })
}

const checkUserAuthentication = (user_session_id) => {
    axios.get("http://127.0.0.1:8000/users/is_authenticated", {
        params: {
            user_session_id: user_session_id
        }
    }).then((response) => {
        if (response.status == 200) {
            isUserAuthenticated.value = true
        }
    }).catch((error) => console.error)
}

onMounted(() => {
    const uniqueIdentifier = router1.params.id;
    retrieveChannelInfo(uniqueIdentifier)

    const user_session_id = sessionStorage.getItem("user_session_id")
    if (user_session_id) {
        checkUserAuthentication(user_session_id)
    }

    document.addEventListener('click', handleClickOutside);
});

</script>
<template>
    <div class="channel-container w-[1070px] h-100 absolute left-[345px] top-16">
        <div>
            <img class="h-[172px] rounded-2xl w-[100%]" :src="channelInfo.banner_url ?? ''" alt="">
        </div>
        <div class="flex flex-row mt-8 gap-x-4">
            <img class="w-[160px] h-[160px] rounded-full" :src="channelInfo.profile_url" alt="">
            <div class="flex flex-col gap-y-3">
                <span class="text-4xl font-bold -mt-2">{{ channelInfo.name }}</span>
                <div class="flex flex-row text-sm font-normal text-[#9b97a5] gap-x-1 justify-start items-center">
                    <span>{{ channelInfo.name }} &nbsp;.</span>
                    <span>{{ channelInfo.total_subs }} subscribers &nbsp;.</span>
                </div>
                <div class="flex flex-row text-sm font-normal justify-start items-center">
                    <span class="text-[#9b97a5]">{{ truncateChannelDescription(channelInfo.description ?? '') }}<span
                            @click="toggleDescription" class="text-black font-bold cursor-pointer ml-2">{{
                                isDescriptionOpen ? "Show Less" : "Show More" }}</span></span>
                </div>
                <button v-if="isChannelSubscribed" @click="toggleChannelOptions" class="w-[150px] h-[36px] rounded-2xl bg-[#f2f2f2] hover:bg-[#e5e5e5]
                 flex justify-center items-center">
                    <img class="w-5 h-6" :src="channelNotification ? fillBellSrc : emptyBellSrc" alt="">
                    <span class="text-black text-sm font-medium ml-2">Subscribed</span>
                    <img class="w-3 h-3 ml-5" src="@/assets/icons/svg-icons/thin-chevron-arrow-bottom-icon.svg" alt="">
                </button>
                <button v-else @click="channelSubscribe(channelInfo.id)"
                    class="w-[94px] h-[36px] rounded-3xl bg-black mt-2">
                    <span class="text-sm font-medium text-white">Subscribe</span>
                </button>

                <div v-if="isChannelSubscribed && isChannelOptionsOpen" class="channel-options w-[256px]
                 h-auto flex flex-col my-shadow rounded-xl text-sm font-normal -mt-3">
                    <button @click="toggleChannelNotification(channelInfo.id, 'all')" class="w-[100%] h-[40px] mt-2">
                        <img :src="fillBellSrc" alt="">
                        <span>All</span>
                    </button>
                    <!-- <a class="w-[100%] h-[40px]">
                        <img src="@/assets/icons/svg-icons/bell-line-icon.svg" alt="">
                        <span>Personalized</span>
                    </a> -->
                    <button @click="toggleChannelNotification(channelInfo.id, 'none')" class="w-[100%] h-[40px]">
                        <img src="@/assets/icons/svg-icons/remove-bell-notification-icon.svg" alt="">
                        <span>None</span>
                    </button>
                    <button @click="channelSubscribe(channelInfo.id)" class="w-[100%] h-[40px] mb-2">
                        <img src="@/assets/icons/svg-icons/remove-male-user-icon.svg" alt="">
                        <span>Unsubscribe</span>
                    </button>
                </div>
            </div>
        </div>
        <div class="tabs-inner-container w-[1280px] h-[48px] bg-white ml-[-115px] mt-3 border-b">
            <div class="flex flex-row ml-[130px] items-center">
                <router-link :to="`/channel-page/${$route.params.id}`"
                    :class="[$route.name == 'channel-home' ? 'active' : '', 'tab', 'w-[48px]']">Home</router-link>
                <router-link :to="{ name: 'channel-videos', params: { id: $route.params.id } }"
                    :class="[$route.name == 'channel-videos' ? 'active' : '', 'tab', 'w-[48px]']">Videos</router-link>
                <router-link :to="{ name: 'channel-shorts', params: { id: $route.params.id } }"
                    :class="[$route.name == 'channel-shorts' ? 'active' : '', 'tab', 'w-[48px]']">Shorts</router-link>
                <router-link :to="{ name: 'channel-playlists', params: { id: $route.params.id } }"
                    :class="[$route.name == 'channel-playlists' ? 'active' : '', 'tab', 'w-[50px]']">Playlists</router-link>
                <router-link :to="{ name: 'channel-community', params: { id: $route.params.id } }"
                    :class="[$route.name == 'channel-community' ? 'active' : '', 'tab', 'w-[73px]']">Community</router-link>
                <div class="flex flex-row h-[28px] gap-x-6 items-center">
                    <button id="search-button" @click="toggleSearchBar"
                        class="mr-0 w-10 h-10 flex justify-center items-center">
                        <img class="w-5 h-5" src="@/assets/icons/svg-icons/search-line-icon.svg" alt="">
                    </button>
                    <input @keydown="submitSearch" autocomplete="off" id="search-input" v-if="isSearchBarOpen"
                        name="query" class="flex placeholder:font-normal text-sm w-[174px] ml-[-15px]
                     border-b-2 border-b-black outline-none pb-1" type="text" placeholder="Search">
                </div>
            </div>
        </div>
        <div id="content-container" class="mb-20">
            <router-view></router-view>
        </div>
    </div>
</template>