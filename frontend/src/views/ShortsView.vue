<script setup>
import { ref, reactive, computed } from 'vue';
import socialShare from '@/components/socialShare.vue';
import { sharedState } from '@/sharedState';



// Toggling Sharing Tab
const toggleSharingTab = () => {
    sharedState.isSharingTabOpen = !sharedState.isSharingTabOpen
}


// Toggling Comment Container
const isCommentContainerOpen = ref(false)
const toggleCommentContainer = () => {
    const shortVideoWrapper = document.querySelector(".short-video-wrapper")
    isCommentContainerOpen.value = !isCommentContainerOpen.value;
    shortVideoWrapper.style.marginRight = isCommentContainerOpen.value ? "350px" : "0px";
}


// Fake comments
const comments = [
    { id: 1, text: "Hello World" },
    { id: 2, text: "Hello World" },
    { id: 3, text: "Hello World" },
]


// Toggle User Comment Options
const isUserOptionsOpen = ref(false)
const toggleUserOptions = () => isUserOptionsOpen.value = !isUserOptionsOpen.value


// Handling Comment opening
const openComments = reactive({})
const toggleUserComment = (commentId, state) => {
    if (!openComments[commentId]) {
        openComments[commentId] = { replyContainerVisible: false, userReplyOptionsVisible: false, replyOptionsVisible: false };
    }
    openComments[commentId][state] = !openComments[commentId][state];
}
const toggleReplyContainer = (comment_id) => toggleUserComment(comment_id, 'replyContainerVisible')
const toggleUserReplyOptionsVisible = (comment_id) => toggleUserComment(comment_id, 'userReplyOptionsVisible')
const toggleReplyOptions = (comment_id) => toggleUserComment(comment_id, 'replyOptionsVisible')


// Handle video`s playing
const isVideoPlayed = ref(true)
const toggleVideoPlay = () => {
    const video = document.getElementById("main-video")
    if (video.paused) {
        video.play()
    }
    else {
        video.pause()
    }
    isVideoPlayed.value = !isVideoPlayed.value
}


// Handle video`s voice 
const isVideoMuted = ref(false)
const toggleVideoMute = () => {
    const video = document.getElementById("main-video")
    video.muted = !video.muted
    isVideoMuted.value = !isVideoMuted.value
}


// Update video volume based on input range
const volumeValue = ref(100); // default volume value
const updateVolume = (event) => {
    volumeValue.value = event.target.value;
    const video = document.getElementById("main-video");
    video.volume = volumeValue.value / 100; // we devided the value by 100 because the 'volume' method 
    // only supports an int between 0 to 1
}


// Derived states for icons
const videoPlayIcon = computed(() => isVideoPlayed.value ? '/src/assets/icons/svg-icons/play-white-icon.png' : '/src/assets/icons/svg-icons/pause-icon.png');
const videoVolumeIcon = computed(() => {
    if (!isVideoMuted.value && volumeValue.value >= 50) return '/src/assets/icons/svg-icons/volume-white-icon.svg';
    if (!isVideoMuted.value) return '/src/assets/icons/svg-icons/speaker-icon-2.png';
    return '/src/assets/icons/svg-icons/muted-icon-2.png';
});



// Handle video fullscreen
const isVideoFullscreen = ref(false)
const toggleVideoFullscreen = () => {
    const video = document.getElementById("main-video");
    video.requestFullscreen();
    isVideoFullscreen.value = !isVideoFullscreen.value;
}
</script>

