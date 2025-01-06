<script setup>
import { watch, ref } from "vue";
import { useShareLink } from "vue3-social-sharing";
import { sharedState } from "@/sharedState";
import { useToast } from "vue-toastification";

const toast = useToast()
const currentRoute = ref(window.location.href)

watch(sharedState, () => {
    const sharingTab = document.querySelector(".short-video-sharing-tab");
    sharingTab.classList.toggle("visible");
})

// Share in social media
const { shareLink } = useShareLink();
const shareFacebook = (url) => {
    shareLink({
        network: "facebook",
        url: url,
    })
}

const shareTelegram = (url) => {
    shareLink({
        network: "telegram",
        url: url,
    })
}

const shareWhatsapp = (url) => {
    shareLink({
        network: "whatsapp",
        url: url,
    })
}

const shareTwitter = (url) => {
    shareLink({
        network: "twitter",
        url: url,
    })
}

const shareEmail = (url) => {
    shareLink({
        network: "email",
        url: url,
    })
}

const copyToClipboard = (url) => {
    navigator.clipboard.writeText(url)
    toast.info("Link copied to clipboard")
}
</script>
<template>
    <div v-show="sharedState.isSharingTabOpen" class="short-video-sharing-tab flex flex-col absolute top-[29%] left-[33.5%] w-[518px] h-[264px]
    bg-white z-40 rounded-2xl custom-shadow">
        <div class='flex flex-row relative mt-4 ml-[22.5px]'>
            <p>Share</p>
            <button @click="sharedState.isSharingTabOpen = false" class="w-6 h-6 right-2 absolute">
                <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/x-mark-icon.svg" alt="">
            </button>
        </div>
        <div class="flex flex-row justify-center items-center gap-x-4 mt-4 flex-wrap">
            <div @click="shareWhatsapp(currentRoute)" class="flex flex-col justify-center items-center">
                <button class="w-[60px] h-[60px]">
                    <img class="w-[100%] h-[100%] rounded-full" src="@/assets/icons/svg-icons/whatsapp-icon.svg" alt="">
                </button>
                <span class="text-center">Whatsapp</span>
            </div>
            <div @click="shareTwitter(currentRoute)" class="flex flex-col justify-center items-center">
                <button class="w-[60px] h-[60px]">
                    <img class="w-[100%] h-[100%] rounded-full" src="@/assets/icons/svg-icons/twitter-icon.svg" alt="">
                </button>
                <span>Twitter</span>
            </div>
            <div @click="shareFacebook(currentRoute)" class="flex flex-col justify-center items-center">
                <button class="w-[60px] h-[60px]">
                    <img class="w-[100%] h-[100%] rounded-full" src="@/assets/icons/svg-icons/facebook-icon.svg" alt="">
                </button>
                <span>Facebook</span>
            </div>
            <div @click="shareEmail(currentRoute)" class="flex flex-col justify-center items-center">
                <button class="w-[60px] h-[60px]">
                    <img class="w-[100%] h-[100%] rounded-full" src="@/assets/icons/svg-icons/email-round-icon.svg"
                        alt="">
                </button>
                <span>Email</span>
            </div>
            <div @click="shareTelegram(currentRoute)" class="flex flex-col justify-center items-center">
                <button class="w-[60px] h-[60px]">
                    <img class="w-[100%] h-[100%] rounded-full" src="@/assets/icons/svg-icons/telegram-icon.svg" alt="">
                </button>
                <span>Telegram</span>
            </div>
        </div>
        <div
            class="share-bar flex flex-row mt-[35px] ml-[22.5px] w-[470px] h-[53.6px] pl-4 justify-start items-center rounded-lg border-black border-2">
            <input readonly type="text" :value="currentRoute" class="bg-white min-w-[360px] h-[19.6px] outline-none">
            <button @click="copyToClipboard(currentRoute)" class="w-[63px] h-[36px] text-sm font-medium text-white
            bg-[#065fd4] hover:bg-[#0556bf] rounded-3xl">Copy</button>
        </div>
    </div>
</template>