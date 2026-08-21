import { describe, expect, it } from 'vitest'
import { createMemoryHistory, createRouter } from 'vue-router'
import { routes } from './index'

const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'

function resolve(path: string) {
  return createRouter({ history: createMemoryHistory(), routes }).resolve(path)
}

describe('recrutements tab routes', () => {
  it('maps /mes-recrutements to the actifs tab', () => {
    const route = resolve('/mes-recrutements')
    expect(route.name).toBe('mes-recrutements')
    expect(route.meta.tab).toBe('actifs')
  })

  it('maps /mes-recrutements/archives to the archives tab', () => {
    const route = resolve('/mes-recrutements/archives')
    expect(route.name).toBe('mes-recrutements-archives')
    expect(route.meta.tab).toBe('archives')
  })

  it('prefers the archives tab over the recrutement detail route', () => {
    expect(resolve('/mes-recrutements/archives').name).not.toBe('recrutement-candidatures-kanban')
  })
})

describe('recrutement detail routes', () => {
  it('matches a uuid segment', () => {
    const route = resolve(`/mes-recrutements/${RECRUTEMENT_UUID}`)
    expect(route.name).toBe('recrutement-candidatures-kanban')
    expect(route.params.recrutementUuid).toBe(RECRUTEMENT_UUID)
  })

  it('matches the etapes route under a uuid segment', () => {
    const route = resolve(`/mes-recrutements/${RECRUTEMENT_UUID}/etapes-recrutement`)
    expect(route.name).toBe('recrutement-etapes-recrutement')
  })

  it('falls through to not-found when the segment is not a uuid', () => {
    expect(resolve('/mes-recrutements/archivees').name).toBe('not-found')
    expect(resolve('/mes-recrutements/42').name).toBe('not-found')
  })
})

describe('not-found route', () => {
  it('catches unknown paths', () => {
    expect(resolve('/rien-du-tout').name).toBe('not-found')
  })

  it('does not shadow known paths', () => {
    expect(resolve('/').name).toBe('home')
    expect(resolve('/organismes').name).toBe('organismes')
    expect(resolve('/mon-organisme').name).toBe('mon-organisme')
  })
})
