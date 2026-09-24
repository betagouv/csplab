import type { DocumentListe } from '../types'
import { PiniaColada } from '@pinia/colada'
import { render, screen, within } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { describe, expect, it, vi } from 'vitest'
import { CANDIDATURE_PARAMS } from '@/test/fixtures/candidatures'
import { getCandidatureDocuments } from '../api'
import CandidatureDocuments from './CandidatureDocuments.vue'

vi.mock('../api', async importOriginal => ({
  ...await importOriginal<typeof import('../api')>(),
  getCandidatureDocuments: vi.fn(),
}))

const CV: DocumentListe = {
  uuid: 'ffffffff-0001-0001-0001-000000000001',
  type: 'cv',
  nom_original: 'CV Alice Dupont.pdf',
  content_type: 'application/pdf',
  taille: 73_400,
  depose_par_uuid: 'eeeeeeee-0001-0001-0001-000000000001',
  depose_par: 'Alice Dupont',
  depose_le: '2025-06-10T09:15:00Z',
}

const LETTRE: DocumentListe = {
  ...CV,
  uuid: 'ffffffff-0001-0001-0001-000000000002',
  type: 'lettre_motivation',
  nom_original: 'Lettre.docx',
  content_type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  taille: 12_000,
}

async function renderDocuments() {
  vi.mocked(getCandidatureDocuments).mockResolvedValue({ count: 2, results: [CV, LETTRE] })
  render(CandidatureDocuments, {
    props: { candidature: CANDIDATURE_PARAMS },
    global: { plugins: [createPinia(), PiniaColada] },
  })
  await screen.findByText('2 documents')
  return screen.getAllByRole('listitem').map(item => within(item))
}

describe('candidatureDocuments', () => {
  it('lists the documents with their type and size', async () => {
    const [cv, lettre] = await renderDocuments()

    expect(cv!.getByText(/Curriculum vitae · 73 ko/)).toBeInTheDocument()
    expect(lettre!.getByText(/Lettre de motivation · 12 ko/)).toBeInTheDocument()
  })

  it('opens and downloads only the PDF documents', async () => {
    const [cv, lettre] = await renderDocuments()

    const view = cv!.getByRole('link', { name: 'Voir' })
    expect(view).toHaveAttribute('href', expect.stringMatching(new RegExp(`/documents/${CV.uuid}$`)))
    expect(view).toHaveAttribute('target', '_blank')
    expect(cv!.getByRole('link', { name: 'Télécharger' })).toHaveAttribute('download', 'CV Alice Dupont.pdf')
    expect(lettre!.queryByRole('link')).not.toBeInTheDocument()
  })
})
