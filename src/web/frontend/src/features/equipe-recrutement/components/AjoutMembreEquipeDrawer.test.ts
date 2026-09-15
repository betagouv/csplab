import type { AgentOrganisme } from '@/features/organismes/types'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { nextTick } from 'vue'
import CspCombobox from '@/components/base/CspCombobox/CspCombobox.vue'
import AjoutMembreEquipeDrawer from './AjoutMembreEquipeDrawer.vue'

const AGENT_ID = 'bbbbbbbb-0001-0001-0001-000000000001'

const AGENTS: AgentOrganisme[] = [
  {
    agent_id: AGENT_ID,
    organisme_id: '11111111-1111-1111-1111-111111111111',
    nom: 'Dupont',
    prenom: 'Jeanne',
    email: 'jeanne.dupont@example.gouv.fr',
    poste: 'Chargée de recrutement',
    role: 'agent',
    date_derniere_activite: null,
    date_creation_compte: '2026-01-01T00:00:00Z',
  },
]

function mountDrawer(props: Record<string, unknown> = {}) {
  return mount(AjoutMembreEquipeDrawer, {
    props: {
      open: true,
      agents: AGENTS,
      ...props,
    },
    attachTo: document.body,
  })
}

function submitButton() {
  return document.querySelector<HTMLButtonElement>('button[type="submit"]')!
}

async function pickAgent(wrapper: ReturnType<typeof mountDrawer>, agentId: string) {
  wrapper.findComponent(CspCombobox).vm.$emit('update:modelValue', agentId)
  await nextTick()
}

async function pickRole(value: string) {
  document.querySelector<HTMLElement>(`[role="radio"][value="${value}"]`)?.click()
  await nextTick()
}

describe('ajoutMembreEquipeDrawer', () => {
  it('adds the selected agent as contributeur by default', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    await pickAgent(wrapper, AGENT_ID)
    submitButton().click()
    await nextTick()

    expect(wrapper.emitted('add')).toEqual([[
      { agent_id: AGENT_ID, recrutement_role: 'contributeur' },
    ]])
    wrapper.unmount()
  })

  it('adds the selected agent with the chosen role', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    await pickAgent(wrapper, AGENT_ID)
    await pickRole('responsable')
    submitButton().click()
    await nextTick()

    expect(wrapper.emitted('add')).toEqual([[
      { agent_id: AGENT_ID, recrutement_role: 'responsable' },
    ]])
    wrapper.unmount()
  })

  it('lists the selectable agents by their email', async () => {
    const wrapper = mountDrawer()
    await nextTick()

    expect(wrapper.findComponent(CspCombobox).props('options')).toEqual([
      { value: AGENT_ID, label: AGENTS[0].email },
    ])
    wrapper.unmount()
  })

  it('does not add anybody while no agent is selected', async () => {
    const wrapper = mountDrawer()
    await nextTick()

    expect(submitButton().disabled).toBe(true)
    submitButton().click()
    await nextTick()

    expect(wrapper.emitted('add')).toBeUndefined()
    wrapper.unmount()
  })

  it('explains the dead end when every member is already in the team', async () => {
    const wrapper = mountDrawer({ agents: [] })
    await nextTick()

    expect(document.body.textContent).toContain(
      'Tous les membres de l\'organisme font déjà partie de cette équipe.',
    )
    wrapper.unmount()
  })
})
