import type { AgentRecherche } from '@/features/organismes/types'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { nextTick } from 'vue'
import AjoutMembreEquipeDrawer from './AjoutMembreEquipeDrawer.vue'

const AGENT: AgentRecherche = {
  agent_id: 'bbbbbbbb-0001-0001-0001-000000000001',
  email: 'jeanne.dupont@example.gouv.fr',
  prenom: 'Jeanne',
  nom: 'Dupont',
  intitule_poste: 'Chargée de recrutement',
}

function mountDrawer(props: Record<string, unknown> = {}) {
  return mount(AjoutMembreEquipeDrawer, {
    props: {
      open: true,
      status: 'idle',
      ...props,
    },
    attachTo: document.body,
  })
}

function submitButton() {
  return document.querySelector<HTMLButtonElement>('button[type="submit"]')
}

async function pickRole(value: string) {
  document.querySelector<HTMLElement>(`[role="radio"][value="${value}"]`)?.click()
  await nextTick()
}

describe('ajoutMembreEquipeDrawer', () => {
  it('offers no role and no submission before the search has answered', async () => {
    const wrapper = mountDrawer()
    await nextTick()

    expect(submitButton()).toBeNull()
    expect(document.querySelector('[role="radiogroup"]')).toBeNull()
    wrapper.unmount()
  })

  it('adds the found agent as contributeur by default', async () => {
    const wrapper = mountDrawer({ status: 'found', agent: AGENT })
    await nextTick()

    expect(document.body.textContent).toContain('Jeanne Dupont')
    expect(submitButton()!.textContent).toContain('Ajouter le membre')
    submitButton()!.click()
    await nextTick()

    expect(wrapper.emitted('add')).toEqual([['contributeur']])
    wrapper.unmount()
  })

  it('adds the found agent with the chosen role', async () => {
    const wrapper = mountDrawer({ status: 'found', agent: AGENT })
    await nextTick()
    await pickRole('responsable')
    submitButton()!.click()
    await nextTick()

    expect(wrapper.emitted('add')).toEqual([['responsable']])
    wrapper.unmount()
  })

  it('announces the account creation when no agent matches the email', async () => {
    const wrapper = mountDrawer({ status: 'not-found' })
    await nextTick()

    expect(document.body.textContent).toContain('Un compte sera créé')
    expect(submitButton()!.textContent).toContain('Créer et ajouter')
    wrapper.unmount()
  })
})
