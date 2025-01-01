<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import uploadImage from '/src/assets/img/upload-video-img.svg'
import { useToast } from 'vue-toastification';

const bannerImgPreview = ref(null)
const bannerImgInput = ref(null)
const uploadBannerImage = (event) => {
    const file = event.target.files[0];
    channelInfo.banner_img = file;
    bannerImgPreview.value = URL.createObjectURL(file)
}
const removeBannerImg = () => {
    if (!confirm("Delete your image?")) {
        return;
    };
    bannerImgPreview.value = null
    channelInfo.banner_img = null
}

const profileImgPreview = ref(null)
const profilePictureInput = ref(null)
const uploadProfilePicture = (event) => {
    const file = event.target.files[0];
    channelInfo.profile_picture = file;
    profileImgPreview.value = URL.createObjectURL(file)
}
const removeProfilePicture = () => {
    if (!confirm("Delete your image?")) {
        return;
    };
    profileImgPreview.value = null
    channelInfo.profile_picture = null
}

const watermarkImgPreview = ref(null)
const channelWatermarkInput = ref(null)
const uploadChannelWatermark = (event) => {
    const file = event.target.files[0];
    channelInfo.video_watermark = file;
    watermarkImgPreview.value = URL.createObjectURL(file)
}
const removeChannelWatermark = () => {
    if (!confirm("Delete your image?")) {
        return;
    };
    watermarkImgPreview.value = null
    channelInfo.video_watermark = null
}

const formData = reactive({
    "detail": {
        "owner_id": '',
        'name': '',
        'unique_identifier': '',
        'description': '',
        'contact_email': '',
    },
    'banner_img': null,
    'profile_picture': null,
    'video_watermark': null,
})

const channelInfo = reactive({
    "detail": {
        "owner_id": '',
        'name': '',
        'unique_identifier': '',
        'description': '',
        'contact_email': '',
    },
    'banner_img': null,
    'profile_picture': null,
    'video_watermark': null,
})

