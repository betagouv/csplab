import type { OrganismeRole, Utilisateur } from '@/api/utilisateur'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import { getOrganismeDetail } from '@/api/organismes'
import { getMe } from '@/api/utilisateur'
import { routes } from '@/router/routes'
import { ORGANISME_DETAIL } from '@/test/fixtures/organismes'
import { useRouteOrganisme } from './routeOrganisme'

vi.mock('@/api/organismes', () => ({
  getOrganismeDetail: vi.fn(),
}))

const MTE = 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'
const BRIANCON = 'b2b2b2b2-b2b2-b2b2-b2b2-b2b2b2b2b2b2'
const INCONNU = 'c3c3c3c3-c3c3-c3c3-c3c3-c3c3c3c3c3c3'

const ROLE_MTE: OrganismeRole = { organisme_uuid: MTE, nom: 'Ministère de la Transition Écologique', role: 'superviseur' }
const ROLE_BRIANCON: OrganismeRole = { organisme_uuid: BRIANCON, nom: 'Commune de Briançon', role: 'agent' }

function makeUser(
  organismeRoles: Utilisateur['organisme_roles'],
  isStaff = false,
  organismes: Utilisateur['organismes'] = [],
): Utilisateur {
  return {
    email: 'marie.dupont@example.gouv.fr',
    prenom: 'Marie',
    nom: 'Dupont',
    is_staff: isStaff,
    authorized_actions: isStaff ? ['list_organismes'] : [],
    organismes,
    organisme_roles: organismeRoles,
  }
}

async function mountAt(path: string) {
  const router = createRouter({ history: createMemoryHistory(), routes })
  await router.push(path)

  let result!: ReturnType<typeof useRouteOrganisme>

  mount(defineComponent({
    setup() {
      result = useRouteOrganisme()
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada, router],
    },
  })

  return result
}

describe('useRouteOrganisme', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset()
    vi.mocked(getOrganismeDetail).mockReset()
  })

  it('takes the organisme from the url', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))

    const { organismeUuid, organisme } = await mountAt(`/organismes/${BRIANCON}/recrutements`)

    await vi.waitFor(() => expect(organisme.value).toEqual(ROLE_BRIANCON))
    expect(organismeUuid.value).toBe(BRIANCON)
  })

  it('falls back to the first organisme when the url carries none', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))

    const { organismeUuid, routeOrganismeUuid } = await mountAt('/organismes')

    await vi.waitFor(() => expect(organismeUuid.value).toBe(MTE))
    expect(routeOrganismeUuid.value).toBeNull()
  })

  it('reads the actions of an organisme a staff user holds no role on from its detail', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([], true))
    vi.mocked(getOrganismeDetail).mockResolvedValue({ ...ORGANISME_DETAIL, uuid: INCONNU, authorized_actions: ['list_organisme_agents'] })

    const { organismeUuid, organisme, canOnOrganisme } = await mountAt(
      `/organismes/${INCONNU}/recrutements`,
    )

    await vi.waitFor(() => expect(canOnOrganisme('list_organisme_agents')).toBe(true))
    expect(canOnOrganisme('set_recrutements_responsable')).toBe(false)
    expect(getOrganismeDetail).toHaveBeenCalledWith({ organismeUuid: INCONNU })
    expect(organismeUuid.value).toBe(INCONNU)
    expect(organisme.value).toBeNull()
  })

  it('tells the actions of an organisme a staff user holds no role on are loading until its detail arrives', async () => {
    let resolveDetail!: (detail: typeof ORGANISME_DETAIL) => void
    vi.mocked(getMe).mockResolvedValue(makeUser([], true))
    vi.mocked(getOrganismeDetail).mockReturnValue(new Promise((resolve) => {
      resolveDetail = resolve
    }))

    const { actionsPending } = await mountAt(`/organismes/${INCONNU}/recrutements`)

    await vi.waitFor(() => expect(getOrganismeDetail).toHaveBeenCalled())
    expect(actionsPending.value).toBe(true)

    resolveDetail({ ...ORGANISME_DETAIL, uuid: INCONNU })

    await vi.waitFor(() => expect(actionsPending.value).toBe(false))
  })

  it('does not read the detail of an organisme the staff user belongs to', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE], true, [
      { uuid: MTE, nom: ROLE_MTE.nom, authorized_actions: ['list_organisme_agents'] },
    ]))

    const { canOnOrganisme } = await mountAt(`/organismes/${MTE}/recrutements`)

    await vi.waitFor(() => expect(canOnOrganisme('list_organisme_agents')).toBe(true))
    expect(getOrganismeDetail).not.toHaveBeenCalled()
  })

  it('reads the authorized actions of the organisme in the url', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON], false, [
      { uuid: MTE, nom: ROLE_MTE.nom, authorized_actions: ['list_organisme_agents'] },
      { uuid: BRIANCON, nom: ROLE_BRIANCON.nom, authorized_actions: ['list_recrutements'] },
    ]))

    const { canOnOrganisme } = await mountAt(`/organismes/${BRIANCON}/recrutements`)

    await vi.waitFor(() => expect(canOnOrganisme('list_recrutements')).toBe(true))
    expect(canOnOrganisme('list_organisme_agents')).toBe(false)
  })

  it('exposes no organisme for an agent without any role', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([]))

    const { organismeUuid, organisme } = await mountAt('/organismes')

    await vi.waitFor(() => expect(getMe).toHaveBeenCalled())
    expect(organismeUuid.value).toBeNull()
    expect(organisme.value).toBeNull()
  })
})
