export class HttpError extends Error {
  constructor(
    public readonly status: number,
    public readonly statusText: string,
    public readonly data?: unknown,
  ) {
    super(`HTTP ${status}: ${statusText}`)
    this.name = 'HttpError'
  }
}

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

async function request<T>(
  method: HttpMethod,
  url: string,
  data?: unknown,
  options: RequestOptions = {},
): Promise<T> {
  const hasBody = data !== undefined
  const headers: Record<string, string> = { ...options.headers }

  if (hasBody) {
    headers['Content-Type'] = 'application/json'
  }
  if (method !== 'GET') {
    headers['X-CSRFToken'] = readCsrfCookie()
  }

  let finalUrl = url
  if (options.params) {
    const searchParams = new URLSearchParams()
    for (const [key, value] of Object.entries(options.params)) {
      searchParams.append(key, String(value))
    }
    finalUrl = `${url}?${searchParams.toString()}`
  }

  const response = await fetch(finalUrl, {
    method,
    headers,
    body: hasBody ? JSON.stringify(data) : undefined,
    credentials: 'same-origin',
    signal: options.signal,
  })

  if (response.status === 401) {
    redirectToLogin()
  }

  if (!response.ok) {
    let errorData: unknown
    try {
      errorData = await response.json()
    }
    catch {
      errorData = undefined
    }
    throw new HttpError(response.status, response.statusText, errorData)
  }

  if (response.status === 204) {
    return undefined as T
  }

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
