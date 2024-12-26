import { reactive } from 'vue';

export const sharedState = reactive({
    isPlaylistCreationOpen: false,
    isVideoCreationOpen: { 'open': false, 'video_id': null },
    refreshRetrieveVideos: false,
    thumbnailPictureSrc: null,
});
