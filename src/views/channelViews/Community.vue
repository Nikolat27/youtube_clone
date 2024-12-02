<script setup>

</script>

<template>
    <div id="communityDivision">
        <div class="flex flex-col mt-20 gap-y-4">
            <div class="w-[852px] h-[777px] rounded-2xl flex flex-row pt-4 pl-4
                 border-[1px] border-[#ebebeb]">
                <a href="#" class="mr-4">
                    <img class="w-10 h-10 rounded-full" src="@/assets/img/Django.png" alt="">
                </a>
                <div class="flex flex-col">
                    <div class="flex flex-row gap-x-2">
                        <a href="#" class="text-[13px] font-medium">Channel name</a>
                        <span class="text-[12px] font-normal">10 hours ago</span>
                    </div>
                    <p class="text-lg font-normal">asdfhasdhfhasdhfasdf</p>
                    <img class="w-[638px] h-[638px] rounded-xl mt-1" src="@/assets/img/Django.png" alt="">
                    <div class="flex flex-row mt-3 items-center">
                        <button class="w-8 h-8 rounded-full hover:bg-[#e5e5e5] flex justify-center items-center">
                            <img class="w-[75%] h-[75%]" src="@/assets/icons/svg-icons/like-empty.svg" alt="">
                        </button>
                        <span class="text-xs font-normal">385</span>
                        <button class="ml-2 w-8 h-8 rounded-full hover:bg-[#e5e5e5] flex justify-center items-center">
                            <img class="w-[75%] h-[75%]" src="@/assets/icons/svg-icons/dislike-empty.svg" alt="">
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>