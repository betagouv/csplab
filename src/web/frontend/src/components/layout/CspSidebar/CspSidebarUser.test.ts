import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { provideSidebar } from '@/composables/ui/useSidebar'
import { createLocalStorageMock } from '@/test/browser'
import { renderWithApp } from '@/test/render'
import CspSidebarUser from './CspSidebarUser.vue'

function host(defaultExpanded: boolean) {
  return defineComponent({
    setup() {
      provideSidebar({ defaultExpanded, persistState: false })
      return () => h(CspSidebarUser, { name: 'Marie Dupont' })
    },
  })
}

describe('cspSidebarUser', () => {
  beforeEach(() => {
    vi.stubGlobal('localStorage', createLocalStorageMock())
  })

  it('names the account button after its visible text and describes it as the account', async () => {
    await renderWithApp(host(true))

    expect(screen.getByRole('button', { name: 'Marie Dupont' })).toHaveAccessibleDescription('Compte')
  })

  it('names the account button after the user name when the sidebar is collapsed', async () => {
    await renderWithApp(host(false))

    expect(screen.getByRole('button', { name: 'Marie Dupont' })).toBeInTheDocument()
  })
})
