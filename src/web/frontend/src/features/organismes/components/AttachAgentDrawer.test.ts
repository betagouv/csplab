import { fireEvent, render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { defineComponent, h, nextTick, ref } from 'vue'
import { AGENT_RECHERCHE } from '@/test/fixtures/organismes'
import { setupUser } from '@/test/render'
import AttachAgentDrawer from './AttachAgentDrawer.vue'

type DrawerInstance = InstanceType<typeof AttachAgentDrawer>

async function renderDrawer(props: Record<string, unknown> = {}) {
  const drawer = ref<DrawerInstance | null>(null)
  const Host = defineComponent({
    emits: ['search', 'add', 'reset'],
    setup(_, { emit }) {
      return () => h(AttachAgentDrawer, {
        ref: drawer,
        open: true,
        status: 'idle',
        agent: null,
        onSearch: (email: string) => emit('search', email),
        onAdd: (role: string) => emit('add', role),
        onReset: () => emit('reset'),
        ...props,
      })
    },
  })
  const result = render(Host)
  await nextTick()
  return { ...result, drawer }
}

function emailInput() {
  return screen.getByRole('textbox', { name: 'Adresse électronique de l\'agent' })
}

describe('attachAgentDrawer', () => {
  it('rejects an invalid email without emitting a search', async () => {
    const user = setupUser()
    const { emitted } = await renderDrawer()

    await user.type(emailInput(), 'jeanne.dupont')
    await user.click(screen.getByRole('button', { name: 'Rechercher' }))

    expect(emitted().search).toBeUndefined()
    expect(screen.getByText('Renseignez une adresse électronique valide.')).toBeInTheDocument()
  })

  it('emits the trimmed email on search', async () => {
    const user = setupUser()
    const { emitted } = await renderDrawer()

    await user.type(emailInput(), '  jeanne.dupont@example.gouv.fr  ')
    await user.click(screen.getByRole('button', { name: 'Rechercher' }))

    expect(emitted().search).toEqual([['jeanne.dupont@example.gouv.fr']])
  })

  it('shows the matching agent without any editable identity field', async () => {
    await renderDrawer({ status: 'found', agent: AGENT_RECHERCHE })

    const dialog = screen.getByRole('dialog')
    expect(dialog).toHaveTextContent('Jeanne Dupont')
    expect(dialog).toHaveTextContent('Responsable recrutement')
    expect(dialog).toHaveTextContent('jeanne.dupont@example.gouv.fr')
    expect(screen.queryByRole('textbox', { name: /nom|prénom/i })).not.toBeInTheDocument()
  })

  it('attaches the agent as membre by default', async () => {
    const user = setupUser()
    const { emitted } = await renderDrawer({ status: 'found', agent: AGENT_RECHERCHE })

    await user.click(screen.getByRole('button', { name: 'Ajouter le membre' }))

    expect(emitted().add).toEqual([['agent']])
  })

  it('attaches the agent with the selected role', async () => {
    const user = setupUser()
    const { emitted } = await renderDrawer({ status: 'found', agent: AGENT_RECHERCHE })

    await user.click(screen.getByRole('radio', { name: 'Responsable' }))
    await user.click(screen.getByRole('button', { name: 'Ajouter le membre' }))

    expect(emitted().add).toEqual([['superviseur']])
  })

  it('creates and adds the member when no account matches', async () => {
    const user = setupUser()
    const { emitted } = await renderDrawer({ status: 'not-found' })

    expect(screen.getByRole('dialog')).toHaveTextContent('Aucun compte ne correspond à cette adresse.')
    await user.click(screen.getByRole('button', { name: 'Créer et ajouter' }))

    expect(emitted().add).toEqual([['agent']])
  })

  it('asks for a reset when the email changes after a search', async () => {
    const { emitted } = await renderDrawer({ status: 'found', agent: AGENT_RECHERCHE })

    await fireEvent.update(emailInput(), 'autre.agent@example.gouv.fr')

    expect(emitted().reset).toHaveLength(1)
  })

  it('surfaces a conflict on the email field', async () => {
    const { drawer } = await renderDrawer({ status: 'found', agent: AGENT_RECHERCHE })

    drawer.value!.setEmailError('Cet agent est déjà rattaché à l\'organisme.')

    expect(await screen.findByText('Cet agent est déjà rattaché à l\'organisme.')).toBeInTheDocument()
  })
})
