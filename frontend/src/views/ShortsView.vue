<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useToast } from 'vue-toastification';
import { useRoute, useRouter } from 'vue-router';
import socialShare from '@/components/socialShare.vue';
import { sharedState } from '@/sharedState';
import axios from 'axios';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue';


// Icons
import emptyLikeIcon from '/src/assets/icons/svg-icons/like-empty.svg'
import fillLikeIcon from '/src/assets/icons/svg-icons/like-fill.svg'
import emptyDislikeIcon from '/src/assets/icons/svg-icons/dislike-empty.svg'
import fillDislikeIcon from '/src/assets/icons/svg-icons/dislike-fill.svg'


const toast = useToast()
const router1 = useRoute()
const router2 = useRouter()

// Toggling Sharing Tab
const toggleSharingTab = () => {
    sharedState.isSharingTabOpen = !sharedState.isSharingTabOpen
}


const userCommentText = ref(null)
const userReplyText = ref(null)

const submitVideoComment = (parentId = null) => {
    const commentText = userCommentText.value;
    const replyText = userReplyText.value;

    const user_session_id = sessionStorage.getItem("user_session_id")

    const submitFormData = new FormData()
    submitFormData.append("user_session_id", user_session_id)
    submitFormData.append("comment_text", commentText ?? replyText) // We either use comment or reply text!
    submitFormData.append("video_id", videoInfo.id)
    if (parentId) {
        submitFormData.append("parent_id", parentId)
    }

    axios.post(`http://127.0.0.1:8000/videos/comment/add/`, submitFormData).then((response) => {
        if (response.status == 201) {
            retrieveVideoComments(videoInfo.id);
            openComments = {}
            videoInfo.total_comments += 1
            userReplyText.value = null
            userCommentText.value = null // Delete the comment text
            toast.success("Your comment has been Posted!");
        }
    }).catch((error) => {
        toast.error(error)
    })
};

// Toggling Comment Container
const isCommentContainerOpen = ref(false)
const toggleCommentContainer = () => {
    const shortVideoWrapper = document.querySelector(".short-video-wrapper")
    isCommentContainerOpen.value = !isCommentContainerOpen.value;
    shortVideoWrapper.style.marginRight = isCommentContainerOpen.value ? "350px" : "0px";
}

watch(isCommentContainerOpen, (newVal) => {
    if (newVal) {
        retrieveVideoComments(router1.params.id)
    }
})

// Toggle User Comment Options
const isUserOptionsOpen = ref(false)
const toggleUserOptions = () => isUserOptionsOpen.value = !isUserOptionsOpen.value


// Handling Comment opening
let openComments = reactive({})
const toggleUserComment = (commentId, state) => {
    if (!openComments[commentId]) {
        openComments[commentId] = { replyContainerVisible: false, userReplyOptionsVisible: false, replyOptionsVisible: false };
    }
    openComments[commentId][state] = !openComments[commentId][state];
}

const toggleUserReplyOptionsVisible = (comment_id) => {
    // Close all other reply inputs first
    Object.keys(openComments).forEach(key => {
        if (key !== comment_id.toString()) {
            openComments[key].userReplyOptionsVisible = false
        }
    })

    toggleUserComment(comment_id, 'userReplyOptionsVisible')
}
const toggleReplyOptions = (comment_id) => toggleUserComment(comment_id, 'replyOptionsVisible')
const retrieveCommentReplies = async (comment_id) => {
    Object.keys(openComments).forEach(key => {
        if (key !== comment_id.toString()) {
            openComments[key].replyContainerVisible = false
        }
    })

    toggleUserComment(comment_id, 'replyContainerVisible')
    if (openComments[comment_id]?.replyContainerVisible) {
        await axios.get(`http://127.0.0.1:8000/videos/replies/list/${comment_id}`, {
            params: {
                user_session_id: sessionStorage.getItem("user_session_id")
            }
        }).then((response) => {
            if (response.status == 200) {
                comments.forEach(comment => {
                    if (comment.id === comment_id) {
                        comment.replies = response.data.data
                        return;
                    }
                })
            }
        }).catch((error) => {
            toast.error(error)
        })
    }
}

// Handle video`s playing
const isVideoPlayed = ref(true)
const toggleVideoPlay = () => {
    const video = videoRef.value
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
    const video = videoRef.value
    video.muted = !video.muted
    isVideoMuted.value = !isVideoMuted.value
}


// Update video volume based on input range
const volumeValue = ref(50); // default volume value
const updateVolume = (event) => {
    volumeValue.value = event.target.value;
    const video = videoRef.value
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
    const video = videoRef.value
    video.requestFullscreen();
    isVideoFullscreen.value = !isVideoFullscreen.value;
}


