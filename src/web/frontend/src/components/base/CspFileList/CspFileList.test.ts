import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { defineComponent, h, ref } from 'vue'
import { setupUser } from '@/test/render'
import CspFileList from './CspFileList.vue'

const Host = defineComponent({
  setup() {
    const items = ref([
      { key: 'a', name: 'a.pdf', size: 1200 },
      { key: 'b', name: 'b.pdf', size: 3_400_000 },
      { key: 'c', name: 'c.pdf', size: 500, error: 'Format refusé.' },
    ])
    return () => h(CspFileList, { label: 'Fichiers', items: items.value, onRemove: (key: string) => {
      items.value = items.value.filter(item => item.key !== key)
    } })
  },
})

describe('cspFileList', () => {
  it('lists each file with its size and its error', () => {
    render(Host)

    expect(screen.getByRole('list', { name: 'Fichiers' })).toBeInTheDocument()
    expect(screen.getByText('1 ko')).toBeInTheDocument()
    expect(screen.getByText('3,4 Mo')).toBeInTheDocument()
    expect(screen.getByText('Format refusé.')).toBeInTheDocument()
  })

  it('moves the focus to the next file, then to the previous one, after a removal', async () => {
    const user = setupUser()
    render(Host)

    await user.click(screen.getByRole('button', { name: 'Retirer b.pdf' }))
    expect(screen.queryByText('b.pdf')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Retirer c.pdf' })).toHaveFocus()

    await user.click(screen.getByRole('button', { name: 'Retirer c.pdf' }))
    expect(screen.getByRole('button', { name: 'Retirer a.pdf' })).toHaveFocus()
  })
})
