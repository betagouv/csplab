import type { EtapeRecrutementDetailedCandidatures } from '../types'
import { describe, expect, it } from 'vitest'
import { ref } from 'vue'
import { useKanbanSelection } from './useKanbanSelection'

const ETAPE_1_UUID = 'eeeeeeee-0001-0001-0001-000000000001'
const ETAPE_2_UUID = 'eeeeeeee-0001-0001-0001-000000000002'

const CANDIDATURE_1_UUID = 'cccccccc-0001-0001-0001-000000000001'
const CANDIDATURE_2_UUID = 'cccccccc-0001-0001-0001-000000000002'
const CANDIDATURE_3_UUID = 'cccccccc-0001-0001-0001-000000000003'

const CANDIDATURE_1 = {
  uuid: CANDIDATURE_1_UUID,
  date_soumission: '2025-06-10T09:15:00Z',
  date_derniere_activite: '2025-06-11T10:00:00Z',
  candidat: { uuid: 'dddddddd-0001-0001-0001-000000000001', nom: 'Dupont', prenom: 'Alice' },
}

const CANDIDATURE_2 = {
  uuid: CANDIDATURE_2_UUID,
  date_soumission: '2025-06-11T14:30:00Z',
  date_derniere_activite: '2025-06-12T09:15:00Z',
  candidat: { uuid: 'dddddddd-0001-0001-0001-000000000002', nom: 'Martin', prenom: 'Bruno' },
}

const CANDIDATURE_3 = {
  uuid: CANDIDATURE_3_UUID,
  date_soumission: '2025-06-08T10:00:00Z',
  date_derniere_activite: '2025-06-11T10:00:00Z',
  candidat: { uuid: 'dddddddd-0001-0001-0001-000000000003', nom: 'Bernard', prenom: 'Élise' },
}

function createEtapes(): EtapeRecrutementDetailedCandidatures[] {
  return [
    {
      etape_uuid: ETAPE_1_UUID,
      nom: 'À traiter',
      categorie: 'ENTREE',
      candidatures: [CANDIDATURE_1, CANDIDATURE_2],
    },
    {
      etape_uuid: ETAPE_2_UUID,
      nom: 'Entretien',
      categorie: 'EN_COURS',
      candidatures: [CANDIDATURE_3],
    },
  ]
}

