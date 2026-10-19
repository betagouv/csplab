// To add a scenario: write styles/etiquettes/<id>.css with every rule under :root[data-csp-etiquettes='<id>'], import it in index.css, then list it in SCENARIOS (DEFAULT_SCENARIO shows it without the toolbar).

import type { PaletteColor } from '../palette'
import { DEFAULT_PALETTE_COLOR } from '../palette'

// Thresholds that palette.test.ts checks for one scenario only; a distance is in OKLab, between any two colors
export interface ScenarioChecks {
  // Distance on the role where the two colors differ most, background or text, in both themes
  backgroundOrTextDistance?: number
  lightBackgroundDistance?: number
  darkTextDistance?: number
  // Contrast of the dot, or of its outline, on the overlap background, in both themes
  dotContrast?: number
}

export interface Scenario {
  id: string
  name: string
  // Color preselected when creating a label, DEFAULT_PALETTE_COLOR otherwise
  defaultColor?: PaletteColor
  checks?: ScenarioChecks
}

export const SCENARIOS: Scenario[] = [
  { id: 'dsfr', name: 'Rester dans le DSFR', defaultColor: 'grey', checks: { backgroundOrTextDistance: 0.045 } },
  { id: 'kit', name: 'Palette du kit' },
  { id: 'lasuite', name: 'Couleurs de La Suite numérique', checks: { lightBackgroundDistance: 0.02, darkTextDistance: 0.04, dotContrast: 3 } },
  { id: 'libre', name: 'Sans les contraintes' },
]

export const DEFAULT_SCENARIO: string | null = 'dsfr'

export const SCENARIO_ATTRIBUTE = 'data-csp-etiquettes'

export function applyScenario(element: HTMLElement, id: string | null | undefined): void {
  if (id && SCENARIOS.some(scenario => scenario.id === id)) {
    element.setAttribute(SCENARIO_ATTRIBUTE, id)
  }
  else {
    element.removeAttribute(SCENARIO_ATTRIBUTE)
  }
}

export function scenarioDefaultColor(element: HTMLElement = document.documentElement): PaletteColor {
  const id = element.getAttribute(SCENARIO_ATTRIBUTE)
  return SCENARIOS.find(scenario => scenario.id === id)?.defaultColor ?? DEFAULT_PALETTE_COLOR
}
