import { render } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { setupUser } from '@/test/render'
import CspTag from './CspTag.vue'
import CspTagGroup from './CspTagGroup.vue'

const CspIconStub = defineComponent({
  name: 'CspIcon',
  props: { name: { type: String, required: true } },
  setup: props => () => h('i', { 'class': 'csp-icon', 'data-icon': props.name }),
})

const global = { stubs: { CspIcon: CspIconStub } }

function renderTag(props: Record<string, unknown>) {
  const result = render(CspTag, { props, global })
  return { ...result, root: result.container.firstElementChild as HTMLElement }
}

function icon(container: Element, name: string) {
  return container.querySelector(`[data-icon="${name}"]`)
}

describe('cspTag: root element per variant', () => {
  it('static variant renders <p>', () => {
    const { root } = renderTag({ label: 'Cat' })
    expect(root.tagName).toBe('P')
    expect(root).toHaveTextContent('Cat')
  })

  it('clickable variant with href renders a link', () => {
    const { getByRole } = renderTag({ variant: 'clickable', label: 'Lien', href: '/x' })
    expect(getByRole('link', { name: 'Lien' })).toHaveAttribute('href', '/x')
  })

  it('clickable variant without href renders a button', () => {
    const { getByRole } = renderTag({ variant: 'clickable', label: 'Action' })
    expect(getByRole('button', { name: 'Action' })).toHaveAttribute('type', 'button')
  })

  it('disabled clickable with href renders a disabled button', () => {
    const { getByRole } = renderTag({ variant: 'clickable', label: 'X', href: '/x', disabled: true })
    expect(getByRole('button', { name: 'X' })).toBeDisabled()
  })

  it('dismissible variant renders a button named after the filter', () => {
    const { getByRole } = renderTag({ variant: 'dismissible', label: 'Vue' })
    expect(getByRole('button', { name: 'Retirer le filtre Vue' })).toBeInTheDocument()
  })

  it('static can be rendered `as`', () => {
    const { root } = renderTag({ label: 'X', as: 'li' })
    expect(root.tagName).toBe('LI')
  })
})

describe('cspTag: icon', () => {
  it('renders the icon on a variant that allows it', () => {
    const { container } = renderTag({ label: 'Cat', icon: 'ri:bookmark-line' })
    expect(icon(container, 'ri:bookmark-line')).toBeInTheDocument()
  })

  it('dismissible renders the cross as its only icon', () => {
    const { container } = renderTag({ variant: 'dismissible', label: 'Vue' })
    expect(icon(container, 'ri:close-line')).toBeInTheDocument()
    expect(container.querySelectorAll('[data-icon]')).toHaveLength(1)
  })
})

describe('cspTag: selectable', () => {
  it('reflects the pressed state and emits update:pressed on click', async () => {
    const user = setupUser()
    const { getByRole, emitted } = renderTag({ variant: 'selectable', label: 'F', pressed: false })

    await user.click(getByRole('button', { name: 'F', pressed: false }))

    expect(emitted()['update:pressed']).toEqual([[true]])
  })

  it('does not emit update:pressed when disabled', async () => {
    const user = setupUser()
    const { getByRole, emitted } = renderTag({ variant: 'selectable', label: 'F', disabled: true })

    await user.click(getByRole('button', { name: 'F' }))

    expect(emitted()['update:pressed']).toBeUndefined()
  })
})

describe('cspTag: dismissible', () => {
  it('emits dismiss on click', async () => {
    const user = setupUser()
    const { getByRole, emitted } = renderTag({ variant: 'dismissible', label: 'Vue' })

    await user.click(getByRole('button', { name: 'Retirer le filtre Vue' }))

    expect(emitted().dismiss).toHaveLength(1)
  })

  it('prefers an explicit dismissLabel', () => {
    const { getByRole } = renderTag({ variant: 'dismissible', label: 'Vue', dismissLabel: 'Fermer Vue' })
    expect(getByRole('button', { name: 'Fermer Vue' })).toBeInTheDocument()
  })
})

describe('cspTagGroup', () => {
  function renderGroup(groupProps: Record<string, unknown>) {
    const Host = defineComponent({
      components: { CspTag, CspTagGroup },
      props: { groupProps: { type: Object, required: true } },
      template: `
        <CspTagGroup v-bind="groupProps">
          <CspTag variant="selectable" value="a" label="A" />
          <CspTag variant="selectable" value="b" label="B" />
        </CspTagGroup>
      `,
    })
    return render(Host, { props: { groupProps }, global })
  }

  it('applies the size of the group to every tag', () => {
    const { container } = renderGroup({ modelValue: [], size: 'sm' })
    expect(container.querySelectorAll('.csp-tag--sm')).toHaveLength(2)
  })

  it('single mode: selecting a tag updates the v-model', async () => {
    const user = setupUser()
    const onUpdate = vi.fn()
    const { getByRole } = renderGroup({ 'modelValue': 'a', 'type': 'single', 'onUpdate:modelValue': onUpdate })

    await user.click(getByRole('button', { name: 'B', pressed: false }))

    expect(onUpdate).toHaveBeenCalledWith('b')
  })
})
