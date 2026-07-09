/// <reference types="vitest" />
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

const __dirname = dirname(fileURLToPath(import.meta.url))

export default defineConfig(({ command }) => ({
  base: command === 'build' ? '/static/frontend/' : '/',
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  build: {
    outDir: '../static/frontend',
    emptyOutDir: true,
    manifest: 'manifest.json',
    rollupOptions: {
      input: resolve(__dirname, 'src/app/main.ts'),
    },
  },
  server: {
    port: 5173,
    origin: 'http://localhost:5173',
    cors: {
      origin: 'http://localhost:8000',
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: {
      provider: 'v8',
      include: ['src/utils/**', 'src/api/**', 'src/stores/**', 'src/composables/**', 'src/features/**/composables/**'],
      exclude: ['**/*.stories.ts', 'src/composables/dnd/**'],
      thresholds: {
        'src/utils/**': { statements: 80, branches: 80, functions: 80, lines: 80 },
        'src/composables/**': { statements: 80, branches: 80, functions: 80, lines: 80 },
        'src/features/**/composables/**': { statements: 80, branches: 80, functions: 80, lines: 80 },
      },
    },
  },
}))