const toast = useToast()
const submitForm = () => {
    print(channelInfo)
}
onMounted(() => {
    axios.get("http://127.0.0.1:8000/videos/channel/customization", {
        params: {
            "user_session_id": sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        channelInfo.detail = response.data.data
    }).catch((error) => {
        toast.error(error)
    })
})

</script>

<template>
    <div class="flex font-roboto flex-col w-full justify-start items-center pl-12 absolute
     left-[240px] top-[90px]">
        <div class="title w-full h-[55px]">
            <h1 class="text-[25px] font-semibold">Channel customization</h1>
        </div>
        <div class="flex flex-row items-center w-[1214px] mr-auto h-[48px] mt-6 border-b sticky top-0 bg-white z-40">
            <div class="z-0 flex flex-row justify-self-start mr-auto gap-x-10 text-[15px]
             font-medium">
                <div class="border-b-[3px] border-black mt-3 pb-2">
                    <button class="border-b-[3px] border-transparent ">
                        Profile
                    </button>
                </div>
            </div>
            <div class="flex flex-row justify-self-end ml-auto gap-x-2 mr-10 text-[14px] font-medium pb-2">
                <button class="w-[75px] h-[36px] bg-black text-white rounded-3xl">
                    Cancel
                </button>
                <button class="w-[75px] h-[36px] bg-[#d8d8d8] rounded-3xl">
                    Publish
                </button>
            </div>
        </div>

        <section class="flex flex-col gap-y-6 w-full mt-6">
            <div class="flex flex-col gap-y-2">
                <p class="text-[15px] font-medium">Banner image</p>
                <span class="text-[13px] font-normal">This image will appear across the top of your channel</span>
                <div class="flex flex-row gap-x-4">
                    <div class="w-[270px] h-[160px] rounded-lg bg-[#f9f9f9] z-0">
                        <img :src="bannerImgPreview" class="w-full h-full z-10" draggable="false" alt="">
                    </div>
                    <div class="flex flex-col gap-y-2">
                        <div class="max-w-[330px] h-[40px]">
                            <p class="text-[13px] text-gray-500 font-normal">For the best results on all devices, use an
                                image that’s at least 2048 x 1152 pixels and 6MB or less.
                            </p>
                        </div>
                        <input hidden @change="uploadBannerImage" ref="bannerImgInput" type="file">
                        <div class="flex flex-row gap-x-2 mt-10">
                            <button @click="bannerImgInput.click()"
                                class="w-[76px] h-[36px] rounded-3xl text-[14px] font-medium bg-[#eaeaea]">
                                Upload
                            </button>
                            <button @click="removeBannerImg"
                                class="w-[76px] h-[36px] rounded-3xl text-[14px] font-medium bg-[#eaeaea]">
                                Remove
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex flex-col gap-y-2">
                <p class="text-[15px] font-medium">Picture </p>
                <span class="text-[13px] font-normal">Your profile picture will appear where your channel is presented
                    on YouTube, like next to your videos and comments </span>
                <div class="flex flex-row gap-x-4">
                    <div class="w-[270px] h-[160px] rounded-lg bg-[#f9f9f9] flex justify-center items-center">
                        <img class="w-[140px] h-[140px] rounded-full" :src="profileImgPreview ?? uploadImage" alt="">
                    </div>
                    <div class="flex flex-col gap-y-2 h-auto">
                        <div class="max-w-[330px] h-[80px]">
                            <p class="text-[13px] text-gray-500 font-normal">It’s recommended to use a picture that’s at
                                least 98 x 98 pixels and 4MB or less. Use a PNG or GIF (no animations) file. Make sure
                                your picture follows the YouTube Community Guidelines.
                            </p>
                        </div>
                        <div class="flex flex-row gap-x-4">
                            <input hidden @change="uploadProfilePicture" ref="profilePictureInput" type="file">
                            <button @click="profilePictureInput.click()"
                                class="w-[76px] h-[36px] rounded-3xl text-[14px] font-medium bg-[#eaeaea]">
                                Change
                            </button>
                            <button @click="removeProfilePicture"
                                class="w-[76px] h-[36px] rounded-3xl text-[14px] font-medium bg-[#eaeaea]">
                                Remove
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex flex-col gap-y-2">
                <p class="text-[15px] font-medium">Name</p>
                <span class="text-[13px] font-normal">Choose a channel name that represents you and your content.
                    Changes made to your name and picture are visible only on YouTube and not other Google services. You
                    can change your name twice in 14 days. </span>
                <div class="w-[876px] h-[46px] rounded-lg border-black border pl-4 flex justify-center items-center">
                    <input v-model="channelInfo.detail.name" required placeholder="Enter your name..."
                        class="w-[844px] h-[24px] text-[15px] font-normal outline-none" type="text">
                </div>
            </div>
            <div class="flex flex-col gap-y-2">
                <p class="text-[15px] font-medium">Id</p>
                <span class="text-[13px] font-normal">Choose your unique handle by adding letters and numbers. You can
                    change your handle back within 14 days. Handles can be changed twice every 14 days. </span>
                <div
                    class="w-[876px] h-[46px] rounded-lg border-black border pl-4 flex justify-center items-center flex-row">
                    <span>@</span>
                    <input v-model="channelInfo.detail.unique_identifier" required placeholder="Enter your id"
                        class="ml-2 w-[844px] h-[24px] text-[15px] font-normal outline-none" type="text">
                </div>
                <span class="text-[13px] font-normal text-gray-500">https://www.youtube.com/@hello-q2b </span>
            </div>
            <div class="flex flex-col gap-y-2">
                <p class="text-[15px] font-medium">Description</p>
                <div class="w-[876px] h-[156px] pt-1 pl-3 rounded-lg border-black border flex justify-center items-center 
                flex-row">
                    <textarea v-model="channelInfo.detail.description"
                        class="text-[15px] font-normal w-[844px] h-[126px] outline-none"
                        placeholder="Tell viewers about your channel..."></textarea>
                </div>
            </div>
            <div class="flex flex-col gap-y-2">
                <p class="text-[15px] font-medium">Contact Info</p>
                <span class="text-[13px] font-normal">Let people know how to contact you with business inquiries. The
                    email address you enter may appear in the About section of your channel and be visible to viewers.
                </span>
                <div
                    class="w-[320px] hover:border-2 pt-1 h-[52px] rounded-lg border-black border gap-y-1 flex flex-col justify-start items-center">
                    <span class="ml-4 mr-auto text-[12px] font-medium text-gray-500">Email</span>
                    <input v-model="channelInfo.detail.contact_email" required placeholder="Email address"
                        class="w-[288px] h-[24px] text-[15px] font-normal outline-none" type="text">
                </div>
            </div>
            <div class="flex flex-col gap-y-2 mb-20">
                <p class="text-[15px] font-medium">Video watermark</p>
                <span class="text-[13px] font-normal">The watermark will appear on your videos in the right-hand corner
                    of the video player</span>
                <div class="flex flex-row gap-x-4">
                    <div class="w-[270px] h-[160px] rounded-lg bg-[#f9f9f9] flex justify-center items-center">
                        <img class="w-[140px] h-[140px] rounded-full" :src="watermarkImgPreview ?? uploadImage" alt="">
                    </div>
                    <div class="flex flex-col gap-y-2 h-auto">
                        <div class="max-w-[330px] h-[60px]">
                            <p class="text-[13px] text-gray-500 font-normal">An image that’s 150 x 150 pixels is
                                recommended. Use a PNG, GIF (no animations), BMP, or JPEG file that’s 1MB or less.
                            </p>
                        </div>
                        <div class="flex flex-row gap-x-4">
                            <input hidden @change="uploadChannelWatermark" ref="channelWatermarkInput" type="file">
                            <button @click="channelWatermarkInput.click()"
                                class="w-[76px] h-[36px] rounded-3xl text-[14px] font-medium bg-[#eaeaea]">
                                Upload
                            </button>
                            <button @click="removeChannelWatermark"
                                class="w-[76px] h-[36px] rounded-3xl text-[14px] font-medium bg-[#eaeaea]">
                                Remove
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>
<style scoped>
textarea {
    resize: none;
}
</style>