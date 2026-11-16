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
import { BRIANCON_UUID as BRIANCON, ORGANISME_INCONNU_UUID as INCONNU, makeUser, MTE_UUID as MTE, ORGANISME_BRIANCON, ORGANISME_MTE, STAFF_ACTIONS } from '@/test/fixtures/utilisateur'
import { useRouteOrganisme } from './routeOrganisme'

vi.mock('@/api/organismes', () => ({
  getOrganismeDetail: vi.fn(),
}))

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
    vi.mocked(getMe).mockResolvedValue(makeUser([ORGANISME_MTE, ORGANISME_BRIANCON]))

    const { organismeUuid, organisme } = await mountAt(`/organismes/${BRIANCON}/recrutements`)

    await vi.waitFor(() => expect(organisme.value).toEqual(ORGANISME_BRIANCON))
    expect(organismeUuid.value).toBe(BRIANCON)
  })

  it('falls back to the first organisme when the url carries none', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([ORGANISME_MTE, ORGANISME_BRIANCON]))

    const { organismeUuid, routeOrganismeUuid } = await mountAt('/organismes')

    await vi.waitFor(() => expect(organismeUuid.value).toBe(MTE))
    expect(routeOrganismeUuid.value).toBeNull()
  })

  it('reads the actions of an organisme a staff user holds no role on from its detail', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([], STAFF_ACTIONS))
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
    vi.mocked(getMe).mockResolvedValue(makeUser([], STAFF_ACTIONS))
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
    vi.mocked(getMe).mockResolvedValue(makeUser([
      { ...ORGANISME_MTE, authorized_actions: ['list_organisme_agents'] },
    ], STAFF_ACTIONS))

    const { canOnOrganisme } = await mountAt(`/organismes/${MTE}/recrutements`)

    await vi.waitFor(() => expect(canOnOrganisme('list_organisme_agents')).toBe(true))
    expect(getOrganismeDetail).not.toHaveBeenCalled()
  })

  it('reads the authorized actions of the organisme in the url', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([
      { ...ORGANISME_MTE, authorized_actions: ['list_organisme_agents'] },
      { ...ORGANISME_BRIANCON, authorized_actions: ['list_recrutements'] },
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
