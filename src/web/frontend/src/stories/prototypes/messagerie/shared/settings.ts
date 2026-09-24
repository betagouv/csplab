import type { Order, Presentation, Preset, Settings, SideRule } from './types'

export type Auto<T extends string> = 'auto' | T

export interface SettingsArgs {
  presentation: Presentation
  regleDeCote: SideRule
  reglages: Preset
  saisie: Auto<'ouverte' | 'bouton'>
  dates: Auto<'relatives' | 'absolues'>
  lu: Auto<'affiche' | 'masque'>
  etat: Auto<'affiche' | 'masque'>
  avancement: Auto<'affiche' | 'masque'>
  ordre: Order
  delai: boolean
}

type Viewer = 'recruteur' | 'candidat'

const PRESETS: Record<Preset, (viewer: Viewer) => Pick<Settings, 'composer' | 'dates' | 'readReceipts' | 'waitingLine' | 'progress'>> = {
  immediat: () => ({
    composer: 'ouverte',
    dates: 'relatives',
    readReceipts: true,
    waitingLine: false,
    progress: false,
  }),
  differe: viewer => ({
    composer: 'bouton',
    dates: 'absolues',
    readReceipts: viewer === 'recruteur',
    waitingLine: true,
    progress: true,
  }),
}

function flag(value: Auto<'affiche' | 'masque'>, fallback: boolean): boolean {
  return value === 'auto' ? fallback : value === 'affiche'
}

export function resolveSettings(args: SettingsArgs, viewer: Viewer): Settings {
  const preset = PRESETS[args.reglages](viewer)
  return {
    presentation: args.presentation,
    sideRule: args.regleDeCote,
    composer: args.saisie === 'auto' ? preset.composer : args.saisie,
    dates: args.dates === 'auto' ? preset.dates : args.dates,
    readReceipts: flag(args.lu, preset.readReceipts),
    waitingLine: flag(args.etat, preset.waitingLine),
    progress: flag(args.avancement, preset.progress),
    order: args.ordre,
    indicativeDelay: args.delai,
  }
}

export const DEFAULT_ARGS: SettingsArgs = {
  presentation: 'correspondance',
  regleDeCote: 'equipe',
  reglages: 'differe',
  saisie: 'auto',
  dates: 'auto',
  lu: 'auto',
  etat: 'auto',
  avancement: 'auto',
  ordre: 'chronologique',
  delai: false,
}

const AUTO_LABEL = 'Selon les réglages'

export const SETTINGS_ARG_TYPES = {
  presentation: {
    name: 'Présentation',
    control: { type: 'inline-radio' },
    options: ['bulles', 'pile', 'correspondance'],
    labels: { bulles: 'Bulles', pile: 'Pile de messages', correspondance: 'Correspondance' },
  },
  regleDeCote: {
    name: 'Côté des bulles',
    control: { type: 'inline-radio' },
    options: ['equipe', 'moi'],
    labels: { equipe: 'Équipe à droite', moi: 'Moi à droite' },
    if: { arg: 'presentation', eq: 'bulles' },
  },
  reglages: {
    name: 'Indices d’immédiateté',
    control: { type: 'inline-radio' },
    options: ['immediat', 'differe'],
    labels: { immediat: 'Immédiat', differe: 'Différé' },
  },
  saisie: {
    name: 'Zone de saisie',
    control: { type: 'select' },
    options: ['auto', 'ouverte', 'bouton'],
    labels: { auto: AUTO_LABEL, ouverte: 'Ouverte en permanence', bouton: 'Ouverte par « Répondre »' },
  },
  dates: {
    name: 'Dates',
    control: { type: 'select' },
    options: ['auto', 'relatives', 'absolues'],
    labels: { auto: AUTO_LABEL, relatives: 'Relatives', absolues: 'Absolues' },
  },
  lu: {
    name: 'Accusé de lecture',
    control: { type: 'select' },
    options: ['auto', 'affiche', 'masque'],
    labels: { auto: AUTO_LABEL, affiche: 'Affiché', masque: 'Masqué' },
  },
  etat: {
    name: 'Ligne d’attente',
    control: { type: 'select' },
    options: ['auto', 'affiche', 'masque'],
    labels: { auto: AUTO_LABEL, affiche: 'Affichée', masque: 'Masquée' },
  },
  avancement: {
    name: 'Avancement côté candidat',
    control: { type: 'select' },
    options: ['auto', 'affiche', 'masque'],
    labels: { auto: AUTO_LABEL, affiche: 'Affiché', masque: 'Masqué' },
  },
  ordre: {
    name: 'Ordre',
    control: { type: 'inline-radio' },
    options: ['chronologique', 'recent-en-haut'],
    labels: { 'chronologique': 'Chronologique', 'recent-en-haut': 'Plus récent en haut' },
  },
  delai: {
    name: 'Délai indicatif côté candidat',
    control: { type: 'boolean' },
  },
} as const
