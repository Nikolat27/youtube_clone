<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import { useRoute, useRouter } from 'vue-router';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import axios from 'axios';
import { sharedState } from '@/sharedState';

const toast = useToast()
const router1 = useRoute()
const router2 = useRouter()

const isClearHistoryDialogOpen = ref(false)
const isPauseHistoryDialogOpen = ref(false)
const isPlayHistoryDialogOpen = ref(false)
const isDeleteCommentsDialogOpen = ref(false)

const clearAllUserWatchHistory = () => {
    const user_session_id = sessionStorage.getItem("user_session_id")
    axios.delete(`${sharedState.websiteUrl}/videos/clear-all-user-watch-history`, {
        params: {
            user_session_id: user_session_id
        }
    }).then((response) => {
        if (response.status == 204) {
            retrieveVideos(user_session_id)
            toast.success("Your cleared your watch history!")
            isClearHistoryDialogOpen.value = false
        }
    }).catch(() => toast.error("Error!"))
}

const toggleWatchHistory = () => {
    axios.get(`${sharedState.websiteUrl}/videos/toggle-watch-history`, {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 200) {
            isPauseHistoryDialogOpen.value = false
            isPlayHistoryDialogOpen.value = false
            toast.success("You changed your watch history!")
            historyEnable.value = !historyEnable.value
        }
    }).catch(() => toast.error("Error!"))
}

const clearAllUserCommentsReplies = () => {
    axios.delete(`${sharedState.websiteUrl}/videos/clear-user-comments-replies`, {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 204) {
            toast.success("Your comments and replies have been removed")
            isDeleteCommentsDialogOpen.value = false
        }
    }).catch(() => toast.error("Error!"))
}

const toggleClearHistoryDialog = () => isClearHistoryDialogOpen.value = !isClearHistoryDialogOpen.value
const togglePauseHistoryDialog = () => isPauseHistoryDialogOpen.value = !isPauseHistoryDialogOpen.value
const togglePlayHistoryDialog = () => isPlayHistoryDialogOpen.value = !isPlayHistoryDialogOpen.value
const toggleDeleteCommentsDialog = () => isDeleteCommentsDialogOpen.value = !isDeleteCommentsDialogOpen.value

const dialogBar = {
    props: ["main_title", "fst_para", "sec_para", "submitBtnText", 'isDialogOpen', 'toggleDialog', 'submitFunction'],
    template: `
        <div v-if='isDialogOpen' class="z-50 bg-white top-[150px] left-[130px] flex mx-auto justify-start p-6 items-start absolute flex-col gap-y-4
        w-[688px] min-h-[262px] h-auto rounded-2xl font-roboto" style="box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);">
            <p class="font-normal text-base">{{ main_title }}</p>
            <p class="font-medium text-sm text-[#666666]">{{ fst_para }}</p>
            <p class="font-medium text-sm text-[#666666] mb-12">{{ sec_para }}</p>
            <div class="flex flex-row gap-x-2 text-sm font-medium absolute bottom-2 right-2">
                <button @click="toggleDialog" class="w-[74.9px] h-[36px] font-roboto rounded-3xl text-black
                hover:bg-[#e5e5e5]">Cancel</button>
                <button @click="submitFunction" class="w-auto pl-4 pr-4 h-[36px] rounded-3xl text-[#1a6cd8]
                hover:bg-[#def1ff]">{{ submitBtnText }}</button>
            </div >
        </div >
    `
}

const videos = reactive([])
const isLoading = ref(false)
const historyEnable = ref(null)

const retrieveVideos = async (user_session_id) => {
    isLoading.value = true
    await axios.get(`${sharedState.websiteUrl}/videos/user-watch-history`, {
        params: {
            user_session_id: user_session_id
        }
    }).then((response) => {
        if (response.status == 200) {
            videos.splice(0, videos.length, ...response.data.data)
            historyEnable.value = response.data.history_enable
        }
    }).catch((error) => console.log("Error: ", error)).finally(() => isLoading.value = false)
}

