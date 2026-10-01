import type { CspAccordionItemProps } from './CspAccordionItem.vue'
import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { defineComponent, h } from 'vue'
import { setupUser } from '@/test/render'
import CspAccordion from './CspAccordion.vue'
import CspAccordionItem from './CspAccordionItem.vue'

const CspIconStub = defineComponent({
  name: 'CspIcon',
  props: { name: { type: String, required: true } },
  setup: props => () => h('i', { 'class': 'csp-icon', 'data-icon': props.name }),
})

function renderAccordion(itemProps: Partial<CspAccordionItemProps> = {}) {
  return render(
    defineComponent({
      setup() {
        return () =>
          h(CspAccordion, null, () => [
            h(CspAccordionItem, { ...itemProps, value: 'a', title: 'Question A' }, () => 'Réponse A'),
            h(CspAccordionItem, { ...itemProps, value: 'b', title: 'Question B' }, () => 'Réponse B'),
            h(CspAccordionItem, { ...itemProps, value: 'c', title: 'Question C' }, () => 'Réponse C'),
          ])
      },
    }),
    { global: { stubs: { CspIcon: CspIconStub } } },
  )
}

describe('cspAccordion', () => {
  it('starts with every section closed', () => {
    renderAccordion()

    expect(screen.getByRole('button', { name: 'Question A' })).toHaveAttribute('aria-expanded', 'false')
    expect(screen.queryByText('Réponse A')).not.toBeInTheDocument()
  })

  it('opens a section into a region labelled by its title', async () => {
    const user = setupUser()
    renderAccordion()
    const trigger = screen.getByRole('button', { name: 'Question A' })

    await user.click(trigger)

    const region = screen.getByRole('region', { name: 'Question A' })
    expect(trigger).toHaveAttribute('aria-expanded', 'true')
    expect(trigger).toHaveAttribute('aria-controls', region.id)
    expect(region).toHaveTextContent('Réponse A')
  })

  it('closes an open section with Enter', async () => {
    const user = setupUser()
    renderAccordion()
    const trigger = screen.getByRole('button', { name: 'Question A' })
    await user.click(trigger)

    await user.keyboard('{Enter}')

    expect(trigger).toHaveAttribute('aria-expanded', 'false')
  })

  it('moves the focus to the next title with ArrowDown', async () => {
    const user = setupUser()
    renderAccordion()
    screen.getByRole('button', { name: 'Question A' }).focus()

    await user.keyboard('{ArrowDown}')

    expect(screen.getByRole('button', { name: 'Question B' })).toHaveFocus()
  })

  it('moves the focus to the previous title with ArrowUp', async () => {
    const user = setupUser()
    renderAccordion()
    screen.getByRole('button', { name: 'Question C' }).focus()

    await user.keyboard('{ArrowUp}')

    expect(screen.getByRole('button', { name: 'Question B' })).toHaveFocus()
  })

  it('moves the focus to the first title with Home', async () => {
    const user = setupUser()
    renderAccordion()
    screen.getByRole('button', { name: 'Question C' }).focus()

    await user.keyboard('{Home}')

    expect(screen.getByRole('button', { name: 'Question A' })).toHaveFocus()
  })

  it('moves the focus to the last title with End', async () => {
    const user = setupUser()
    renderAccordion()
    screen.getByRole('button', { name: 'Question A' }).focus()

    await user.keyboard('{End}')

    expect(screen.getByRole('button', { name: 'Question C' })).toHaveFocus()
  })

  it('wraps each title in an h3 by default', () => {
    renderAccordion()

    expect(screen.getByRole('heading', { level: 3, name: 'Question A' })).toBeInTheDocument()
  })

  it('wraps each title in the heading level it is given', () => {
    renderAccordion({ headingLevel: 2 })

    expect(screen.getByRole('heading', { level: 2, name: 'Question A' })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { level: 3 })).not.toBeInTheDocument()
  })

  it('keeps several sections open by default', async () => {
    const user = setupUser()
    renderAccordion()

    await user.click(screen.getByRole('button', { name: 'Question A' }))
    await user.click(screen.getByRole('button', { name: 'Question B' }))

    expect(screen.getAllByRole('region')).toHaveLength(2)
  })
})
