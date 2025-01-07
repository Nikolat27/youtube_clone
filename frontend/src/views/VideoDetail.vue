<script setup>
import { ref, computed, onMounted, reactive, watch } from 'vue';
import { sharedState } from '@/sharedState';
import { useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';

import socialShare from '@/components/socialShare.vue';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue';
import axios from 'axios';

// Icons
import playIcon from '/src/assets/icons/video-player/play-icon.png'
import pauseIcon from '/src/assets/icons/video-player/pause-icon.png'
import onSubtitleIcon from '/src/assets/icons/video-player/subtitle-on-icon.png'
import offSubtitleIcon from '/src/assets/icons/video-player/subtitle-off-icon.png'
import fullSpeakerIcon from '/src/assets/icons/video-player/full-speaker-icon.png'
import halfSpeakerIcon from '/src/assets/icons/video-player/half-speaker-icon.png'
import muteSpeakerIcon from '/src/assets/icons/video-player/mute-speaker-icon.png'

import emptyLikeIcon from '/src/assets/icons/svg-icons/like-empty.svg'
import fillLikeIcon from '/src/assets/icons/svg-icons/like-fill.svg'
import emptyDislikeIcon from '/src/assets/icons/svg-icons/dislike-empty.svg'
import fillDislikeIcon from '/src/assets/icons/svg-icons/dislike-fill.svg'
import saveIcon from '/src/assets/icons/svg-icons/save-btn.svg'
import unSaveIcon from '/src/assets/icons/svg-icons/unsave-btn.svg'
import replyIcon from '/src/assets/icons/svg-icons/reply-icon.svg'

const route = useRoute()

// Description Toggling
const showFullDescription = ref(false);
const toggleFullDescription = () => {
    showFullDescription.value = !showFullDescription.value;
};

const truncatedDescription = computed(() => {
    const description = videoInfo.description
    if (description.length >= 60) {
        return showFullDescription.value ? description : `${description.substring(0, 60)}...`;
    } else {
        return description;
    }
});


const comments = reactive([])
const commentScrollLoading = ref(false)
const userCommentText = ref(null)
const userReplyText = ref(null)

watch(() => userCommentText.value, () => { })

const commentRetrievingLoading = ref(false)
const retrieveVideoComments = async (videoId) => {
    commentRetrievingLoading.value = true
    await axios.get(`http://127.0.0.1:8000/videos/comment/list/${videoId}`, {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 200) {
            Object.assign(comments, response.data.data)
        }
    }).catch((error) => {
        toast.error(error)
    }).finally(() => commentRetrievingLoading.value = false)
}

const replyRetrievingLoading = ref(false)
const retrieveCommentReplies = async (commentId) => {
    replyRetrievingLoading.value = true
    toggleReplyContainer(commentId)

    await axios.get(`http://127.0.0.1:8000/videos/replies/list/${commentId}`).then((response) => {
        if (response.status == 200) {
            comments.forEach(comment => {
                if (comment.id === commentId) {
                    comment.replies = response.data.data
                    return;
                }
            })
        }
    }).catch((error) => {
        toast.error(error)
    }).finally(() => replyRetrievingLoading.value = false)
}

// Video Comment Toggling
const videoCommentButtonsShow = ref(false);
const toggleVideoCommentButtons = () => videoCommentButtonsShow.value = !videoCommentButtonsShow.value
const cancelUserComment = () => {
    userCommentText.value = null;
    videoCommentButtonsShow.value = false
}

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

    axios.post("http://127.0.0.1:8000/videos/comment/add", submitFormData).then((response) => {
        if (response.status == 201) {
            retrieveVideoComments(videoInfo.id);
            commentStates.value = {}; // Closing the opened Tabs (for replies)
            userReplyText.value = null
            userCommentText.value = null // Delete the comment text
            toast.success("Your comment has been Posted!");
        }
    }).catch((error) => {
        toast.error(error)
    })
};


// Comment and Reply Toggling Management
const commentStates = ref({});
const toggleCommentState = (commentId, state) => {
    if (!commentStates.value[commentId]) { // This Id doesnt exists, Create one
        commentStates.value[commentId] = { repliesVisible: false, replyContainerVisible: false, replyCommentButtonVisible: false };
    }
    commentStates.value[commentId][state] = !commentStates.value[commentId][state];
};

const toggleUserCommentReplyButtons = (commentId) => toggleCommentState(commentId, 'repliesVisible');
const toggleReplyContainer = (commentId) => toggleCommentState(commentId, 'replyContainerVisible');
const toggleReplyCommentButtons = (commentId) => toggleCommentState(commentId, 'replyCommentButtonVisible');

watch(commentStates.value, () => {
    videoCommentButtonsShow.value = false
    userCommentText.value = null;
    userReplyText.value = null;
})

// Playlist Toggling
let playlistExpanded = ref(false);
const playListExpandingToggle = () => {
    playlistExpanded.value = !playlistExpanded.value;
}

// Styles for related-video div
const relatedVideosStyle = computed(() => ({
    position: 'absolute',
    right: '107px',
    top: playlistExpanded.value ? '575px' : '130px', // Collapsing and Uncollapsing the playlist (Expanding also)
    transition: 'top 0.1s ease-in-out'
}));

// Slider for short related videos (Right side container)
const scrollHorizontally = (direction) => {
    const shortDivContainer = document.querySelector(".short-video-groups");
    shortDivContainer.scrollLeft += direction === 'next' ? 131 : -131;
}


// Playlist divison toggling
let isPlaylistDivisonOpen = ref(false)
const togglePlaylistDivision = () => {
    isPlaylistDivisonOpen.value = !isPlaylistDivisonOpen.value
}


