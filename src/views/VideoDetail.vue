<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';

// Icons
import playIcon from '@/assets/icons/video-player/play-icon.png'
import pauseIcon from '@/assets/icons/video-player/pause-icon.png'
import onSubtitleIcon from '@/assets/icons/video-player/subtitle-on-icon.png'
import offSubtitleIcon from '@/assets/icons/video-player/subtitle-off-icon.png'
import fullSpeakerIcon from '@/assets/icons/video-player/full-speaker-icon.png'
import halfSpeakerIcon from '@/assets/icons/video-player/half-speaker-icon.png'
import muteSpeakerIcon from '@/assets/icons/video-player/mute-speaker-icon.png'

const route = useRoute()
const videoId = route.params.id

// Description Toggling
const showFullDescription = ref(false);
const toggleFullDescription = () => {
    showFullDescription.value = !showFullDescription.value;
};

const comments = [
    {
        id: 1, text: "Hello World", replies: [
            { id: 2, parent_id: 1, text: `Reply 1`, replies: [] },
            {
                id: 3, parent_id: 1, text: `Reply 2`, replies: [
                    { parent_id: 3, id: 4, text: "Reply 3" },
                ]
            },
            { id: 5, parent_id: 1, text: `Reply 4`, replies: [] },
        ]
    }
]

const truncatedDescription = computed(() => {
    const description = "<p id=''>Lorem ipsum dolor sit amet consectetur adipisicing elit. Perspiciatis eos doloribus quibusdam quidem tempore qui voluptatibus ducimus veritatis sunt alias aliquid inventore iure, ex dolor consectetur eveniet, deleniti nobis aperiam.</p>";
    return showFullDescription.value
        ? description
        : `${description.substring(0, 60)}...`;
});


// Video Comment Toggling
const videoCommentButtonsShow = ref(false);
const toggleVideoCommentButtons = () => {
    videoCommentButtonsShow.value = !videoCommentButtonsShow.value;
};
const submitVideoComment = () => {
    const commentText = document.getElementById("comment-text").value;
};


// Comment and Reply Toggling Management
const commentStates = ref({});
const toggleCommentState = (commentId, state) => {
    if (!commentStates.value[commentId]) {
        commentStates.value[commentId] = { repliesVisible: false, replyContainerVisible: false, replyCommentButtonVisible: false };
    }
    commentStates.value[commentId][state] = !commentStates.value[commentId][state];
};

const toggleUserCommentReplyButtons = (commentId) => toggleCommentState(commentId, 'repliesVisible');
const toggleReplyContainer = (commentId) => toggleCommentState(commentId, 'replyContainerVisible');
const toggleReplyCommentButtons = (commentId) => toggleCommentState(commentId, 'replyCommentButtonVisible');


// Playlist Toggling
let playlistExpanded = ref(false);
const playListExpandingToggle = () => {
    playlistExpanded.value = !playlistExpanded.value;
}


// Styles for related-video div
const relatedVideosStyle = computed(() => ({
    position: 'absolute',
    right: '107px',
    top: playlistExpanded.value ? '575px' : '130px',
    transition: 'top 0.1s ease-in-out'
}));


// Sliding for related short videos
const scrollLeft = () => {
    const shortDivContainer = document.querySelector(".short-video-groups");
    shortDivContainer.scrollLeft -= 131;
}

const scrollRight = () => {
    const shortDivContainer = document.querySelector(".short-video-groups");
    shortDivContainer.scrollLeft += 131;
}


// Playlist divison toggling
let isPlaylistDivisonOpen = ref(false)
const togglePlaylistDivision = () => {
    isPlaylistDivisonOpen.value = !isPlaylistDivisonOpen.value
}


// Handling Main video
const playVideoIcon = ref(playIcon)
const isVideoPlayed = ref(false)
const toggleVideoPlay = async () => {
    const video = document.querySelector(".main-video")
    isVideoPlayed.value = !isVideoPlayed.value
    if (!isVideoPlayed.value) {
        video.pause()
        playVideoIcon.value = `${playIcon}`
    } else {
        video.play()
        playVideoIcon.value = `${pauseIcon}`
    }

    // Ensure the DOM has updated
    await nextTick();
}

const subtitleIconSrc = ref(offSubtitleIcon)
const isSubtitleOn = ref(false)
const toggleSubtitle = () => {
    isSubtitleOn.value = !isSubtitleOn.value
    subtitleIconSrc.value = isSubtitleOn.value ? `${onSubtitleIcon}` : `${offSubtitleIcon}`
}

const isVideoOptionsOpen = ref(false)
const toggleVideoOptions = () => isVideoOptionsOpen.value = !isVideoOptionsOpen.value

