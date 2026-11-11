import { PiniaColada } from '@pinia/colada'
import { render, screen, within } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { describe, expect, it } from 'vitest'
import { CANDIDATURE_PARAMS, CV_DOCUMENT, LETTRE_DOCUMENT } from '@/test/fixtures/candidatures'
import { candidatureDocuments } from '@/test/handlers/candidatures'
import { server } from '@/test/server'
import CandidatureDocuments from './CandidatureDocuments.vue'

async function renderDocuments() {
  server.use(candidatureDocuments([CV_DOCUMENT, LETTRE_DOCUMENT]))
  render(CandidatureDocuments, {
    props: { candidature: CANDIDATURE_PARAMS },
    global: { plugins: [createPinia(), PiniaColada] },
  })
  await screen.findByText('2 documents')
  const [cv, lettre] = screen.getAllByRole('listitem')
  return { cv, lettre }
}

describe('candidatureDocuments', () => {
  it('lists the documents with their type and size', async () => {
    const { cv, lettre } = await renderDocuments()

    expect(within(cv).getByText(/Curriculum vitae · 73 ko/)).toBeInTheDocument()
    expect(within(lettre).getByText(/Lettre de motivation · 12 ko/)).toBeInTheDocument()
  })

  it('opens each document in a new tab', async () => {
    const { cv, lettre } = await renderDocuments()

    const view = within(cv).getByRole('link', { name: 'Voir' })
    expect(view).toHaveAttribute('href', expect.stringMatching(new RegExp(`/documents/${CV_DOCUMENT.uuid}$`)))
    expect(view).toHaveAttribute('target', '_blank')
    expect(within(lettre).getByRole('link', { name: 'Voir' })).toHaveAttribute('href', expect.stringMatching(new RegExp(`/documents/${LETTRE_DOCUMENT.uuid}$`)))
  })
})
