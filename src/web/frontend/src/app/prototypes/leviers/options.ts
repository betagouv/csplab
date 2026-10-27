import type { Decorator } from '@storybook/vue3-vite'
import { onBeforeUnmount } from 'vue'

// Values of existing role variables, written on the root element; an option without values keeps the kit.
export type Valeurs = Record<`--${string}`, string>

export interface LevierOption {
  // Kebab-case name of the story export that renders the option alone
  id: string
  nom: string
  valeurs: Valeurs
  // Values that replace those of valeurs in the dark theme
  sombre?: Valeurs
  // Values that replace those of valeurs when the system asks for reduced motion
  reduit?: Valeurs
  // Attributes of the root element that select a setting of styles/themes, such as data-csp-backdrop
  attributs?: Record<`data-csp-${string}`, string>
}

// Controls (button, field), indicators (checkbox), surfaces (card, table), floating layers (menu, toast), regions (kanban column)
function rayons(controle: string, surface: string, region: string, interne: string): Valeurs {
  return {
    '--csp-action-radius': controle,
    '--csp-field-radius': controle,
    '--csp-indicator-radius': interne,
    '--csp-surface-radius': surface,
    '--csp-overlap-radius': surface,
    '--csp-region-radius': region,
  }
}

export const ARRONDIS: LevierOption[] = [
  { id: 'droits', nom: '0 et 4 px, kit actuel', valeurs: {} },
  { id: 'legers', nom: '2 et 4 px', valeurs: rayons('2px', '4px', '4px', '2px') },
  { id: 'moyens', nom: '4 et 8 px', valeurs: rayons('4px', '8px', '12px', '2px') },
  { id: 'marques', nom: '8 et 12 px', valeurs: rayons('8px', '12px', '16px', '4px') },
  // Control 6 px, card 10 px, panel 16 px; an element in a narrow container takes the role below
  { id: 'roles', nom: 'Rayons par rôle, 6, 10 et 16 px', valeurs: rayons('0.375rem', '0.625rem', '1rem', '0.375rem') },
]

// A transparent shadow: components list these variables with other shadows, where none is invalid
export const SANS_OMBRE = '0 0 #0000'

// A quarter of the beige-gris-galet step of the same rank in a DSFR grey
function grisChaud(gris: string, beige: string, part = 25): string {
  return `color-mix(in oklab, var(${gris}) ${100 - part}%, var(${beige}))`
}

// Backgrounds of the zones: canvas, nav, chrome, regions
export const ZONES: LevierOption[] = [
  { id: 'kit', nom: 'Kit actuel', valeurs: {} },
  {
    id: 'gris-dsfr',
    nom: 'Gris du DSFR',
    valeurs: {
      '--csp-canvas-background': 'var(--background-alt-grey)',
      '--csp-nav-background': 'var(--background-alt-grey)',
      '--csp-region-background': 'var(--background-contrast-grey)',
      '--csp-region-border-color': 'transparent',
    },
  },
  {
    id: 'gris-chauds',
    nom: 'Gris à peine chauds',
    valeurs: {
      '--background-alt-grey': grisChaud('--grey-975-75', '--beige-gris-galet-950-100'),
      '--border-default-grey': grisChaud('--grey-900-175', '--beige-gris-galet-850-200', 20),
      '--text-mention-grey': grisChaud('--grey-425-625', '--beige-gris-galet-sun-407-moon-821', 20),
      '--csp-neutral-background': grisChaud('--grey-950-100', '--beige-gris-galet-925-125'),
    },
  },
  {
    id: 'cadre-blanc',
    nom: 'Cadre blanc',
    valeurs: {
      '--csp-canvas-background': 'var(--background-alt-grey)',
      '--csp-nav-background': 'var(--background-default-grey)',
      '--csp-chrome-background': 'var(--background-default-grey)',
      '--csp-region-background': 'var(--background-contrast-grey)',
      '--csp-region-border-color': 'transparent',
    },
  },
]

