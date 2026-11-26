export const UI_SHAPES = ['dsfr', 'rounded'] as const
export const UI_DENSITIES = ['standard'] as const

export interface UiSettings {
  shape: typeof UI_SHAPES[number]
  density: typeof UI_DENSITIES[number]
}

type UiAxis = keyof UiSettings

// The first value of each axis is its default: it sets no attribute, so no theme sheet applies
export const UI_AXES = {
  shape: { attribute: 'data-csp-shape', values: UI_SHAPES },
  density: { attribute: 'data-csp-density', values: UI_DENSITIES },
} as const

const PREVIEW_ATTRIBUTE = 'data-csp-ui-preview'
const STORAGE_KEY = 'csp_ui_settings'

function pick<A extends UiAxis>(axis: A, candidates: unknown[]): UiSettings[A] {
  const values: readonly unknown[] = UI_AXES[axis].values
  return (candidates.find(candidate => values.includes(candidate)) ?? values[0]) as UiSettings[A]
}

function readStored(): Partial<Record<UiAxis, unknown>> {
  try {
    return JSON.parse(sessionStorage.getItem(STORAGE_KEY) ?? '{}')
  }
  catch {
    return {}
  }
}

export function applyUiSettings(settings: UiSettings): void {
  for (const axis of Object.keys(UI_AXES) as UiAxis[]) {
    const { attribute, values } = UI_AXES[axis]
    if (settings[axis] === values[0]) {
      document.documentElement.removeAttribute(attribute)
    }
    else {
      document.documentElement.setAttribute(attribute, settings[axis])
    }
  }
}

export function initUiSettings(): void {
  const root = document.documentElement
  if (!root.hasAttribute(PREVIEW_ATTRIBUTE)) {
    return
  }
  const query = new URLSearchParams(window.location.search)
  const requested = Object.fromEntries((Object.keys(UI_AXES) as UiAxis[])
    .map(axis => [axis, query.get(axis)])
    .filter(([axis, value]) => pick(axis as UiAxis, [value]) === value))
  const stored = { ...readStored(), ...requested }
  if (Object.keys(requested).length > 0) {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(stored))
    }
    catch {}
  }
  applyUiSettings({
    shape: pick('shape', [stored.shape, root.getAttribute(UI_AXES.shape.attribute)]),
    density: pick('density', [stored.density, root.getAttribute(UI_AXES.density.attribute)]),
  })
}
