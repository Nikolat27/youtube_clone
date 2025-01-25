<script setup>
import channelProfile from '/src/assets/img/Ruby.png'
import dashboardIcon from '/src/assets/icons/svg-icons/dashboard-icon.svg'
import contentIcon from '/src/assets/icons/svg-icons/content-icon.svg'
import analyticsIcon from '/src/assets/icons/svg-icons/analytics-icon.svg'
import communityIcon from '/src/assets/icons/svg-icons/community-icon.svg'
import earnIcon from '/src/assets/icons/svg-icons/earn-icon.svg'
import customizationIcon from '/src/assets/icons/svg-icons/customization-icon.svg'
import advertisingIcon from '/src/assets/icons/svg-icons/advertising-icon.svg'

</script>

<template>
    <aside id="large-aside" class="border-r font-roboto hidden flex-col absolute left-0 top-[63.2px]
     h-[100vh] w-[255.2px] border-solid">
        <div class="mt-4 thumbnail h-[208px] w-[255.2px] flex flex-col justify-center items-center">
            <img class="w-[112px] h-[112px] rounded-full" :src="channelProfile" alt="">
            <p class="text-[15px] font-medium mt-3 mb-1">Your channel</p>
            <p class="text-[12px] font-normal">channel name</p>
        </div>
        <div class="top-section flex flex-col pl-4 mt-4">
            <router-link to="/studio/">
                <div class="large-menu-item">
                    <img :src="dashboardIcon" alt="">
                    <p>Dashboard</p>
                </div>
            </router-link>
            <div class="large-menu-item">
                <img :src="contentIcon" alt="">
                <p>Content</p>
            </div>
            <div class="large-menu-item">
                <img :src="analyticsIcon" alt="">
                <p>Analytics</p>
            </div>
            <router-link to="/posts" class="large-menu-item">
                <img :src="communityIcon" alt="">
                <p>Community</p>
            </router-link>
            <div class="large-menu-item">
                <img :src="earnIcon" alt="">
                <p>Earn</p>
            </div>
            <router-link to="/studio/customization">
                <div class="large-menu-item">
                    <img :src="customizationIcon" alt="">
                    <p>Customization</p>
                </div>
            </router-link>
            <router-link to="/studio/create-ads">
                <div class="large-menu-item">
                    <img :src="advertisingIcon" alt="">
                    <p>Create Ads</p>
                </div>
            </router-link>
        </div>
    </aside>
    <aside id="small-aside"
        class="border-r font-roboto hidden flex-col absolute left-0 top-[63.2px] h-[100vh] w-[71.2px]">
        <div class="mt-4 thumbnail h-[60px] w-[71.2px] flex justify-center items-center cursor-pointer">
            <img class="w-[32px] h-[39.2px] rounded-full" :src="channelProfile" alt="">
        </div>
        <div class="top-section gap-y-2 flex flex-col mt-2 justify-center items-center">
            <div class="menu-item">
                <img :src="dashboardIcon" alt="">
            </div>
            <div class="menu-item">
                <img :src="contentIcon" alt="">
            </div>
            <div class="menu-item">
                <img :src="analyticsIcon" alt="">
            </div>
            <div class="menu-item">
                <img :src="communityIcon" alt="">
            </div>
            <div class="menu-item">
                <img :src="earnIcon" alt="">
            </div>
            <div class="menu-item">
                <img :src="customizationIcon" alt="">
            </div>
        </div>
    </aside>
</template>

<style scoped>
@media (min-width: 1200px) {
    #large-aside {
        display: flex;
    }
}

@media (max-width: 1199px) {
    #small-aside {
        display: flex;
    }
}

.large-menu-item {
    cursor: pointer;
    width: 231px;
    height: 48px;
    background-color: white;
    border-radius: 8px;
    display: flex;
    flex-direction: row;
    justify-content: start;
    align-items: center;
    padding-left: 8px;
}

.large-menu-item:hover {
    background-color: #f9f9f9;
}

.large-menu-item img {
    width: 24px;
    height: 24px;
    margin-right: 24px;
}

.large-menu-item p {
    font-weight: 400;
    font-size: 15px;
}

.small-menu-item {
    cursor: pointer;
    width: 52px;
    height: 48px;
    background-color: white;
    border-radius: 8px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    padding: 2px;
}

.small-menu-item:hover {
    background-color: #f9f9f9;
}

.small-menu-item img {
    width: 24px;
    height: 24px;
}
</style>