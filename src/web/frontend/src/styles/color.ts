// Color math for palette rules and their tests: OKLCH, WCAG contrast, OKLab distance, simulated dichromacy.

export type LinearRgb = readonly [number, number, number]

export interface Oklch {
  l: number
  c: number
  h: number
}

export type Dichromacy = 'protanopia' | 'deuteranopia' | 'tritanopia'

export const DICHROMACIES: readonly Dichromacy[] = ['protanopia', 'deuteranopia', 'tritanopia']

// Machado, Oliveira and Fernandes (2009), severity 1, applied to linear RGB
export const DICHROMACY_MATRICES: Record<Dichromacy, readonly LinearRgb[]> = {
  protanopia: [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
  deuteranopia: [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.01182, 0.04294, 0.968881]],
  tritanopia: [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.3039]],
}

const GAMUT_TOLERANCE = 1e-6

function clamp(value: number): number {
  return Math.min(1, Math.max(0, value))
}

function clampRgb([r, g, b]: LinearRgb): LinearRgb {
  return [clamp(r), clamp(g), clamp(b)]
}

export function oklchToLinearRgb({ l, c, h }: Oklch): LinearRgb {
  const a = c * Math.cos((h * Math.PI) / 180)
  const b = c * Math.sin((h * Math.PI) / 180)
  const long = (l + 0.3963377774 * a + 0.2158037573 * b) ** 3
  const medium = (l - 0.1055613458 * a - 0.0638541728 * b) ** 3
  const short = (l - 0.0894841775 * a - 1.291485548 * b) ** 3
  return [
    4.0767416621 * long - 3.3077115913 * medium + 0.2309699292 * short,
    -1.2684380046 * long + 2.6097574011 * medium - 0.3413193965 * short,
    -0.0041960863 * long - 0.7034186147 * medium + 1.707614701 * short,
  ]
}

function linearRgbToOklab([r, g, b]: LinearRgb): LinearRgb {
  const long = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
  const medium = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
  const short = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)
  return [
    0.2104542553 * long + 0.793617785 * medium - 0.0040720468 * short,
    1.9779984951 * long - 2.428592205 * medium + 0.4505937099 * short,
    0.0259040371 * long + 0.7827717662 * medium - 0.808675766 * short,
  ]
}

export function hexToLinearRgb(hex: string): LinearRgb {
  const digits = hex.replace('#', '')
  const full = digits.length === 3 ? [...digits].map(digit => digit + digit).join('') : digits
  const [r, g, b] = [0, 2, 4].map((start) => {
    const channel = Number.parseInt(full.slice(start, start + 2), 16) / 255
    return channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4
  })
  return [r, g, b]
}

export function isInSrgb(rgb: LinearRgb): boolean {
  return rgb.every(channel => channel >= -GAMUT_TOLERANCE && channel <= 1 + GAMUT_TOLERANCE)
}

// Largest chroma up to `chroma` that keeps the lightness and the hue inside sRGB, floored to 3 decimals
export function fitChroma(l: number, chroma: number, h: number): number {
  if (isInSrgb(oklchToLinearRgb({ l, c: chroma, h }))) {
    return chroma
  }
  let [low, high] = [0, chroma]
  for (let step = 0; step < 32; step += 1) {
    const middle = (low + high) / 2
    if (isInSrgb(oklchToLinearRgb({ l, c: middle, h }))) {
      low = middle
    }
    else {
      high = middle
    }
  }
  return Math.floor(low * 1000) / 1000
}

function relativeLuminance(rgb: LinearRgb): number {
  const [r, g, b] = clampRgb(rgb)
  return 0.2126 * r + 0.7152 * g + 0.0722 * b
}

export function contrastRatio(first: LinearRgb, second: LinearRgb): number {
  const [high, low] = [relativeLuminance(first), relativeLuminance(second)].sort((a, b) => b - a)
  return (high! + 0.05) / (low! + 0.05)
}

export function deltaEOk(first: LinearRgb, second: LinearRgb): number {
  const [l1, a1, b1] = linearRgbToOklab(clampRgb(first))
  const [l2, a2, b2] = linearRgbToOklab(clampRgb(second))
  return Math.hypot(l1 - l2, a1 - a2, b1 - b2)
}

export function simulateDichromacy(rgb: LinearRgb, type: Dichromacy): LinearRgb {
  const [first, second, third] = DICHROMACY_MATRICES[type]
  const apply = (row: LinearRgb) => row[0] * rgb[0] + row[1] * rgb[1] + row[2] * rgb[2]
  return clampRgb([apply(first), apply(second), apply(third)])
}
