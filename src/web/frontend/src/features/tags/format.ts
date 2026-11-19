import type { TagSummary } from './types'
import type { PaletteColor } from '@/styles/palette'
import { DEFAULT_TAG_COLOR, TAG_COLOR_PALETTE } from './constants/tag'

export function tagPaletteColor(tag: Pick<TagSummary, 'color'>): PaletteColor {
  return TAG_COLOR_PALETTE[tag.color ?? DEFAULT_TAG_COLOR]
}