<template>
    <div class="flex flex-col justify-center items-center mt-16 gap-y-7">
        <div class="short-video-wrapper">
            <div class="short-video w-[350px] h-[600px] relative">
                <video id="main-video" oncontextmenu="return false;" class="w-[100%] h-[100%] object-cover rounded-2xl"
                    src="@/assets/video/test-vid3.mp4">
                </video>
                <button @click="toggleVideoPlay" class="w-[48px] h-[48px] flex justify-center items-center bg-opacity-75 rounded-full absolute top-2 left-4
                     bg-[#b2b1b2] hover:bg-[#797879]">
                    <img class="w-[15px] h-[17px]" :src="videoPlayIcon" alt="">
                </button>
                <button class="volume-button w-[48px] hover:w-[201px] h-[48px] flex justify-center items-center bg-opacity-75 rounded-full absolute top-2 left-20
                     bg-[#b2b1b2] hover:bg-[#797879]">
                    <img @click="toggleVideoMute" class="w-[22px] h-[22px] cursor-pointer" :src="videoVolumeIcon"
                        alt="">
                    <input id="volume-value" @input="updateVolume" v-model="volumeValue" type="range" min="0" max="100"
                        class="hidden ml-4 w-[132px] h-[29.3] bg-black outline-none">
                </button>
                <button @click="toggleVideoFullscreen" class="fullscreen-btn w-[48px] h-[48px] flex justify-center items-center bg-opacity-75 rounded-full absolute top-2 right-4
                     bg-[#b2b1b2] hover:bg-[#797879] cursor-pointer">
                    <img class="w-[22px] h-[22px]" src="@/assets/icons/svg-icons/fullscreen-icon.png" alt="">
                </button>
                <div class="short-video-info flex flex-col absolute bottom-7 left-4 text-white">
                    <div class="flex flex-row justify-center items-center gap-x-3">
                        <img src="@/assets/img/Django.png" class="w-8 h-8 rounded-full border-white border" alt="">
                        <p class="text-[14px] font-medium">@channelName</p>
                        <button
                            class="bg-white text-black w-[76px] h-[32px] rounded-2xl text-[12px] font-medium">Subscribe</button>
                    </div>
                    <h2 class="text-[14px] font-normal mt-4">Short video title</h2>
                </div>
                <div class="flex flex-col gap-y-4 justify-center items-center
                 absolute right-[-65px] bottom-[30px]">
                    <button class="w-12 h-12 bg-[#f2f2f2] rounded-full hover:bg-[#e5e5e5]">
                        <img src="@/assets/icons/svg-icons/like-empty.svg" class="h-[80%] w-[80%] m-auto" alt="">
                    </button>
                    <span class="mt-[-10px]">2k</span>
                    <button class="w-12 h-12 bg-[#f2f2f2] rounded-full hover:bg-[#e5e5e5]">
                        <img src="@/assets/icons/svg-icons/dislike-empty.svg" class="h-[80%] w-[80%] m-auto" alt="">
                    </button>
                    <span class="mt-[-10px]">Dislike</span>
                    <button @click="toggleCommentContainer"
                        class="comment-toggle-btn w-12 h-12 bg-[#f2f2f2] rounded-full hover:bg-[#e5e5e5]">
                        <img src="@/assets/icons/svg-icons/comment-empty-icon.svg" class="h-[60%] w-[60%] m-auto"
                            alt="">
                    </button>
                    <span class="mt-[-10px]">8</span>
                    <button @click="toggleSharingTab" class="w-12 h-12 bg-[#f2f2f2] rounded-full hover:bg-[#e5e5e5]">
                        <img src="@/assets/icons/svg-icons/share-btn.svg" class="h-[60%] w-[60%] m-auto" alt="">
                    </button>
                    <span class="mt-[-10px]">Share</span>
                    <button class="w-11 h-11 bg-[#f2f2f2] hover:bg-[#e5e5e5] rounded-full">
                        <a href="#"><img src="@/assets/img/Django.png" class="h-[100%] w-[100%] rounded-md"></a>
                    </button>
                </div>
                <div v-if="isCommentContainerOpen" class="z-10 flex absolute left-[450px] bottom-[50px] flex-col w-[500px] h-[500px] 
                    border-[1px] border-gray-400 rounded-2xl pt-2 max-w-[500px] max-h-[500px]">
                    <div class="flex flex-row justify-start items-center ml-2">
                        <p class="font-bold text-[20px] pl-2">Comments&nbsp;</p><span>414</span>
                        <button @click="toggleCommentContainer" class="w-10 h-10 border-none rounded-full bg-white hover:bg-[#e5e5e5]
                         ml-[310px]">
                            <img class="w-[50%] h-[50%] m-auto" src="@/assets/icons/svg-icons/x-mark-icon.svg" alt="">
                        </button>
                    </div>
                    <hr>
                    <div class="flex-grow flex flex-col overflow-y-auto max-h-[394px]" style="scrollbar-width: thin;">
                        <div v-for="comment in comments" :key="comment.id" class="flex flex-col gap-y-8">
                            <div class="flex flex-row gap-x-2 ml-4 mt-4">
                                <div>
                                    <img class="w-10 h-10 rounded-full" src="@/assets/img/Django.png" alt="">
                                </div>
                                <div class="flex flex-col flex-1 ml-2">
                                    <div class="flex flex-row justify-start items-center">
                                        <p class="text-[13px] font-medium">@Nikolat272</p>
                                        <span class="text-[12px] font-normal ml-2 text-[#918b8b]">13 days ago</span>
                                    </div>
                                    <div class="flex">
                                        <p class="text-[14px] font-normal">{{ comment.text }} / {{ comment.id }}</p>
                                    </div>
                                    <div class="flex flex-row items-center mt-2 relative">
                                        <button
                                            class="flex items-center justify-center w-8 h-8 rounded-full hover:bg-[#e5e5e5]">
                                            <img src="@/assets/icons/svg-icons/like-empty.svg" class="h-[80%] w-[80%]"
                                                alt="">
                                        </button>
                                        <span class="text-gray-500 text-[13px] font-normal">1.1k</span>
                                        <button class="w-8 h-8 rounded-full hover:bg-[#e5e5e5] ml-2">
                                            <img src="@/assets/icons/svg-icons/dislike-empty.svg"
                                                class="h-[80%] w-[80%] m-auto" alt="">
                                        </button>
                                        <button @click="toggleUserReplyOptionsVisible(comment.id)" class="flex justify-center items-center text-[12px] w-[42px] h-[27px]
                                            font-semibold border-none m-auto rounded-2xl hover:bg-[#e5e5e5] ml-2">
                                            Reply
                                        </button>
                                        <div v-if="openComments[comment.id]?.userReplyOptionsVisible"
                                            class="user-reply-creation-container absolute top-10 left-0 flex flex-row justify-center items-center">
                                            <img class="rounded-full w-6 h-6" src="@/assets/img/Django.png" alt="">
                                            <input type="text"
                                                class="ml-2 w-[90%] outline-none border-b hover:border-b-2 hover:border-black"
                                                placeholder="Add a comment..."
                                                style="transition: border-bottom 0.1s ease-in-out;">
                                            <div
                                                class="absolute left-[250px] flex flex-row justify-center items-center">
                                                <button @click="toggleUserReplyOptionsVisible(comment.id)"
                                                    class="cancel-comment-btn w-[70px] h-[32px] rounded-[18px]">Cancel</button>
                                                <button
                                                    class="submit-comment-btn w-[70px] h-[32px] rounded-[18px] ml-2">Reply</button>
                                            </div>
                                        </div>
                                    </div>
                                    <div @click="toggleReplyContainer(comment.id)"
                                        :class="['comment-reply-button', openComments[comment.id]?.userReplyOptionsVisible ? 'mt-10' : '']">
                                        <i
                                            :class="['arrow', openComments[comment.id]?.replyContainerVisible ? 'rotate-[225deg]' : 'button']"></i><span>
                                            &nbsp;&nbsp;63&nbsp;</span>replies
                                    </div>
                                    <div v-if="openComments[comment.id]?.replyContainerVisible"
                                        class="replies-container mt-3">
                                        <div class="reply">
                                            <div class="reply-author-img">
                                                <img src="@/assets/img/Django.png" alt="">
                                            </div>
                                            <div class="reply-detail">
                                                <div class="reply-author-info">
                                                    <p>@</p>
                                                    <p>Nikolat27</p>
                                                    <span>1 years </span>ago
                                                </div>
                                                <p class="reply-value">Hello World</p>
                                                <div class="reply-toolbar">
                                                    <button class="reply-like-button" style="outline: none;">
                                                        <img src="@/assets/icons/svg-icons/like-empty.svg">
                                                    </button>
                                                    <button class="reply-dislike-button" style="outline: none;">
                                                        <img src="@/assets/icons/svg-icons/dislike-empty.svg" alt="">
                                                    </button>
                                                    <button @click="toggleReplyOptions(comment.id)"
                                                        class="reply-comment-button" style="outline: none;">
                                                        Reply
                                                    </button>
                                                    <div v-if="openComments[comment.id]?.replyOptionsVisible"
                                                        class="reply-division flex-col">
                                                        <div class="reply-creation">
                                                            <img src="@/assets/img/Django.png" alt="">
                                                            <input type="text" class="w-[200px] bg-transparent"
                                                                placeholder="Add a Reply...">
                                                        </div>
                                                        <div class="reply-btns mt-2">
                                                            <button @click="toggleReplyOptions(comment.id)"
                                                                class="cancel-reply-btn">Cancel</button>
                                                            <button class="submit-reply-btn">Reply</button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="max-h-[56.8px] flex flex-row mt-10 absolute bottom-0 left-0 gap-x-4 w-full
                     border-t pt-2 pl-2 pb-2">
                        <div class="w-10 h-10">
                            <img class="w-[100%] h-[100%] rounded-full cursor-pointer" src="@/assets/img/Django.png"
                                alt="">
                        </div>
                        <div @click="toggleUserOptions"><input class="border-gray-400 bg-transparent border-b-[0.5px] outline-none
                             short-video-comment-creation" type="text" placeholder="Add a comment...">
                        </div>
                        <div v-if="isUserOptionsOpen" class="flex flex-row gap-x-4 font-medium text-sm">
                            <button @click="toggleUserOptions"
                                class="hover:bg-[#e5e5e5] w-[74px] h-[36px] rounded-2xl">Cancel</button>
                            <button class="bg-[#065fd4] hover:bg-[#0556bf] text-white rounded-2xl w-[93px]
                              h-[36px]">Comment</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <socialShare></socialShare>

    <div class="flex flex-col gap-y-4 absolute right-4 top-[47%]">
        <div class="w-[56px] h-[56px] rounded-full bg-[#f2f2f2] hover:bg-[#d9d9d9] cursor-pointer">
            <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/angle-circle-up-icon.svg" alt="">
        </div>
        <div class="w-[56px] h-[56px] rounded-full bg-[#f2f2f2] hover:bg-[#d9d9d9] cursor-pointer">
            <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/angle-circle-down-icon.svg" alt="">
        </div>
    </div>
</template>