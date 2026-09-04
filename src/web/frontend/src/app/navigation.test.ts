import { describe, expect, it } from 'vitest'
import { createMemoryHistory, createRouter } from 'vue-router'
import { routes } from '@/router'
import { isNavItemActive, navigationFor } from './navigation'

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'
const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'

const MEMBRE = { isStaff: false, organismeUuid: ORGANISME_UUID, canManageOrganisme: false }
const RESPONSABLE = { ...MEMBRE, canManageOrganisme: true }
const STAFF = { isStaff: true, organismeUuid: null, canManageOrganisme: true }

function matchedNamesFor(path: string): string[] {
  const resolved = createRouter({ history: createMemoryHistory(), routes }).resolve(path)
  return resolved.matched
    .map(record => record.name)
    .filter((name): name is string => typeof name === 'string')
}

function activeLabelsOn(path: string, items: ReturnType<typeof navigationFor>) {
  const matched = matchedNamesFor(path)
  return items.filter(item => isNavItemActive(item, matched)).map(item => item.label)
}

describe('navigationFor', () => {
  it('gives a membre only the recrutements of their organisme', () => {
    const items = navigationFor(MEMBRE)

    expect(items.map(item => item.label)).toEqual(['Recrutements'])
    expect(items[0]?.params).toEqual({ organismeUuid: ORGANISME_UUID })
  })

  it('adds the organisme settings for a responsable', () => {
    const items = navigationFor(RESPONSABLE)

    expect(items.map(item => item.label)).toEqual(['Recrutements', 'Paramètres de l\'organisme'])
    expect(items[1]?.params).toEqual({ organismeUuid: ORGANISME_UUID })
  })

  it('gives a staff user the organismes list', () => {
    expect(navigationFor(STAFF).map(item => item.label)).toEqual(['Gestion des organismes'])
  })

  it('adds the organisme entries when a staff user browses an organisme', () => {
    const items = navigationFor({ ...STAFF, organismeUuid: ORGANISME_UUID })

    expect(items.map(item => item.label)).toEqual([
      'Gestion des organismes',
      'Recrutements',
      'Paramètres de l\'organisme',
    ])
  })

  it('gives nothing to an agent without any organisme', () => {
    expect(navigationFor({ ...MEMBRE, organismeUuid: null })).toEqual([])
  })
})

describe('nav highlighting against the real route table', () => {
  const items = navigationFor(RESPONSABLE)

  it.each([
    `/organismes/${ORGANISME_UUID}/recrutements`,
    `/organismes/${ORGANISME_UUID}/recrutements/archives`,
    `/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}`,
    `/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}/liste`,
    `/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}/activites`,
    `/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}/etapes-recrutement`,
  ])('%s highlights only Recrutements', (path) => {
    expect(activeLabelsOn(path, items)).toEqual(['Recrutements'])
  })

  it.each([
    `/organismes/${ORGANISME_UUID}`,
    `/organismes/${ORGANISME_UUID}/etapes`,
  ])('%s highlights only the organisme settings', (path) => {
    expect(activeLabelsOn(path, items)).toEqual(['Paramètres de l\'organisme'])
  })

  it('highlights the staff entry on the organismes list only', () => {
    const staffItems = navigationFor(STAFF)

    expect(activeLabelsOn('/organismes', staffItems)).toEqual(['Gestion des organismes'])
    expect(activeLabelsOn(`/organismes/${ORGANISME_UUID}`, staffItems)).toEqual([])
  })
})
