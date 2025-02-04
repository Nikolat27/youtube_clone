<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from "axios";
import { useToast } from 'vue-toastification';
import { sharedState } from '@/sharedState';

const toast = useToast()
const router1 = useRoute();
const router2 = useRouter();
const isRegisterShown = ref(router1.query.mode === 'register' || !router1.query.mode);
const toggleRegisterShowing = () => isRegisterShown.value = !isRegisterShown.value

// Handle Sign in Form
const loginUsername = ref('')
const loginPassword = ref('')
const submitLoginForm = (event) => {
    event.preventDefault(); // For preventing the page from refreshing
    axios.post(`${sharedState.websiteUrl}/users/login`, {
        username: loginUsername.value,
        password: loginPassword.value,

    }, {
        params: {
            user_session_id: sessionStorage.getItem('user_session_id')
        }
    }).then((response) => {
        const userSessionId = response.data.user_session_id;
        sessionStorage.setItem('user_session_id', userSessionId);
        router2.go(-1)
    }, (error) => {
        console.log(error)
    })
}


// Handle Register Form
const registerUsername = ref('')
const registerEmail = ref('')
const registerPassword = ref('')
const registerPassword2 = ref('')

const submitRegisterForm = async (event) => {
    event.preventDefault(); // To prevent the page from refreshing
    await axios.post(`${sharedState.websiteUrl}/users/register`, {
        username: registerUsername.value,
        email: registerEmail.value,
        password1: registerPassword.value,
        password2: registerPassword2.value,
    }).then((response) => {
        if (response.status == 201) {
            toast.success("User account successfully created!")
        }
    }, (error) => console.log(error));
}

// Change the browsers title
watch(() => isRegisterShown.value, () => {
    isRegisterShown.value ? document.title = "Register" : document.title = "Login"
})

onMounted(() => {
    document.title = "Register"
})
</script>

<template>
    <form v-if="!isRegisterShown" @submit="submitLoginForm">
        <div class="mx-auto mt-20 shadow-inner flex flex-col h-[600px] w-[300px] justify-center items-center
        gap-y-4 sign-up-container border-2 rounded-lg">
            <img draggable="false" src="@/assets/icons/svg-icons/youtube-tv-icon.svg" class="w-30 h-20 mb-7 mt-[-100px]"
                alt="">
            <p class="mb-7 mt-[-15px] text-2xl">Sign in</p>
            <input type="text" placeholder="Username" v-model="loginUsername">
            <input type="password" placeholder="Password" v-model="loginPassword">
            <button type="submit" class="bg-red-600 text-white w-24 h-9 text-center rounded-lg shadow-lg">Log
                in</button>
            <a @click="toggleRegisterShowing" class="cursor-pointer">
                <p class="text-blue-700 italic">Don`t have an Account? <span class="underline">Sign up</span></p>
            </a>
            <router-link to="/">
                <p class="text-blue-800 italic">Home <span class="underline">Page</span></p>
            </router-link>
        </div>
    </form>

    <form v-else @submit="submitRegisterForm">
        <div class="mx-auto shadow-inner flex flex-col mt-20 h-[600px] w-[300px] justify-center items-center
         align-top gap-y-4 sign-up-container border-2 rounded-lg">
            <img draggable="false" src="@/assets/icons/svg-icons/youtube-tv-icon.svg" class="w-30 h-20 mb-5" alt="">
            <p class="mb-[50px] mt-[-15px] text-2xl">Register</p>
            <input class="hover:border-2 hover:border-red" type="text" placeholder="Username"
                v-model="registerUsername">
            <input type="email" placeholder="Email" v-model="registerEmail">
            <input type="password" placeholder="Password" v-model="registerPassword">
            <input type="password" placeholder="Repeat Password" v-model="registerPassword2">
            <button class="bg-red-600 text-white w-24 h-9 text-center rounded-lg shadow-lg">Register</button>
            <a @click="toggleRegisterShowing" class="cursor-pointer">
                <p class="text-blue-700 italic">Already have an account? <span class="underline">Sign in</span></p>
            </a>
            <router-link to="/">
                <p class="text-blue-800 italic">Home <span class="underline">Page</span></p>
            </router-link>
        </div>
    </form>
</template>