<script setup></script>

<template>
    <div id="playlistsDivision">
        <div class="flex flex-row mt-7 relative">
            <span class="text-base font-normal left-0">Created playlists</span>
            <button class="playlistSortingToggle flex flex-row absolute right-0">
                <img class="w-6 h-6" src="@/assets/icons/svg-icons/filter-filtering-icon.svg" alt="">
                <span class="ml-2">Sort by</span>
            </button>
            <div class="playlistSortingDiv my-shadow absolute right-0 top-10 w-[164px] h-[112px]
                 hidden flex-col rounded-xl font-normal text-sm pt-2">
                <a href="#"
                    class="active w-[164px] h-[48px] flex flex-row justify-start items-center hover:bg-[#e5e5e5]">
                    <span class="pl-3">Date added (newest)</span>
                </a>
                <a href="#" class="w-[164px] h-[48px] flex flex-row justify-start items-center hover:bg-[#e5e5e5]">
                    <span class="pl-3">Last video added</span>
                </a>
            </div>
        </div>

        <div class="flex flex-row flex-wrap mt-4 gap-x-1 gap-y-4">
            <div class="cursor-pointer">
                <a href="#" class="flex flex-col">
                    <img class="w-[210px] h-[118px] rounded-2xl" src="@/assets/img/Django.png" alt="">
                    <p class="text-sm font-medium mt-2 mb-2">
                        Playlist title
                    </p>
                    <span class="text-sm font-normal text-gray-600">View full playlist</span>
                </a>
            </div>
        </div>
    </div>
</template>