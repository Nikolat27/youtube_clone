<script setup>
import { ref, computed, reactive } from 'vue';
import axios from 'axios';
import { onClickOutside } from '@vueuse/core'
import { sharedState } from '@/sharedState';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import { useToast } from 'vue-toastification';

// Icons
import closeIcon from '/src/assets/icons/svg-icons/close-icon2.svg'
import arrowDown from '/src/assets/icons/svg-icons/thin-chevron-arrow-bottom-icon.svg'


const userAbleToSave = computed(() => { // User can only save the information if the title`s length is equal or greater than 0
    return (formData.playlist_title.length > 0 ? true : false)
})

const closePlaylistCreation = () => {
    sharedState.isPlaylistCreationOpen.open = false;
};

// Playlist Visibility settings
const isPlaylistVisibilityOpen = ref(false)
const togglePlaylistVisibility = () => isPlaylistVisibilityOpen.value = !isPlaylistVisibilityOpen.value
const changePlaylistVisibility = (type) => {
    isPlaylistVisibilityOpen.value = false;
    formData.playlist_visibility = type === 'public' ? 'public' : 'private'
}

const toast = useToast();

const retrievePlaylist = async () => {
    await axios.get(`${sharedState.websiteUrl}/studio/playlist/get/${sharedState.isPlaylistCreationOpen.playlist_id}`, {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        formData.playlist_id = response.data.data.id;
        formData.playlist_title = response.data.data.title;
        formData.playlist_description = response.data.data.description;
        formData.playlist_visibility = response.data.data.visibility;
    }).catch((error) => {
        console.log(error)
    }).finally(() => {
        sharedState.refreshRetrievePlaylists = false
    })
}

if (sharedState.isPlaylistCreationOpen.playlist_id) {
    retrievePlaylist()
}

const formData = reactive({
    playlist_id: '',
    playlist_title: '',
    playlist_description: '',
    playlist_visibility: 'private'
})

const isLoading = ref(false)
const submitForm = async () => {
    isLoading.value = true

    const submitFormData = new FormData()
    submitFormData.append("title", formData.playlist_title)
    submitFormData.append("description", formData.playlist_description)
    submitFormData.append("visibility", formData.playlist_visibility)
    submitFormData.append("user_session_id", sessionStorage.getItem("user_session_id"))

    const playlist_id = sharedState.isPlaylistCreationOpen.playlist_id
    if (playlist_id) {
        await axios.put(`${sharedState.websiteUrl}/studio/playlist/edit/${playlist_id}`, submitFormData).then((response) => {
            isLoading.value = false
            toast.success("Your playlist Updated Successfully!")
            sharedState.isPlaylistCreationOpen.playlist_id = null
            sharedState.isPlaylistCreationOpen.open = false
            sharedState.refreshRetrievePlaylists = true
        }, (error) => toast.error(error))
    } else {
        await axios.post(`${sharedState.websiteUrl}/studio/playlist/create`, submitFormData).then((response) => {
            isLoading.value = false
            toast.success("Your playlist Created Successfully!")
            sharedState.isPlaylistCreationOpen.playlist_id = null
            sharedState.isPlaylistCreationOpen.open = false
            sharedState.refreshRetrievePlaylists = true
        }, (error) => toast.error(error))
    }

}

const toggleButtonRef = ref(null)
onClickOutside(toggleButtonRef, () => { // Close the dropdown by clicking outside
    isPlaylistVisibilityOpen.value = false;
})
</script>

