import { setCustomIconLoader } from '@iconify/vue'
import '@/app/icons.custom'
import '@/app/icons.generated'

// Catch unregistered ri:* icons instead of fetching them from the Iconify API.
setCustomIconLoader((name) => {
  console.error(`Missing icon "ri:${name}", run: pnpm icons`)
  return null
}, 'ri')
