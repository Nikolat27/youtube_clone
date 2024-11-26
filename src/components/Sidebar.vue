<script setup>
import { ref, reactive, computed } from 'vue';
import { RouterLink } from 'vue-router';

const items = reactive([{ title: "1" }, { title: "2" }, { title: "3" }, { title: "4" }])
let maxChannelShown = ref(1);
let isCollapsed = computed(() => maxChannelShown.value === 1) // if value == 1 then collapsed is True

const toggleSubscriptionChannels = () => {
    maxChannelShown.value = isCollapsed.value ? 10 : 1;
};
</script>

<template>
    <aside class="side-bar-div">
        <div class="side-bar-links">
            <img src="@/assets/icons/side-bar/youtube-home.png" alt="">
            <p>Home</p>
        </div>
        <div class="side-bar-links">
            <img src="@/assets/icons/side-bar/youtube-shorts.jpg" alt="">
            <p>Shorts</p>
        </div>
        <div class="side-bar-links">
            <img src="@/assets/icons/side-bar/subscription.png" alt="">
            <p>Subscriptions</p>
        </div>

        <div class="side-bar-links">
            <p><span style="font-family: Roboto, Arial; font-size: 16px; font-weight: bold;">You ></span></p>
        </div>
        <div class="side-bar-links">
            <img src="@/assets/icons/side-bar/history-utube.png" alt="">
            <p>History</p>
        </div>
        <div class="side-bar-links">
            <a class="side-bar-links-link">
                <img src="@/assets/icons/side-bar/youtube_playlist_icon.png" alt="">
                <p>Playlists</p>
            </a>
        </div>
        <div class="side-bar-links">
            <img src="@/assets/icons/side-bar/your-videos.png" alt="">
            <p>Your videos</p>
        </div>
        <div class="side-bar-links">
            <img src="@/assets/icons/side-bar/watch-later.webp" alt="">
            <p>Watch Later</p>
        </div>
        <div class="side-bar-links">
            <img src="@/assets\icons\svg-icons\like-empty.svg" alt="">
            <p>Liked</p>
        </div>

        <div class="side-bar-links">
            <p>Subscriptions</p>
        </div>

        <transition-group name="slide-down">
            <div v-for="(channel, index) in items.slice(0, maxChannelShown)" :key="index"
                class="side-bar-links subscriptions-div">
                <img style="border-radius: 50%;" src="@/assets/img/Django.png" alt="">
                <p>{{ channel.title }}</p>
            </div>
        </transition-group>

        <div class="side-bar-links">
            <p style="font-size: 26px;">></p>
            <button @click="toggleSubscriptionChannels" id="show-more-btn">{{ isCollapsed ? 'Show more' : 'Show less'
                }}</button>
        </div>
    </aside>
</template>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
    transition: all 0.5s ease-in-out;
}

.slide-down-enter-from,
.slide-down-leave-to {
    opacity: 1;
    transform: translateY(-20px);
}
</style>