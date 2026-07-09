import * as Sentry from '@sentry/vue'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from '@/router'
import App from './App.vue'
import '@/app/icons'
import '@/styles/index.css'

const router = createRouter({
  history: createWebHistory('/ats/'),
  routes,
})

const app = createApp(App)
app.use(createPinia())
app.use(router)

if (import.meta.env.PROD && import.meta.env.VITE_SENTRY_DSN) {
  Sentry.init({
    app,
    dsn: import.meta.env.VITE_SENTRY_DSN,
    environment: import.meta.env.VITE_SENTRY_ENVIRONMENT ?? 'production',
    release: import.meta.env.VITE_SENTRY_RELEASE,
    tracesSampleRate: 0,
    sendDefaultPii: false,
  })
}

app.mount('#ats-app')
