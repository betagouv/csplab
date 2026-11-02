import type { TagCategory, TagColor } from '../types'
import type { CspTagAccent } from '@/components/base/CspTag/tag'

export const TAG_NAME_MAX_LENGTH = 25

export const TAG_CATEGORIES: TagCategory[] = ['candidature', 'note', 'recrutement_agent']

export const TAG_CATEGORY_OPTIONS_ORDER: TagCategory[] = ['candidature', 'recrutement_agent', 'note']

export const TAG_CATEGORY_TEXTS: Record<TagCategory, { title: string, option: string, description: string }> = {
  candidature: {
    title: 'Candidature',
    option: 'Candidature',
    description: 'Affichée sur la candidature. Permet de qualifier rapidement les profils candidats.',
  },
  note: {
    title: 'Note',
    option: 'Note',
    description: 'Affichée sur les notes d\'une candidature. Permet d\'identifier la nature des notes.',
  },
  recrutement_agent: {
    title: 'Équipe de recrutement',
    option: 'Membre recrutement',
    description: 'Affichée dans l\'équipe d\'un recrutement. Permet d\'indiquer ce que fait chaque membre sur ce recrutement.',
  },
}

export const DEFAULT_TAG_COLOR: TagColor = 'bleu'

export const TAG_COLOR_LABELS: Record<TagColor, string> = {
  bleu: 'Bleu',
  vert: 'Vert',
  menthe: 'Menthe',
  violet: 'Violet',
  rose: 'Rose',
  orange: 'Orange',
  beige: 'Beige',
  jaune: 'Jaune',
  gris: 'Gris',
}

export const TAG_COLOR_ACCENTS: Record<TagColor, CspTagAccent | undefined> = {
  bleu: 'blue-cumulus',
  vert: 'green-emeraude',
  menthe: 'green-menthe',
  violet: 'purple-glycine',
  rose: 'pink-macaron',
  orange: 'orange-terre-battue',
  beige: 'beige-gris-galet',
  jaune: 'yellow-tournesol',
  gris: undefined,
}
