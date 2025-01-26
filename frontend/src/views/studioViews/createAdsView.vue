<script setup>
import { ref, reactive } from 'vue';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import axios from 'axios';
import uploadImage from '/src/assets/img/upload-video-img.svg' // Default preview image for tags
import { useToast } from 'vue-toastification';

const cancelPublishing = () => location.reload()

const companyImgPreview = ref(null)
const companyImgInput = ref(null)
const uploadCompanyProfile = (event) => {
    const file = event.target.files[0];
    adInfo.company_picture_url = file
    companyImgPreview.value = URL.createObjectURL(file)
}


const videoKey = ref(0)
const adVideoPreview = ref(null)
const adVideoInput = ref(null)
const uploadAdVideo = (event) => {
    const file = event.target.files[0];
    adInfo.file_url = file;
    adVideoPreview.value = URL.createObjectURL(file)
    videoKey.value += 1
}


const adInfo = reactive({
    title: '',
    company_contact_url: '',
    company_picture_url: '',
    file_url: ''
})


const isLoading = ref(false)
const toast = useToast()
const submitForm = () => {
    const submitFormData = new FormData()

    submitFormData.append("user_session_id", sessionStorage.getItem("user_session_id"))
    submitFormData.append('ad_title', adInfo.title)
    submitFormData.append('company_contact_url', adInfo.company_contact_url)
    submitFormData.append('company_picture_file', adInfo.company_picture_url)
    submitFormData.append('ad_video_file', adInfo.file_url)

    axios.post("http://127.0.0.1:8000/videos/create-ad", submitFormData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }).then((response) => {
        if (response.status == 201) {
            toast.success("Ad created successfully!")
            for (let key in adInfo) {
                adInfo[key] = '';
            }
        }
    }).catch((error) => {
        toast.error(error)
    })
}
</script>

<template>
    <div class="flex font-roboto flex-col w-full h-full justify-start items-center pl-12 absolute
     left-[240px] top-[90px]">
        <div class="title w-full h-[55px]">
            <h1 class="text-[25px] font-semibold">Create your Ads</h1>
        </div>
        <div class="flex flex-row items-center w-[1214px] mr-auto h-[48px] mt-6 border-b sticky top-0 bg-white z-40">
            <div class="z-0 flex flex-row justify-self-start mr-auto gap-x-10 text-[15px]
             font-medium">
                <div class="border-b-[3px] border-black mt-3 pb-2">
                    <button class="border-b-[3px] border-transparent ">
                        Detail
                    </button>
                </div>
            </div>
            <div class="flex flex-row justify-self-end ml-auto gap-x-2 mr-10 text-[14px] font-medium pb-2">
                <button @click="cancelPublishing" class="w-[75px] h-[36px] bg-black text-white rounded-3xl">
                    Cancel
                </button>
                <button @click="submitForm" class="w-[75px] h-[36px] bg-[#d8d8d8] rounded-3xl">
                    Publish
                </button>
            </div>
        </div>

        <section v-if="!isLoading" class="flex flex-col gap-y-6 w-full mt-6">
            <div class="flex flex-col gap-y-2 mb-4">
                <p class="text-[15px] font-medium">Ad title</p>
                <span class="text-[13px] font-normal">Pls enter an appropriate title for you add (maximum 100
                    chars)</span>
                <div class="w-[876px] h-[46px] rounded-lg border-black border pl-4 flex justify-center items-center">
                    <input v-model="adInfo.title" required placeholder="Enter title..."
                        class="w-[844px] h-[24px] text-[15px] font-normal outline-none" type="text">
                </div>
            </div>
            <div class="flex flex-col gap-y-2 mb-20">
                <p class="text-[15px] font-medium">Company Profile Picture</p>
                <span class="text-[13px] font-normal">This image will appear across your ad in the video as the
                    companies
                    profile</span>
                <div class="flex flex-row gap-x-4">
                    <div class="w-[270px] h-[160px] rounded-lg bg-[#f9f9f9] flex justify-center items-center">
                        <img class="w-[140px] h-[140px] rounded-full" :src="companyImgPreview ?? uploadImage" alt="">
                    </div>
                    <div class="flex flex-col gap-y-2 h-auto">
                        <div class="max-w-[330px] h-[60px]">
                            <p class="text-[13px] text-gray-500 font-normal">An image that’s 150 x 150 pixels is
                                recommended. Use a PNG, GIF (no animations), BMP, or JPEG file that’s 1MB or less.
                            </p>
                        </div>
                        <div class="flex flex-row gap-x-4">
                            <input hidden @change="uploadCompanyProfile" ref="companyImgInput" type="file">
                            <button @click="companyImgInput.click()"
                                class="w-[76px] h-[36px] rounded-3xl text-[14px] font-medium bg-[#eaeaea]">
                                Upload
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex flex-col gap-y-2">
                <p class="text-[15px] font-medium">Ads Video </p>
                <span class="text-[13px] font-normal">The actual Ad that will play before or between a video</span>
                <div class="flex flex-row gap-x-4">
                    <div @click="playVideo"
                        class="w-[270px] h-[160px] rounded-lg bg-[#f9f9f9] flex justify-center items-center">
                        <video v-if="adVideoPreview" :src="adVideoPreview" :key="videoKey"></video>
                    </div>
                    <div class="flex flex-col gap-y-2 h-auto">
                        <div class="max-w-[330px] h-[20px]">
                            <p class="text-[13px] text-gray-500 font-normal">Upload a maximum 2 minute video
                            </p>
                        </div>
                        <div class="flex flex-row gap-x-4">
                            <input hidden @change="uploadAdVideo" ref="adVideoInput" type="file">
                            <button @click="adVideoInput.click()"
                                class="w-auto px-4 h-[36px] rounded-3xl text-[14px] font-medium bg-[#eaeaea]">
                                Upload Video
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex flex-col gap-y-2 mb-24">
                <p class="text-[15px] font-medium">Copmany contact url</p>
                <span class="text-[13px] font-normal">Pls put a website url</span>
                <div class="w-[876px] h-[46px] rounded-lg border-black border pl-4 flex justify-center items-center">
                    <input v-model="adInfo.company_contact_url" required placeholder="Enter your url"
                        class="w-[844px] h-[24px] text-[15px] font-normal outline-none" type="text">
                </div>
            </div>
        </section>
        <div v-else class="h-full w-full mr-[200px] mb-[100px] flex justify-center items-center">
            <PulseLoader color="red" size="22px"></PulseLoader>
        </div>
    </div>
</template>
