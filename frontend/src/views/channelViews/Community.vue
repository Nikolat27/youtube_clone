<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import axios from 'axios';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue';
import { sharedState } from '@/sharedState';

const toast = useToast()
const props = defineProps({
    channelInfo: Object
})

// Icons
import fillLikeIcon from '/src/assets/icons/svg-icons/like-fill.svg';
import emptyLikeIcon from '/src/assets/icons/svg-icons/like-empty.svg';

import fillDislikeIcon from '/src/assets/icons/svg-icons/dislike-fill.svg';
import emptyDislikeIcon from '/src/assets/icons/svg-icons/dislike-empty.svg';


let isLoading = ref(false)
const communities = reactive([])

const retrieveCommunities = (channelId) => {
    axios.get(`${sharedState.websiteUrl}/channel/${channelId}/communities`, {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (response.status == 200) {
            communities.push(...response.data.data)
        }
    }).catch((error) => console.log(error))
}


const likeCommunity = (communityId, action) => {
    let action_type = action === "like" ? true : false
    let user_session_id = sessionStorage.getItem("user_session_id")
    axios.get(`${sharedState.websiteUrl}/channel/like/${communityId}/${action_type}/${user_session_id}`).then((response) => {
        if (response.status == 201) { // true, false, null
            communities.find(community => community.id === communityId).total_likes = response.data.total_likes
            communities.find(community => community.id === communityId).is_liked = response.data.data
        }
    }).catch((error) => toast.error(error))
}

const router = useRoute()
onMounted(() => {
    const channelId = router.params.id
    retrieveCommunities(channelId)
})
</script>

<template>
    <div id="communityDivision">
        <div class="flex flex-col mt-20 gap-y-4">
            <div v-for="(community, index) in communities" :key="index" class="w-[852px] h-[777px] rounded-2xl flex flex-row pt-4 pl-4
                 border-[1px] border-[#ebebeb]">
                <a href="#" class="mr-4">
                    <img class="w-10 h-10 rounded-full" :src="props.channelInfo.profile_url" alt="">
                </a>
                <div class="flex flex-col">
                    <div class="flex flex-row gap-x-2 text-[13px]">
                        <a href="#" class="font-medium">{{ channelInfo.name }}</a>
                        <span class="font-normal">1 days ago</span>
                    </div>
                    <p class="text-lg font-normal">{{ community.title }}</p>
                    <img class="w-[638px] h-[638px] rounded-xl mt-1" :src="community.image_url" alt="">
                    <div class="flex flex-row mt-3 items-center">
                        <button @click="likeCommunity(community.id, 'like')"
                            class="w-8 h-8 rounded-full hover:bg-[#e5e5e5] flex justify-center items-center">
                            <img class="w-[75%] h-[75%]"
                                :src="community.is_liked === true ? fillLikeIcon : emptyLikeIcon" alt="">
                        </button>
                        <span class="text-xs font-normal">{{ community.total_likes }}</span>
                        <button @click="likeCommunity(community.id, 'dislike')"
                            class="ml-2 w-8 h-8 rounded-full hover:bg-[#e5e5e5] flex justify-center items-center">
                            <img class="w-[75%] h-[75%]"
                                :src="community.is_liked === false ? fillDislikeIcon : emptyDislikeIcon" alt="">
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="isLoading" class="flex justify-center items-center mt-14 mb-20">
            <ClipLoader size="45px" color="red"></ClipLoader>
        </div>
    </div>
</template>