const MountPage = (user_session_id) => {
    retrieveVideos(user_session_id)
}

const removeVideoFromWatchHistory = (video_id) => {
    const user_session_id = sessionStorage.getItem("user_session_id")
    axios.delete(`${sharedState.websiteUrl}/videos/delete-user-watch-history/${video_id}`, {
        params: {
            user_session_id: user_session_id
        }
    }).then((response) => {
        if (response.status == 204) {
            retrieveVideos(user_session_id)
        }
    })
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
    if (!isUserAuthenticated.value) {
        router2.push({ name: "auth" })
    }

    MountPage(user_session_id)

})
</script>

<template>
    <div class="flex flex-row w-[1070px] ml-[300px] mt-[130px] relative">
        <div class="z-auto flex flex-col w-[628px] h-[600px] gap-y-4 relative">
            <div class="flex flex-col">
                <div class="top-[-45px] font-bold text-4xl relative">
                    <p>Watch History</p>
                </div>
                <!-- <div class="relative font-bold text-xl">
                    <p>Today</p>
                </div> -->
            </div>
            <div v-if="!isLoading" class="flex flex-col">
                <div v-for="video in videos" :key="video.unique_id" class="history-video flex flex-row relative">
                    <div class="w-[246px] h-[138px] flex flex-row">
                        <img class="w-[100%] h-[100%] rounded-lg" :src="video.thumbnail_url" alt="">
                    </div>
                    <div class="flex flex-col cursor-pointer ml-4">
                        <router-link :to="`video/${video.unique_id}`">
                            <p class="font-normal text-lg">{{ video.title }}</p>
                        </router-link>
                        <div class="flex flex-row">
                            <router-link :to="`/channel-page/${video.channel_id}`">
                                <p class="text-xs font-normal text-[#7d8a9f] hover:text-[#6b6b6b]">{{ video.channel_name
                                    }}&nbsp;
                                </p>
                            </router-link>
                            <span class="text-[#7d8a9f] text-xs font-normal hover:text-[#6b6b6b] mb-4">. {{ video.views
                                }}
                                views</span>
                        </div>
                        <p class="text-[#7d8a9f] text-xs font-normal hover:text-[#6b6b6b]">{{ video.description }}</p>
                    </div>
                    <button @click="removeVideoFromWatchHistory(video.unique_id)"
                        class="w-10 h-10 absolute right-0 top-0 rounded-full hover:bg-[#e5e5e5] flex justify-center items-center">
                        <img class="w-5 h-5" src="@/assets/icons/svg-icons/x-mark-icon.svg" alt="">
                    </button>
                    <div class="remove-history hidden flex-col pl-2 pt-3 text-white bg-[#717171] text-xs font-normal w-[110px] h-[55px]
                    rounded-md absolute right-[-35px] top-12 opacity-90">
                        <p>Remove from</p>
                        <p>watch history</p>
                    </div>
                </div>
                <div v-if="videos.length <= 0">
                    <p class="text-[20px] font-semibold underline">No Videos currently!</p>
                </div>
            </div>
            <div v-else class="mt-40 ml-20">
                <PulseLoader size="20px" color="red"></PulseLoader>
            </div>
            <!-- <div class="flex flex-col relative mt-[80px]">
                <div class="top-[-60px] absolute font-bold text-xl">
                    <p>Yesterday</p>
                </div>
                <div class="w-4 h-4 flex flex-row justify-start items-center absolute left-2 top-[-5px]">
                    <img src="@/assets/icons/svg-icons/shorts-icon.svg">
                    <p class="font-bold text-xl">&nbsp;&nbsp;Shorts</p>
                </div>
                <button id="prevButton"
                    class="z-10 w-9 h-9 absolute top-[210px] left-[-20px] shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                    <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-left-icon.svg"
                        alt="">
                </button>
                <div id="slider" class="z-0 history-short-video flex overflow-hidden flex-row gap-x-1
                gap-y-8 h-[485px] w-[640px] relative">
                    <div class="flex flex-col w-[210px] h-[405px] mt-8 relative">
                        <img class="w-[100%] h-[100%] rounded-lg" src="@/assets/img/Django.png" alt="">
                        <p class="text-base font-medium mt-2">Lorem ipsum</p>
                        <button class="short-video-options-toggle flex justify-center items-center absolute bottom-[-6px] right-0
                        w-8 h-8 rounded-full hover:bg-[#9c8c8c]">
                            <img class="w-[50%] h-[50%]" src="@/assets/icons/svg-icons/kebab-menu.svg" alt="">
                        </button>
                        <div id="short-video-1" class="z-auto w-[230px] h-10 history-short-video-options absolute right-[-198px] bottom-[-45px]
                        hidden flex-col gap-y-4 rounded-xl bg-white shadow-lg">
                            <a href="#">
                                <div
                                    class="pl-3 w-[230px] h-10 flex flex-row rounded-xl justify-start items-center gap-x-2 hover:bg-[#e5e5e5]">
                                    <img class="w-5 h-5 rounded-full" src="@/assets/icons/svg-icons/hide-icon.svg"
                                        alt="">
                                    <p class="text-base font-normal">Hide</p>
                                </div>
                            </a>
                        </div>
                    </div>
                    <div class="flex flex-col w-[210px] h-[405px] mt-8 relative">
                        <img class="w-[100%] h-[100%] rounded-lg" src="@/assets/img/Django.png" alt="">
                        <p class="text-base font-medium mt-2">Lorem ipsum</p>
                        <button class="short-video-options-toggle flex justify-center items-center absolute bottom-[-6px] right-0
                        w-8 h-8 rounded-full hover:bg-[#e5e5e5]">
                            <img class="w-[50%] h-[50%]" src="@/assets/icons/svg-icons/kebab-menu.svg" alt="">
                        </button>
                        <div id="short-video-2" class="z-auto w-[230px] h-10 history-short-video-options absolute right-[-198px] bottom-[-45px]
                        hidden flex-col gap-y-4 rounded-xl bg-white shadow-lg">
                            <a href="#">
                                <div
                                    class="pl-3 w-[230px] h-10 flex flex-row rounded-xl justify-start items-center gap-x-2 hover:bg-[#e5e5e5]">
                                    <img class="w-5 h-5 rounded-full" src="@/assets/icons/svg-icons/hide-icon.svg"
                                        alt="">
                                    <p class="text-base font-normal">Hide</p>
                                </div>
                            </a>
                        </div>
                    </div>
                </div>
                <hr>
                <button id="nextButton"
                    class="z-auto w-9 h-9 absolute top-[210px] right-[-30px] shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                    <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-right-icon.svg"
                        alt="">
                </button>
            </div> -->
        </div>
        <div v-if="isClearHistoryDialogOpen || isPauseHistoryDialogOpen || isDeleteCommentsDialogOpen"
            class="fixed inset-0 bg-[#b2b2b2] bg-opacity-80 z-40"></div>
        <dialogBar :isDialogOpen="isClearHistoryDialogOpen" :toggleDialog="toggleClearHistoryDialog"
            main_title="Clear watch history?" fst_para="Your YouTube watch history will be cleared from all
                YouTube apps on all devices." sec_para="Your video recommendations will be reset, but may still be
                influenced by activity on other Google products." submitBtnText="Clear watch history"
            :submitFunction="clearAllUserWatchHistory"></dialogBar>
        <dialogBar :isDialogOpen="isPauseHistoryDialogOpen" :toggleDialog="togglePauseHistoryDialog"
            :submitFunction="toggleWatchHistory" main_title="Pause watch history?" fst_para="Pausing YouTube watch history can make it harder to find videos you watched, and you may see fewer recommendations for new videos in YouTube and other Google products.
                "
            sec_para="Remember, pausing this setting doesn't delete any previous activity, but you can view, edit and delete your private YouTube watch history data anytime. When you pause and clear your watch history, YouTube features that rely on history to personalize your experience are disabled."
            submitBtnText="Pause"></dialogBar>
        <dialogBar :isDialogOpen="isPlayHistoryDialogOpen" :toggleDialog="togglePlayHistoryDialog"
            :submitFunction="toggleWatchHistory" main_title="Play watch history?"
            fst_para="Playing YouTube watch history"
            sec_para="Remember, playing this setting doesn't delete any previous activity, but you can view, edit and delete your private YouTube watch history data anytime. When you play and clear your watch history, YouTube features that rely on history to personalize your experience are disabled."
            submitBtnText="Play"></dialogBar>
        <dialogBar :isDialogOpen="isDeleteCommentsDialogOpen" :toggleDialog="toggleDeleteCommentsDialog"
            :submitFunction="clearAllUserCommentsReplies" main_title="Delete all the comments and replies?" fst_para="َAll the comments and replies that you have shared since your YouTube account has been created
             will be deleted (Even the comments that people have replied to you)!" submitBtnText="Delete All">
        </dialogBar>
        <div class="flex flex-col w-[441px] ml-[200px] mt-10">
            <!-- Search history div -->
            <!-- <div class="flex flex-row w-[235px] h-[10]">
                <button
                    class="w-12 h-10 mr-2 rounded-full cursor-pointer hover:bg-[#e5e5e5] flex justify-center items-center">
                    <img class="w-5 h-5" src="@/assets/icons/svg-icons/search-line-icon.svg" alt="">
                </button>
                <input type="text" name="query"
                    class="w-[235px] outline-none border-b-[1px] border-b-black focus:border-b-[#0f0f0f] focus:border-b-[2px] transition-all duration-100"
                    placeholder="Search watch history">
            </div> -->
            <div @click="toggleClearHistoryDialog" class="cursor-pointer flex flex-row w-[194px] h-[36px] mb-4 mt-7 justify-start
            items-center hover:bg-[#e5e5e5] rounded-3xl">
                <button class="w-10 h-10 flex justify-center items-center">
                    <img class="w-5 h-5" src="@/assets/icons/svg-icons/trash-can-icon.svg" alt="">
                </button>
                <p class="text-sm font-medium">Clear all watch history</p>
            </div>
            <div v-if="historyEnable" @click="togglePauseHistoryDialog"
                class="cursor-pointer flex flex-row w-[194px] h-[36px] justify-start items-center hover:bg-[#e5e5e5] rounded-3xl">
                <button class="w-10 h-10 flex justify-center items-center">
                    <img class="w-4 h-4" src="@/assets/icons/svg-icons/pause-icon.svg" alt="">
                </button>
                <p class="text-sm font-medium">Pause watch history</p>
            </div>
            <div v-else @click="togglePlayHistoryDialog"
                class="cursor-pointer flex flex-row w-[194px] h-[36px] justify-start items-center hover:bg-[#e5e5e5] rounded-3xl">
                <button class="w-10 h-10 flex justify-center items-center">
                    <img class="w-4 h-4" src="@/assets/icons/svg-icons/play-icon.svg" alt="">
                </button>
                <p class="text-sm font-medium">Play watch history</p>
            </div>
            <div @click="toggleDeleteCommentsDialog"
                class="cursor-pointer mb-4 mt-4 flex flex-row w-[260px] h-[45px] justify-start items-center hover:bg-[#e5e5e5] rounded-3xl">
                <button class="w-10 h-10 flex justify-center items-center pl-3">
                    <img class="w-7 h-7" src="@/assets/icons/svg-icons/speaking-bubbles-b-w-icon.svg" alt="">
                </button>
                <p class="text-sm font-medium pl-4">Clear all comments and replies history</p>
            </div>
        </div>
    </div>
</template>