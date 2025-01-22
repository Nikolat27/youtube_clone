<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import axios from 'axios';

// Icons
import editIcon from '@/assets/icons/svg-icons/edit-icon.svg'
import kebabMenuIcon from '@/assets/icons/svg-icons/kebab-menu.svg'
import uninstallIcon from '@/assets/icons/svg-icons/uninstall-icon.svg'


// Edit Video Title Management
const communityText = ref('')
const communityTextLength = computed(() => communityText.value.length)

const communityTextEdit = (event) => {
    communityText.value = event.target.value;
}
const userAbleToSave = computed(() => { // User can only save the information if the title`s length is equal or greater than 0
    return (communityText.value.length > 0 ? true : false)
})


// Opening closing video options 
const communityOptionStates = ref({});
const toggleOptions = (community_id, community_text = '', option) => {
    if (!communityOptionStates.value[community_id]) {
        communityOptionStates.value = {};
        communityOptionStates.value[community_id] = { optionDiv: false, editDiv: false }
    }
    communityOptionStates.value[community_id][option] = !communityOptionStates.value[community_id][option]

    communityText.value = community_text;
}

const toggleCommunityOptions = (community_id, community_text) => toggleOptions(community_id, community_text, 'optionDiv')
const toggleCommunityEdit = (community_id, community_text) => toggleOptions(community_id, community_text, 'editDiv')

const router = useRoute()

watch(router, () => {
    retrieveAllPosts()
})

const deleteCommunity = (id) => {
    axios.delete(`http://127.0.0.1:8000/studio/community/delete/${id}`).then((response) => {
        if (response.status == 204) {
            toast.success("Post deleted successfully!")
            retrieveAllPosts()
        }
    }).catch((error) => console.error(error))
}

let posts = reactive([])
const retrieveAllPosts = async () => {
    await axios.get("http://127.0.0.1:8000/studio/community/list", {
        params: {
            'user_session_id': sessionStorage.getItem('user_session_id'),
            'queries': router.query
        }
    }).then((response) => {
        posts.splice(0, posts.length, ...response.data.data)
    }).catch((error) => {
        console.log(error)
    })
}

