import type { LevierOption, Valeurs } from '../options'

// Four steps, from the smallest element to the largest container: an indicator, a control, a surface, a region
const INDICATEUR = '0.25rem'
const CONTROLE = '0.375rem'
const SURFACE = '0.625rem'
const REGION = '1rem'

// A container whose padding is narrow, 4px at most, gives its element its own radius less that padding, so that both
// curves stay parallel; a container with a wide padding holds elements of the role below its own. A loading
// placeholder stands for text or an image, and takes the radius of an indicator.
const RAYONS: Valeurs = {
  '--csp-indicator-radius': INDICATEUR,
  '--csp-badge-radius': 'var(--csp-indicator-radius)',
  '--csp-skeleton-radius': 'var(--csp-indicator-radius)',
  '--csp-action-radius': CONTROLE,
  '--csp-nav-control-radius': 'var(--csp-action-radius)',
  '--csp-field-radius': CONTROLE,
  '--csp-tooltip-radius': 'var(--csp-action-radius)',
  '--csp-tabs-trigger-radius': 'var(--csp-action-radius)',
  '--csp-segmented-highlight-radius': 'max(0px, var(--csp-field-radius) - var(--csp-space-1))',
  '--csp-surface-radius': SURFACE,
  '--csp-frame-radius': 'var(--csp-surface-radius)',
  '--csp-overlap-radius': SURFACE,
  '--csp-message-radius': 'var(--csp-surface-radius)',
  '--csp-menu-item-radius': 'max(0px, var(--csp-overlap-radius) - var(--csp-menu-padding))',
  '--csp-region-radius': REGION,
  '--csp-lifted-radius': REGION,
}

// A thick bar does not follow a curve: a callout or a notification takes a frame in the colour of its tone, and the
// category of a kanban column tints its header, which keeps under its title the padding of the column
const SANS_BARRE: Valeurs = {
  '--csp-message-bar-width': '0px',
  '--csp-message-border-width': '0px',
  '--csp-message-frame-width': '1px',
  '--csp-category-accent-width': '0px',
  '--csp-category-neutral-background': 'var(--background-contrast-grey)',
  '--csp-category-progress-background': 'var(--background-contrast-info)',
  '--csp-category-negative-background': 'var(--background-contrast-error)',
  '--csp-category-positive-background': 'var(--background-contrast-success)',
  '--csp-region-badge-background': 'var(--background-default-grey)',
  '--csp-kanban-column-header-padding-bottom': 'var(--csp-kanban-column-padding)',
}

export const RAYONS_AFFIRMES: LevierOption[] = [
  { id: 'kit', nom: 'Aujourd’hui', valeurs: {} },
  { id: 'affirmes', nom: 'Rayons affirmés par rôle, 4, 6, 10 et 16 px', valeurs: { ...RAYONS, ...SANS_BARRE } },
]
