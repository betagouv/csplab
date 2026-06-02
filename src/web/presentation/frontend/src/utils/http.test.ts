import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { HttpError, NetworkError, ValidationError } from './errors'
import { http } from './http'

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
    json: () => Promise.resolve(data),
  } as Response)
}

beforeEach(() => {
  setCsrfCookie(MOCK_CSRF_TOKEN)
  vi.stubGlobal('fetch', vi.fn())
})

afterEach(() => {
  vi.restoreAllMocks()
})

describe('http', () => {
  it('does not include CSRF token on GET', async () => {
    mockFetchResponse({})
    await http.get('/api/test')
    expect(fetch).toHaveBeenCalledWith('/api/test', expect.objectContaining({
      headers: expect.not.objectContaining({ 'X-CSRFToken': expect.any(String) }),
    }))
  })

  it('reads CSRF token from cookie on mutating requests', async () => {
    mockFetchResponse({}, 201)
    await http.post('/api/test', { name: 'test' })
    expect(fetch).toHaveBeenCalledWith('/api/test', expect.objectContaining({
      headers: expect.objectContaining({ 'X-CSRFToken': MOCK_CSRF_TOKEN }),
    }))
  })

  it('redirects to /utilisateur/connexion/ on 401', async () => {
    const mockLocation = { href: '', pathname: '/ats/dashboard', search: '' }
    vi.stubGlobal('location', mockLocation)
    mockFetchResponse({}, 401, 'Unauthorized')

    await expect(http.get('/api/test')).rejects.toThrow('Redirecting to login')
    expect(mockLocation.href).toBe('/utilisateur/connexion/?next=%2Fats%2Fdashboard')
  })

  it('does NOT redirect on 403 (permission denied is not auth)', async () => {
    const mockLocation = { href: '', pathname: '/ats/x', search: '' }
    vi.stubGlobal('location', mockLocation)
    mockFetchResponse({ detail: 'Forbidden' }, 403, 'Forbidden')

    await expect(http.get('/api/test')).rejects.toBeInstanceOf(HttpError)
    expect(mockLocation.href).toBe('')
  })

  it('throws HttpError with status and data on non-validation 4xx', async () => {
    const errorData = { detail: 'Not found' }
    mockFetchResponse(errorData, 404, 'Not Found')

    try {
      await http.get('/api/missing')
      expect.fail('Should have thrown')
    }
    catch (error) {
      expect(error).toBeInstanceOf(HttpError)
      expect(error).not.toBeInstanceOf(ValidationError)
      expect((error as HttpError).status).toBe(404)
      expect((error as HttpError).data).toEqual(errorData)
    }
  })

  it('returns undefined on 204 No Content', async () => {
    mockFetchResponse(null, 204, 'No Content')
    const result = await http.delete('/api/things/1')
    expect(result).toBeUndefined()
  })

  it('serializes query params into the URL', async () => {
    mockFetchResponse({})
    await http.get('/api/things', {
      params: { q: 'hello world', page: 2, active: true },
    })
    expect(fetch).toHaveBeenCalledWith(
      '/api/things?q=hello+world&page=2&active=true',
      expect.any(Object),
    )
  })

  it('merges custom headers without overriding CSRF', async () => {
    mockFetchResponse({}, 201)
    await http.post('/api/test', { x: 1 }, {
      headers: { 'X-Trace-Id': 'abc-123' },
    })
    expect(fetch).toHaveBeenCalledWith('/api/test', expect.objectContaining({
      headers: expect.objectContaining({
        'X-Trace-Id': 'abc-123',
        'X-CSRFToken': MOCK_CSRF_TOKEN,
        'Content-Type': 'application/json',
      }),
    }))
  })

  describe('on network failure', () => {
    it('wraps fetch failures', async () => {
      const cause = new TypeError('Failed to fetch')
      vi.mocked(fetch).mockRejectedValueOnce(cause)

      try {
        await http.get('/api/test')
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
      await expect(http.get('/api/test')).rejects.toBe(abortError)
    })
  })

  describe('on validation failure', () => {
    it('is thrown on 400 with DRF native field errors', async () => {
      const payload = {
        email: ['Enter a valid email address.'],
        name: ['This field is required.'],
      }
      mockFetchResponse(payload, 400, 'Bad Request')

      try {
        await http.post('/api/candidates', {})
        expect.fail('Should have thrown')
      }
      catch (error) {
        expect(error).toBeInstanceOf(ValidationError)
        expect((error as ValidationError).fieldErrors).toEqual(payload)
      }
    })

    it('is thrown on 422 with custom handler details', async () => {
      const payload = {
        status: 'error',
        message: 'Validation failed',
        type: 'CandidateValidationError',
        details: { age: ['Must be between 16 and 99.'] },
      }
      mockFetchResponse(payload, 422, 'Unprocessable Entity')

      try {
        await http.post('/api/candidates', {})
        expect.fail('Should have thrown')
      }
      catch (error) {
        expect(error).toBeInstanceOf(ValidationError)
        expect((error as ValidationError).fieldErrors).toEqual({
          age: ['Must be between 16 and 99.'],
        })
      }
    })

    it('has empty fieldErrors when payload is unparseable', async () => {
      mockFetchResponse('Bad Request', 400, 'Bad Request')

      try {
        await http.post('/api/test', {})
        expect.fail('Should have thrown')
      }
      catch (error) {
        expect(error).toBeInstanceOf(ValidationError)
        expect((error as ValidationError).fieldErrors).toEqual({})
      }
    })
  })
})
