import { describe, expect, it, vi } from 'vitest'
import { makeCandidatureRow } from '@/test/fixtures/candidatures'
import { candidatureListePages } from '@/test/handlers/candidatures'
import { server } from '@/test/server'
import { getCandidatureListe } from './api'

describe('getCandidatureListe', () => {
  it('receives the whole liste in a single request beyond the default page size of the server', async () => {
    const rows = Array.from({ length: 250 }, (_, index) => makeCandidatureRow(index))
    const requested = vi.fn()
    server.use(candidatureListePages(rows, requested))

    const liste = await getCandidatureListe({ organismeUuid: 'organisme', recrutementUuid: 'recrutement' })

    expect(liste.results.map(row => row.uuid)).toEqual(rows.map(row => row.uuid))
    expect(requested).toHaveBeenCalledOnce()
  })
})
