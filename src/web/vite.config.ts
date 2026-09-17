/// <reference types="vitest" />
import { dirname, resolve } from 'node:path'
import process from 'node:process'
import { fileURLToPath } from 'node:url'
import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import { defaultAllowedOrigins, defineConfig } from 'vite'
import checker from 'vite-plugin-checker'

const __dirname = dirname(fileURLToPath(import.meta.url))

const devOrigin = process.env.WEB_VITE_DEV_ORIGIN ?? 'http://localhost:5173'
const atsOrigin = process.env.WEB_ATS_ORIGIN
const devUrl = new URL(devOrigin)

const cors = { origin: atsOrigin ? [defaultAllowedOrigins, atsOrigin] : defaultAllowedOrigins }

const listenHost = process.env.HOST
const listenPort = Number(process.env.PORT) || undefined

const server = devUrl.protocol === 'https:'
  ? {
      host: listenHost,
      port: listenPort,
      strictPort: Boolean(listenPort),
      origin: devOrigin,
      cors,
      hmr: {
        protocol: 'wss',
        host: devUrl.hostname,
        clientPort: Number(devUrl.port) || 443,
      },
    }
  : {
      host: listenHost,
      port: listenPort ?? (Number(devUrl.port) || 5173),
      strictPort: true,
      origin: devOrigin,
      cors,
    }

export default defineConfig(({ command }) => ({
  base: command === 'build' ? '/static/frontend/' : '/',
  root: 'frontend',
  plugins: [vue(), tailwindcss(), checker({ vueTsc: { tsconfigPath: 'frontend/tsconfig.json' }, enableBuild: false })],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'frontend/src'),
    },
  },
  build: {
    outDir: '../presentation/static/frontend',
    emptyOutDir: true,
    manifest: 'manifest.json',
    rollupOptions: {
      input: resolve(__dirname, 'frontend/src/app/main.ts'),
    },
  },
  server,
  test: {
    environment: 'jsdom',
    setupFiles: ['src/test/setup.ts'],
    testTimeout: 10_000,
    coverage: {
      provider: 'v8',
      include: ['src/utils/**', 'src/api/**', 'src/stores/**', 'src/composables/**', 'src/features/**/composables/**', 'src/components/base/**', 'src/features/**/components/**'],
      exclude: ['**/*.stories.ts', 'src/composables/dnd/**', 'src/test/**'],
      thresholds: {
        'src/utils/**': { statements: 80, branches: 80, functions: 80, lines: 80 },
        'src/composables/**': { statements: 80, branches: 80, functions: 80, lines: 80 },
        'src/features/**/composables/**': { statements: 80, branches: 80, functions: 80, lines: 80 },
        'src/components/base/**': { statements: 55, lines: 55 },
        'src/features/**/components/**': { statements: 40, lines: 40 },
      },
    },
  },
}))
