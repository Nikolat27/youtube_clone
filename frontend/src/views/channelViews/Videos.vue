<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, watch, computed } from 'vue';
import { useRoute } from 'vue-router';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';

// Handling Infinite Scrolling
const router = reactive(useRoute())
const videos = reactive([])
let page = ref(1)
let isLoading = ref(true)

const generateVideos = (page_number) => {
    for (let i = (page_number * 10 - 10); i < page_number * 10; i++) {
        videos.push({ id: i, title: `${i} Video`, views: Math.floor(Math.random() * 100000), date: new Date(Date.now() - Math.random() * 10000000000) });
    }
};

const loadMore = () => {
    if (isLoading.value) return;
    isLoading.value = true
    setTimeout(function () {
        page.value += 1, generateVideos(page.value), isLoading.value = false
    }, 500)
}

const checkScroll = () => {
    const handleScroll = () => {
        const endOfPage = window.innerHeight + window.scrollY > document.documentElement.scrollHeight - 200
        if (endOfPage && !isLoading.value) {
            loadMore()
        }
    }
    document.addEventListener("scroll", handleScroll)

    onBeforeUnmount(() => {
        document.removeEventListener("scroll", handleScroll);
    });
}


onMounted(() => {
    setTimeout(function () {
        generateVideos(page.value);
        checkScroll();
        isLoading.value = false
    }, 1000);
})

// Computed property to sort videos
const sortedVideos = computed(() => {
    let sorted = videos;
    const sortBy = router.query.sortBy;
    if (sortBy === 'latest') {
        sorted.sort((a, b) => b.date - a.date);
    } else if (sortBy === 'popular') {
        sorted.sort((a, b) => b.views - a.views);
    } else if (sortBy === 'oldest') {
        sorted.sort((a, b) => a.date - b.date);
    }

    return sorted;
});

watch(() => router.query.sortBy, () => {
    videos.splice(0, videos.length); // Clear the videos array
    page.value = 1; // Reset page
    generateVideos(page.value); // Regenerate videos based on the new sortBy
})
</script>

<template>
    <div id="videosDivision">
        <div class="flex flex-col mt-4">
            <div class="flex flex-row">
                <router-link :to="'/channel-page/videos?sortBy=latest'"><button
                        :class="[!router.query.sortBy || router.query.sortBy === 'latest' ? 'active' : '', 'w-[63px]', 'h-[32px]']">Latest</button></router-link>
                <router-link :to="'/channel-page/videos?sortBy=popular'"><button
                        :class="[router.query.sortBy === 'popular' ? 'active' : '', 'w-[63px]', 'h-[32px]']">Popular</button></router-link>
                <router-link :to="'/channel-page/videos?sortBy=oldest'"><button
                        :class="[router.query.sortBy === 'oldest' ? 'active' : '', 'w-[63px]', 'h-[32px]']">Oldest</button></router-link>
            </div>
            <div id="infinite-scroll-division" class="flex flex-row flex-wrap mt-4 gap-x-4 gap-y-8">
                <div v-for="video in sortedVideos" :key="video.id" class="flex flex-col">
                    <div class="relative">
                        <img loading="lazy" class="w-[251px] h-[141px] rounded-2xl" src="@/assets/img/Django.png"
                            alt="">
                        <span
                            class="bg-opacity-80 w-10 h-4 rounded-md absolute bottom-2 right-2 font-medium text-xs bg-black text-white flex justify-center items-center">
                            12:12
                        </span>
                    </div>
                    <p class="text-sm font-medium mt-3 mb-2">
                        {{ video.title }}
                    </p>
                    <div class="flex flex-row text-xs font-normal text-gray-600">
                        <span>{{ video.views }} views&nbsp;</span>
                        <span>{{ new Date(video.date).toLocaleDateString() }}&nbsp;</span>
                    </div>
                </div>
            </div>
            <PulseLoader v-if="isLoading" :color="['red']" class="mt-10 mb-5" draggable="false"></PulseLoader>
        </div>
    </div>
</template>