// Advertisement and such...
let isVideoAd = ref(false)
let adSkipDuration = ref(5) // in seconds
let adFinished = ref(false)
let durationInternal = null; // Interval for advertisement


const startAdCountdown = () => {
    durationInternal = setInterval(() => { // Start the count down by 1 each 1 second
        if (adSkipDuration.value > 1) { // if the countdown finished! (reached to 1)
            adSkipDuration.value -= 1;
        } else { // Make the user to skip the ad
            stopAdCountdown() // Stop it
            adFinished.value = true // Enable the user to skip the ad
        }
    }, 1000);
}
const stopAdCountdown = () => {
    clearInterval(durationInternal); // Stopping the Countdown
}


// Handling Main video
const isVideoPlayed = ref(false);
const toggleVideoPlay = () => {
    const video = videoRef.value;
    isVideoPlayed.value = !isVideoPlayed.value;
    if (isVideoPlayed.value) {
        video.play();
        startAdCountdown();
    } else {
        video.pause();
        stopAdCountdown();
    }
}

// Handling the video`s subtitle
const subtitleIconSrc = ref(offSubtitleIcon)
const isSubtitleOn = ref(false)
const toggleSubtitle = () => {
    isSubtitleOn.value = !isSubtitleOn.value
    subtitleIconSrc.value = isSubtitleOn.value ? `${onSubtitleIcon}` : `${offSubtitleIcon}`
}


// Handling the Video options (To see the annotations and playback speed)
const isVideoOptionsOpen = ref(false)
const toggleVideoOptions = () => isVideoOptionsOpen.value = !isVideoOptionsOpen.value


// Fullscreening the video
const toggleFullScreenMode = () => {
    document.querySelector(".main-video").requestFullscreen();
}


// Mute and Unmuting the video
const videoMuted = ref(false)
const speakerIconSrc = ref(fullSpeakerIcon)
const muteVideo = () => {
    videoMuted.value = !videoMuted.value
    speakerIconSrc.value = videoMuted.value ? muteSpeakerIcon : fullSpeakerIcon
}

// Handling the volume of the video (Audio) Notice: When you mute a video and change its volume, it will be unmuted
const videoVolumeChanging = (event) => {
    const video = videoRef.value
    videoMuted.value = false
    video.volume = event.target.value / 100
    speakerIconSrc.value = video.volume >= 0.5 && !video.muted ? `${fullSpeakerIcon}` : (video.volume > 0 && !video.muted ? `${halfSpeakerIcon}` : `${muteSpeakerIcon}`);
}


// Handling playback speed for Main video (0.25x speed up to 2x)
const isPlaybackSpeedDivOpen = ref(false)
const togglePlaybackSpeedDiv = () => isPlaybackSpeedDivOpen.value = !isPlaybackSpeedDivOpen.value
const changePlayBackSpeed = (speed) => { // From 0.25x to 2x
    videoRef.value.playbackRate = speed;
    togglePlaybackSpeedDiv();
}

// Handling Video progress track, specific time showing and the rest...
const videoRef = ref(null) // videoRef is the video tag itself
const videoProgress = ref(0) // videoProgress is the time that we currently at (video must be played)
const currentVideoTime = ref('0:00')
const videoDuration = ref(null)
// This func is to know what percentage of the video are we at (When video is played) e.g sec5 of 10sec duration is 50% of it
// So what`s the usage? to update the range input field (for see the progress of the video)
const updateProgress = () => {
    if (videoRef.value) {
        videoProgress.value = (videoRef.value.currentTime / videoRef.value.duration) * 100
        currentVideoTime.value = calculateTime(videoRef.value.currentTime)
        videoDuration.value = calculateTime(videoRef.value.duration)
    }
}


// This func is for when you CLICK on a specific time of the video and go there
const seekVideo = (event) => {
    if (videoRef.value) {
        const newTime = (event.target.value / 100) * videoRef.value.duration;
        videoRef.value.currentTime = newTime;
    }
}


// handling some opacity transititions
const isControlBarVisible = ref(false)
const handleControlBar = (type) => {
    isControlBarVisible.value = type === 'open';
    document.querySelector(".control-bar").style.opacity = type === 'open' ? 1 : 0 // Just open or close
}


// The actual handling for the canvas and specific time showing
let mouseValue = ref(null)
let canvasDisplay = ref('none')
let position = ref(0)

let videoTimeDisplay = ref('none')
let videoTimeValue = ref(null)
let videoTimePosition = ref(null)

let timeout;
function debounce(func, delay) {
    return function (...args) {
        const context = this;
        clearTimeout(timeout); // Clears the timeout
        timeout = setTimeout(() => func.apply(context, args), delay);
    };
}

const clearTimeOut = () => {
    clearTimeout(timeout);
}