const FILET = 'var(--border-default-grey)'
const CANEVAS = 'var(--background-alt-grey)'

// Chrome (sidebar, page header and the line between them and the content), canvas, kanban columns and cards,
// with these surface rules: the content stays flat, the shadow belongs to the layers
// above it such as the panel, a container splits inside with soft lines, and the panel lays its sections on the canvas.
function chrome(barre: string, entete: string, filet: string, canevas: string, colonne: string, carte: string): Valeurs {
  return {
    '--csp-nav-background': barre,
    '--csp-chrome-background': entete,
    '--csp-chrome-border-color': filet,
    '--csp-canvas-background': canevas,
    '--csp-region-background': 'var(--background-default-grey)',
    '--csp-region-border-color': colonne,
    '--csp-raised-border-color': carte,
    '--csp-raised-shadow': SANS_OMBRE,
    '--csp-raised-shadow-hover': SANS_OMBRE,
    '--csp-raised-shadow-drag': SANS_OMBRE,
    '--csp-divider-color': FILET,
    '--csp-kanban-gap': 'var(--csp-space-5)',
    '--csp-kanban-column-padding': 'var(--csp-space-4)',
    '--csp-kanban-column-header-padding-bottom': 'var(--csp-space-3)',
    '--csp-kanban-column-header-divider-width': '1px',
    '--csp-panel-background': canevas,
    '--csp-document-frame-header-background': 'var(--background-default-grey)',
    '--csp-aside-background': 'var(--background-default-grey)',
    '--csp-aside-border-color': colonne,
  }
}

const BLANC = 'var(--background-default-grey)'

export const CHROME: LevierOption[] = [
  { id: 'kit', nom: 'Aujourd’hui', valeurs: {} },
  {
    id: 'teinte-unifie',
    nom: 'Chrome teinté unifié',
    valeurs: chrome('var(--background-contrast-grey)', 'var(--background-contrast-grey)', FILET, CANEVAS, FILET, FILET),
  },
  {
    id: 'tout-blanc',
    nom: 'Tout blanc',
    valeurs: chrome(BLANC, BLANC, FILET, BLANC, FILET, FILET),
  },
  {
    id: 'separe',
    nom: 'Barre latérale teintée, en-tête blanc',
    valeurs: chrome('var(--background-alt-grey)', BLANC, FILET, CANEVAS, FILET, FILET),
  },
  {
    id: 'blanc-bordures-fermes',
    nom: 'Chrome blanc, bordures fermes',
    valeurs: chrome(BLANC, BLANC, FILET, CANEVAS, FILET, FILET),
  },
]

function role(nom: string, taille: string, interligne: string, graisse: number): Valeurs {
  return {
    [`--csp-text-${nom}-size`]: taille,
    [`--csp-text-${nom}-line-height`]: interligne,
    [`--csp-text-${nom}-weight`]: String(graisse),
  }
}

// Text roles on the DSFR scale: h3, h5, h6, then the sm and xs text sizes; CspCard keeps
// the title size set by its size prop
export const TYPOGRAPHIE: LevierOption[] = [
  { id: 'kit', nom: 'Kit actuel', valeurs: {} },
  {
    id: 'roles',
    nom: 'Rôles de texte sur l\'échelle du DSFR',
    valeurs: {
      ...role('page-title', '1.75rem', '2.25rem', 700),
      ...role('section-title', '1.25rem', '1.75rem', 700),
      ...role('group-title', '0.875rem', '1.5rem', 700),
      ...role('label', '0.875rem', '1.5rem', 500),
      ...role('meta', '0.875rem', '1.5rem', 400),
      ...role('caption', '0.75rem', '1.25rem', 400),
    },
  },
]

