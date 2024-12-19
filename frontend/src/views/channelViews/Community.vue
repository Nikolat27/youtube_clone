<script setup>
import { ref, reactive, onMounted } from 'vue';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue';

let page = ref(1)
let isLoading = ref(false)
const communities = reactive([])

const generateTestCommunities = (page_number) => {
    // 5 here indicates the total shown items in a single page
    for (let i = page_number * 5 - 4; i <= page_number * 5; i++) {
        communities.push({ id: i, title: `${i} Community title` })
    }
}

const scrollMore = () => {
    isLoading.value = true
    setTimeout(() => {
        page.value += 1
        generateTestCommunities(page.value)
        isLoading.value = false
    }, 2000)
}

const checkScroll = () => {
    const endOfPage = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 200
    if (endOfPage && !isLoading.value) {
        scrollMore()
    }
}

onMounted(() => {
    generateTestCommunities(page.value)
    document.addEventListener("scroll", checkScroll);
})
</script>

<template>
    <div id="communityDivision">
        <div class="flex flex-col mt-20 gap-y-4">
            <div v-for="community in communities" :key="community.id" class="w-[852px] h-[777px] rounded-2xl flex flex-row pt-4 pl-4
                 border-[1px] border-[#ebebeb]">
                <a href="#" class="mr-4">
                    <img class="w-10 h-10 rounded-full" src="@/assets/img/Django.png" alt="">
                </a>
                <div class="flex flex-col">
                    <div class="flex flex-row gap-x-2 text-[13px]">
                        <a href="#" class="font-medium">Django Tutorial Channel</a>
                        <span class="font-normal">10 hours ago</span>
                    </div>
                    <p class="text-lg font-normal">{{ community.title }}</p>
                    <img class="w-[638px] h-[638px] rounded-xl mt-1" src="@/assets/img/Django.png" alt="">
                    <div class="flex flex-row mt-3 items-center">
                        <button class="w-8 h-8 rounded-full hover:bg-[#e5e5e5] flex justify-center items-center">
                            <img class="w-[75%] h-[75%]" src="@/assets/icons/svg-icons/like-empty.svg" alt="">
                        </button>
                        <span class="text-xs font-normal">385</span>
                        <button class="ml-2 w-8 h-8 rounded-full hover:bg-[#e5e5e5] flex justify-center items-center">
                            <img class="w-[75%] h-[75%]" src="@/assets/icons/svg-icons/dislike-empty.svg" alt="">
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