import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { nextTick } from 'vue'
import { AGENT_ORGANISME, AGENT_UUID } from '@/test/fixtures/organismes'
import { setupUser } from '@/test/render'
import AjoutMembreEquipeDrawer from './AjoutMembreEquipeDrawer.vue'

async function renderDrawer(props: Record<string, unknown> = {}) {
  const result = render(AjoutMembreEquipeDrawer, {
    props: { open: true, agents: [AGENT_ORGANISME], ...props },
  })
  await nextTick()
  return result
}

function submitButton() {
  return screen.getByRole('button', { name: 'Ajouter le membre' })
}

async function pickAgent(user: ReturnType<typeof setupUser>, email: string) {
  await user.click(screen.getByRole('combobox', { name: 'Membre de l\'organisme' }))
  await user.click(await screen.findByRole('option', { name: email }))
}

describe('ajoutMembreEquipeDrawer', () => {
  it('adds the selected agent as contributeur by default', async () => {
    const user = setupUser()
    const { emitted } = await renderDrawer()

    await pickAgent(user, AGENT_ORGANISME.email)
    await user.click(submitButton())

    expect(emitted().add).toEqual([[{ agent_id: AGENT_UUID, recrutement_role: 'contributeur' }]])
  })

  it('adds the selected agent with the chosen role', async () => {
    const user = setupUser()
    const { emitted } = await renderDrawer()

    await pickAgent(user, AGENT_ORGANISME.email)
    await user.click(screen.getByRole('radio', { name: 'Responsable' }))
    await user.click(submitButton())

    expect(emitted().add).toEqual([[{ agent_id: AGENT_UUID, recrutement_role: 'responsable' }]])
  })

  it('lists the selectable agents by their email', async () => {
    const user = setupUser()
    await renderDrawer()

    await user.click(screen.getByRole('combobox', { name: 'Membre de l\'organisme' }))

    expect((await screen.findAllByRole('option')).map(option => option.textContent?.trim()))
      .toEqual([AGENT_ORGANISME.email])
  })

  it('does not add anybody while no agent is selected', async () => {
    const user = setupUser()
    const { emitted } = await renderDrawer()

    expect(submitButton()).toBeDisabled()
    await user.click(submitButton())

    expect(emitted().add).toBeUndefined()
  })

  it('explains the dead end when every member is already in the team', async () => {
    await renderDrawer({ agents: [] })

    expect(screen.getByRole('dialog')).toHaveTextContent('Tous les membres de l\'organisme font déjà partie de cette équipe.')
  })
})
