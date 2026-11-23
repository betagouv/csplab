import type { TagSummary } from '../types'
import { render, screen, within } from '@testing-library/vue'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { setupUser } from '@/test/render'
import TagList from './TagList.vue'

const TAGS: TagSummary[] = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo'].map((name, index) => ({
  uuid: `aaaaaaaa-0001-0001-0001-00000000000${index}`,
  name,
  color: 'bleu',
}))

const ROW_WIDTH = 200
const TAG_WIDTH = 90
const LINE_HEIGHT = 20
const MORE_WIDTH = 20

function rect(left: number, top: number, width: number): DOMRect {
  return { left, top, width, height: LINE_HEIGHT, right: left + width, bottom: top + LINE_HEIGHT, x: left, y: top, toJSON: () => ({}) }
}

// jsdom lays nothing out: two tags fit on each line of the measuring row
function layOutTwoTagsPerLine(): void {
  vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockImplementation(function (this: HTMLElement) {
    if (this.hasAttribute('data-fitting-item')) {
      const index = [...(this.parentElement?.querySelectorAll('[data-fitting-item]') ?? [])].indexOf(this)
      return rect((index % 2) * (TAG_WIDTH + 10), Math.floor(index / 2) * LINE_HEIGHT, TAG_WIDTH)
    }
    if (this.hasAttribute('data-fitting-more')) {
      return rect(0, 0, MORE_WIDTH)
    }
    return rect(0, 0, ROW_WIDTH)
  })
}

describe('tagList', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

  it('shows every tag when no line limit is set', () => {
    render(TagList, { props: { 'tags': TAGS, 'aria-label': 'Étiquettes' } })

    expect(within(screen.getByRole('list', { name: 'Étiquettes' })).getAllByRole('listitem')).toHaveLength(TAGS.length)
    expect(screen.queryByRole('button', { name: /autres? étiquettes?/ })).not.toBeInTheDocument()
  })

  it('keeps the tags that fit in the line limit and counts the others, with room for the count', async () => {
    layOutTwoTagsPerLine()
    render(TagList, { props: { 'tags': TAGS, 'maxLines': 2, 'aria-label': 'Étiquettes' } })

    const more = await screen.findByRole('button', { name: '2 autres étiquettes' })
    expect(more).toHaveTextContent('+2')
    const list = within(screen.getByRole('list', { name: 'Étiquettes' }))
    expect(list.getAllByRole('listitem').map(item => item.textContent?.trim())).toEqual(['Alpha', 'Bravo', 'Charlie', '+2'])
  })

  it('keeps the first tag with the count when it is wider than the row', async () => {
    vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockImplementation(function (this: HTMLElement) {
      if (this.hasAttribute('data-fitting-item')) {
        const index = [...(this.parentElement?.querySelectorAll('[data-fitting-item]') ?? [])].indexOf(this)
        return rect(0, index * LINE_HEIGHT, ROW_WIDTH + 10)
      }
      if (this.hasAttribute('data-fitting-more')) {
        return rect(0, 0, MORE_WIDTH)
      }
      return rect(0, 0, ROW_WIDTH)
    })
    render(TagList, { props: { 'tags': TAGS.slice(0, 2), 'maxLines': 1, 'aria-label': 'Étiquettes' } })

    await screen.findByRole('button', { name: '1 autre étiquette' })
    const list = within(screen.getByRole('list', { name: 'Étiquettes' }))
    expect(list.getAllByRole('listitem').map(item => item.textContent?.trim())).toEqual(['Alpha', '+1'])
  })

  it('names the hidden tags on keyboard focus of the count', async () => {
    layOutTwoTagsPerLine()
    vi.stubGlobal('IntersectionObserver', class {
      observe = vi.fn()
      unobserve = vi.fn()
      disconnect = vi.fn()
    })
    const user = setupUser()
    render(TagList, { props: { 'tags': TAGS, 'maxLines': 2, 'aria-label': 'Étiquettes' } })
    const more = await screen.findByRole('button', { name: '2 autres étiquettes' })

    await user.tab()

    expect(more).toHaveFocus()
    await vi.waitFor(() => expect(more).toHaveAccessibleDescription('Delta, Echo'))
  })
})
