<script setup>

</script>
<template>
    <div class="flex flex-col absolute w-[1270px] h-[100%] left-[225px] top-[125px] justify-start items-start">
        <div>
            <p class="text-[25px] font-semibold font-youtube mb-7">Channel content</p>
        </div>
        <div class="chnl-tab-content flex flex-row gap-x-6 border-b border-[#f1f1f1] w-[100%] h-[48px]">
            <a class="active" data-target="videos">Videos</a>
            <a class="" data-target="shorts">Shorts</a>
            <a class="" data-target="live">Live</a>
            <a class="" data-target="posts">Posts</a>
            <a class="" data-target="playlists" style="width: 56px;" >Playlists</a>
        </div>
        <div class="chnl-filter-bar flex flex-row justify-start items-center gap-x-6
         border-b border-[#f1f1f1] w-[100%] h-[48px] mt-1 relative">
            <img class="w-6 h-6 cursor-pointer" src="@/assets/icons/svg-icons/filter-filtering-icon.svg" alt="">
            <input class="w-[1184px] h-[48px] outline-none" type="text" placeholder="Filter">
            <div class="flex flex-col w-[142px] h-[400px]">
                <div class="w-[142px] h-[32px]">Age restriction</div>
                <div class="w-[142px] h-[32px]">Copyright</div>
                <div class="w-[142px] h-[32px]">Description</div>
                <div class="w-[142px] h-[32px]">Made for kids</div>
                <div class="w-[142px] h-[32px]">Title</div>
                <div class="w-[142px] h-[32px]">Views</div>
                <div class="w-[142px] h-[32px]">Visibility</div>
            </div>
        </div>

    </div>
</template>