<script setup>
import { ref, reactive } from 'vue';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';


// Handling Infinite Scrolling
const videos = reactive([])
let page = ref(1)

const generateVideos = (page_number) => {
    for (let i = 0; i < page_number * 10; i++) {
        videos.push({ id: i, title: `${i} Video` })
    }
}

let isLoading = ref(false)
const loadMore = () => {
    isLoading.value = true
    setTimeout(function () {
        page.value += 1, generateVideos(page.value), isLoading.value = false
    }, 2000)
}

const checkScroll = () => {
    document.addEventListener("scroll", () => {
        const endOfPage = window.innerHeight + window.scrollY > document.documentElement.scrollHeight - 200
        console.log(isLoading.value)
        if (endOfPage && !isLoading.value) {
            loadMore()
        }
    })
}

generateVideos(page.value)
checkScroll()
</script>

<template>
    <div id="videosDivision">
        <div class="flex flex-col mt-4">
            <div class="flex flex-row">
                <button class="active w-[63px] h-[32px]">Latest</button>
                <button class="w-[72.5px] h-[32px]">Popular</button>
                <button class="w-[64.5px] h-[32px]">Oldest</button>
            </div>
            <div id="infinite-scroll-division" class="flex flex-row flex-wrap mt-4 gap-x-4 gap-y-8">
                <div v-for="video in videos" :key="video.id" class="flex flex-col">
                    <div class="relative">
                        <img class="w-[251px] h-[141px] rounded-2xl" src="@/assets/img/Django.png" alt="">
                        <span class="bg-opacity-80 w-10 h-4 rounded-md absolute bottom-2 right-2
                             font-medium text-xs bg-black text-white
                             flex justify-center items-center">
                            12:12
                        </span>
                    </div>
                    <p class="text-sm font-medium mt-3 mb-2">
                        {{ video.title }}
                    </p>
                    <div class="flex flex-row text-xs font-normal text-gray-600">
                        <span>73K views&nbsp;</span>
                        <span>6 days ago&nbsp;</span>
                    </div>
                </div>
            </div>
            <PulseLoader v-if="isLoading" :color="['red']" class="mt-10 mb-5"></PulseLoader>
        </div>
    </div>
</template>