const toggleFullScreenMode = () => {
    document.querySelector(".main-video").requestFullscreen();
}

const speakerIconSrc = ref(fullSpeakerIcon)
const videoVolumeChanging = (event) => {
    const video = document.querySelector(".main-video")
    video.muted = false
    video.volume = event.target.value / 100
    speakerIconSrc.value = video.volume >= 0.5 ? `${fullSpeakerIcon}` : (video.volume > 0 ? `${halfSpeakerIcon}` : `${muteSpeakerIcon}`);
}

const muteVideo = () => {
    const video = document.querySelector(".main-video")
    const speakerBtn = document.querySelector(".speaker-btn")
    video.muted = !video.muted
    speakerBtn.src = video.muted ? `${muteSpeakerIcon}` : `${fullSpeakerIcon}`
}

//Handling playback speed for Main video
const isPlaybackSpeedOpen = ref(false)
const togglePlaybackSpeed = () => isPlaybackSpeedOpen.value = !isPlaybackSpeedOpen.value

const videoRef = ref(null)
const videoProgress = ref(0)
const updateProgress = () => {
    if (videoRef.value) {
        videoProgress.value = (videoRef.value.currentTime / videoRef.value.duration) * 100
    }
}

const seekVideo = (event) => {
    if (videoRef.value) {
        const newTime = (event.target.value / 100) * videoRef.value.duration;
        videoRef.value.currentTime = newTime;
    }
}

const openControlBar = () => {
    document.querySelector(".control-bar").style.opacity = 1
}

const closeControlBar = () => {
    document.querySelector(".control-bar").style.opacity = 0
}

let mouseValue = ref(null)
let position = ref(null)
const getVideoFrame = (event) => {
    const input = event.target
    const { left, width } = input.getBoundingClientRect();
    const positionX = event.clientX - left;
    if (positionX - 100 >= 0) {
        position.value = positionX - left
    } else {
        position.value = 0
    }
    const percentage = Math.round(positionX / (width / 100))
    const video = videoRef.value;
    mouseValue.value = (video.duration / 100) * percentage
    const canvas = document.getElementById("myCanvas");
    const context = canvas.getContext('2d');

    const hiddenVideo = document.createElement('video');
    hiddenVideo.src = video.src;

    hiddenVideo.addEventListener('loadeddata', () => {
        hiddenVideo.currentTime = mouseValue.value;
    });

    hiddenVideo.addEventListener('seeked', () => {
        context.drawImage(hiddenVideo, 0, 0, canvas.width, canvas.height);
    });

    hiddenVideo.load();
}

onMounted(() => {
    videoRef.value.addEventListener('timeupdate', updateProgress);
});
</script>


