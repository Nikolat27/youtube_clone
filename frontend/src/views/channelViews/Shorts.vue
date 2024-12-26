<script setup>
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';

const router = useRoute();
let page = ref(1)
let isLoading = ref(false)
const shorts = reactive([])

const generateTestVideos = (page_number) => {
    for (let i = page_number * 12 - 12; i < page_number * 12; i++) {
        shorts.push({ id: `${i}`, title: `${i} Short Video` })
    }
}

const scrollMore = () => {
    isLoading.value = true;
    setTimeout(() => {
        page.value += 1;
        generateTestVideos(page.value);
        isLoading.value = false;
    }, 2000)
}

const checkScroll = () => {
    const endOfPage = window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 200;
    if (endOfPage && !isLoading.value) {
        scrollMore()
    }
}

onMounted(() => {
    generateTestVideos(page.value)
    document.addEventListener("scroll", checkScroll)
})

// Cleanup on unmount
onUnmounted(() => {
    window.removeEventListener('scroll', checkScroll);
});

watch(() => router.query.sortBy, () => {
})

const autoScrollTop = () => {
    window.scrollTo({
        top: 450,
        left: 0,
        behavior: 'smooth',
    });
}
</script>
<template>
    <div id="shortsDivision">
        <div class="flex flex-col mt-4">
            <div class="flex flex-row">
                <router-link :to="'/channel-page/shorts?sortBy=latest'"><button
                        :class="[!router.query.sortBy || router.query.sortBy === 'latest' ? 'active' : '', 'w-[63px]', 'h-[32px]']">Latest</button></router-link>
                <router-link :to="'/channel-page/shorts?sortBy=popular'"><button
                        :class="[router.query.sortBy === 'popular' ? 'active' : '', 'w-[63px]', 'h-[32px]']">Popular</button></router-link>
                <router-link :to="'/channel-page/shorts?sortBy=oldest'"><button
                        :class="[router.query.sortBy === 'oldest' ? 'active' : '', 'w-[63px]', 'h-[32px]']">Oldest</button></router-link>
            </div>
            <div class="flex flex-row flex-wrap mt-4 gap-y-5 gap-x-2 w-[1100px]">
                <div v-for="short in shorts" :key="short.id" class="flex flex-col">
                    <img class="w-[209.98px] h-[372.37px] rounded-2xl" src="@/assets/img/Django.png" alt="">
                    <p class="text-base font-medium mt-2 mb-0">
                        {{ short.title }}
                    </p>
                    <span class="text-sm font-normal text-gray-600">73K views&nbsp;</span>
                </div>
            </div>
            <PulseLoader v-if="isLoading" color="red" class="mt-10"></PulseLoader>
        </div>
    </div>
</template>