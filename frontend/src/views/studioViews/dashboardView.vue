<script setup>
import uploadIcon from '/src/assets/icons/svg-icons/upload-icon.svg'
import editIcon from '@/assets/icons/svg-icons/edit-icon.svg'
import uploadImage from '/src/assets/img/upload-video-img.svg'
</script>

<template>
    <div
        class="flex font-roboto flex-col w-full h-[55px] justify-start items-center pl-12 absolute left-[82px] top-[90px]">
        <div class="flex flex-row w-[80%] justify-start items-center">
            <div class="title justify-self-start items-center">
                <h1 class="text-[25px] font-semibold">Channel dashboard</h1>
            </div>
            <div class="buttons w-[10%] flex flex-row gap-x-2 justify-self-end ml-auto">
                <button
                    class="w-[39px] h-[39px] rounded-full flex justify-center border hover:bg-[#f9f9f9] border-black items-center">
                    <img class="w-[18px] h-[18px]" :src="uploadIcon" alt="">
                </button>
                <button
                    class="w-[39px] h-[39px] rounded-full flex justify-center border hover:bg-[#f9f9f9] border-black items-center">
                    <img class="w-[18px] h-[18px]" :src="editIcon" alt="">
                </button>
            </div>
        </div>
        <div class="flex flex-row w-full ml-[290px] mt-6">
            <div class="w-[338px] h-[548px] rounded-2xl flex-col justify-start items-center">
                <div class="justify-self-start mt-4 w-[288px] h-[498px] rounded-xl border p-4 flex justify-center items-center
                 flex-col gap-y-2">
                    <img class="w-[152px] h-[152px]" :src="uploadImage" alt="">
                    <p class="text-[13px] font-normal">Want to see metrics on your recent video?
                        Upload and publish a video to get started. </p>
                    <button class="w-[120px] h-[36px] rounded-3xl bg-black text-white text-[14px] font-medium flex justify-center
                 items-center">
                        Upload videos
                    </button>
                </div>
            </div>
            <div class="w-[338px] h-[548px] rounded-2xl flex-col justify-start items-center">
                <div class="justify-self-start mt-4 w-[288px] h-[498px] rounded-xl border p-4 flex justify-start
                 items-start flex-col">
                    <div class="flex flex-col border-b pb-10 w-full">
                        <h1 class="text-[18px] font-medium">Channel analytics</h1>
                        <p class="mt-2 text-[13px] font-normal">Current subscribers</p>
                        <p class="text-[34px] font-normal">0</p>
                    </div>
                    <div class="flex flex-col w-full border-b pb-10 mt-4">
                        <p class="text-[15px] font-medium">Summary</p>
                        <p class="text-[12px] font-normal text-gray-600">Last 28 days</p>
                        <div class="flex flex-row w-full mt-4">
                            <div class="justify-self-start">
                                <p class="text-[13px] font-normal">Views</p>
                            </div>
                            <div class="justify-self-end ml-auto mr-1">
                                <p class="text-[13px] font-normal">1</p>
                            </div>
                        </div>
                        <div class="flex flex-row w-full mt-4">
                            <div class="justify-self-start">
                                <p class="text-[13px] font-normal">Watch time (hours)</p>
                            </div>
                            <div class="justify-self-end ml-auto mr-1">
                                <p class="text-[13px] font-normal"> 0.0
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="flex flex-col w-full mt-4">
                        <p class="text-[15px] font-medium">Top videos</p>
                        <p class="text-[12px] font-normal text-gray-600">Last 48 hours · Views </p>
                        <button class="text-[14px] font-medium w-[177px] h-[36px] rounded-3xl text-black bg-[#f9f9f9]
                         hover:bg-[#e5e5e5] mt-4">Go to channel analytics</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>