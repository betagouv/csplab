import { describe, expect, it } from 'vitest'
import { createMemoryHistory, createRouter } from 'vue-router'
import { routes } from './index'

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'
const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'

function resolve(path: string) {
  return createRouter({ history: createMemoryHistory(), routes }).resolve(path)
}

describe('organisme scoped routes', () => {
  it.each([
    ['/organismes', 'organismes'],
    [`/organismes/${ORGANISME_UUID}`, 'organisme'],
    [`/organismes/${ORGANISME_UUID}/etapes`, 'organisme-etapes'],
    [`/organismes/${ORGANISME_UUID}/recrutements`, 'recrutements'],
    [`/organismes/${ORGANISME_UUID}/recrutements/archives`, 'recrutements-archives'],
    [`/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}`, 'recrutement-candidatures-kanban'],
    [`/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}/liste`, 'recrutement-candidatures'],
    [`/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}/activites`, 'recrutement-activites'],
    [`/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}/etapes-recrutement`, 'recrutement-etapes-recrutement'],
  ])('%s resolves to %s', (path, name) => {
    expect(resolve(path).name).toBe(name)
  })

  it('keeps the tab meta on the recrutements list', () => {
    expect(resolve(`/organismes/${ORGANISME_UUID}/recrutements`).meta.tab).toBe('actifs')
    expect(resolve(`/organismes/${ORGANISME_UUID}/recrutements/archives`).meta.tab)
      .toBe('archives')
  })

  it('exposes both uuids on a recrutement page', () => {
    expect(resolve(`/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}`).params)
      .toEqual({ organismeUuid: ORGANISME_UUID, recrutementUuid: RECRUTEMENT_UUID })
  })

  it.each([
    '/organismes/pas-un-uuid',
    '/organismes/pas-un-uuid/recrutements',
    `/organismes/${ORGANISME_UUID}/recrutements/archivees`,
    `/organismes/${ORGANISME_UUID}/recrutements/42`,
  ])('%s falls through to not-found', (path) => {
    expect(resolve(path).name).toBe('not-found')
  })
})

describe('tab switching keeps the route params', () => {
  it.each([
    'recrutement-activites',
    'recrutement-candidatures',
  ])('inherits both params when switching to %s', async (name) => {
    const router = createRouter({ history: createMemoryHistory(), routes })
    await router.push(`/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}`)

    await router.push({ name })

    expect(router.currentRoute.value.params).toEqual({
      organismeUuid: ORGANISME_UUID,
      recrutementUuid: RECRUTEMENT_UUID,
    })
  })

  it('inherits the organisme when switching the recrutements tab', async () => {
    const router = createRouter({ history: createMemoryHistory(), routes })
    await router.push(`/organismes/${ORGANISME_UUID}/recrutements`)

    await router.push({ name: 'recrutements-archives' })

    expect(router.currentRoute.value.params).toEqual({ organismeUuid: ORGANISME_UUID })
  })
})

describe('not-found route', () => {
  it('catches unknown paths', () => {
    expect(resolve('/rien-du-tout').name).toBe('not-found')
  })

  it('does not shadow known paths', () => {
    expect(resolve('/').name).toBe('home')
    expect(resolve('/organismes').name).toBe('organismes')
  })
})
