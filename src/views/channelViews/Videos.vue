<script setup>
import { ref } from 'vue';
</script>

<template>
    <div id="videosDivision">
        <div class="flex flex-col mt-4">
            <div class="flex flex-row">
                <button class="active w-[63px] h-[32px]">Latest</button>
                <button class="w-[72.5px] h-[32px]">Popular</button>
                <button class="w-[64.5px] h-[32px]">Oldest</button>
            </div>
            <div id="infinite-scroll-division" class="flex flex-row flex-wrap mt-4 gap-x-4 gap-y-8">
                <div class="flex flex-col">
                    <div class="relative">
                        <img class="w-[251px] h-[141px] rounded-2xl" src="@/assets/img/Django.png" alt="">
                        <span class="bg-opacity-80 w-10 h-4 rounded-md absolute bottom-2 right-2
                             font-medium text-xs bg-black text-white
                             flex justify-center items-center">
                            12:12
                        </span>
                    </div>
                    <p class="text-sm font-medium mt-3 mb-2">
                        Video title
                    </p>
                    <div class="flex flex-row text-xs font-normal text-gray-600">
                        <span>73K views&nbsp;</span>
                        <span>6 days ago&nbsp;</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>