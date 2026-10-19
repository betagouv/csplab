import type { StorybookConfig } from '@storybook/vue3-vite'
import { realpathSync } from 'node:fs'
import process from 'node:process'
import { fileURLToPath } from 'node:url'
import remarkGfm from 'remark-gfm'
import { searchForWorkspaceRoot } from 'vite'

const config: StorybookConfig = {
  stories: [
    '../src/**/*.mdx',
    '../src/**/*.stories.@(js|jsx|mjs|ts|tsx)',
  ],
  framework: {
    name: '@storybook/vue3-vite',
    options: {
      builder: {
        viteConfigPath: 'vite.config.ts',
      },
      docgen: {
        plugin: 'vue-component-meta',
        tsconfig: 'frontend/tsconfig.json',
      },
    },
  },
  addons: [
    {
      name: '@storybook/addon-docs',
      options: {
        mdxPluginOptions: {
          mdxCompileOptions: {
            remarkPlugins: [remarkGfm],
          },
        },
      },
    },
  ],
  features: {
    changeDetection: true,
  },
  viteFinal: async (config) => {
    config.base = process.env.STORYBOOK_BASE_URL ?? '/'
    // A node_modules linked from another checkout (git worktree) lies outside the workspace root that Vite serves.
    const nodeModules = realpathSync(fileURLToPath(new URL('../../node_modules', import.meta.url)))
    config.server = {
      ...config.server,
      fs: {
        ...config.server?.fs,
        allow: [...(config.server?.fs?.allow ?? [searchForWorkspaceRoot(process.cwd())]), nodeModules],
      },
    }
    return config
  },
}

export default config