// A message is a frame in the colour of its tone, without side bar; an empty state is a card with a medallion, a section title and a description in metadata size
export const MESSAGES: LevierOption[] = [
  { id: 'kit', nom: 'Kit actuel', valeurs: {} },
  {
    id: 'cadres',
    nom: 'Cadre du ton et état vide en carte',
    valeurs: {
      '--csp-message-bar-width': '0px',
      '--csp-message-border-width': '0px',
      '--csp-message-frame-width': '1px',
      '--csp-empty-state-background': 'var(--background-default-grey)',
      '--csp-empty-state-frame-width': '1px',
      '--csp-empty-state-padding-block': 'var(--csp-space-12)',
      '--csp-empty-state-gap': 'var(--csp-space-3)',
      '--csp-empty-state-icon-padding': 'var(--csp-space-3)',
      '--csp-empty-state-icon-background': 'var(--background-action-low-blue-france)',
      '--csp-empty-state-icon-color': 'var(--text-action-high-blue-france)',
      '--csp-empty-state-icon-radius': 'var(--csp-surface-radius, 0.25rem)',
      '--csp-empty-state-title-size': '1.125rem',
      '--csp-empty-state-title-weight': '600',
      '--csp-empty-state-description-size': '0.875rem',
      '--csp-panel-background': CANEVAS,
    },
  },
]

// A table lies flat on its card, with column headers as small capitals in mention grey
export const COLLECTIONS: LevierOption[] = [
  { id: 'kit', nom: 'Kit actuel', valeurs: {} },
  {
    id: 'petites-capitales',
    nom: 'En-têtes en petites capitales et filets doux',
    valeurs: {
      '--csp-table-head-background': 'transparent',
      '--csp-table-footer-background': 'transparent',
      '--csp-table-divider-color': FILET,
      '--csp-table-header-size': '0.75rem',
      '--csp-table-header-weight': '700',
      '--csp-table-header-transform': 'uppercase',
    },
  },
]

// The list and the detail are two surfaces side by side, and the selected element takes
// a tinted background
const OUVERTE: Valeurs = {
  '--csp-raised-background-current': 'var(--background-alt-blue-france)',
  '--csp-raised-border-width-current': '1px',
  '--csp-raised-border-color-current': 'var(--border-default-blue-france)',
}

export const PARCOURS: LevierOption[] = [
  { id: 'kit', nom: 'Kit actuel', valeurs: {} },
  { id: 'carte-ouverte', nom: 'Carte ouverte teintée', valeurs: OUVERTE },
  {
    id: 'cote-a-cote',
    nom: 'Panneau à côté du kanban',
    valeurs: {
      ...OUVERTE,
      '--csp-panel-width-wide': '42rem',
      '--csp-panel-page-offset': '42rem',
      '--csp-panel-shadow-docked': SANS_OMBRE,
    },
  },
]

// The colour of a category tints the header of its container, never the page;
// the contrast backgrounds of the DSFR give the tint of each category
export const CATEGORIES: LevierOption[] = [
  { id: 'kit', nom: 'Kit actuel', valeurs: {} },
  {
    id: 'en-tete-teinte',
    nom: 'En-tête de colonne teinté',
    valeurs: {
      '--csp-category-neutral-background': 'var(--background-contrast-grey)',
      '--csp-category-progress-background': 'var(--background-contrast-info)',
      '--csp-category-negative-background': 'var(--background-contrast-error)',
      '--csp-category-positive-background': 'var(--background-contrast-success)',
      '--csp-region-badge-background': 'var(--background-default-grey)',
    },
  },
]

// Backgrounds with gradient, glow, dots or grain on the surfaces that frame a section: the page header, the panel
// header and the empty states. The colours come from the DSFR; the treatment gives the surfaces their character.
interface Fond {
  calques: string[]
  tailles?: string[]
  repetitions?: string[]
}

const SURFACES = ['page-header', 'drawer-header', 'empty-state'] as const

