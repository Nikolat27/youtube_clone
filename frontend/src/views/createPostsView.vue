<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

// Icons
import randomPic from '/src/assets/img/Django.png'
import imageIcon from '/src/assets/img/image-icon.svg'

const postImage = ref(null)
const imageSrc = ref(null)
const uploadPostImage = (event) => {
    const file = event.target.files[0]
    imageSrc.value = file ? URL.createObjectURL(file) : null
}

const goBack = () => {
    router.go(-1);
}

onMounted(() => {
    // post page is just for authenticated Users
    axios.get("http://localhost:8000/users/is_authenticated", {
        params: {
            user_session_id: sessionStorage.getItem("user_session_id")
        }
    }).then((response) => {
        if (!response.data) router.push({ name: 'auth' });
    })
})
</script>

<template>
    <div class="w-[852px] min-h-[162.6px] h-auto rounded-2xl justify items-center border flex flex-col gap-y-2
     absolute left-[240px] top-[90px] font-roboto pt-4 pl-2">
        <div class="flex flex-row justify-self-start mr-auto ml-2 gap-x-2">
            <img class="w-[25px] h-[25px] rounded-full" :src="randomPic" alt="">
            <p>Username</p>
        </div>
        <div>
            <img v-if="imageSrc" class="w-[400px] h-[400px] self-center mx-auto my-4" :src="imageSrc" alt="">
            <input @change="uploadPostImage" ref="postImage" class="hidden" type="file">
            <input placeholder="Your community text... (max 200 characters)" maxlength="200"
                class="text-[16px] self-center mt-4 font-normal outline-none w-[818px] h-[20px]" type="text">
        </div>
        <div class="flex flex-row w-full mt-6">
            <div>
                <button @click="postImage.click()" class="w-[95px] h-[36px] rounded-3xl flex justify-center items-center gap-x-2
                 hover:bg-[#e5e5e5]">
                    <img class="w-[20px] h-[20px]" :src="imageIcon" alt="">
                    <p>Image</p>
                </button>
            </div>
            <div class="flex flex-row gap-x-2 text-[15px] font-medium items-end justify-self-end ml-auto mr-2 mb-4">
                <button @click="goBack" class="w-[74.9px] h-[36px] rounded-3xl bg-white text-black hover:bg-[#e5e5e5]">
                    Cancel
                </button>
                <button class="w-[74.9px] h-[36px] rounded-3xl bg-blue-600 text-white hover:bg-blue-700">
                    Post
                </button>
            </div>
        </div>
    </div>
</template>