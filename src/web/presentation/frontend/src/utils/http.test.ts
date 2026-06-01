import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { http, HttpError } from './http'

const MOCK_CSRF_TOKEN = 'test-csrf-token'

function setCsrfCookie(value: string) {
  Object.defineProperty(document, 'cookie', {
    configurable: true,
    get: () => `csrftoken=${value}`,
  })
}

function clearCookies() {
  Object.defineProperty(document, 'cookie', {
    configurable: true,
    get: () => '',
  })
}

beforeEach(() => {
  setCsrfCookie(MOCK_CSRF_TOKEN)
  vi.stubGlobal('fetch', vi.fn())
})

afterEach(() => {
  vi.restoreAllMocks()
  clearCookies()
})

function mockFetchResponse(data: unknown, status = 200, statusText = 'OK') {
  return vi.mocked(fetch).mockResolvedValueOnce({
    ok: status >= 200 && status < 300,
    status,
    statusText,
    json: () => Promise.resolve(data),
  } as Response)
}

describe('http', () => {
  it('should not include CSRF token on GET', async () => {
    mockFetchResponse({})
    await http.get('/api/test')
    expect(fetch).toHaveBeenCalledWith('/api/test', expect.objectContaining({
      headers: expect.not.objectContaining({ 'X-CSRFToken': expect.any(String) }),
    }))
  })

  it('should read CSRF token from cookie on mutating requests', async () => {
    mockFetchResponse({}, 201)
    await http.post('/api/test', { name: 'test' })
    expect(fetch).toHaveBeenCalledWith('/api/test', expect.objectContaining({
      headers: expect.objectContaining({ 'X-CSRFToken': MOCK_CSRF_TOKEN }),
    }))
  })

  it('should send empty CSRF header when cookie is missing', async () => {
    clearCookies()
    mockFetchResponse({}, 201)
    await http.post('/api/test', {})
    expect(fetch).toHaveBeenCalledWith('/api/test', expect.objectContaining({
      headers: expect.objectContaining({ 'X-CSRFToken': '' }),
    }))
  })

  it('should redirect to /login/ on 401 only', async () => {
    const mockLocation = { href: '', pathname: '/ats/dashboard', search: '' }
    vi.stubGlobal('location', mockLocation)
    mockFetchResponse({}, 401, 'Unauthorized')

    await expect(http.get('/api/test')).rejects.toThrow('Redirecting to login')
    expect(mockLocation.href).toBe('/login/?next=%2Fats%2Fdashboard')
  })

  it('should NOT redirect on 403 (permission denied is not auth)', async () => {
    const mockLocation = { href: '', pathname: '/ats/x', search: '' }
    vi.stubGlobal('location', mockLocation)
    mockFetchResponse({ detail: 'Forbidden' }, 403, 'Forbidden')

    await expect(http.get('/api/test')).rejects.toBeInstanceOf(HttpError)
    expect(mockLocation.href).toBe('')
  })

  it('should throw HttpError with status and data on non-2xx', async () => {
    const errorData = { detail: 'Not found' }
    mockFetchResponse(errorData, 404, 'Not Found')

    try {
      await http.get('/api/missing')
      expect.fail('Should have thrown')
    }
    catch (error) {
      expect(error).toBeInstanceOf(HttpError)
      expect((error as HttpError).status).toBe(404)
      expect((error as HttpError).data).toEqual(errorData)
    }
  })
})
