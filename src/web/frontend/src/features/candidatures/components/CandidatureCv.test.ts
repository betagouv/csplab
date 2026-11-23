import type { RequestHandler } from 'msw'
import { PiniaColada } from '@pinia/colada'
import { render, screen } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { describe, expect, it, vi } from 'vitest'
import { CANDIDATURE_PARAMS, CV_DOCUMENT, LETTRE_DOCUMENT } from '@/test/fixtures/candidatures'
import {
  candidatureDocumentFile,
  candidatureDocumentFileFailure,
  candidatureDocuments,
  candidatureDocumentsFailure,
} from '@/test/handlers/candidatures'
import { server } from '@/test/server'
import CandidatureCv from './CandidatureCv.vue'

const CV_URL = `/recruteur/organismes/${CANDIDATURE_PARAMS.organismeUuid}/recrutements/${CANDIDATURE_PARAMS.recrutementUuid}/candidatures/${CANDIDATURE_PARAMS.candidatureUuid}/documents/${CV_DOCUMENT.uuid}`

function renderCv(...handlers: RequestHandler[]) {
  const checked = vi.fn()
  server.use(...handlers, candidatureDocumentFile(checked))
  render(CandidatureCv, {
    props: { candidature: CANDIDATURE_PARAMS, candidatNom: 'Alice Dupont' },
    global: { plugins: [createPinia(), PiniaColada] },
  })
  return { checked }
}

describe('candidatureCv', () => {
  it('displays a PDF CV in a frame, with a full page link', async () => {
    renderCv(candidatureDocuments([LETTRE_DOCUMENT, CV_DOCUMENT]))

    expect(await screen.findByTitle('CV de Alice Dupont')).toHaveAttribute('src', CV_URL)
    expect(screen.getByRole('link', { name: 'Afficher pleine page' })).toHaveAttribute('href', CV_URL)
  })

  it('says when the CV is not a PDF', async () => {
    const { checked } = renderCv(candidatureDocuments([{ ...CV_DOCUMENT, nom_original: 'CV.docx', content_type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' }]))

    expect(await screen.findByText('Le CV ne peut pas être affiché ici.')).toBeInTheDocument()
    expect(screen.queryByRole('link')).not.toBeInTheDocument()
    expect(screen.queryByTitle('CV de Alice Dupont')).not.toBeInTheDocument()
    expect(checked).not.toHaveBeenCalled()
  })

  it('says when the candidature has no CV', async () => {
    const { checked } = renderCv(candidatureDocuments([LETTRE_DOCUMENT]))

    expect(await screen.findByText('La candidature ne contient pas de CV')).toBeInTheDocument()
    expect(screen.queryByRole('link')).not.toBeInTheDocument()
    expect(checked).not.toHaveBeenCalled()
  })

  it('shows an error when the CV file cannot be loaded', async () => {
    renderCv(candidatureDocuments([CV_DOCUMENT]), candidatureDocumentFileFailure(500))

    expect(await screen.findByText('Le CV n\'a pas pu être chargé.')).toBeInTheDocument()
    expect(screen.queryByTitle('CV de Alice Dupont')).not.toBeInTheDocument()
    expect(screen.queryByRole('link')).not.toBeInTheDocument()
  })

  it('shows an error when the documents cannot be loaded', async () => {
    renderCv(candidatureDocumentsFailure(500))

    expect(await screen.findByText('Le CV n\'a pas pu être chargé.')).toBeInTheDocument()
  })
})
