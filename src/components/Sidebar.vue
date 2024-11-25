<script setup>
import { ref, watch } from 'vue';
import { RouterLink } from 'vue-router';

const items = ref([{ title: "1" }, { title: "2" }, { title: "3" }, { title: "4" }])
let maxChannelShown = ref(1);
let isCollapsed = ref(false)

function subscriptionChannelShown() {
    isCollapsed.value = !isCollapsed.value;
    if (isCollapsed.value) {
        maxChannelShown.value = 10;
    }
    else {
        maxChannelShown.value = 1;
    }
}

watch(maxChannelShown);

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

        <div v-for="channel in items.slice(0, maxChannelShown)" :key="channel" class="side-bar-links subscriptions-div">
            <img style="border-radius: 50%;" src="@/assets/img/Django.png" alt="">
            <p>{{ channel.title }}</p>
        </div>

        <div class="side-bar-links">
            <p style="font-size: 26px;">></p>
            <button @click="subscriptionChannelShown" id="show-more-btn">Show more</button>
        </div>
    </aside>
</template>