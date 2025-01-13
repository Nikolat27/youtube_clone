<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';

const router1 = useRoute()
const router2 = useRouter()

// Icons
import arrowDown from '/src/assets/icons/svg-icons/arrow-down-icon.svg'
import playIcon from '/src/assets/icons/video-player/play-icon.png'
import kebabMenuIcon from '/src/assets/icons/svg-icons/kebab-menu.svg'

const isFilterOpen = ref(false)
const toggleFilterOpening = () => {
    isFilterOpen.value = !isFilterOpen.value
}

const filterPlaylists = () => { }


const retrievePlaylists = (user_session_id) => {
    axios.get("http://127.0.0.1:8000/playlist/", {
        params: {
            user_session_id: user_session_id
        }
    }).then((response) => {
        if (response.status == 200) {
            console.log(response.data.data)
        }
    }).catch((error) => { console.log(error) })
}

onMounted(() => {
    const user_session_id = sessionStorage.getItem("user_session_id")
    if (user_session_id) {
        retrievePlaylists(user_session_id)
    } else {
        router2.push({ name: "auth" })
    }
})
</script>

<template>
    <div class="flex flex-col font-roboto left-[260px] top-[70px] relative gap-y-4">
        <div class="title">
            <p class="text-[36px] font-bold">Playlists</p>
        </div>
        <div class="filters">
            <button @click="toggleFilterOpening" class="bg-[#f2f2f2] w-[62.35px] h-[32px] rounded-lg flex flex-row justify-center
             items-center gap-x-2">
                <span class="font-medium text-[14px]">
                    A-Z
                </span>
                <img class="w-[12px] h-[12px]" :src="arrowDown" alt="">
            </button>
            <div v-if="isFilterOpen" class="w-[256px] h-[80px] rounded-lg flex flex-col text-[14px] font-normal bg-white
             custom-shadow-inner">
                <button class="w-full h-1/2 text-left pl-2 hover:bg-[#f2f2f2] rounded-tl-lg rounded-tr-lg">
                    A-Z
                </button>
                <button class="w-full h-1/2 text-left pl-2 hover:bg-[#f2f2f2] rounded-bl-lg rounded-br-lg">
                    Recently added
                </button>
            </div>
        </div>
        <div class="flex flex-row flex-wrap gap-x-4 gap-y-12">
            <div class="playlist">
                <div class="flex flex-col gap-y-2">
                    <div class="relative w-[295px] h-[166px]">
                        <img class="w-full h-full object-fill rounded-lg"
                            src="C:\Users\Sam\Desktop\youtube_clone\frontend\src\assets\img\Django.png" alt="">
                        <div class="cursor-pointer play-buttons flex flex-row gap-x-4 absolute top-1/2 left-[83px]">
                            <img class="w-[20px] h-[20px]" :src="playIcon" alt="">
                            <span class="text-[14px] font-medium text-white">Play all</span>
                        </div>
                        <span class="absolute bottom-2 right-2 w-[63px] h-[20px] text-[12px] text-white
                         bg-[#474646] font-medium text-center rounded-md bg-opacity-80">
                            3 videos</span>
                    </div>
                </div>
                <div class="flex flex-col mt-1">
                    <div class="flex flex-row justify-start items-center">
                        <p class="text-[14px] font-medium">Playlist title</p>
                        <button
                            class="justify-self-end ml-auto w-[36px] h-[36px] rounded-full flex justify-center items-center hover:bg-[#e5e5e5]">
                            <img class="w-[14px] h-[14px]" :src="kebabMenuIcon" alt="">
                        </button>
                    </div>
                    <p class="text-[14px] font-normal text-gray-600">Public or private</p>
                    <p class="text-[14px] font-normal text-gray-700">View full playlist</p>
                </div>
            </div>
        </div>
    </div>
</template>
<style scoped>
.custom-shadow-inner {
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.5);
}
</style>