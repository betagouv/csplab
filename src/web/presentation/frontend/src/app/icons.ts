import { setCustomIconLoader } from '@iconify/vue'
import '@/app/icons.custom'
import '@/app/icons.generated'

setCustomIconLoader((name) => {
  console.error(`Missing icon "ri:${name}", run: pnpm icons`)
  return null
}, 'ri')
