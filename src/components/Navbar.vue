<script setup>

const message = "Hello World";

</script>

<template>
    <header class="header">
        <div class="left-div">
            <img class="hamburger-img" src="@/assets/icons/header/hamburger-menu.svg" alt="">
            <img class="youtube-logo-img" src="@/assets/icons/header/youtube-logo.svg" alt="">
        </div>
        <div class="search-div">
            <input type="text" name="q" class="search-bar" placeholder="Search">
            <button class="search-btn">
                <img src="@/assets/icons/header/search.svg" alt="">
            </button>
            <button class="audio-search-btn">
                <img src="@/assets/icons/header/voice-search-icon.svg" alt="">
            </button>
        </div>
        <div class="right-div">
            <div class="right-div-buttons">
                <button class="upload-video-btn" data-tooltip="Upload">
                    <img src="@/assets/icons/header/upload.svg" class="create-video-img" alt="">
                </button>
                <button class="notification-btn" data-tooltip="Notifications">
                    <img src="@/assets/icons/header/notifications.svg" class="notification-img" alt="">
                </button>
            </div>
            <button class="channel-profile-btn">
                <img src="@/assets/img/Django.png" class="channel-profile-img" alt="">
            </button>
        </div>
    </header>
</template>