<script setup>
import { ref, defineProps } from 'vue';
import subtitleIcon from '/src/assets/icons/svg-icons/subtitle-icon-3.svg'

const props = defineProps({
    formData: Object
});

// Uploading the subtitle File
const subtitleFileInput = ref(null) // Opening the subtitle input (file type)
const uploadSubtitleFile = (event) => {
    props.formData.subtitleFile = event.target.files[0]
}
</script>

<template>
    <div class="w-full h-auto flex flex-col pl-[50px]">
        <div class="flex flex-col text-[25px] font-semibold mt-2">
            <p class="text-left">Video elements</p>
        </div>
        <div class="video-elements">
            <div
                class="flex flex-row w-[864px] h-[88px] justify-start items-center gap-x-6 mt-4 pl-10 bg-[#f9f9f9] rounded-2xl">
                <div class="flex justify-center items-center">
                    <img class="w-[24px] h-[24px]" :src="subtitleIcon" alt="">
                </div>
                <div class="flex flex-col gap-y-[1px] justify-start items-start px-4">
                    <h3 class="text-[20px] font-medium">Add Subtitle</h3>
                    <p class="text-[13px] font-normal text-gray-500">Reach a broader audience by adding subtitles to
                        your video</p>
                    <h1 class="font-bold text-[14px]">Subtitle source: {{ props.formData.subtitleFile || 'Nothing yet' }}</h1>
                </div>
                <div class="justify-self-end ml-auto mr-4">
                    <button @click="subtitleFileInput.click()" class="w-[57.1px] h-[36px] rounded-3xl text-[14px] font-medium bg-[#ececec]
                     text-black">
                        Add
                    </button>
                    <input @change="uploadSubtitleFile" ref="subtitleFileInput" class="hidden" type="file">
                </div>
            </div>
        </div>
    </div>
</template>