<template>
    <div @mouseover="openControlBar" @mouseleave="closeControlBar" class="video-container top-12 relative overflow-hidden mx-auto flex justify-center
     items-center rounded-2xl">
        <video ref="videoRef" src="/src/assets/video/test-vid2.mp4" volume="0.5"
            class="main-video source-video cursor-pointer w-full h-full object-fill">
            <!-- <source class="source-video" src="@/assets/video/test-vid2.mp4"> -->
        </video>

        <div class="bg-transparent z-50 control-bar flex opacity-0 w-full h-[48px] max-h-[48px] absolute bottom-0 justify-center
         items-center flex-row">
            <div class="video-progress-bar w-[906px] h-[8px] absolute bottom-14">
                <div class="z-10 video-img-tracker overflow-hidden w-[225px] h-[130px] rounded-lg border-[3px] border-white
                  absolute bottom-12" :class="[`left-[${position}px]`]">
                    <canvas id="myCanvas" class="z-0 w-full h-full object-fill"></canvas>
                </div>
                <input @mousemove="getVideoFrame" @mouseleave="mouseValue = null" min="0" max="100"
                    :value="videoProgress" id="progress-bar" class="h-full w-full" type="range" @input="seekVideo">
            </div>
            <div class="w-[618px] h-full left-controls flex flex-row justify-start
             items-center gap-x-6 pl-2">
                <button @click="toggleVideoPlay">
                    <img class="play-video-button" style="width: 20px; height: 20px;" :src="playVideoIcon" alt="">
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
                    <span class="current-video-time">0:00</span>
                    <span>/</span>
                    <span class="end-video-time">6:48</span>
                </p>
            </div>
            <div class="w-[288px] h-full right-controls flex flex-row justify-end
             items-center gap-x-4 pr-2">
                <button>
                    <img @click="toggleSubtitle" style="width: 30px; height: 30px;" :src="subtitleIconSrc" alt="">
                </button>
                <button @click="toggleVideoOptions" class="setting-btn">
                    <img src="@/assets/icons/video-player/settings-icon.png" alt="">
                </button>
                <div v-if="!isPlaybackSpeedOpen && isVideoOptionsOpen" class="video-options select-none video-settings flex flex-col text-white items-start justify-center w-[250px] h-auto pb-4 pt-4
                 rounded-xl text-sm font-medium absolute bottom-16 right-2 bg-[#22191d] bg-opacity-80">
                    <div class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px]
                     gap-x-3 pl-2 hover:bg-[#383838]">
                        <img class="w-[26px] h-[26px]" src="@/assets/icons/video-player/double-qoutes-icon.png" alt="">
                        <p class="text-center">Annotations</p>
                    </div>
                    <div @click="togglePlaybackSpeed" class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px]
                     gap-x-3 pl-2 hover:bg-[#383838]">
                        <img class="w-[26px] h-[26px]" src="@/assets/icons/video-player/speed-icon.png" alt="">
                        <p class="text-center text-sm font-medium">Playback speed</p>
                        <p class="text-left ml-auto">0.75</p>
                        <img class="w-3 h-3 mr-2 rotate-180" src="@/assets/icons/video-player/arrow-icon.png" alt="">
                    </div>
                </div>
                <div v-if="isPlaybackSpeedOpen" class="video-backspeed select-none flex flex-col text-white items-start justify-center w-[250px] h-auto pb-4 pt-4
                 rounded-xl absolute bottom-16 right-2 text-sm font-medium bg-[#22191d] bg-opacity-90">
                    <div @click="togglePlaybackSpeed"
                        class="cursor-pointer  flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-[20px] hover:bg-[#383838]">
                        <img class="w-3 h-3" src="@/assets/icons/video-player/arrow-icon.png" alt="">
                        <p class="text-center ">Playback speed</p>
                    </div>
                    <div
                        class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-5 hover:bg-[#383838]">
                        <p class="text-center">0.25</p>
                    </div>
                    <div
                        class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-5 hover:bg-[#383838]">
                        <p class="text-center">0.5</p>
                    </div>
                    <div
                        class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-5 hover:bg-[#383838]">
                        <p class="text-center">0.75</p>
                    </div>
                    <div
                        class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-5 hover:bg-[#383838]">
                        <p class="text-center">Normal</p>
                    </div>
                    <div
                        class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-5 hover:bg-[#383838]">
                        <p class="text-center">1.25</p>
                    </div>
                    <div
                        class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-5 hover:bg-[#383838]">
                        <p class="text-center">1.5</p>
                    </div>
                    <div
                        class="cursor-pointer flex flex-row justify-start items-center w-full h-[35px] gap-x-3 pl-5 hover:bg-[#383838]">
                        <p class="text-center">1.75</p>
                    </div>
                    <div
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
        <h1 class="video-title cursor-pointer">Video title</h1>
    </div>

    <div class="video-detail-info">
        <img class="video-detail-channel-logo" src="@/assets/img/Django.png" alt="">
        <div class="video-detail-upload-info">
            <p class="video-detail-channel-name">Channel name</p>
            <p class="video-detail-channel-sub-count">2.5K subscribers</p>
        </div>
        <button class="video-detail-channel-sub-btn">Subscribe</button>
        <div class="video-detail-other-btn">
            <button class="like-btn"><img src="@/assets/icons/svg-icons/like-empty.svg" alt="">
                <span class="like-amount">1K</span>
            </button>
            <button class="dislike-btn"><img src="@/assets/icons/svg-icons/dislike-empty.svg" alt=""></button>
            <button class="share-btn"><img src="@/assets/icons/svg-icons/share-btn.svg" alt="">
                <span>&nbsp;Share</span>
            </button>
            <button class="save-btn"><img src="@/assets/icons/svg-icons/save-btn.svg" alt="">
                <span>Save</span>
            </button>
            <button class="download-btn"><img src="@/assets/icons/svg-icons/download-icon.svg" alt="">
                <span>Download</span>
            </button>
        </div>
    </div>

    <div class="video-description">
        <p class="video-detail-stats"><span class="view-amount">6.1M </span>views
            <span class="upload-date">2 years </span>ago
            <span class="hashtags">#slowedandreverb #coolio #tiktoksong</span>
        </p>
        <p id="shortDescription">{{ truncatedDescription }}</p>
        <button @click="toggleFullDescription" id="readMoreButton">
            {{ showFullDescription ? "Read less" : "Read more" }}
        </button>
    </div>

    <div class="comments-header mt-4">
        <div class="comments-stats">
            <p class="total-comments">{{ comments.length }} Comments</p>
        </div>
        <div class="comment-creation mt-6">
            <img class="user-profile-img" src="@/assets/img/Django.png" alt="">
            <input @click="toggleVideoCommentButtons" class="add-comment-input" id="comment-text" type="text"
                placeholder="Add a Comment...">
        </div>
        <div v-if="videoCommentButtonsShow" class="comment-btns">
            <button @click="toggleVideoCommentButtons" class="cancel-comment-btn">Cancel</button>
            <button @click="submitVideoComment" class="add-comment-btn">Comment</button>
        </div>
    </div>

    <div class="comment-container">
        <div v-for="comment in comments" :key="comment.id" class="comment flex flex-row">
            <div class="author-thumbnail">
                <img src="@/assets/img/Django.png" alt="">
            </div>
            <div class="comment-detail">
                <div class="author-info">@nikolat27 <span class="created_at">2 months ago</span></div>
                <div class="comment-text -mt-2">{{ comment.text }}</div>
                <div class="comment-container-button">
                    <button class="comment-like-button" style="outline: none;">
                        <img src="@/assets/icons/svg-icons/like-empty.svg">
                    </button>
                    <button class="comment-dislike-button" style="outline: none;">
                        <img src="@/assets/icons/svg-icons/dislike-empty.svg">
                    </button>
                    <button @click="toggleUserCommentReplyButtons(comment.id)" class="user-comment-reply-button"
                        style="outline: none;">
                        <img class="image-y-z w-8 h-8" src="@/assets/icons/svg-icons/reply-icon.svg" alt="">
                    </button>
                </div>
                <div v-if="commentStates[comment.id]?.repliesVisible"
                    class="w-auto flex justify-start items-center relative">
                    <div class="reply-creation">
                        <img class="user-profile-img" src="@/assets/img/Django.png" alt="">
                        <input class="add-reply-input" id="reply-text" type="text" placeholder="Add a Reply...">
                    </div>
                    <div class="reply-btns flex justify-center items-center">
                        <button @click="toggleUserCommentReplyButtons(comment.id)" class="cancel-reply-btn"
                            data-target="comment-id-1">Cancel</button>
                        <button @click="submitUserCommentReply(comment.id)" class="submit-reply-btn"
                            data-target="comment-id-1">Reply</button>
                    </div>
                </div>
                <div @click="toggleReplyContainer(comment.id)" class="comment-reply-button" data-target="comment-id-1">
                    <i
                        :class="['arrow', commentStates[comment.id]?.replyContainerVisible ? 'button-reversed' : 'button']">
                    </i><span class="reply-count">&nbsp;&nbsp;63&nbsp;</span>replies
                </div>
                <div v-if="commentStates[comment.id]?.replyContainerVisible" class="replies-container">
                    <div v-for="(reply, index) in comment.replies" :key="index" class="reply">
                        <div class="reply-author-img">
                            <img src="@/assets/img/Django.png" alt="">
                        </div>
                        <div class="reply-detail">
                            <div class="reply-author-info">
                                <p>@</p>
                                <p>Nikolat27</p>
                                <span>1 years </span>ago
                            </div>
                            <p class="reply-value">{{ reply.text }} / {{ reply.parent_id }}</p>
                            <div class="reply-toolbar">
                                <button class="reply-like-button" style="outline: none;">
                                    <img src="@/assets/icons/svg-icons/like-empty.svg">
                                </button>
                                <button class="reply-dislike-button" style="outline: none;">
                                    <img src="@/assets/icons/svg-icons/dislike-empty.svg" alt="">
                                </button>
                                <button @click="toggleReplyCommentButtons(reply.id)" class="reply-comment-button"
                                    style="outline: none;" data-target="reply-input-1">
                                    Reply
                                </button>
                                <div v-if="commentStates[reply.id]?.replyCommentButtonVisible" class="reply-division"
                                    id="reply-input-1">
                                    <div class="reply-creation mt-3">
                                        <img class="user-profile-img" src="@/assets/img/Django.png" alt="">
                                        <input class="add-reply-input" id="reply-text" type="text"
                                            placeholder="Add a Reply...">
                                    </div>
                                    <div class="reply-btns">
                                        <button @click="toggleReplyCommentButtons(reply.id)" class="cancel-reply-btn"
                                            data-target="reply-input-1">Cancel</button>
                                        <button class="submit-reply-btn" data-target="reply-input-1">Reply</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="right-side-container flex flex-col">
        <div class="top-12 w-[400px] h-[66px] bg-[#e4dfec] hover:bg-[#d1c2e9] flex flex-col justify-center
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
                <button class="prev" @click="scrollLeft">❮</button>
                <button class="next" @click="scrollRight">❯</button>
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

#progress-bar::-moz-range-progress {
    background: #ff0033;
}

#progress-bar:hover::-moz-range-thumb {
    visibility: visible;
}

#progress-bar:hover {
    transform: scaleY(1.3);
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
