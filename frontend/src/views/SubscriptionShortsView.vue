<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import axios from 'axios';
import { sharedState } from '@/sharedState';

const toast = useToast()
const router1 = useRoute()
const router2 = useRouter()

const shortVideos = reactive([])
const MountPage = (user_session_id) => {
    axios.get(`${sharedState.websiteUrl}/videos/subscriptions-list-shorts`, {
        params: {
            user_session_id: user_session_id
        }
    }).then((response) => {
        if (response.status == 200) {
            shortVideos.splice(0, shortVideos.length, ...response.data.short_videos)
        }
    }).catch((error) => console.log("Error: ", error))
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

    await userAuthentication(user_session_id)
    if (!isUserAuthenticated) {
        router2.push({ name: "auth" })
    }

    MountPage(user_session_id)
})
</script>
<template>
    <div class="flex flex-col absolute left-[240px] top-[80px] font-roboto">
        <div class="w-full h-auto items-center flex flex-row">
            <p class="text-[20px] font-bold mt-6 mb-4 pb-3">Shorts</p>
            <router-link class="ml-auto mr-2" to="/subscriptions">
                <button
                    class="w-auto px-3 h-[36px] text-[14px] font-medium rounded-3xl text-blue-600 hover:bg-[#def1ff]">
                    View Videos
                </button>
            </router-link>
        </div>
        <div class="flex flex-row flex-wrap w-[1279px] gap-x-1 gap-y-2">
            <div v-for="video in shortVideos" :key="video.unique_id" class="relative video w-[209px] h-[370px]">
                <router-link :to="`/short/${video.unique_id}`">
                    <img class="w-full h-full"
                        :src="video.thumbnail_url" alt="">
                    <span class="absolute bottom-1 left-2 text-[15px] font-normal text-white">{{ video.views }}
                        views</span>
                </router-link>
            </div>
        </div>
    </div>
</template>