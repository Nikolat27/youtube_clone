<script setup></script>

<template>
    <section class="text-center flex flex-col justify-center items-center h-96">
        <h1>{{ $route.fullPath }}</h1>
        <i class="pi pi-exclamation-triangle text-yellow-400 text-7xl mb-5"></i>
        <h1 class="text-6xl font-bold mb-4">404 Not Found</h1>
        <p class="text-xl mb-5">This page does not exist</p>
        <RouterLink to="/" class="text-white bg-red-700 hover:bg-red-900 rounded-md px-3 py-2
         mt-4">Go Back
        </RouterLink>
    </section>
</template>