const videoRef = ref(null)
let videoInfo = reactive({
    id: '',
    unique_id: '',
    total_likes: '',
    user_id: '',
    title: '',
    description: '',
    thumbnail_url: '',
    video_url: '',
    duration: '',
    created_at: '',
    channel_id: '',
    channel_name: '',
    channel_profile_url: '',
})


const youtubeVideoLink = ref(null)
const retrieveVideoDetail = async (videoId, user_session_id) => {
    await axios.get(`http://127.0.0.1:8000/videos/detail/${videoId}`, {
        params: {
            unique_id: router1.query.unique_id,
            user_session_id: user_session_id
        }
    }).then((response) => {
        if (response.status == 200) {
            Object.assign(videoInfo, response.data.data)
        } else {
            youtubeVideoLink.value = response.data.data
        }
        isChannelSubscribed.value = videoInfo.is_channel_subed
    }).catch((error) => {
        console.log(error)
    })
}


const comments = reactive([])
const commentRetrievingLoading = ref(false)
const retrieveVideoComments = async (videoId) => {
    commentRetrievingLoading.value = true
    await axios.get(`http://127.0.0.1:8000/videos/comment/list/${videoId}`, {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 200) {
            comments.splice(0, comments.length, ...response.data.data)
        }
    }).catch((error) => {
        toast.error(error)
    }).finally(() => commentRetrievingLoading.value = false)
}


const likeComment = async (commentId, actionType, replyId = null) => {
    await axios.get(`http://127.0.0.1:8000/videos/comment/like/${replyId ? replyId : commentId}`, {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id"),
            action_type: actionType
        }
    }).then((response) => {
        if (response.status == 200) {
            const comment = comments.find(comment => comment.id === commentId)
            if (replyId) {
                const reply = comment.replies.find(reply => reply.id = replyId)
                reply.is_liked = reply.is_liked === actionType ? null : actionType
            } else {
                comment.is_liked = comment.is_liked === actionType ? null : actionType
                comment.total_likes = response.data.total_likes
            }
        }
    }).catch((error) => {
        toast.error(error)
    })
}


const deleteComment = (commentId) => {
    if (!confirm("Confirm that you wanna delete your comment.")) return;

    axios.delete(`http://127.0.0.1:8000/videos/comment/delete/${commentId}`, {
        params: {
            user_id: userId.value
        }
    }).then((response) => {
        if (response.status == 204) {
            toast.success("Your comment deleted successfully!")
            retrieveVideoComments(router1.params.id)
            videoInfo.total_comments -= 1
        }
    }).catch(() => toast.error("Error!"))
}


const isChannelSubscribed = ref(null)
const subscribeChannel = (channelId) => {
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
        }
    }).catch((error) => {
        toast.error(error)
    })
}


const totalLikes = ref(null)
const likeSituation = ref(null)
const userLikeSituation = async (video_id, user_session_id) => {
    await axios.get(`http://127.0.0.1:8000/videos/like-situation/${video_id}/${user_session_id}`).then((response) => {
        if (response.status == 200) {
            likeSituation.value = response.data.data
            totalLikes.value = response.data.total_likes
        }
    }).catch((error) => {
        console.log(error)
    })
}


const likeVideo = (action_type) => { // true == 'like', false == 'dislike', null == 'None'
    const user_session_id = sessionStorage.getItem("user_session_id")
    if (!user_session_id) {
        toast.error("You have to be Logged in!")
        return;
    }
    axios.get(`http://127.0.0.1:8000/videos/like/${videoInfo.id}/${action_type}/${user_session_id}`).then(() => {
        userLikeSituation(router1.params.id, user_session_id)
    }).catch((error) => {
        toast.error("Error: ", error)
    })
}


const playAnotherVideo = (direction) => {
    axios.get(`http://127.0.0.1:8000/videos/${direction}-video/${router1.params.id}/short_video`).then((response) => {
        if (response.status == 200) {
            router2.push({ name: 'short_detail', params: { id: response.data.unique_id }, state: { is_first: response.data.is_first, is_last: response.data.is_last } })
        }
    }).catch(() => toast.error("Error!"))
}


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