const getVideoFrame = debounce((event) => {
    const input = event.target;
    const { left, width } = input.getBoundingClientRect();
    const positionX = event.clientX - left;

    // Half Width of the canvas(because we want to Locate the Canvas, Center Top of Our mouse cursor)
    const canvasWidth = 225;
    const halfCanvasWidth = canvasWidth / 2;

    // Calculate the desired left position
    let leftPosition = positionX - halfCanvasWidth;

    // We ensure the canvas stays within the frames of the video tracker (with Min and Max modules)
    leftPosition = Math.max(0, Math.min(leftPosition, width - canvasWidth));
    position.value = leftPosition;

    const percentage = Math.round(positionX / (width / 100));
    mouseValue.value = (videoInfo.duration / 100) * percentage;

    // Time tracker (under the canvas)
    videoTimePosition.value = positionX - 15
    videoTimeValue.value = calculateTime(mouseValue.value);

    // Creating the canvas
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = 225;
    canvas.height = 130;
    const videoFrameImg = document.getElementById("video-frame-img");

    const hiddenVideo = document.createElement('video');
    hiddenVideo.crossOrigin = "anonymous"; // This is necassary for CORS origin
    hiddenVideo.src = `http://127.0.0.1:8000/videos/stream/${videoInfo.id}/`;
    hiddenVideo.currentTime = mouseValue.value;

    hiddenVideo.addEventListener('loadeddata', () => {
        if (hiddenVideo.readyState >= 2) { // 3 and 4 means loading and completed (They are loading request situations)
            hiddenVideo.pause();
            context.drawImage(hiddenVideo, 0, 0, canvas.width, canvas.height);
            videoFrameImg.src = canvas.toDataURL(); // Set the image source to the canvas data URL
        }
    });

    hiddenVideo.addEventListener('seeked', () => {
        context.drawImage(hiddenVideo, 0, 0, canvas.width, canvas.height);
        videoFrameImg.src = canvas.toDataURL(); // Update the image source
    });
    hiddenVideo.load();

    // handling display for appearing and disappearing the canvas
    canvasDisplay.value = 'flex'
    videoTimeDisplay.value = 'flex'
}, 300);


// Using divmod to convert the total seconds to hours and minutes
function divmod(a, b) {
    return [Math.floor(a / b), a % b]; // Directly return the quotient and remainder as an array
}

// This function is used to put a zero (0) in the left of a digit it was less than 10 e.g: 5, 13, 9  ==> 05, 13, 09
const formatTime = (unit) => (unit < 10 ? `0${unit}` : unit);
const calculateTime = (duration) => {
    const [hours, remainingSeconds] = divmod(duration, 3600);
    const [minutes, seconds] = divmod(remainingSeconds, 60);
    if (hours) {
        return `${Math.round(hours)}:${Math.round(minutes)}:${formatTime(Math.round(seconds))}`; // output ==> 33:66:99
    } else {
        return `${Math.round(minutes)}:${formatTime(Math.round(seconds))}`; // output ==> 66:99 (We dont show the hour)
    }
};

// Annotation for main video handling
const showAnnotation = ref(true)
const annotationTimeout = ref(null);
const annotationIsHovered = ref(false)
const showAnnotationButton = () => {
    annotationIsHovered.value = true;
    clearTimeout(annotationTimeout.value)
};

const hideAnnotationButton = () => {
    annotationTimeout.value = setTimeout(() => {
        annotationIsHovered.value = false;
    }, 1000);
};

const toast = useToast()
const likeVideo = (action_type) => { // true == 'like', false == 'dislike', null == 'None'
    const user_session_id = sessionStorage.getItem("user_session_id")
    if (!user_session_id) {
        toast.error("You have to be Logged in!")
        return;
    }
    axios.get(`http://127.0.0.1:8000/videos/like/${videoInfo.id}/${action_type}/${user_session_id}`).then((response) => {
        userLikeSituation(route.params.id, user_session_id)
    }).catch((error) => {
        toast.error(error)
    })
}

let videoInfo = reactive({
    id: '',
    user_id: '',
    title: '',
    description: '',
    thumbnail_url: '',
    video_url: '',
    duration: '',
    created_at: '',
    channel_name: '',
    channel_profile_url: '',
    channel_watermark_url: '',
})

const likeSituation = ref(null)
const userLikeSituation = async (video_id, user_session_id) => {
    await axios.get(`http://127.0.0.1:8000/videos/like-situation/${video_id}/${user_session_id}`).then((response) => {
        if (response.status == 200) {
            likeSituation.value = response.data.data
        }
    }).catch((error) => {
        console.log(error)
    })
}

const saveSituation = ref(null)
const saveVideoToPlaylist = async () => {
    const user_session_id = sessionStorage.getItem("user_session_id")
    if (!user_session_id) {
        toast.error("You have to be Logged in!")
        return;
    }

    await axios.get(`http://127.0.0.1:8000/videos/save/${route.params.id}/${user_session_id}`).then((response) => {
        if (response.status == 200) {
            toast.info("Your Video Saved successfully!")
            videoSaveSituation(route.params.id, user_session_id)
        }
    }).catch((error) => {
        toast.error(error)
    })
}

const videoSaveSituation = async (video_id, user_session_id) => {
    await axios.get(`http://127.0.0.1:8000/videos/is-save/${video_id}/${user_session_id}`).then((response) => {
        if (response.status == 200) {
            saveSituation.value = response.data.data
        }
    }).catch((error) => {
        console.log(error)
    })
}

const retrieveVideoDetail = (videoId) => {
    axios.get(`http://127.0.0.1:8000/videos/detail/${videoId}`, {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 200) {
            Object.assign(videoInfo, response.data.data)
            videoDuration.value = calculateTime(videoInfo.duration)
        }
    }).catch((error) => {
        console.log(error)
    })
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

// Toggling Sharing Tab
const toggleSharingTab = () => {
    sharedState.isSharingTabOpen = !sharedState.isSharingTabOpen
}

const downloadVideo = (videoId) => {
    return; // Im gonna work on this function later
    axios.get(`http://127.0.0.1:8000/videos/download/${videoId}`).then((response) => {
        if (response.status == 200) {
            toast.info("Your download is started!")
        }
    }).catch((error) => {
        toast.error(error)
    })
}

onMounted(async () => {
    // This 'timeupdate' invokes whenever timeCurrent of the video changes
    videoRef.value.addEventListener('timeupdate', updateProgress);

    const videoId = route.params.id // Current Video Id
    retrieveVideoDetail(videoId)

    const user_session_id = sessionStorage.getItem("user_session_id")
    if (user_session_id) {
        await userAuthentication(user_session_id)
        if (isUserAuthenticated.value) {
            userLikeSituation(videoId, user_session_id)
            videoSaveSituation(videoId, user_session_id)
            await retrieveUserProfileImg(user_session_id)
            retrieveVideoComments(videoId)
        }
    }
});
</script>


