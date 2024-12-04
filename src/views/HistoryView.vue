<script setup>

</script>

<template>
    <div class="flex flex-row w-[1070px] ml-[300px] mt-[100px]">
        <div class="flex flex-col w-[628px] h-[600px] gap-y-4 relative">
            <div class="flex flex-col">
                <div class="top-[-45px] font-bold text-4xl relative">
                    <p>Watch History</p>
                </div>
                <div class="relative font-bold text-xl">
                    <p>Today</p>
                </div>
            </div>
            <a href="">
                <div class="history-video flex flex-row relative">
                    <div class="w-[246px] h-[138px] flex flex-row">
                        <img class="w-[100%] h-[100%] rounded-lg" src="@/assets/img/Django.png" alt="">
                    </div>
                    <div class="flex flex-col cursor-pointer ml-4">
                        <p class="font-normal text-lg">Video Title</p>
                        <div class="flex flex-row">
                            <p class="text-xs font-normal text-[#7d8a9f] hover:text-[#6b6b6b]">Channel name&nbsp;
                            </p>
                            <span class="text-[#7d8a9f] text-xs font-normal hover:text-[#6b6b6b] mb-4">. 25M
                                views</span>
                        </div>
                        <p class="text-[#7d8a9f] text-xs font-normal hover:text-[#6b6b6b]">video description</p>
                    </div>
                    <button
                        class="w-10 h-10 absolute right-0 top-0 rounded-full hover:bg-[#e5e5e5] flex justify-center items-center">
                        <img class="w-5 h-5" src="@/assets/icons/svg-icons/x-mark-icon.svg" alt="">
                    </button>
                    <div class="remove-history hidden flex-col pl-2 pt-3 text-white bg-[#717171] text-xs font-normal w-[110px] h-[55px]
                     rounded-md absolute right-[-35px] top-12 opacity-90">
                        <p>Remove from</p>
                        <p>watch history</p>
                    </div>
                </div>
            </a>
            <a href="">
                <div class="history-video flex flex-row relative">
                    <div class="w-[246px] h-[138px] flex flex-row">
                        <img class="w-[100%] h-[100%] rounded-lg" src="@/assets/img/Django.png" alt="">
                    </div>
                    <div class="flex flex-col cursor-pointer ml-4">
                        <p class="font-normal text-lg">Video Title</p>
                        <div class="flex flex-row">
                            <p class="text-xs font-normal text-[#7d8a9f] hover:text-[#6b6b6b]">Channel name&nbsp;
                            </p>
                            <span class="text-[#7d8a9f] text-xs font-normal hover:text-[#6b6b6b] mb-4">. 25M
                                views</span>
                        </div>
                        <p class="text-[#7d8a9f] text-xs font-normal hover:text-[#6b6b6b]">video description</p>
                    </div>
                    <button
                        class="w-10 h-10 absolute right-0 top-0 rounded-full hover:bg-[#e5e5e5] flex justify-center items-center">
                        <img class="w-5 h-5" src="@/assets/icons/svg-icons/x-mark-icon.svg" alt="">
                    </button>
                    <div class="remove-history hidden flex-col pl-2 pt-3 text-white bg-[#717171] text-xs font-normal w-[110px] h-[55px]
                     rounded-md absolute right-[-35px] top-12 opacity-90">
                        <p>Remove from</p>
                        <p>watch history</p>
                    </div>
                </div>
            </a>
            <div class="flex flex-col relative mt-[80px]">
                <div class="top-[-60px] absolute font-bold text-xl">
                    <p>Yesterday</p>
                </div>
                <div class="w-4 h-4 flex flex-row justify-start items-center absolute left-2 top-[-5px]">
                    <img src="@/assets/icons/svg-icons/shorts-icon.svg">
                    <p class="font-bold text-xl">&nbsp;&nbsp;Shorts</p>
                </div>
                <button id="prevButton"
                    class="w-9 h-9 absolute top-[210px] left-[-20px] z-50 shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                    <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-left-icon.svg"
                        alt="">
                </button>
                <div id="slider" class="history-short-video flex overflow-hidden flex-row gap-x-1
                 gap-y-8 h-[485px] w-[640px] relative">
                    <div class="flex flex-col w-[210px] h-[405px] mt-8 relative">
                        <img class="w-[100%] h-[100%] rounded-lg" src="@/assets/img/Django.png" alt="">
                        <p class="text-base font-medium mt-2">Lorem ipsum</p>
                        <!-- Beware of data-targets (for backend) -->
                        <button data-target="short-video-1" class="short-video-options-toggle flex justify-center items-center absolute bottom-[-6px] right-0
                         w-8 h-8 rounded-full hover:bg-[#9c8c8c]">
                            <img class="w-[50%] h-[50%]" src="@/assets/icons/svg-icons/kebab-menu.svg" alt="">
                        </button>
                        <div id="short-video-1" class="z-auto w-[230px] h-10 history-short-video-options absolute right-[-198px] bottom-[-45px]
                         hidden flex-col gap-y-4 rounded-xl bg-white shadow-lg">
                            <a href="#">
                                <div
                                    class="pl-3 w-[230px] h-10 flex flex-row rounded-xl justify-start items-center gap-x-2 hover:bg-[#e5e5e5]">
                                    <img class="w-5 h-5 rounded-full" src="@/assets/icons/svg-icons/hide-icon.svg"
                                        alt="">
                                    <p class="text-base font-normal">Hide</p>
                                </div>
                            </a>
                        </div>
                    </div>
                    <div class="flex flex-col w-[210px] h-[405px] mt-8 relative">
                        <img class="w-[100%] h-[100%] rounded-lg" src="@/assets/img/Django.png" alt="">
                        <p class="text-base font-medium mt-2">Lorem ipsum</p>
                        <!-- Beware of data-targets (for backend) -->
                        <button data-target="short-video-2" class="short-video-options-toggle flex justify-center items-center absolute bottom-[-6px] right-0
                         w-8 h-8 rounded-full hover:bg-[#e5e5e5]">
                            <img class="w-[50%] h-[50%]" src="@/assets/icons/svg-icons/kebab-menu.svg" alt="">
                        </button>
                        <div id="short-video-2" class="z-auto w-[230px] h-10 history-short-video-options absolute right-[-198px] bottom-[-45px]
                         hidden flex-col gap-y-4 rounded-xl bg-white shadow-lg">
                            <a href="#">
                                <div
                                    class="pl-3 w-[230px] h-10 flex flex-row rounded-xl justify-start items-center gap-x-2 hover:bg-[#e5e5e5]">
                                    <img class="w-5 h-5 rounded-full" src="@/assets/icons/svg-icons/hide-icon.svg"
                                        alt="">
                                    <p class="text-base font-normal">Hide</p>
                                </div>
                            </a>
                        </div>
                    </div>
                </div>
                <hr>
                <button id="nextButton"
                    class="w-9 h-9 absolute top-[210px] right-[-30px] shadow-lg bg-white hover:bg-[#e5e5e5] rounded-full">
                    <img class="w-[100%] h-[100%]" src="@/assets/icons/svg-icons/thin-chevron-round-right-icon.svg"
                        alt="">
                </button>
            </div>
            <a href="">
                <div class="history-video flex flex-row relative">
                    <div class="w-[246px] h-[138px] flex flex-row">
                        <img class="w-[100%] h-[100%] rounded-lg" src="@/assets/img/Django.png" alt="">
                    </div>
                    <div class="flex flex-col cursor-pointer ml-4">
                        <p class="font-normal text-lg">Video Title</p>
                        <div class="flex flex-row">
                            <p class="text-xs font-normal text-[#7d8a9f] hover:text-[#6b6b6b]">Channel name&nbsp;
                            </p>
                            <span class="text-[#7d8a9f] text-xs font-normal hover:text-[#6b6b6b] mb-4">. 25M
                                views</span>
                        </div>
                        <p class="text-[#7d8a9f] text-xs font-normal hover:text-[#6b6b6b]">video description</p>
                    </div>
                    <button
                        class="w-10 h-10 absolute right-0 top-0 rounded-full hover:bg-[#e5e5e5] flex justify-center items-center">
                        <img class="w-5 h-5" src="@/assets/icons/svg-icons/x-mark-icon.svg" alt="">
                    </button>
                    <div class="remove-history hidden flex-col pl-2 pt-3 text-white bg-[#717171] text-xs font-normal w-[110px] h-[55px]
                     rounded-md absolute right-[-35px] top-12 opacity-90">
                        <p>Remove from</p>
                        <p>watch history</p>
                    </div>
                </div>
            </a>
            <a href="">
                <div class="history-video flex flex-row relative">
                    <div class="w-[246px] h-[138px] flex flex-row">
                        <img class="w-[100%] h-[100%] rounded-lg" src="@/assets/img/Django.png" alt="">
                    </div>
                    <div class="flex flex-col cursor-pointer ml-4">
                        <p class="font-normal text-lg">Video Title</p>
                        <div class="flex flex-row">
                            <p class="text-xs font-normal text-[#7d8a9f] hover:text-[#6b6b6b]">Channel name&nbsp;
                            </p>
                            <span class="text-[#7d8a9f] text-xs font-normal hover:text-[#6b6b6b] mb-4">. 25M
                                views</span>
                        </div>
                        <p class="text-[#7d8a9f] text-xs font-normal hover:text-[#6b6b6b]">video description</p>
                    </div>
                    <button
                        class="w-10 h-10 absolute right-0 top-0 rounded-full hover:bg-[#e5e5e5] flex justify-center items-center">
                        <img class="w-5 h-5" src="@/assets/icons/svg-icons/x-mark-icon.svg" alt="">
                    </button>
                    <div class="remove-history hidden flex-col pl-2 pt-3 text-white bg-[#717171] text-xs font-normal w-[110px] h-[55px]
                     rounded-md absolute right-[-35px] top-12 opacity-90">
                        <p>Remove from</p>
                        <p>watch history</p>
                    </div>
                </div>
            </a>

        </div>
        <div class="flex flex-col w-[441px] ml-[200px] mt-10">
            <form action="">
                <div class="flex flex-row w-[235px] h-[10]">
                    <button
                        class="w-10 h-10 rounded-full cursor-pointer hover:bg-[#e5e5e5] flex justify-center items-center">
                        <img class="w-5 h-5" src="@/assets/icons/svg-icons/search-line-icon.svg" alt="">
                    </button>
                    <input type="text" name="query"
                        class="w-[235px] outline-none border-b-[1px] border-b-black focus:border-b-[#0f0f0f] focus:border-b-[2px] transition-all duration-100"
                        placeholder="Search watch history">
                </div>
            </form>
            <div
                class="flex flex-row w-[194px] h-[36px] mb-4 mt-7 justify-start items-center hover:bg-[#e5e5e5] rounded-3xl">
                <button class="w-10 h-10 flex justify-center items-center">
                    <img class="w-5 h-5" src="@/assets/icons/svg-icons/trash-can-icon.svg" alt="">
                </button>
                <p class="text-sm font-medium">Clear all watch history</p>
            </div>
            <div class="flex flex-row w-[194px] h-[36px] justify-start items-center hover:bg-[#e5e5e5] rounded-3xl">
                <button class="w-10 h-10 flex justify-center items-center">
                    <img class="w-4 h-4" src="@/assets/icons/svg-icons/pause-icon.svg" alt="">
                </button>
                <p class="text-sm font-medium">Pause watch history</p>
            </div>
            <div
                class="mb-4 mt-4 flex flex-row w-[260px] h-[45px] justify-start items-center hover:bg-[#e5e5e5] rounded-3xl">
                <button class="w-10 h-10 flex justify-center items-center pl-3">
                    <img class="w-7 h-7" src="@/assets/icons/svg-icons/speaking-bubbles-b-w-icon.svg" alt="">
                </button>
                <p class="text-sm font-medium pl-4">Clear all comments and replies history</p>
            </div>
        </div>
    </div>
</template>