// Each layer of the backdrop carries its position, size and repeat, since a component draws it with the background shorthand
function habillage({ calques, tailles, repetitions }: Fond): Valeurs {
  const backdrop = calques
    .map((calque, index) => `${calque} 0 0 / ${tailles?.[index] ?? '100% 100%'} ${repetitions?.[index] ?? 'no-repeat'}`)
    .join(', ')
  const valeurs: Valeurs = {
    '--csp-empty-state-background': 'var(--background-default-grey)',
    '--csp-empty-state-frame-width': '1px',
  }
  for (const surface of SURFACES) {
    valeurs[`--csp-${surface}-backdrop`] = backdrop
  }
  return valeurs
}

const GRAIN = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0.2 0 0 0 0 0.15 0 0 0 0 0.1 0 0 0 0.16 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)'/%3E%3C/svg%3E")`

export const HABILLAGES: LevierOption[] = [
  { id: 'kit', nom: 'Kit actuel', valeurs: {} },
  {
    id: 'degrade',
    nom: 'Dégradé bleu France',
    valeurs: habillage({
      calques: ['linear-gradient(180deg, var(--blue-france-925-125), var(--blue-france-975-75) 60%, var(--background-default-grey))'],
    }),
  },
  {
    id: 'lueur',
    nom: 'Lueur bleu France et cumulus',
    valeurs: habillage({
      calques: [
        'radial-gradient(55% 150% at 100% 0%, var(--blue-france-850-200), transparent 70%)',
        'radial-gradient(40% 130% at 70% 120%, var(--blue-cumulus-925-125), transparent 75%)',
        'linear-gradient(var(--blue-france-975-75), var(--blue-france-975-75))',
      ],
    }),
  },
  {
    id: 'points',
    nom: 'Trame de points',
    valeurs: habillage({
      calques: [
        'linear-gradient(90deg, var(--blue-france-975-75) 10%, transparent 65%)',
        'radial-gradient(circle at 1px 1px, var(--blue-france-850-200) 1.2px, transparent 1.6px)',
        'linear-gradient(var(--blue-france-975-75), var(--blue-france-975-75))',
      ],
      tailles: ['100% 100%', '12px 12px', '100% 100%'],
      repetitions: ['no-repeat', 'repeat', 'no-repeat'],
    }),
  },
  {
    id: 'rayures',
    nom: 'Rayures fines',
    valeurs: habillage({
      calques: [
        'linear-gradient(90deg, var(--blue-france-975-75) 15%, transparent 70%)',
        'repeating-linear-gradient(135deg, var(--blue-france-925-125) 0 1px, transparent 1px 7px)',
        'linear-gradient(var(--blue-france-975-75), var(--blue-france-975-75))',
      ],
    }),
  },
  {
    id: 'grain',
    nom: 'Grain sur beige gris galet',
    valeurs: habillage({
      calques: [
        GRAIN,
        'linear-gradient(160deg, var(--beige-gris-galet-925-125), var(--beige-gris-galet-975-75) 60%, var(--background-default-grey))',
      ],
      tailles: ['160px 160px', '100% 100%'],
      repetitions: ['repeat', 'no-repeat'],
    }),
  },
]

export function valeursOf(option: LevierOption, theme: string): Valeurs {
  const reduit = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? option.reduit : undefined
  return { ...option.valeurs, ...(theme === 'dark' ? option.sombre : undefined), ...reduit }
}

// Writes the option named by parameters.option on the root element, for the story only
export function withLevierOption(options: LevierOption[]): Decorator {
  return (story, context) => ({
    components: { story },
    setup() {
      const option = options.find(({ id }) => id === context.parameters.option)
      if (!option) {
        return
      }
      const root = document.documentElement
      const valeurs = valeursOf(option, context.globals.theme)
      const attributs = option.attributs ?? {}
      for (const [name, value] of Object.entries(valeurs)) {
        root.style.setProperty(name, value)
      }
      for (const [name, value] of Object.entries(attributs)) {
        root.setAttribute(name, value)
      }
      onBeforeUnmount(() => {
        for (const name of Object.keys(valeurs)) {
          root.style.removeProperty(name)
        }
        for (const name of Object.keys(attributs)) {
          root.removeAttribute(name)
        }
      })
    },
    template: '<story />',
  })
}