<template>
    <div @mouseover="handleControlBar('open')" @mouseleave="handleControlBar('close')"
        class="video-container top-14 left-12 relative overflow-hidden w-[920px] h-[480px] flex justify-center items-center rounded-2xl">
        <video ref="videoRef" :poster="videoInfo.thumbnail_url" :muted="videoMuted" volume="0.5"
            class="main-video cursor-pointer w-full h-full object-fill overflow-hidden">
            <source :src="`http://127.0.0.1:8000/videos/stream/${$route.params.id}/`" type="video/mp4" />
        </video>
        <button :disabled="!adFinished" @click="skipVideoAd" :style="{ backgroundColor: adFinished ? 'black' : 'gray' }"
            class="skip-ad-btn text-[14px] gap-x-1 font-normal text-white cursor-pointer absolute bottom-36
             right-6 w-20 h-8 rounded-2xl flex justify-center items-center p-2">
            Skip <span v-if="!adFinished" class="remaining-time">{{ adSkipDuration }}</span>
            <img style="width: 15px; height: 15px;" src="\src\assets\icons\video-player\arrow-icon.png"
                class="rotate-180" alt="">
        </button>
        <div v-if="showAnnotation" :style="{ bottom: isControlBarVisible ? '64px' : '8px' }" class="annotation-div absolute right-3 w-10
         h-10 bg-transparent">
            <img @mouseenter="showAnnotationButton" @mouseleave="hideAnnotationButton"
                class="annotation-img w-full h-full cursor-pointer" :src="videoInfo.channel_watermark_url" alt="">
            <div @mouseenter="showAnnotationButton" @mouseleave="hideAnnotationButton"
                :style="{ opacity: annotationIsHovered ? '1' : '0', display: annotationIsHovered ? 'flex' : 'none' }"
                class="annotation-btn bg-[#191919] bg-opacity-90 p-1 absolute right-[48px] -bottom-[2px] w-[124px] h-[75px] rounded-xl flex-col items-center
             justify-center text-white">
                <span class="text-[11px] font-normal text-left self-start ml-3 mb-1">channel name</span>
                <button class="w-[94.5px] h-[36px] rounded-3xl bg-white cursor-pointer">
                    <span class="text-[14px] font-medium text-black">Subscribe</span>
                </button>
            </div>
        </div>
        <div class="bg-transparent z-50 control-bar flex opacity-0 w-full h-[48px] max-h-[48px] absolute bottom-0 justify-center
         items-center flex-row bg-gray-200 bg-opacity-80">
            <div class="video-progress-bar w-[906px] h-[8px] absolute bottom-14">
                <div class="video-img-tracker z-10 overflow-hidden w-[225px] h-[130px] rounded-lg border-[3px] border-white
                        absolute bottom-12" :style="{ left: `${position}px`, display: `${canvasDisplay}`, }">
                    <img class="w-full h-full" id="video-frame-img" loading="lazy" alt="">
                </div>
                <p class="text-[13px] text-white absolute bottom-4 font-medium"
                    :style="{ left: `${videoTimePosition}px`, display: `${videoTimeDisplay}` }">
                    {{ videoTimeValue }}
                </p>
                <input :disabled="isVideoAd" @mousemove="getVideoFrame"
                    @mouseleave="mouseValue = null, canvasDisplay = 'none', videoTimeDisplay = 'none'; clearTimeOut()"
                    min="0" max="100" :value="videoProgress" id="progress-bar" class="h-full w-full" type="range"
                    @input="seekVideo">
            </div>
            <div class="w-[618px] h-full left-controls flex flex-row justify-start
             items-center gap-x-6 pl-2">
                <button @click="toggleVideoPlay">
                    <img class="play-video-button" style="width: 20px; height: 20px;"
                        :src="isVideoPlayed ? pauseIcon : playIcon" alt="">
                </button>
                <button>
                    <img src="@/assets/icons/video-player/next-icon.png" alt="">
                </button>
                <button class="flex flex-row justify-center items-center">
                    <img @click="muteVideo" class="speaker-btn" :src="speakerIconSrc" alt="">
                    <input @input="videoVolumeChanging" value="50" id="volume-bar" class="w-[52px] h-[48px] ml-2 hidden"
                        type="range">
                </button>
                <p class="text-[13px] text-white -ml-2">
                    <span class="current-video-time">{{ currentVideoTime }}</span>
                    <span>/</span>
                    <span class="end-video-time">{{ videoDuration }}</span>
                </p>
            </div>
            <div class="w-[288px] h-full right-controls flex flex-row justify-end
             items-center gap-x-4 pr-2">
                <button>
                    <img @click="toggleSubtitle" style="width: 30px; height: 30px;" :src="subtitleIconSrc" alt="">
                </button>
                <button :disabled="isVideoAd" @click="toggleVideoOptions" class="setting-btn">
                    <img src="@/assets/icons/video-player/settings-icon.png" alt="">
                </button>
                <div v-if="!isPlaybackSpeedDivOpen && isVideoOptionsOpen" class="video-options select-none video-settings flex flex-col text-white items-start justify-center w-[250px] h-auto pb-4 pt-4
                 rounded-xl text-sm font-medium absolute bottom-16 right-2 bg-[#22191d] bg-opacity-80">
                    <div class="flex flex-row justify-start items-center w-full h-[35px]
                     gap-x-3 pl-2 hover:bg-[#383838]">
                        <img class="w-[26px] h-[26px]" src="@/assets/icons/video-player/double-qoutes-icon.png" alt="">
                        <p class="text-center">Annotations</p>
                        <label class="cursor-pointer toggle-switch justify-self-end ml-auto mr-2">
                            <input v-model="showAnnotation" type="checkbox" />
                            <span class="slider"></span>
                        </label>
                    </div>
                    <div @click="togglePlaybackSpeedDiv" class="flex flex-row justify-start items-center w-full h-[35px]
                     gap-x-3 pl-2 hover:bg-[#383838]">
                        <img class="w-[26px] h-[26px]" src="@/assets/icons/video-player/speed-icon.png" alt="">
                        <p class="text-center text-sm font-medium">Playback speed</p>
                        <p class="text-left ml-auto">{{ videoRef.playbackRate }}</p>
                        <img class="w-3 h-3 mr-2 rotate-180 cursor-pointer "
                            src="@/assets/icons/video-player/arrow-icon.png" alt="">
                    </div>
                </div>
                <div v-if="isPlaybackSpeedDivOpen && isVideoOptionsOpen" class="video-backspeed select-none flex flex-col text-white items-start justify-center w-[250px] h-auto pb-4 pt-4
                 rounded-xl absolute bottom-16 right-2 text-sm font-medium bg-[#22191d] bg-opacity-90">
                    <div @click="togglePlaybackSpeedDiv"
                        class="cursor-pointer  flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-[20px] hover:bg-[#383838]">
                        <img class="w-3 h-3" src="@/assets/icons/video-player/arrow-icon.png" alt="">
                        <p class="text-center ">Playback speed</p>
                    </div>
                    <div @click="changePlayBackSpeed(0.25)"
                        class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-5 hover:bg-[#383838]">
                        <p class="text-center">0.25</p>
                    </div>
                    <div @click="changePlayBackSpeed(0.5)"
                        class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-5 hover:bg-[#383838]">
                        <p class="text-center">0.5</p>
                    </div>
                    <div @click="changePlayBackSpeed(0.75)"
                        class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-5 hover:bg-[#383838]">
                        <p class="text-center">0.75</p>
                    </div>
                    <div @click="changePlayBackSpeed(1)"
                        class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-5 hover:bg-[#383838]">
                        <p class="text-center">Normal</p>
                    </div>
                    <div @click="changePlayBackSpeed(1.25)"
                        class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-5 hover:bg-[#383838]">
                        <p class="text-center">1.25</p>
                    </div>
                    <div @click="changePlayBackSpeed(1.5)"
                        class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-5 hover:bg-[#383838]">
                        <p class="text-center">1.5</p>
                    </div>
                    <div @click="changePlayBackSpeed(1.75)"
                        class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-5 hover:bg-[#383838]">
                        <p class="text-center">1.75</p>
                    </div>
                    <div @click="changePlayBackSpeed(2)"
                        class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-5 hover:bg-[#383838]">
                        <p class="text-center">2</p>
                    </div>
                </div>
                <button @click="toggleFullScreenMode" class="fullscreen-btn">
                    <img src="@/assets/icons/video-player/fullscree-icon.png" alt="">
                </button>
            </div>
        </div>
    </div>

    <div class="mt-14">
        <h1 class="video-title cursor-pointer">{{ videoInfo.title }}</h1>
    </div>

    <div class="video-detail-info">
        <img class="video-detail-channel-logo" loading="eager" :src="videoInfo.channel_profile_url" alt="">
        <div class="video-detail-upload-info">
            <p class="video-detail-channel-name">{{ videoInfo.channel_name }}</p>
            <p class="video-detail-channel-sub-count">2.5K subscribers</p>
        </div>
        <button class="video-detail-channel-sub-btn">Subscribe</button>
        <div class="video-detail-other-btn">
            <button @click="likeVideo(true)" class="like-btn"><img
                    :src="likeSituation === true ? fillLikeIcon : emptyLikeIcon" alt="">
                <span class="like-amount">1K</span>
            </button>
            <button @click="likeVideo(false)" class="dislike-btn"><img
                    :src="likeSituation === false ? fillDislikeIcon : emptyDislikeIcon" alt=""></button>
            <button @click="toggleSharingTab" class="share-btn"><img src="@/assets/icons/svg-icons/share-btn.svg"
                    alt="">
                <span>&nbsp;Share</span>
            </button>
            <button @click="saveVideoToPlaylist" class="save-btn"><img :src="saveSituation ? unSaveIcon : saveIcon">
                <span>Save</span>
            </button>
            <button @click="downloadVideo(videoInfo.id)" class="download-btn"><img
                    src="@/assets/icons/svg-icons/download-icon.svg" alt="">
                <span>Download</span>
            </button>
        </div>
    </div>

    <div class="video-description">
        <p class="video-detail-stats"><span class="view-amount">6.1M </span>views
            <span class="upload-date">{{ videoInfo.created_at }} </span>ago
            <span class="hashtags">#slowedandreverb #coolio #tiktoksong</span>
        </p>
        <p id="shortDescription">{{ truncatedDescription }}</p>
        <button v-if="videoInfo.description.length > 60" @click="toggleFullDescription" id="readMoreButton">
            {{ showFullDescription ? "Read less" : "Read more" }}
        </button>
    </div>
    <socialShare></socialShare>

    <div class="mb-12">
        <div v-if="isUserAuthenticated && !commentRetrievingLoading">
            <div class="comments-header mt-4">
                <div class="comments-stats">
                    <p class="total-comments">{{ comments.length }} Comments</p>
                </div>
                <div class="comment-creation mt-6">
                    <img class="user-profile-img" :src="userProfileImgSrc ?? ''" alt="">
                    <input v-model="userCommentText" @click="toggleVideoCommentButtons" type="text"
                        placeholder="Add a Comment...">
                </div>
                <div v-if="videoCommentButtonsShow" class="comment-btns">
                    <button @click="cancelUserComment" class="cancel-comment-btn">Cancel</button>
                    <button @click="submitVideoComment(null)" class="add-comment-btn">Comment</button>
                </div>
            </div>
            <div class="comment-container gap-y-6">
                <div v-for="comment in comments" :key="comment.id" class="comment flex flex-row">
                    <div class="author-thumbnail">
                        <img :src="comment.user_profile_picrure" alt="">
                    </div>
                    <div class="comment-detail">
                        <div class="author-info">@{{ comment.username ?? 'Anonymous User' }}
                            <span class="created_at">{{
                                comment.created_at }} days ago</span>
                        </div>
                        <div class="comment-text -mt-2">{{ comment.text }}</div>
                        <div class="comment-container-button">
                            <button class="comment-like-button" style="outline: none;">
                                <img :src="comment.is_liked === true ? fillLikeIcon : emptyLikeIcon">
                            </button>
                            <button class="comment-dislike-button" style="outline: none;">
                                <img :src="comment.is_liked === false ? fillDislikeIcon : emptyDislikeIcon">
                            </button>
                            <button @click="toggleUserCommentReplyButtons(comment.id)" class="user-comment-reply-button"
                                style="outline: none;">
                                <img class="w-8 h-8" :src="replyIcon" alt="">
                            </button>
                        </div>
                        <div v-if="commentStates[comment.id]?.repliesVisible"
                            class="w-auto flex justify-start items-center relative">
                            <div class="reply-creation">
                                <img class="user-profile-img" :src="userProfileImgSrc" alt="">
                                <input v-model="userReplyText" type="text" placeholder="Add a Reply...">
                            </div>
                            <div class="reply-btns flex justify-center items-center">
                                <button @click="toggleUserCommentReplyButtons(comment.id)"
                                    class="cancel-reply-btn">Cancel</button>
                                <button @click="submitVideoComment(comment.id)" class="submit-reply-btn">Reply</button>
                            </div>
                        </div>
                        <div v-if="comment.replies_count > 0" @click="retrieveCommentReplies(comment.id)"
                            class="comment-reply-button">
                            <i
                                :class="['arrow', commentStates[comment.id]?.replyContainerVisible ? 'button-reversed' : 'button']">
                            </i><span class="reply-count">&nbsp;&nbsp;{{ comment.replies_count }}&nbsp;</span>replies
                        </div>
                        <div v-if="commentStates[comment.id]?.replyContainerVisible" class="replies-container">
                            <div v-for="reply in comment.replies" :key="reply.id" class="reply">
                                <div class="reply-author-img">
                                    <img :src="reply.user_profile_picrure" alt="">
                                </div>
                                <div class="reply-detail">
                                    <div class="reply-author-info">
                                        <p>@</p>
                                        <p>{{ reply.username }}</p>
                                        <span>&nbsp;{{ reply.created_at }} days </span>ago
                                    </div>
                                    <p class="reply-value"><span class="text-blue-600 font-medium mr-2">@{{
                                        reply.parent_username
                                            }}</span>{{ reply.text }}</p>
                                    <div class="reply-toolbar">
                                        <button class="reply-like-button" style="outline: none;">
                                            <img :src="reply.is_liked === true ? fillLikeIcon : emptyLikeIcon">
                                        </button>
                                        <button class="reply-dislike-button" style="outline: none;">
                                            <img :src="reply.is_liked === false ? fillDislikeIcon : emptyDislikeIcon"
                                                alt="">
                                        </button>
                                        <button @click="toggleReplyCommentButtons(reply.id)"
                                            class="reply-comment-button" style="outline: none;">
                                            Reply
                                        </button>
                                        <div v-if="commentStates[reply.id]?.replyCommentButtonVisible"
                                            class="reply-division">
                                            <div class="reply-creation mt-3">
                                                <img class="user-profile-img" :src="userProfileImgSrc" alt="">
                                                <input v-model="userReplyText" type="text" placeholder="Add a Reply...">
                                            </div>
                                            <div class="reply-btns">
                                                <button @click="toggleReplyCommentButtons(reply.id)"
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
                <div v-if="commentScrollLoading" class="w-[50%] my-10">
                    <ClipLoader color="red" size="45px"></ClipLoader>
                </div>
            </div>
        </div>

        <div v-if="!isUserAuthenticated" class="w-[70%] flex justify-center items-center my-6">
            <router-link to="/auth/">
                <p class="font-medium text-[14px]">For seeing the Comments you have to be Logged in! <span
                        class="underline text-blue-500">Click Here</span></p>
            </router-link>
        </div>
        <div v-if="commentRetrievingLoading" class="w-[70%] my-10">
            <ClipLoader color="red" size="45px"></ClipLoader>
        </div>
    </div>

    <div class="right-side-container flex flex-col">
        <div class="top-14 w-[400px] h-[66px] bg-[#e4dfec] hover:bg-[#d1c2e9] flex flex-col justify-center
         absolute right-[110px] rounded-xl pl-3 transition-all duration-300 ease-in-out">
            <div class="flex flex-row items-center text-base">
                <p class="font-semibold">Next:&nbsp;</p>
                <p class="font-normal">Video title</p>
            </div>
            <div class="flex flex-row font-normal text-xs">
                <a href="#">Playlist name -&nbsp;</a>
                <p>1&nbsp;/&nbsp;367</p>
            </div>
            <button @click="playListExpandingToggle" class="absolute right-0 top-1/2 transform -translate-y-1/2 w-10 h-10 rounded-full bg-inherit hover:bg-[#cdc8d4]
                     flex justify-center items-center">
                <img class="w-3 h-3" src="@/assets/icons/svg-icons/thin-chevron-arrow-bottom-icon.svg" alt="">
            </button>
        </div>

        <div v-if="playlistExpanded" class="bg-white z-20 flex flex-col w-[400px] h-[500px] border-[#ededed] border-[1px]
                mb-10 absolute right-[110px] top-12 rounded-xl transition-all duration-300 ease-in-out">
            <div class="pl-3 pt-2">
                <a href="#" class="font-bold text-xl pt-2 mb-2">Playlist title</a>
                <div class="flex flex-row text-xs font-normal">
                    <a href="#" class="text-[#304354]">Playlist title -&nbsp;</a>
                    <span class="text-[#858c9c]">1/312</span>
                </div>
                <button @click="playListExpandingToggle"
                    class="absolute right-1 top-3 w-10 h-10 rounded-full hover:bg-[#e5e5e5] flex justify-center items-center">
                    <img class="w-4 h-4" src="@/assets/icons/svg-icons/x-mark-icon.svg" alt="">
                </button>
                <button class="w-10 h-10 rounded-full hover:bg-[#e5e5e5] flex justify-center items-center">
                    <img class="w-5 h-5" src="@/assets/icons/svg-icons/shuffle-icon.svg" alt="">
                </button>
                <button @click="togglePlaylistDivision" class="playlist-div-toggle flex justify-center items-center absolute top-[60px] right-[3px] w-10 h-10
                 rounded-full hover:bg-[#e5e5e5]">
                    <img class="w-4 h-4" src="@/assets/icons/svg-icons/kebab-menu.svg" alt="">
                </button>
                <a v-if="isPlaylistDivisonOpen" href="#" class="bg-white my-shadow w-[200px] h-[52px] rounded-xl flex items-center justify-center absolute
                    right-0 top-[100px]">
                    <div class="flex flex-row justify-center items-center cursor-pointer hover:bg-[#e5e5e5]
                     w-[200px] h-9">
                        <img class="w-6 h-6 pr-1" src="@/assets/icons/svg-icons/save-btn.svg" alt="">
                        <span class="font-normal text-sm">Save playlist to Library</span>
                    </div>
                </a>
            </div>

            <div class="playlist-videos-container overflow-x-hidden overflow-y-auto flex flex-col
                    gap-y-2 max-h-[422px]">
                <div class="playlist-video active pl-4 cursor-pointer hover:bg-[#f2f2f2] hover:shadow-2xl pt-2 pb-2">
                    <a href="#" class="flex flex-row">
                        <span class="ml-[-18px] flex justify-center items-center text-gray-500 text-sm">
                            1
                        </span>
                        <img class="flex-shrink-0 w-[100px] h-[56px] rounded-xl ml-2" src="@/assets/img/Django.png"
                            alt="">
                        <div class="flex flex-col ml-2">
                            <p class="font-semibold text-sm mb-2">Video title</p>
                            <p class="font-normal text-xs text-gray-600">channel name</p>
                        </div>
                    </a>
                </div>
                <div class="playlist-video pl-4 cursor-pointer hover:bg-[#f2f2f2] hover:shadow-2xl pt-2 pb-2">
                    <a href="#" class="flex flex-row">
                        <span class="ml-[-18px] flex justify-center items-center text-gray-500 text-sm">
                            1
                        </span>
                        <img class="flex-shrink-0 w-[100px] h-[56px] rounded-xl ml-2" src="@/assets/img/Django.png"
                            alt="">
                        <div class="flex flex-col ml-2">
                            <p class="font-semibold text-sm mb-2">Video title</p>
                            <p class="font-normal text-xs text-gray-600">channel name</p>
                        </div>
                    </a>
                </div>
            </div>
        </div>

        <div class="related-videos" :style="relatedVideosStyle">
            <div class="related-video">
                <div class="related-video-thumbnail">
                    <img src="@/assets/img/Django.png" alt="">
                </div>
                <div class="related-video-details">
                    <p><a href="">Django tutorial</a></p>
                    <p style="color: #6a6360; font-size: 13px;">channel name</p>
                    <p style="color: #6a6360; font-size: 13px;"><span class="related-video-views">2.4M</span> views
                        .
                        <span class="related-video-created_at">2 years</span> ago
                    </p>
                </div>
            </div>

            <div class="related-short-videos">
                <div class="title-container">
                    <img class="youtube-short-icon" src="@/assets/icons/svg-icons/shorts-icon.svg" alt="">
                    <p style="font-weight: bold; font-size: 16px;">Shorts</p>
                </div>
                <div class="short-video-groups gap-x-1 scroll-smooth">
                    <div class="related-short-video">
                        <div class="related-short-video-thumbnail">
                            <img src="@/assets/img/Django.png" alt="">
                        </div>
                        <div class="related-short-video-title h-auto">
                            <p class="video-title" style="margin-bottom: 3px;"><a href="">Django tutorial</a></p>
                            <p class="video-info"><span>5M</span> Views</p>
                        </div>
                    </div>
                    <div class="related-short-video">
                        <div class="related-short-video-thumbnail">
                            <img src="@/assets/img/Django.png" alt="">
                        </div>
                        <div class="related-short-video-title">
                            <p class="video-title" style="margin-bottom: 3px;"><a href="">Django tutorial</a></p>
                            <p class="video-info"><span>5M</span> Views</p>
                        </div>
                    </div>
                    <div class="related-short-video">
                        <div class="related-short-video-thumbnail">
                            <img src="@/assets/img/Django.png" alt="">
                        </div>
                        <div class="related-short-video-title">
                            <p class="video-title" style="margin-bottom: 3px;"><a href="">Django tutorial</a></p>
                            <p class="video-info"><span>5M</span> Views</p>
                        </div>
                    </div>
                    <div class="related-short-video">
                        <div class="related-short-video-thumbnail">
                            <img src="@/assets/img/Django.png" alt="">
                        </div>
                        <div class="related-short-video-title">
                            <p class="video-title" style="margin-bottom: 3px;"><a href="">Django tutorial</a></p>
                            <p class="video-info"><span>5M</span> Views</p>
                        </div>
                    </div>
                    <div class="related-short-video">
                        <div class="related-short-video-thumbnail">
                            <img src="@/assets/img/Django.png" alt="">
                        </div>
                        <div class="related-short-video-title">
                            <p class="video-title" style="margin-bottom: 3px;"><a href="">Django tutorial</a></p>
                            <p class="video-info"><span>5M</span> Views</p>
                        </div>
                    </div>
                    <div class="related-short-video">
                        <div class="related-short-video-thumbnail">
                            <img src="@/assets/img/Django.png" alt="">
                        </div>
                        <div class="related-short-video-title">
                            <p class="video-title" style="margin-bottom: 3px;"><a href="">Django tutorial</a></p>
                            <p class="video-info"><span>5M</span> Views</p>
                        </div>
                    </div>
                    <div class="related-short-video">
                        <div class="related-short-video-thumbnail">
                            <img src="@/assets/img/Django.png" alt="">
                        </div>
                        <div class="related-short-video-title">
                            <p class="video-title" style="margin-bottom: 3px;"><a href="">Django tutorial</a></p>
                            <p class="video-info"><span>5M</span> Views</p>
                        </div>
                    </div>
                    <div class="related-short-video">
                        <div class="related-short-video-thumbnail">
                            <img src="@/assets/img/Django.png" alt="">
                        </div>
                        <div class="related-short-video-title">
                            <p class="video-title" style="margin-bottom: 3px;"><a href="">Django tutorial</a></p>
                            <p class="video-info"><span>5M</span> Views</p>
                        </div>
                    </div>
                    <div class="related-short-video">
                        <div class="related-short-video-thumbnail">
                            <img src="@/assets/img/Django.png" alt="">
                        </div>
                        <div class="related-short-video-title">
                            <p class="video-title" style="margin-bottom: 3px;"><a href="">Django tutorial</a></p>
                            <p class="video-info"><span>5M</span> Views</p>
                        </div>
                    </div>
                </div>
                <button class="prev" @click="scrollHorizontally('prev')">❮</button>
                <button class="next" @click="scrollHorizontally('next')">❯</button>
            </div>

            <div class="related-video">
                <div class="related-video-thumbnail">
                    <img src="@/assets/img/Django.png" alt="">
                </div>
                <div class="related-video-details">
                    <p><a href="">Django tutorial</a></p>
                    <p style="color: #6a6360; font-size: 13px;">channel name</p>
                    <p style="color: #6a6360; font-size: 13px;"><span class="related-video-views">2.4M</span> views
                        .
                        <span class="related-video-created_at">2 years</span> ago
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>
<style scoped>
.annotation-div {
    transition: bottom 0.1s ease-in-out;
}

.annotation-btn {
    transition: opacity 0.1s ease;
}

.toggle-switch {
    position: relative;
    display: inline-block;
    width: 50px;
    height: 24px;
}

.toggle-switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    background-color: #707070;
    border-radius: 24px;
    width: 100%;
    height: 100%;
    transition: background-color 0.3s;
}

.slider::before {
    content: "";
    position: absolute;
    height: 20px;
    width: 20px;
    left: 4px;
    bottom: 2px;
    background-color: white;
    border-radius: 50%;
    transition: transform 0.3s;
}

.toggle-switch input:checked+.slider {
    background-color: #dc002c;
}

.toggle-switch input:checked+.slider::before {
    transform: translateX(22px);
}

.main-video {
    pointer-events: none;
}

.video-container button img {
    width: 24px;
    height: 24px;
}

.control-bar {
    transition: opacity 0.125s ease-in-out;
}

.fullscreen-btn:hover {
    animation: scale-back 0.4s;
}

@keyframes scale-back {

    0%,
    100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.15);
    }
}

.setting-btn:hover {
    animation: rotate-back 0.7s;
}

@keyframes rotate-back {

    0%,
    100% {
        transform: rotate(0);
    }

    50% {
        transform: rotate(45deg);
    }
}

/******** Chrome ********/
#volume-bar::-webkit-slider-runnable-track {
    background: white;
}

/******** Firefox ********/
#volume-bar::-moz-range-track {
    background: black;
}

#volume-bar::-moz-range-progress {
    background: white;
}

#volume-bar::-moz-range-thumb {
    border: none;
    width: 12px;
    height: 12px;
}

button:hover #volume-bar {
    display: flex;
}

#progress-bar:hover::-moz-range-thumb {
    visibility: visible;
}

#progress-bar:hover {
    transform: scaleY(1.3);
}

/* #progress-bar::-moz-range-progress {
    background: #ff0033;
} */

/* #progress-bar::-moz-range-thumb {
    visibility: hidden;
    background: red;
    border: none;
    width: 13px;
    height: 13px;
} */

#progress-bar::-moz-range-progress {
    background: red;
}

#progress-bar::-moz-range-thumb {
    visibility: hidden;
    background: red;
    border: none;
    width: 13px;
    height: 13px;
}

#progress-bar::-moz-range-track {
    background: rgb(150, 148, 148);
}
</style>