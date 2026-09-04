import type { Utilisateur } from '@/api/utilisateur'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { routes } from '@/router'
import { useRouteOrganisme } from './routeOrganisme'

vi.mock('@/api/utilisateur', () => ({
  getMe: vi.fn(),
}))

const MTE = 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'
const BRIANCON = 'b2b2b2b2-b2b2-b2b2-b2b2-b2b2b2b2b2b2'
const INCONNU = 'c3c3c3c3-c3c3-c3c3-c3c3-c3c3c3c3c3c3'

const ROLE_MTE = { organisme_uuid: MTE, nom: 'Ministère de la Transition Écologique', role: 'responsable' }
const ROLE_BRIANCON = { organisme_uuid: BRIANCON, nom: 'Commune de Briançon', role: 'membre' }

function makeUser(
  organismeRoles: Utilisateur['organisme_roles'],
  isStaff = false,
): Utilisateur {
  return {
    email: 'marie.dupont@example.gouv.fr',
    prenom: 'Marie',
    nom: 'Dupont',
    is_staff: isStaff,
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
  })

  it('takes the organisme from the url', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))

    const { organismeUuid, organisme } = await mountAt(`/organismes/${BRIANCON}/recrutements`)

    await vi.waitFor(() => expect(organisme.value).toEqual(ROLE_BRIANCON))
    expect(organismeUuid.value).toBe(BRIANCON)
  })

  it('falls back to the first organisme when the url carries none', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))

    const { organismeUuid, routeOrganismeUuid } = await mountAt('/')

    await vi.waitFor(() => expect(organismeUuid.value).toBe(MTE))
    expect(routeOrganismeUuid.value).toBeNull()
  })

  it('lets a responsable manage their organisme', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_MTE]))

    const { canManageOrganisme } = await mountAt(`/organismes/${MTE}/recrutements`)

    await vi.waitFor(() => expect(canManageOrganisme.value).toBe(true))
  })

  it('does not let a membre manage their organisme', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ROLE_BRIANCON]))

    const { canManageOrganisme } = await mountAt(`/organismes/${BRIANCON}/recrutements`)

    await vi.waitFor(() => expect(canManageOrganisme.value).toBe(false))
  })

  it('lets a staff user manage an organisme they hold no role on', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([], true))

    const { organismeUuid, organisme, canManageOrganisme } = await mountAt(
      `/organismes/${INCONNU}/recrutements`,
    )

    await vi.waitFor(() => expect(canManageOrganisme.value).toBe(true))
    expect(organismeUuid.value).toBe(INCONNU)
    expect(organisme.value).toBeNull()
  })

  it('exposes no organisme for an agent without any role', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([]))

    const { organismeUuid, organisme, canManageOrganisme } = await mountAt('/')

    await vi.waitFor(() => expect(getMe).toHaveBeenCalled())
    expect(organismeUuid.value).toBeNull()
    expect(organisme.value).toBeNull()
    expect(canManageOrganisme.value).toBe(false)
  })
})
