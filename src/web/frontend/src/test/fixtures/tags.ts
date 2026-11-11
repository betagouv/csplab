import type { Tag } from '@/features/tags/types'

export const TO_RECALL: Tag = { uuid: 'aaaaaaaa-0001-0001-0001-000000000001', name: 'À rappeler', category: 'candidature', color: 'bleu', usage_count: 0 }

export const TAGS: Tag[] = [
  TO_RECALL,
  { uuid: 'aaaaaaaa-0001-0001-0001-000000000002', name: 'Profil senior', category: 'candidature', color: 'vert', usage_count: 0 },
  { uuid: 'aaaaaaaa-0001-0001-0001-000000000003', name: 'Entretien', category: 'note', color: 'jaune', usage_count: 0 },
]

export const CREATED_TAG: Tag = { uuid: 'aaaaaaaa-0001-0001-0001-000000000004', name: 'Synthèse', category: 'note', color: 'bleu', usage_count: 0 }
