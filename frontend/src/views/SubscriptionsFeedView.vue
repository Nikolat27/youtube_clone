<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import { useRoute, useRouter } from 'vue-router';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue';
import { sharedState } from '@/sharedState';

const toast = useToast()
const router1 = useRoute()
const router2 = useRouter()

// Icons
import fillBellSrc from '/src/assets/icons/svg-icons/notification-alert-icon.svg'
import emptyBellSrc from '/src/assets/icons/svg-icons/bell-line-icon.svg'

const openChannelOption = reactive([])
const toggleChannelOptions = (channelId) => {
    let index = openChannelOption.indexOf(channelId)
    if (index === -1) {
        openChannelOption.pop()
        openChannelOption.push(channelId)
    } else {
        openChannelOption.pop()
    }
}

const toggleChannelNotification = (channelId, type) => {
    const user_session_id = sessionStorage.getItem("user_session_id")
    axios.get(`${sharedState.websiteUrl}/channel/notification/${channelId}`, {
        params: {
            user_session_id: user_session_id,
            notification: type
        }
    }).then((response) => {
        if (response.status == 200) {
            MountPage(user_session_id)
            toast.success("Channel Notifications changed!")
        }
    }).catch(() => {
        toast.error("Error!")
    })
}

const channelSubscribe = (channelId) => {
    const user_session_id = sessionStorage.getItem("user_session_id")
    axios.get(`${sharedState.websiteUrl}/channel/subscribe/${channelId}`, {
        params: {
            user_session_id: user_session_id
        }
    }).then((response) => {
        if (response.status == 200) {
            MountPage(user_session_id)
            toast.success("Channel Unsubscribed!")
        }
    })
}

const isLoading = ref(false)
const channels = reactive([])
const MountPage = (user_session_id) => {
    openChannelOption.pop()
    isLoading.value = true
    axios.get(`${sharedState.websiteUrl}/channel/feed/subscriptions`, {
        params: {
            user_session_id: user_session_id
        }
    }).then((response) => {
        if (response.status == 200) {
            channels.splice(0, channels.length, ...response.data.data)
        }
    }).catch((error) => console.error(error)).finally(() => isLoading.value = false)
}

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

    await userAuthentication(userAuthentication)
    if (!isUserAuthenticated.value) {
        router2.push({ name: "auth" })
    }

    MountPage(user_session_id)
})
</script>
<template>
    <div class="flex flex-col absolute left-[400px] top-[100px]">
        <div class="text-[36px] font-bold mb-12">
            All Subscriptions
        </div>
        <div v-if="!isLoading">
            <div v-for="channel in channels" :key="channel.unique_identifier" class="flex flex-row w-[920px]">
                <router-link :to="`/channel-page/${channel.unique_identifier}`">
                    <img class="w-[136px] h-[136px] rounded-full mr-6" :src="channel.profile_picture_url" alt="">
                </router-link>
                <div class="flex flex-col justify-start items-start pt-4">
                    <router-link :to="`/channel-page/${channel.unique_identifier}`">
                        <p class="text-[18px] font-normal">{{ channel.name }}</p>
                    </router-link>
                    <div class="flex flex-row items-center mt-2 text-[12px] font-normal text-gray-600">
                        <p>@{{ channel.unique_identifier }}</p>
                        <p class="ml-4">{{ channel.total_subs }} subscribers</p>
                    </div>
                    <p class="text-[12px] font-normal text-gray-600">{{ channel.description }}
                    </p>
                </div>
                <div class="ml-auto pt-6 relative">
                    <button @click="toggleChannelOptions(channel.unique_identifier)" class="w-[150px] z-1 h-[36px] rounded-2xl bg-[#f2f2f2] hover:bg-[#e5e5e5]
                        flex justify-center items-center">
                        <img class="w-5 h-6" :src="channel.notification_type ? fillBellSrc : emptyBellSrc" alt="">
                        <span class="text-black text-sm font-medium ml-2">Subscribed</span>
                        <img class="w-3 h-3 ml-5" src="@/assets/icons/svg-icons/thin-chevron-arrow-bottom-icon.svg"
                            alt="">
                    </button>
                    <div v-if="openChannelOption.includes(channel.unique_identifier)"
                        class="bg-white z-10 channel-options w-[256px]
                        h-auto flex flex-col absolute top-[73px] left-0 my-shadow rounded-xl text-sm font-normal -mt-3">
                        <button @click="toggleChannelNotification(channel.id, 'all')" class="w-[100%] h-[40px] mt-2">
                            <img :src="fillBellSrc" alt="">
                            <span>All</span>
                        </button>
                        <button @click="toggleChannelNotification(channel.id, 'none')" class="w-[100%] h-[40px]">
                            <img src="@/assets/icons/svg-icons/remove-bell-notification-icon.svg" alt="">
                            <span>None</span>
                        </button>
                        <button @click="channelSubscribe(channel.id)" class="w-[100%] h-[40px] mb-2">
                            <img src="@/assets/icons/svg-icons/remove-male-user-icon.svg" alt="">
                            <span>Unsubscribe</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div v-else class="absolute left-[400px] top-[300px]">
            <ClipLoader color="red" size="55px"></ClipLoader>
        </div>
    </div>
</template>