const isVideoFirst = ref(null)
const isVideoLast = ref(null)
const isPageLoading = ref(false)
const MountPage = async () => {
    isVideoFirst.value = history.state.is_first
    isVideoLast.value = history.state.is_last

    console.log(isVideoFirst.value)
    console.log(isVideoLast.value)


    isVideoPlayed.value = true
    isPageLoading.value = true
    const user_session_id = sessionStorage.getItem("user_session_id")
    const videoId = router1.params.id // Current Video Id
    await retrieveVideoDetail(videoId, user_session_id)

    if (user_session_id) {
        await userAuthentication(user_session_id)
        if (isUserAuthenticated.value) {
            userLikeSituation(videoId, user_session_id)
            await retrieveUserProfileImg(user_session_id)
        }
    }
    isPageLoading.value = false
}


watch(() => router1.params.id, () => {
    MountPage()
})


onMounted(() => {
    MountPage()
})
</script>

<template>
    <div v-if="!isPageLoading" class="flex flex-col justify-center items-center mt-16 gap-y-7">
        <div class="short-video-wrapper">
            <div class="short-video w-[350px] h-[600px] relative">
                <video :poster="videoInfo.thumbnail_url" ref="videoRef" oncontextmenu="return false;" volume="0.5"
                    class="w-[100%] h-[100%] object-cover rounded-2xl">
                    <source :src="`http://127.0.0.1:8000/videos/stream/${$route.params.id}/`" type="video/mp4" />
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
                        <router-link :to="`/channel-page/${videoInfo.channel_unique_identifier}`">
                            <img :src="videoInfo.channel_profile_url" class="w-8 h-8 rounded-full border-white border"
                                alt="">
                        </router-link>
                        <router-link :to="`/channel-page/${videoInfo.channel_unique_identifier}`">
                            <p class="text-[14px] font-medium">@{{ videoInfo.channel_name }}</p>
                        </router-link>
                        <button @click="subscribeChannel(videoInfo.channel_id)" v-if="isChannelSubscribed"
                            class="bg-white text-black w-[76px] h-[32px] rounded-2xl text-[12px] font-medium">Subscribed</button>
                        <button @click="subscribeChannel(videoInfo.channel_id)" v-else
                            class="bg-black text-text w-[76px] h-[32px] rounded-2xl text-[12px] font-medium">Subscribe</button>
                    </div>
                    <h2 class="text-[14px] font-normal mt-4">{{ videoInfo.title }}</h2>
                </div>
                <div class="flex flex-col gap-y-4 justify-center items-center
                 absolute right-[-65px] bottom-[30px]">
                    <button @click="likeVideo(true)" class="w-12 h-12 bg-[#f2f2f2] rounded-full hover:bg-[#e5e5e5]">
                        <img :src="likeSituation === true ? fillLikeIcon : emptyLikeIcon" class="h-[80%] w-[80%] m-auto"
                            alt="">
                    </button>
                    <span class="mt-[-10px]">{{ totalLikes }}</span>
                    <button @click="likeVideo(false)" class="w-12 h-12 bg-[#f2f2f2] rounded-full hover:bg-[#e5e5e5]">
                        <img :src="likeSituation === false ? fillDislikeIcon : emptyDislikeIcon"
                            class="h-[80%] w-[80%] m-auto" alt="">
                    </button>
                    <span class="mt-[-10px]">Dislike</span>
                    <button @click="toggleCommentContainer"
                        class="comment-toggle-btn w-12 h-12 bg-[#f2f2f2] rounded-full hover:bg-[#e5e5e5]">
                        <img src="@/assets/icons/svg-icons/comment-empty-icon.svg" class="h-[60%] w-[60%] m-auto"
                            alt="">
                    </button>
                    <span class="mt-[-10px]">{{ videoInfo.total_comments }}</span>
                    <button @click="toggleSharingTab" class="w-12 h-12 bg-[#f2f2f2] rounded-full hover:bg-[#e5e5e5]">
                        <img src="@/assets/icons/svg-icons/share-btn.svg" class="h-[60%] w-[60%] m-auto" alt="">
                    </button>
                    <span class="mt-[-10px]">Share</span>
                    <router-link :to="`/channel-page/${videoInfo.channel_unique_identifier}`">
                        <button class="w-11 h-11 bg-[#f2f2f2] hover:bg-[#e5e5e5] rounded-full">
                            <img :src="videoInfo.channel_profile_url" class="h-[100%] w-[100%] rounded-md">
                        </button>
                    </router-link>
                </div>
                <div v-if="isCommentContainerOpen" class="z-10 flex absolute left-[450px] bottom-[50px] flex-col w-[500px] h-[500px] 
                    border-[1px] border-gray-400 rounded-2xl pt-2 max-w-[500px] max-h-[500px]">
                    <div class="flex flex-row justify-start items-center ml-2">
                        <p class="font-bold text-[20px] pl-2">Comments&nbsp;</p><span>{{ videoInfo.total_comments
                            }}</span>
                        <button @click="toggleCommentContainer" class="w-10 h-10 border-none rounded-full bg-white hover:bg-[#e5e5e5]
                         ml-[310px]">
                            <img class="w-[50%] h-[50%] m-auto" src="@/assets/icons/svg-icons/x-mark-icon.svg" alt="">
                        </button>
                    </div>
                    <hr>
                    <div v-if="!commentRetrievingLoading" class="flex-grow flex flex-col overflow-y-auto max-h-[394px]"
                        style="scrollbar-width: thin;">
                        <div v-for="comment in comments" :key="comment.id" class="flex flex-col gap-y-8">
                            <div class="flex flex-row gap-x-2 ml-4 mt-4">
                                <router-link :to="`/channel-page/${comment.user_channel_id}`">
                                    <div>
                                        <img class="w-10 h-10 rounded-full" :src="comment.user_profile_picrure" alt="">
                                    </div>
                                </router-link>
                                <div class="flex flex-col flex-1 ml-2">
                                    <div class="flex flex-row justify-start items-center">
                                        <p class="text-[13px] font-medium">@{{ comment.username }}</p>
                                        <span class="text-[12px] font-normal ml-2 text-[#918b8b]">{{ comment.created_at
                                            }} days ago</span>
                                        <div v-if="comment.user_id === userId"
                                            class="flex justify-self-end ml-auto mr-4">
                                            <button @click="deleteComment(comment.id)">
                                                <svg xmlns="http://www.w3.org/2000/svg"
                                                    enable-background="new 0 0 24 24" height="24" viewBox="0 0 24 24"
                                                    width="24" focusable="false" aria-hidden="true"
                                                    style="pointer-events: none; display: inherit; width: 100%; height: 100%;">
                                                    <path
                                                        d="M11 17H9V8h2v9zm4-9h-2v9h2V8zm4-4v1h-1v16H6V5H5V4h4V3h6v1h4zm-2 1H7v15h10V5z">
                                                    </path>
                                                </svg>
                                            </button>
                                        </div>
                                    </div>
                                    <div class="flex">
                                        <p class="text-[14px] font-normal">{{ comment.text }}</p>
                                    </div>
                                    <div class="flex flex-row items-center mt-2 relative">
                                        <button @click="likeComment(comment.id, true)"
                                            class="flex items-center justify-center w-8 h-8 rounded-full hover:bg-[#e5e5e5]">
                                            <img :src="comment.is_liked === true ? fillLikeIcon : emptyLikeIcon"
                                                class="h-[80%] w-[80%]" alt="">
                                        </button>
                                        <span class="text-gray-500 text-[13px] font-normal">{{ comment.total_likes
                                            }}</span>
                                        <button @click="likeComment(comment.id, false)"
                                            class="w-8 h-8 rounded-full hover:bg-[#e5e5e5] ml-2">
                                            <img :src="comment.is_liked === false ? fillDislikeIcon : emptyDislikeIcon"
                                                class="h-[80%] w-[80%] m-auto" alt="">
                                        </button>
                                        <button @click="toggleUserReplyOptionsVisible(comment.id)"
                                            class="flex justify-center items-center 
                                            text-[12px] w-[42px] h-[27px] font-semibold border-none m-auto rounded-2xl hover:bg-[#e5e5e5] ml-2">
                                            Reply
                                        </button>
                                        <div v-if="openComments[comment.id]?.userReplyOptionsVisible"
                                            class="user-reply-creation-container absolute top-10 left-0 flex flex-row justify-center items-center">
                                            <img class="rounded-full w-6 h-6" :src="userProfileImgSrc" alt="">
                                            <input type="text" v-model="userReplyText"
                                                class="ml-2 w-[90%] outline-none border-b hover:border-b-2 hover:border-black"
                                                placeholder="Add a comment..."
                                                style="transition: border-bottom 0.1s ease-in-out;">
                                            <div
                                                class="absolute left-[250px] flex flex-row justify-center items-center">
                                                <button @click="toggleUserReplyOptionsVisible(comment.id)"
                                                    class="cancel-comment-btn w-[70px] h-[32px] rounded-[18px]">Cancel</button>
                                                <button @click="submitVideoComment(comment.id)"
                                                    class="submit-comment-btn w-[70px] h-[32px] rounded-[18px] ml-2">Reply</button>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="cursor-pointer" v-if="comment.replies_count >= 1"
                                        @click="retrieveCommentReplies(comment.id)"
                                        :class="['comment-reply-button', openComments[comment.id]?.userReplyOptionsVisible ? 'mt-10' : '']">
                                        <i
                                            :class="['arrow', openComments[comment.id]?.replyContainerVisible ? 'rotate-[225deg]' : 'button']"></i><span>
                                            &nbsp;&nbsp;{{ comment.replies_count }}&nbsp;</span><span>replies</span>
                                    </div>
                                    <div v-if="openComments[comment.id]?.replyContainerVisible"
                                        class="replies-container mt-3">
                                        <div v-for="reply in comment.replies" :key="reply.id" class="reply">
                                            <router-link :to="`/channel-page/${reply.user_channel_id}`">
                                                <div class="reply-author-img">
                                                    <img :src="reply.user_profile_picrure" alt="">
                                                </div>
                                            </router-link>
                                            <div class="reply-detail">
                                                <div class="reply-author-info">
                                                    <p>@</p>
                                                    <p>{{ reply.username }}</p>
                                                    <span>&nbsp;{{ reply.created_at }} days </span>ago
                                                </div>
                                                <p class="reply-value">{{ reply.text }}</p>
                                                <div class="reply-toolbar">
                                                    <button @click="likeComment(comment.id, true, reply.id)"
                                                        class="reply-like-button" style="outline: none;">
                                                        <img
                                                            :src="reply.is_liked === true ? fillLikeIcon : emptyLikeIcon">
                                                    </button>
                                                    <button @click="likeComment(comment.id, false, reply.id)"
                                                        class="reply-dislike-button" style="outline: none;">
                                                        <img
                                                            :src="reply.is_liked === false ? fillDislikeIcon : emptyDislikeIcon">
                                                    </button>
                                                    <button @click="toggleReplyOptions(reply.id)"
                                                        class="reply-comment-button" style="outline: none;">
                                                        Reply
                                                    </button>
                                                    <div v-if="openComments[reply.id]?.replyOptionsVisible"
                                                        class="reply-division flex-col">
                                                        <div class="reply-creation">
                                                            <img :src="userProfileImgSrc" alt="">
                                                            <input v-model="userReplyText" type="text"
                                                                class="w-[200px] bg-transparent"
                                                                placeholder="Add a Reply...">
                                                        </div>
                                                        <div class="reply-btns mt-2">
                                                            <button @click="toggleReplyOptions(reply.id)"
                                                                class="cancel-reply-btn">Cancel</button>
                                                            <button @click="submitVideoComment(reply.id)"
                                                                class="submit-reply-btn">Reply</button>
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
                    <div v-else class="absolute top-0 w-full h-full flex justify-center items-center">
                        <PulseLoader color="red" size="20px"></PulseLoader>
                    </div>
                    <div class="max-h-[56.8px] flex flex-row mt-10 absolute bottom-0 left-0 gap-x-4 w-full
                     border-t pt-2 pl-2 pb-2">
                        <div class="w-10 h-10">
                            <img class="w-[100%] h-[100%] rounded-full cursor-pointer" :src="userProfileImgSrc" alt="">
                        </div>
                        <div @click="toggleUserOptions"><input class="border-gray-400 bg-transparent border-b-[0.5px] outline-none
                            short-video-comment-creation" v-model="userCommentText" type="text"
                                placeholder="Add a comment...">
                        </div>
                        <div v-if="isUserOptionsOpen" class="flex flex-row gap-x-4 font-medium text-sm">
                            <button @click="toggleUserOptions"
                                class="hover:bg-[#e5e5e5] w-[74px] h-[36px] rounded-2xl">Cancel</button>
                            <button @click="submitVideoComment(null)" class="bg-[#065fd4] hover:bg-[#0556bf] text-white rounded-2xl w-[93px]
                              h-[36px]">Comment</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div v-else class="flex justify-center items-center w-full h-full absolute">
        <ClipLoader size="55px" color='red'></ClipLoader>
    </div>

    <socialShare></socialShare>

    <div class="flex flex-col gap-y-4 absolute right-4 top-[47%]">
        <div v-if="!isVideoFirst" @click="playAnotherVideo('previous')"
            class="w-[56px] h-[56px] rounded-full bg-[#f2f2f2] hover:bg-[#d9d9d9] cursor-pointer">
            <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/angle-circle-up-icon.svg" alt="">
        </div>
        <div v-if="!isVideoLast" @click="playAnotherVideo('next')"
            class="w-[56px] h-[56px] rounded-full bg-[#f2f2f2] hover:bg-[#d9d9d9] cursor-pointer">
            <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/angle-circle-down-icon.svg" alt="">
        </div>
    </div>
</template>