<script setup>

</script>
<template>
    <div id="shortsDivision">
        <div class="flex flex-col mt-4">
            <div class="flex flex-row">
                <button class="active w-[63px] h-[32px]">Latest</button>
                <button class="w-[72.5px] h-[32px]">Popular</button>
                <button class="w-[64.5px] h-[32px]">Oldest</button>
            </div>
            <div class="flex flex-row flex-wrap mt-4 gap-x-1 gap-y-4">
                <div class="flex flex-col">
                    <img class="w-[209.98px] h-[372.37px] rounded-2xl" src="@/assets/img/Django.png" alt="">
                    <p class="text-base font-medium mt-2 mb-0">
                        Video title
                    </p>
                    <span class="text-sm font-normal text-gray-600">73K views&nbsp;</span>
                </div>
            </div>
        </div>
    </div>
</template>