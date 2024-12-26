import '@/assets/css/main.css'
import { createApp } from 'vue/dist/vue.esm-bundler.js'
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

import App from './App.vue'
import router from './router'
const app = createApp(App)

const options = {};
app.use(Toast, options)

app.component('VueDatePicker', VueDatePicker);
app.use(router)
app.mount('#app')