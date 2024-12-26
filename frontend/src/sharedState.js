import { reactive } from 'vue';

export const sharedState = reactive({
    isPlaylistCreationOpen: false,
    isVideoCreationOpen: false,
    thumbnailPictureSrc: null,
});
