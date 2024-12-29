import { reactive } from 'vue';

export const sharedState = reactive({
    isPlaylistCreationOpen: { 'open': false, 'playlist_id': null },
    isVideoUploadingOpen: { 'open': false, 'video_type': 'long_video' }, // long_video and short_video
    isVideoCreationOpen: { 'open': false, 'video_id': null },
    refreshRetrieveVideos: false,
    refreshRetrievePlaylists: false,
    thumbnailPictureSrc: null,
});
