/// <reference types="vitest" />
import { dirname, resolve } from 'node:path'
import process from 'node:process'
import { fileURLToPath } from 'node:url'
import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

const __dirname = dirname(fileURLToPath(import.meta.url))

const devOrigin = process.env.WEB_VITE_DEV_ORIGIN ?? 'http://localhost:5173'
const atsOrigin = process.env.WEB_ATS_ORIGIN ?? 'http://localhost:8000'
const devUrl = new URL(devOrigin)

const server = devUrl.protocol === 'https:'
  ? {
      origin: devOrigin,
      cors: { origin: atsOrigin },
      hmr: {
        protocol: 'wss',
        host: devUrl.hostname,
        clientPort: Number(devUrl.port) || 443,
      },
    }
  : {
      port: Number(devUrl.port) || 5173,
      strictPort: true,
      origin: devOrigin,
      cors: { origin: atsOrigin },
    }

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
  server,
  test: {
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
