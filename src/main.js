import '@/assets/css/main.css'
import '@/assets/css/video-player.css'
import { createApp } from 'vue/dist/vue.esm-bundler.js'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)
app.mount('#app')
