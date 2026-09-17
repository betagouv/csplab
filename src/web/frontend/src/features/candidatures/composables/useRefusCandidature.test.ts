import type { EtapeRecrutement, EtapeRecrutementDetailedCandidatures } from '../types'
import { describe, expect, it, vi } from 'vitest'
import { ref } from 'vue'
import { useRefusCandidature } from './useRefusCandidature'

const ETAPE_ENTREE = 'cccccccc-0001-0001-0001-000000000001'
const ETAPE_REFUS = 'cccccccc-0001-0001-0001-000000000009'
const CANDIDATURE_ALICE = 'dddddddd-0001-0001-0001-000000000001'

const ETAPES: EtapeRecrutement[] = [
  { etape_uuid: ETAPE_ENTREE, nom: 'Réception', categorie: 'ENTREE' },
  { etape_uuid: ETAPE_REFUS, nom: 'Refusée', categorie: 'REFUS' },
]

const KANBAN: EtapeRecrutementDetailedCandidatures[] = [
  {
    etape_uuid: ETAPE_ENTREE,
    nom: 'Réception',
    categorie: 'ENTREE',
    candidatures: [{
      uuid: CANDIDATURE_ALICE,
      date_soumission: '2025-06-10T09:15:00Z',
      date_derniere_activite: '2025-06-11T10:00:00Z',
      candidat: { uuid: 'eeeeeeee-0001-0001-0001-000000000001', nom: 'Dupont', prenom: 'Alice' },
    }],
  },
  { etape_uuid: ETAPE_REFUS, nom: 'Refusée', categorie: 'REFUS', candidatures: [] },
]

const TOWARDS_REFUS = { sourceColumnId: ETAPE_ENTREE, targetColumnId: ETAPE_REFUS, cardId: CANDIDATURE_ALICE, cardIndex: 0 }

function setup() {
  const moveCandidature = vi.fn()
  const refus = useRefusCandidature({
    recrutementEtapes: ref(ETAPES),
    candidatureKanban: ref(KANBAN),
    moveCandidature,
  })
  return { refus, moveCandidature }
}

describe('useRefusCandidature', () => {
  it('moves right away when the drop does not target the refus etape', () => {
    const { refus, moveCandidature } = setup()
    const move = { ...TOWARDS_REFUS, targetColumnId: ETAPE_ENTREE }

    refus.handleMove(move)

    expect(moveCandidature).toHaveBeenCalledWith(move)
    expect(refus.isDialogOpen.value).toBe(false)
  })

  it('holds a drop on the refus etape until the recruteur confirms', () => {
    const { refus, moveCandidature } = setup()

    refus.handleMove(TOWARDS_REFUS)

    expect(moveCandidature).not.toHaveBeenCalled()
    expect(refus.isDialogOpen.value).toBe(true)
    expect(refus.description.value).toContain('Alice Dupont')

    refus.confirm()

    expect(moveCandidature).toHaveBeenCalledWith(TOWARDS_REFUS)
    expect(refus.isDialogOpen.value).toBe(false)
  })

  it('leaves the candidature in place when the recruteur cancels', () => {
    const { refus, moveCandidature } = setup()

    refus.handleMove(TOWARDS_REFUS)
    refus.cancel()

    expect(moveCandidature).not.toHaveBeenCalled()
    expect(refus.isDialogOpen.value).toBe(false)
  })
})