const toast = useToast()
const submitFormData = (community_id) => {
    const newFormData = new FormData();

    newFormData.append("user_session_id", sessionStorage.getItem('user_session_id'))
    newFormData.append("community_id", community_id)
    newFormData.append("community_text", communityText.value)

    axios.post("http://127.0.0.1:8000/studio/community/edit", newFormData).then((response) => {
        if (response.status == 200) {
            toast.success("Community updated successfully!");
            toggleCommunityEdit(community_id, communityText.value);
            retrieveAllPosts();
        }
    }).catch((error) => {
        toast.error(error)
    })
}
onMounted(() => {
    retrieveAllPosts()
})
</script>
<template>
    <div class="border-b font-roboto pl-[48px] w-full">
        <div v-for="post in posts" :key="post.id" class="table-itself border-b">
            <div class="video-thumbnail">
                <img draggable="false" :src="post.community_image" alt="">
            </div>
            <div class="video-detail relative flex flex-col font-normal text-[13px] mt-2" style="padding-left: 12px;">
                <span>{{ post.community_text }}</span>
                <div class="flex flex-row justify-start items-center">
                    <button @click="toggleCommunityEdit(post.id, post.community_text)" class="w-[39.2px] h-[39.2px] rounded-full hover:bg-[#eaeaea] flex items-center
                        justify-center">
                        <img class="w-[17px] h-[17px] center" :src="editIcon" alt="">
                    </button>
                    <button @click="toggleCommunityOptions(post.id, post.community_text)" class="w-[39.2px] h-[39.2px] rounded-full hover:bg-[#eaeaea] flex items-center
                        justify-center">
                        <img class="w-[17px] h-[17px] center" :src="kebabMenuIcon" alt="">
                    </button>
                    <div v-if="communityOptionStates[post.id]?.optionDiv" class="absolute left-24 top-0 video-edit-options w-[226px] h-auto rounded-xl bg-white flex flex-col
                        justify-start items-center py-4">
                        <div @click="deleteCommunity(post.id)" class="w-full h-[32px] hover:bg-[#f9f9f9] flex flex-row justify-start items-center
                        text-[15px] font-normal font-roboto">
                            <img class="w-[17px] h-[17px] mx-4" :src="uninstallIcon" alt="">
                            <p>Delete forever</p>
                        </div>
                    </div>
                    <div v-if="communityOptionStates[post.id]?.editDiv" class="edit-post-text bg-white z-40 w-[488px] h-auto max-h-[368px] rounded-lg
                        flex flex-col justify-start pt-2 items-center gap-y-4 absolute left-2 top-6">
                        <div class="w-[464px] h-[91px] rounded-lg border border-solid box-border border-[#d6d6d6] hover:border-black hover:border-2
                            focus:border-2 relative pl-2 pt-2"
                            :style="{ borderColor: userAbleToSave ? 'black' : 'red', borderWidth: !userAbleToSave ? '2px' : '1px' }">
                            <span class="text-[12px] font-medium text-gray-600">Post`s Text (required)</span>
                            <textarea @input="communityTextEdit" v-model="communityText"
                                class="mt-1 edit-title-input w-[440px] h-[41px] outline-none text-[15px] font-normal overflow-hidden leading-4"
                                placeholder="Add Community (post) text" minlength="1" required
                                maxlength="100"></textarea>
                            <span class="text-[12px] font-normal absolute right-1 bottom-1 text-gray-700"><span
                                    class="title-char-counter">{{ communityTextLength }}</span>/100</span>
                        </div>
                        <div class="flex flex-row w-full self-end justify-end items-center font-roboto 
                            gap-x-2 pr-2 pb-2">
                            <span v-if="!userAbleToSave" class="text-[12px] font-normal text-red-800">Your
                                post needs a title</span>
                            <button @click="toggleCommunityEdit(post.id, post.community_text)" class="w-[74.9px] h-[36px] rounded-3xl text-[14px] font-medium
                         items-center text-black bg-[#f2f2f2] hover:bg-[#e5e5e5]">Cancel</button>
                            <button @click="submitFormData(post.id)" :disabled="!userAbleToSave" class="w-[62.2px] h-[36px] rounded-3xl text-[14px] font-medium
                         items-center text-white hover:bg-[#272727]"
                                :style="{ backgroundColor: userAbleToSave ? 'black' : 'gray' }">Save</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="video-info w-[70%] relative h-full flex flex-row justify-end items-center text-[13px] font-normal
                ml-auto mr-8">
                <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[355px]">Draft</p>
                <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[430px]">Draft</p>
                <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[525px]">{{ post.created_at }}</p>
                <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[635px]">Draft</p>
                <p class="ml-4 absolute top-1/3 transform translate-y-1/3 left-[710px]">Draft</p>
                <p class="ml-8 absolute top-1/3 transform translate-y-1/3 left-[775px]">{{ post.total_likes }}, {{
                    post.total_dislikes }}</p>
            </div>
        </div>
    </div>
</template>
<style scoped>
@media (min-width: 1200px) {
    #channel-content {
        left: 254px;
        top: 100px;
    }
}

.filter-options div {
    cursor: pointer;
}

.edit-title-input {
    resize: none;
}

.edit-post-text {
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.15);
}

.channel-main-content div {
    padding-left: 48px;
}

.video-edit-options {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.13);
}

.table-itself {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    width: 100%;
    height: 83px;
}

.video-thumbnail {
    position: relative;
    display: flex;
    justify-content: center;
    align-content: center;
    width: auto;
    height: 83px;
    margin-bottom: 0px;
    align-items: center;
}

.video-thumbnail img {
    width: 120px !important;
    height: 68px !important;
    border-radius: 8px;
}

.video-duration {
    position: absolute;
    right: 3px;
    bottom: 10px;
    border-radius: 0.375rem;
    width: 2rem;
    height: 1rem;
    text-align: center;
    color: white;
    background-color: rgba(107, 114, 128, 0.85);
    font-size: 0.75rem;
    font-weight: 500;
}

.filter-options {
    box-shadow: 0 0 14px rgba(0, 0, 0, 0.13);
}

.filter-options div {
    user-select: none;
    width: 100%;
    height: 32px;
    display: flex;
    justify-content: start;
    align-items: center;
    padding-left: 16px;
}
</style>