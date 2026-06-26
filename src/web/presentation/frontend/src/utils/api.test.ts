import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { api } from './api'
import { HttpError, NetworkError, ValidationError } from './errors'

const MOCK_CSRF_TOKEN = 'test-csrf-token'

function setCsrfCookie(value: string) {
  Object.defineProperty(document, 'cookie', {
    configurable: true,
    get: () => `csrftoken=${value}`,
  })
}

function mockFetchResponse(data: unknown, status = 200, statusText = 'OK') {
  return vi.mocked(fetch).mockResolvedValueOnce({
    ok: status >= 200 && status < 300,
    status,
    statusText,
    headers: new Headers({ 'content-type': 'application/json' }),
    clone() { return this as Response },
    json: () => Promise.resolve(data),
    text: () => Promise.resolve(JSON.stringify(data)),
  } as unknown as Response)
}

beforeEach(() => {
  setCsrfCookie(MOCK_CSRF_TOKEN)
  vi.stubGlobal('fetch', vi.fn())
})

afterEach(() => {
  vi.restoreAllMocks()
})

describe('api client', () => {
  function getLastRequest(): Request {
    return vi.mocked(fetch).mock.calls[0][0] as Request
  }

  it('substitutes path parameters from the OpenAPI schema', async () => {
    mockFetchResponse([])
    await api.GET('/recruteur/organisme/{organisme_uuid}/parametres/etapes', {
      params: { path: { organisme_uuid: 'abc-123' } },
    })
    expect(getLastRequest().url).toContain('/recruteur/organisme/abc-123/parametres/etapes')
  })

  it('does not include CSRF token on GET', async () => {
    mockFetchResponse({})
    await api.GET('/utilisateur/me')
    expect(getLastRequest().headers.has('X-CSRFToken')).toBe(false)
  })

  it('reads CSRF token from cookie on mutating requests', async () => {
    mockFetchResponse([], 200)
    await api.PUT('/recruteur/organisme/{organisme_uuid}/parametres/etapes', {
      params: { path: { organisme_uuid: 'xxx' } },
      body: [],
    })
    expect(getLastRequest().headers.get('X-CSRFToken')).toBe(MOCK_CSRF_TOKEN)
  })

  it('redirects to /utilisateur/connexion on 401', async () => {
    const mockLocation = { href: '', pathname: '/ats/dashboard', search: '' }
    vi.stubGlobal('location', mockLocation)
    mockFetchResponse({}, 401, 'Unauthorized')

    await expect(api.GET('/utilisateur/me')).rejects.toThrow('Redirecting to login')
    expect(mockLocation.href).toBe('/utilisateur/connexion?next=%2Fats%2Fdashboard')
  })

  it('throws HttpError on non-validation 4xx', async () => {
    mockFetchResponse({ detail: 'Not found' }, 404, 'Not Found')

    try {
      await api.GET('/utilisateur/me')
      expect.fail('Should have thrown')
    }
    catch (error) {
      expect(error).toBeInstanceOf(HttpError)
      expect(error).not.toBeInstanceOf(ValidationError)
      expect((error as HttpError).status).toBe(404)
    }
  })

  it('throws ValidationError with parsed field errors on 400', async () => {
    const payload = {
      email: ['Enter a valid email address.'],
      name: ['This field is required.'],
    }
    mockFetchResponse(payload, 400, 'Bad Request')

    try {
      await api.PUT('/recruteur/organisme/{organisme_uuid}/parametres/etapes', {
        params: { path: { organisme_uuid: 'xxx' } },
        body: [],
      })
      expect.fail('Should have thrown')
    }
    catch (error) {
      expect(error).toBeInstanceOf(ValidationError)
      expect((error as ValidationError).fieldErrors).toEqual(payload)
    }
  })

  it('wraps fetch failures as NetworkError', async () => {
    const cause = new TypeError('Failed to fetch')
    vi.mocked(fetch).mockRejectedValueOnce(cause)

    try {
      await api.GET('/utilisateur/me')
      expect.fail('Should have thrown')
    }
    catch (error) {
      expect(error).toBeInstanceOf(NetworkError)
      expect((error as NetworkError).cause).toBe(cause)
    }
  })

  it('propagates AbortError as-is', async () => {
    const abortError = new DOMException('aborted', 'AbortError')
    vi.mocked(fetch).mockRejectedValueOnce(abortError)
    await expect(api.GET('/utilisateur/me')).rejects.toBe(abortError)
  })
})
