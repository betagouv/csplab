import { HttpError, NetworkError, parseFieldErrors, ValidationError } from './errors'

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'

interface RequestOptions {
  params?: Record<string, string | number | boolean>
  headers?: Record<string, string>
  signal?: AbortSignal
}

function readCsrfCookie(): string {
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/)
  return match ? decodeURIComponent(match[1]) : ''
}

function redirectToLogin(): never {
  const next = encodeURIComponent(window.location.pathname + window.location.search)
  window.location.href = `/login/?next=${next}`
  throw new Error('Redirecting to login')
}

function buildUrl(url: string, params?: RequestOptions['params']): string {
  if (!params)
    return url
  const search = new URLSearchParams()
  for (const [k, v] of Object.entries(params)) search.append(k, String(v))
  return `${url}?${search.toString()}`
}

async function request<T>(
  method: HttpMethod,
  url: string,
  data?: unknown,
  options: RequestOptions = {},
): Promise<T> {
  const hasBody = data !== undefined
  const headers: Record<string, string> = { ...options.headers }
  if (hasBody)
    headers['Content-Type'] = 'application/json'
  if (method !== 'GET')
    headers['X-CSRFToken'] = readCsrfCookie()

  let response: Response
  try {
    response = await fetch(buildUrl(url, options.params), {
      method,
      headers,
      body: hasBody ? JSON.stringify(data) : undefined,
      credentials: 'same-origin',
      signal: options.signal,
    })
  }
  catch (err) {
    // Let caller-initiated cancellation surface as-is.
    if (err instanceof DOMException && err.name === 'AbortError')
      throw err
    throw new NetworkError(err)
  }

  if (response.status === 401)
    redirectToLogin()

  if (!response.ok) {
    const errorData = await response.json().catch(() => undefined)
    if (response.status === 400 || response.status === 422) {
      throw new ValidationError(
        response.status,
        response.statusText,
        errorData,
        parseFieldErrors(errorData),
      )
    }
    throw new HttpError(response.status, response.statusText, errorData)
  }

  if (response.status === 204)
    return undefined as T
  return response.json()
}

export const http = {
  get: <T>(url: string, options?: RequestOptions) =>
    request<T>('GET', url, undefined, options),
  post: <T>(url: string, data?: unknown, options?: RequestOptions) =>
    request<T>('POST', url, data, options),
  put: <T>(url: string, data?: unknown, options?: RequestOptions) =>
    request<T>('PUT', url, data, options),
  patch: <T>(url: string, data?: unknown, options?: RequestOptions) =>
    request<T>('PATCH', url, data, options),
  delete: <T>(url: string, options?: RequestOptions) =>
    request<T>('DELETE', url, undefined, options),
}
