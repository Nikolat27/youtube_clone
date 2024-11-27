<script setup>
import { ref, computed, onMounted } from 'vue';


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
    top: playlistExpanded.value ? '580px' : '150px',
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
</script>


<template>
    <div class="video-container paused" data-volume-level="high">
        <img class="thumbnail-img">
        <div class="video-controls-container">
            <div class="timeline-container">
                <div class="timeline">
                    <img class="preview-img">
                    <div class="thumb-indicator"></div>
                </div>
            </div>
            <div class="controls">
                <button class="play-pause-btn">
                    <svg class="play-icon" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M8,5.14V19.14L19,12.14L8,5.14Z" />
                    </svg>
                    <svg class="pause-icon" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M14,19H18V5H14M6,19H10V5H6V19Z" />
                    </svg>
                </button>
                <div class="volume-container">
                    <button class="mute-btn">
                        <svg class="volume-high-icon" viewBox="0 0 24 24">
                            <path fill="currentColor"
                                d="M14,3.23V5.29C16.89,6.15 19,8.83 19,12C19,15.17 16.89,17.84 14,18.7V20.77C18,19.86 21,16.28 21,12C21,7.72 18,4.14 14,3.23M16.5,12C16.5,10.23 15.5,8.71 14,7.97V16C15.5,15.29 16.5,13.76 16.5,12M3,9V15H7L12,20V4L7,9H3Z" />
                        </svg>
                        <svg class="volume-low-icon" viewBox="0 0 24 24">
                            <path fill="currentColor"
                                d="M5,9V15H9L14,20V4L9,9M18.5,12C18.5,10.23 17.5,8.71 16,7.97V16C17.5,15.29 18.5,13.76 18.5,12Z" />
                        </svg>
                        <svg class="volume-muted-icon" viewBox="0 0 24 24">
                            <path fill="currentColor"
                                d="M12,4L9.91,6.09L12,8.18M4.27,3L3,4.27L7.73,9H3V15H7L12,20V13.27L16.25,17.53C15.58,18.04 14.83,18.46 14,18.7V20.77C15.38,20.45 16.63,19.82 17.68,18.96L19.73,21L21,19.73L12,10.73M19,12C19,12.94 18.8,13.82 18.46,14.64L19.97,16.15C20.62,14.91 21,13.5 21,12C21,7.72 18,4.14 14,3.23V5.29C16.89,6.15 19,8.83 19,12M16.5,12C16.5,10.23 15.5,8.71 14,7.97V10.18L16.45,12.63C16.5,12.43 16.5,12.21 16.5,12Z" />
                        </svg>
                    </button>
                    <input class="volume-slider" type="range" min="0" max="1" step="any" value="1">
                </div>
                <div class="duration-container">
                    <div class="current-time">0:00</div>
                    /
                    <div class="total-time"></div>
                </div>
                <button class="captions-btn">
                    <svg viewBox="0 0 24 24">
                        <path fill="currentColor"
                            d="M18,11H16.5V10.5H14.5V13.5H16.5V13H18V14A1,1 0 0,1 17,15H14A1,1 0 0,1 13,14V10A1,1 0 0,1 14,9H17A1,1 0 0,1 18,10M11,11H9.5V10.5H7.5V13.5H9.5V13H11V14A1,1 0 0,1 10,15H7A1,1 0 0,1 6,14V10A1,1 0 0,1 7,9H10A1,1 0 0,1 11,10M19,4H5C3.89,4 3,4.89 3,6V18A2,2 0 0,0 5,20H19A2,2 0 0,0 21,18V6C21,4.89 20.1,4 19,4Z" />
                    </svg>
                </button>
                <button class="speed-btn wide-btn">
                    1x
                </button>
                <button class="mini-player-btn">
                    <svg viewBox="0 0 24 24">
                        <path fill="currentColor"
                            d="M21 3H3c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H3V5h18v14zm-10-7h9v6h-9z" />
                    </svg>
                </button>
                <button class="theater-btn">
                    <svg class="tall" viewBox="0 0 24 24">
                        <path fill="currentColor"
                            d="M19 6H5c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 10H5V8h14v8z" />
                    </svg>
                    <svg class="wide" viewBox="0 0 24 24">
                        <path fill="currentColor"
                            d="M19 7H5c-1.1 0-2 .9-2 2v6c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2zm0 8H5V9h14v6z" />
                    </svg>
                </button>
                <button class="full-screen-btn">
                    <svg class="open" viewBox="0 0 24 24">
                        <path fill="currentColor"
                            d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z" />
                    </svg>
                    <svg class="close" viewBox="0 0 24 24">
                        <path fill="currentColor"
                            d="M5 16h3v3h2v-5H5v2zm3-8H5v2h5V5H8v3zm6 11h2v-3h3v-2h-5v5zm2-11V5h-2v5h5V8h-3z" />
                    </svg>
                </button>
            </div>
        </div>
        <video src="@/assets/video/test-vid2.mp4">
            <track kind="captions" srclang="en" src="@/assets/subtitles.vtt">
        </video>
    </div>

    <h1 class="video-title">Video title</h1>

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
        <div v-for="comment in comments" :key="comment.id" class="comment">
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
                        data-target="comment-id-1" style="outline: none;">
                        <img class="image-y-z" src="@/assets/icons/svg-icons/reply-icon.svg" data-target="comment-id-1"
                            alt="">
                    </button>
                </div>
                <div v-if="commentStates[comment.id]?.repliesVisible"
                    class="w-auto flex justify-center items-center relative" id="comment-id-1">
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
        <div class="w-[400px] h-[66px] bg-[#e4dfec] hover:bg-[#d1c2e9] flex flex-col justify-center
         absolute right-[110px] top-[66px] rounded-xl pl-3 transition-all duration-300 ease-in-out">
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
                mb-10 absolute right-[110px] top-[66px] rounded-xl transition-all duration-300 ease-in-out">
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
                <div class="short-video-groups gap-x-1">
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