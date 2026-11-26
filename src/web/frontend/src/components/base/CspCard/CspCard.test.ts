import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { h } from 'vue'
import CspCard from './CspCard.vue'

describe('cspCard', () => {
  it('names the article after its title', () => {
    render(CspCard, { props: { title: 'Titre de la carte' } })
    expect(screen.getByRole('article', { name: 'Titre de la carte' })).toBeInTheDocument()
  })

  it('names the article after the content of its title slot', () => {
    render(CspCard, { slots: { title: () => h('a', { href: '/page' }, 'Lien du titre') } })
    expect(screen.getByRole('article', { name: 'Lien du titre' })).toBeInTheDocument()
  })

  it('makes a section card a region named after its title', () => {
    render(CspCard, { props: { as: 'section', title: 'Titre de la carte' } })
    expect(screen.getByRole('region', { name: 'Titre de la carte' })).toBeInTheDocument()
  })

  it('leaves a list item card unnamed', () => {
    render(CspCard, { props: { as: 'li', title: 'Titre de la carte' } })
    expect(screen.getByRole('listitem')).not.toHaveAccessibleName()
  })
})
