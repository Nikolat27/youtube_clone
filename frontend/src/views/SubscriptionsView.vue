<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue';
// import PulseLoader from 'vue-spinner/src/MoonLoader.vue';


const data = ref([]);
for (let i = 0; i <= 30; i++) {
    data.value.push({ id: i, title: "Hello World" });
}

let page = 1;
const loading = ref(false);

const loadMoreVideos = async () => {
    if (loading.value) return; // Prevent multiple loads
    loading.value = true;

    try {
        await new Promise(resolve => setTimeout(resolve, 600)); // Delay
        const id = data.value.length;
        data.value.push({ id, title: "More Hello World" }); // Add new data
        page += 1; // Increment the page number
    } catch (error) {
        console.error("Error fetching videos: ", error);
    } finally {
        loading.value = false; // End loading
    }
};


const checkScroll = () => {
    // Check if we've scrolled to the bottom (we only render more contents if we reach to the End)
    const endOfPage = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 450;
    if (endOfPage && !loading.value) {
        console.log("Load more Contents")
        loadMoreVideos();
    }
};

onMounted(() => {
    window.addEventListener('scroll', checkScroll);
});

onBeforeUnmount(() => {
    window.removeEventListener('scroll', checkScroll);
});
</script>

<template>
    <div class="flex flex-col absolute left-[240px] top-[80px]">
        <p class="text-lg font-bold mb-4">Latest</p>
        <div class="videoContainer flex flex-row flex-wrap gap-x-4 gap-y-12">
            <div v-for="video in data.slice(0, 6)" :key="video.id"
                class="subscription-video flex flex-col gap-y-4 cursor-pointer">
                <div class="video-tag w-[400px] h-[224px] relative">
                    <video class="w-[100%] h-[100%] object-fill rounded-2xl" src="@/assets/video/test-vid.mp4"></video>
                    <div
                        class="video-duration bg-black h-6 w-12 flex justify-center items-center rounded-md absolute bottom-2 right-2">
                        <p class="text-white text-center font-[650] text-[12px]">14:20</p>
                    </div>
                </div>
                <div class="flex flex-row gap-x-4">
                    <div class="w-9 h-9">
                        <img class="w-[100%] h-[100%] rounded-full" src="@/assets/img/Django.png" alt="">
                    </div>
                    <div class="flex flex-col">
                        <p class="text-base font-medium">{{ video.title }} / {{ video.id }}</p>
                        <p class="text-sm font-normal text-[#99a4a5]">Channel name</p>
                        <p class="text-sm font-normal text-[#99a4a5]">711K views . 1 hour ago</p>
                    </div>
                </div>
            </div>
        </div>
        <hr class="my-10">
        <div class="videoContainer flex flex-row flex-wrap gap-x-4 gap-y-12">
            <div v-for="video in data.slice(6)" :key="video.id"
                class="subscription-video flex flex-col gap-y-4 cursor-pointer">
                <div class="video-tag w-[400px] h-[224px] relative">
                    <video class="w-[100%] h-[100%] object-fill rounded-2xl" src="@/assets/video/test-vid.mp4"></video>
                    <div
                        class="video-duration bg-black h-6 w-12 flex justify-center items-center rounded-md absolute bottom-2 right-2">
                        <p class="text-white text-center font-[650] text-[12px]">14:20</p>
                    </div>
                </div>
                <div class="flex flex-row gap-x-4">
                    <div class="w-9 h-9">
                        <img class="w-[100%] h-[100%] rounded-full" src="@/assets/img/Django.png" alt="">
                    </div>
                    <div class="flex flex-col">
                        <p class="text-base font-medium">{{ video.title }} / {{ video.id }}</p>
                        <p class="text-sm font-normal text-[#99a4a5]">Channel name</p>
                        <p class="text-sm font-normal text-[#99a4a5]">711K views . 1 hour ago</p>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="loading" class="mt-[60px] pb-20 text-center flex justify-center items-center">
            <ScaleLoader :color="['#df0d3b']" :width="['5px']" :height="['37.5px']" />
        </div>
    </div>
</template>