describe('useKanbanSelection', () => {
  describe('initial state', () => {
    it('starts with empty selection', () => {
      const etapes = ref(createEtapes())
      const { selectedCount, hasSelection, currentEtapeUuid } = useKanbanSelection(etapes)

      expect(selectedCount.value).toBe(0)
      expect(hasSelection.value).toBe(false)
      expect(currentEtapeUuid.value).toBeNull()
    })
  })

  describe('toggleColumnSelection', () => {
    it('selects all candidatures in a column', () => {
      const etapes = ref(createEtapes())
      const { toggleColumnSelection, selectedCount, selectedCandidatures, isColumnSelected } = useKanbanSelection(etapes)

      toggleColumnSelection(etapes.value[0]!)

      expect(selectedCount.value).toBe(2)
      expect(isColumnSelected(ETAPE_1_UUID)).toBe(true)
      expect(selectedCandidatures.value).toHaveLength(2)
      expect(selectedCandidatures.value.map(s => s.candidature.uuid)).toEqual([CANDIDATURE_1_UUID, CANDIDATURE_2_UUID])
    })

    it('deselects all candidatures when toggling a fully selected column', () => {
      const etapes = ref(createEtapes())
      const { toggleColumnSelection, selectedCount, isColumnSelected } = useKanbanSelection(etapes)

      toggleColumnSelection(etapes.value[0]!)
      expect(isColumnSelected(ETAPE_1_UUID)).toBe(true)

      toggleColumnSelection(etapes.value[0]!)
      expect(selectedCount.value).toBe(0)
      expect(isColumnSelected(ETAPE_1_UUID)).toBe(false)
    })

    it('selects column even if partially selected before', () => {
      const etapes = ref(createEtapes())
      const { toggleColumnSelection, toggleCandidatureSelection, selectedCount, isColumnSelected } = useKanbanSelection(etapes)

      toggleCandidatureSelection(CANDIDATURE_1_UUID, ETAPE_1_UUID)
      expect(selectedCount.value).toBe(1)
      expect(isColumnSelected(ETAPE_1_UUID)).toBe(false)

      toggleColumnSelection(etapes.value[0]!)
      expect(selectedCount.value).toBe(2)
      expect(isColumnSelected(ETAPE_1_UUID)).toBe(true)
    })
  })

  describe('toggleCandidatureSelection', () => {
    it('selects a single candidature', () => {
      const etapes = ref(createEtapes())
      const { toggleCandidatureSelection, selectedCount, selectedCandidatures } = useKanbanSelection(etapes)

      toggleCandidatureSelection(CANDIDATURE_1_UUID, ETAPE_1_UUID)

      expect(selectedCount.value).toBe(1)
      expect(selectedCandidatures.value[0]?.candidature.uuid).toBe(CANDIDATURE_1_UUID)
    })

    it('deselects a candidature when toggled again', () => {
      const etapes = ref(createEtapes())
      const { toggleCandidatureSelection, selectedCount } = useKanbanSelection(etapes)

      toggleCandidatureSelection(CANDIDATURE_1_UUID, ETAPE_1_UUID)
      expect(selectedCount.value).toBe(1)

      toggleCandidatureSelection(CANDIDATURE_1_UUID, ETAPE_1_UUID)
      expect(selectedCount.value).toBe(0)
    })

    it('adds candidature to existing selection in same etape', () => {
      const etapes = ref(createEtapes())
      const { toggleCandidatureSelection, selectedCount } = useKanbanSelection(etapes)

      toggleCandidatureSelection(CANDIDATURE_1_UUID, ETAPE_1_UUID)
      toggleCandidatureSelection(CANDIDATURE_2_UUID, ETAPE_1_UUID)

      expect(selectedCount.value).toBe(2)
    })

    it('removes etape from map when last candidature is deselected', () => {
      const etapes = ref(createEtapes())
      const { toggleCandidatureSelection, selectedByEtape } = useKanbanSelection(etapes)

      toggleCandidatureSelection(CANDIDATURE_1_UUID, ETAPE_1_UUID)
      expect(selectedByEtape.value.has(ETAPE_1_UUID)).toBe(true)

      toggleCandidatureSelection(CANDIDATURE_1_UUID, ETAPE_1_UUID)
      expect(selectedByEtape.value.has(ETAPE_1_UUID)).toBe(false)
    })
  })

  describe('isColumnSelected', () => {
    it('returns false for empty selection', () => {
      const etapes = ref(createEtapes())
      const { isColumnSelected } = useKanbanSelection(etapes)

      expect(isColumnSelected(ETAPE_1_UUID)).toBe(false)
    })

    it('returns false for partial selection', () => {
      const etapes = ref(createEtapes())
      const { toggleCandidatureSelection, isColumnSelected } = useKanbanSelection(etapes)

      toggleCandidatureSelection(CANDIDATURE_1_UUID, ETAPE_1_UUID)

      expect(isColumnSelected(ETAPE_1_UUID)).toBe(false)
    })

    it('returns true when all candidatures are selected', () => {
      const etapes = ref(createEtapes())
      const { toggleCandidatureSelection, isColumnSelected } = useKanbanSelection(etapes)

      toggleCandidatureSelection(CANDIDATURE_1_UUID, ETAPE_1_UUID)
      toggleCandidatureSelection(CANDIDATURE_2_UUID, ETAPE_1_UUID)

      expect(isColumnSelected(ETAPE_1_UUID)).toBe(true)
    })

    it('returns false for unknown etape', () => {
      const etapes = ref(createEtapes())
      const { isColumnSelected } = useKanbanSelection(etapes)

      expect(isColumnSelected('ffffffff-0000-0000-0000-000000000000')).toBe(false)
    })
  })

  describe('currentEtapeUuid', () => {
    it('returns null when no selection', () => {
      const etapes = ref(createEtapes())
      const { currentEtapeUuid } = useKanbanSelection(etapes)

      expect(currentEtapeUuid.value).toBeNull()
    })

    it('returns etape uuid when selection is from single etape', () => {
      const etapes = ref(createEtapes())
      const { toggleCandidatureSelection, currentEtapeUuid } = useKanbanSelection(etapes)

      toggleCandidatureSelection(CANDIDATURE_1_UUID, ETAPE_1_UUID)
      toggleCandidatureSelection(CANDIDATURE_2_UUID, ETAPE_1_UUID)

      expect(currentEtapeUuid.value).toBe(ETAPE_1_UUID)
    })

    it('returns null when selection spans multiple etapes', () => {
      const etapes = ref(createEtapes())
      const { toggleCandidatureSelection, currentEtapeUuid } = useKanbanSelection(etapes)

      toggleCandidatureSelection(CANDIDATURE_1_UUID, ETAPE_1_UUID)
      toggleCandidatureSelection(CANDIDATURE_3_UUID, ETAPE_2_UUID)

      expect(currentEtapeUuid.value).toBeNull()
    })
  })

  describe('selectedCandidatures', () => {
    it('filters out candidatures from unknown etapes', () => {
      const etapes = ref(createEtapes())
      const { toggleCandidatureSelection, selectedCandidatures, selectedByEtape } = useKanbanSelection(etapes)

      toggleCandidatureSelection(CANDIDATURE_1_UUID, ETAPE_1_UUID)
      selectedByEtape.value = new Map([
        [ETAPE_1_UUID, new Set([CANDIDATURE_1_UUID])],
        ['ffffffff-0000-0000-0000-000000000000', new Set(['ffffffff-0000-0000-0000-000000000001'])],
      ])

      expect(selectedCandidatures.value).toHaveLength(1)
    })

    it('filters out unknown candidatures', () => {
      const etapes = ref(createEtapes())
      const { selectedCandidatures, selectedByEtape } = useKanbanSelection(etapes)

      selectedByEtape.value = new Map([
        [ETAPE_1_UUID, new Set([CANDIDATURE_1_UUID, 'ffffffff-0000-0000-0000-000000000099'])],
      ])

      expect(selectedCandidatures.value).toHaveLength(1)
      expect(selectedCandidatures.value[0]?.candidature.uuid).toBe(CANDIDATURE_1_UUID)
    })
  })

  describe('clearSelection', () => {
    it('clears all selections', () => {
      const etapes = ref(createEtapes())
      const { toggleColumnSelection, clearSelection, selectedCount, hasSelection } = useKanbanSelection(etapes)

      toggleColumnSelection(etapes.value[0]!)
      expect(selectedCount.value).toBe(2)

      clearSelection()

      expect(selectedCount.value).toBe(0)
      expect(hasSelection.value).toBe(false)
    })
  })

  describe('hasSelection', () => {
    it('returns false when no selection', () => {
      const etapes = ref(createEtapes())
      const { hasSelection } = useKanbanSelection(etapes)

      expect(hasSelection.value).toBe(false)
    })

    it('returns true when there is a selection', () => {
      const etapes = ref(createEtapes())
      const { toggleCandidatureSelection, hasSelection } = useKanbanSelection(etapes)

      toggleCandidatureSelection(CANDIDATURE_1_UUID, ETAPE_1_UUID)

      expect(hasSelection.value).toBe(true)
    })
  })
})
