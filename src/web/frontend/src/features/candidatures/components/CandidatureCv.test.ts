import type { DocumentListe } from '../types'
import { PiniaColada } from '@pinia/colada'
import { render, screen } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { CANDIDATURE_PARAMS } from '@/test/fixtures/candidatures'
import { getCandidatureDocuments } from '../api'
import CandidatureCv from './CandidatureCv.vue'

vi.mock('../api', async importOriginal => ({
  ...await importOriginal<typeof import('../api')>(),
  getCandidatureDocuments: vi.fn(),
}))

const CV_UUID = 'ffffffff-0001-0001-0001-000000000001'
const CV_URL = `/recruteur/organismes/${CANDIDATURE_PARAMS.organismeUuid}/recrutements/${CANDIDATURE_PARAMS.recrutementUuid}/candidatures/${CANDIDATURE_PARAMS.candidatureUuid}/documents/${CV_UUID}`

function document(overrides: Partial<DocumentListe>): DocumentListe {
  return {
    uuid: CV_UUID,
    type: 'cv',
    nom_original: 'CV Alice Dupont.pdf',
    content_type: 'application/pdf',
    taille: 1024,
    depose_par_uuid: 'eeeeeeee-0001-0001-0001-000000000001',
    depose_par: 'Alice Dupont',
    depose_le: '2025-06-10T09:15:00Z',
    ...overrides,
  }
}

function renderCv(results: DocumentListe[]) {
  vi.mocked(getCandidatureDocuments).mockResolvedValue({ count: results.length, results })
  return render(CandidatureCv, {
    props: { candidature: CANDIDATURE_PARAMS, candidatNom: 'Alice Dupont' },
    global: { plugins: [createPinia(), PiniaColada] },
  })
}

describe('candidatureCv', () => {
  afterEach(() => {
    vi.clearAllMocks()
  })

  it('displays a PDF CV in a frame, with a full page link and a download link', async () => {
    renderCv([document({ type: 'lettre_motivation', uuid: 'lettre' }), document({})])

    expect(await screen.findByTitle('CV de Alice Dupont')).toHaveAttribute('src', CV_URL)
    expect(screen.getByRole('link', { name: 'Afficher pleine page' })).toHaveAttribute('href', CV_URL)
    const download = screen.getByRole('link', { name: 'Télécharger' })
    expect(download).toHaveAttribute('href', CV_URL)
    expect(download).toHaveAttribute('download', 'CV Alice Dupont.pdf')
  })

  it('says when the CV is not a PDF', async () => {
    renderCv([document({ nom_original: 'CV.docx', content_type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })])

    expect(await screen.findByText('Le CV ne peut pas être affiché ici.')).toBeInTheDocument()
    expect(screen.queryByRole('link')).not.toBeInTheDocument()
    expect(screen.queryByTitle('CV de Alice Dupont')).not.toBeInTheDocument()
  })

  it('says when the candidature has no CV', async () => {
    renderCv([document({ type: 'lettre_motivation' })])

    expect(await screen.findByText('La candidature ne contient pas de CV')).toBeInTheDocument()
    expect(screen.queryByRole('link')).not.toBeInTheDocument()
  })

  it('shows an error when the documents cannot be loaded', async () => {
    vi.mocked(getCandidatureDocuments).mockRejectedValue(new HttpError(500, 'Internal Server Error', undefined))
    render(CandidatureCv, {
      props: { candidature: CANDIDATURE_PARAMS, candidatNom: 'Alice Dupont' },
      global: { plugins: [createPinia(), PiniaColada] },
    })

    expect(await screen.findByText('Le CV n\'a pas pu être chargé.')).toBeInTheDocument()
  })
})