<template>
    <div class="playlist-creation cursor-auto bg-white relative top-[100px] left-[30%]
     w-[576px] h-[555px] rounded-xl flex flex-col" style="z-index: 999 !important;">
        <div class="header-content pl-6 w-[576px] h-[68px] flex flex-row items-center border-b">
            <p v-if="!sharedState.isPlaylistCreationOpen.playlist_id" class="text-[20px] font-medium">Create a new
                playlist</p>
            <p v-else class="text-[20px] font-medium">Edit your playlist</p>
            <button @click="closePlaylistCreation" class="justify-self-end ml-auto mr-4 w-[39.2px] h-[39.2px] rounded-full hover:bg-[#dfdfdf] flex 
            justify-center items-center">
                <img draggable="false" class="w-[15px] h-[15px]" :src="closeIcon" alt="">
            </button>
        </div>
        <div v-if="!isLoading" class="flex flex-col justify-start items-center mt-6">
            <div class="w-[536px] h-[79px] rounded-lg border border-solid border-[#d6d6d6] hover:border-black hover:border-2
                    focus:border-2 relative pl-2 pt-2 flex flex-col mb-8"
                :style="{ borderColor: userAbleToSave ? 'black' : 'red', borderWidth: !userAbleToSave ? '2px' : '1px' }">
                <span class="text-[12px] font-medium text-gray-600 text-left">Title (required)</span>
                <textarea @input="playlistTitleEdit" v-model="formData.playlist_title"
                    class="mt-1 edit-title-input w-[440px] h-[41px] outline-none text-[15px] font-normal overflow-hidden leading-4"
                    placeholder="Add title" minlength="1" required maxlength="100"></textarea>
                <span class="text-[12px] font-normal absolute right-1 bottom-1 text-gray-700"><span
                        class="title-char-counter">{{ formData.playlist_title.length }}</span>/150</span>
            </div>
            <div class="w-[536px] flex flex-col max-w-[536px] relative h-[163px] max-h-[163px] rounded-lg
                    border border-[#d6d6d6] pl-2 pt-2 hover:border-black hover:border-2">
                <span class="text-[12px] font-medium text-gray-600 text-left">Description</span>
                <textarea style="scrollbar-width: thin;" @input="playlistDescriptionEdit"
                    v-model="formData.playlist_description"
                    class="mt-1 edit-title-input w-[440px] h-[151px] outline-none text-[15px] font-normal overflow-y-auto leading-4"
                    placeholder="Add description" maxlength="5000"></textarea>
                <span class="text-[12px] font-normal absolute right-1 bottom-1 text-gray-700"><span
                        class="title-char-counter">{{ formData.playlist_description.length }}</span>/5000</span>
            </div>
            <div class="flex flex-col w-full gap-y-4 justify-start items-center">
                <p class="text-[15px] font-medium mr-auto ml-6 mt-6">Visibility</p>
                <div ref="toggleButtonRef" @click="togglePlaylistVisibility" class="flex w-[256px] h-[56px] rounded-xl flex-row mr-auto ml-6 border
                        justify-start pl-2 items-center relative cursor-pointer">
                    <div class="flex flex-col">
                        <span class="text-[12px] font-medium text-gray-600">Visibility</span>
                        <p class="text-[15px] font-normal">{{ formData.playlist_visibility }}</p>
                    </div>
                    <div class="justify-self-end ml-auto mr-4">
                        <img class="w-[14px] h-[14px]" :src="arrowDown" alt="">
                    </div>
                </div>
                <div ref="dropdownvisibility" v-if="isPlaylistVisibilityOpen" class="z-10 absolute left-[290px] bottom-20 bg-white py-4 w-[256px] text-[15px] font-normal h-auto rounded-xl
                        flex flex-col justify-start items-center" style="box-shadow: 0 0 8px rgba(0, 0, 0, 0.15);">
                    <button @click="changePlaylistVisibility('public')"
                        :class="[formData.playlist_visibility == 'public' ? 'active' : '']"
                        class="w-full h-[32px] text-left pl-6 hover:bg-[#f9f9f9]">Public</button>
                    <button @click="changePlaylistVisibility('private')"
                        :class="[formData.playlist_visibility == 'private' ? 'active' : '']"
                        class="w-full h-[32px] text-left pl-6 hover:bg-[#f9f9f9]">Private</button>
                </div>
            </div>
            <div class="playlist-footer w-full h-[68px] flex justify-end items-center pr-8
                    mt-4 border-t gap-x-2">
                <button @click="closePlaylistCreation" class="w-[73px] h-[36px] rounded-3xl hover:bg-[#f9f9f9] border-black border-2  text-black text-[14px]
                    font-medium">Cancel</button>
                <button v-if="!sharedState.isPlaylistCreationOpen.playlist_id" @click="submitForm"
                    :disabled="!userAbleToSave" :class="[!userAbleToSave ? 'opacity-80' : '']" class="w-[73px] h-[36px] rounded-3xl bg-black text-white text-[14px]
                    font-medium">Create</button>
                <button v-else @click="submitForm" :disabled="!userAbleToSave"
                    :class="[!userAbleToSave ? 'opacity-80' : '']" class="w-[73px] h-[36px] rounded-3xl bg-black text-white text-[14px]
                    font-medium">Save</button>
            </div>
        </div>
        <div v-else class="flex items-center h-full justify-center">
            <PulseLoader size="20px" color="red"></PulseLoader>
        </div>
    </div>
</template>
<style scoped>
@media (max-width: 740px) {
    .middle-section {
        display: none;
    }
}

button.active {
    background-color: #f1f1f1;
}

.playlist-creation {
    box-shadow: 0 0 14px rgba(0, 0, 0, 0.15);
}

textarea {
    resize: none;
}

.stepper-div button {
    margin-right: 45px;
}

.video-listbox {
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.13);
}

.upload-div {
    box-shadow: 0 0 14px rgba(0, 0, 0, 0.15);
}
</style>