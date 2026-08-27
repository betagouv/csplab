import { addIcon } from '@iconify/vue'

// Hand-authored icons missing from @iconify-icons/ri; build-icons.mjs skips them.
addIcon('ri:progress-4-line', {
  width: 24,
  height: 24,
  body: '<path fill="currentColor" d="M2 12c0 5.523 4.477 10 10 10s10-4.477 10-10S17.523 2 12 2S2 6.477 2 12m18 0a8 8 0 1 1-16 0a8 8 0 0 1 16 0m-2 0a6 6 0 0 1-6 6V6a6 6 0 0 1 6 6"/>',
})
addIcon('ri:sidebar-fold-line', {
  width: 24,
  height: 24,
  body: '<path fill="currentColor" d="M5 5h8v14H5zm14 14h-4V5h4zM4 3a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1zm3 9l4-3.5v7z"/>',
})
addIcon('ri:sidebar-unfold-line', {
  width: 24,
  height: 24,
  body: '<path fill="currentColor" d="M5 5h8v14H5zm14 14h-4V5h4zM4 3a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1zm7 9L7 8.5v7z"/>',
})
