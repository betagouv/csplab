import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { getMe } from '@/api/utilisateur'
import { renderWithApp, setupUser } from '@/test/render'
import App from './App.vue'

vi.mock('@/api/utilisateur', () => ({
  getMe: vi.fn(),
}))

describe('app', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset()
  })

  it('reports a failed account load and lets the user retry', async () => {
    vi.mocked(getMe).mockRejectedValue(new HttpError(500, 'Server Error', undefined))
    const user = setupUser()

    await renderWithApp(App)

    expect(await screen.findByRole('alert')).toHaveTextContent('Une erreur est survenue lors du chargement de votre compte.')

    await user.click(screen.getByRole('button', { name: 'Réessayer' }))

    expect(getMe).toHaveBeenCalledTimes(2)
  })
})
