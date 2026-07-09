import type { Middleware } from 'openapi-fetch'
import type { paths } from '@/types/api'
import createClient from 'openapi-fetch'
import { HttpError, NetworkError, parseFieldErrors, ValidationError } from './errors'

function readCsrfCookie(): string {
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/)
  return match ? decodeURIComponent(match[1]) : ''
}

function redirectToLogin(): never {
  const next = encodeURIComponent(window.location.pathname + window.location.search)
  window.location.href = `/utilisateur/connexion?next=${next}`
  throw new Error('Redirecting to login')
}

const csrfMiddleware: Middleware = {
  async onRequest({ request }) {
    if (request.method === 'GET')
      return undefined
    request.headers.set('X-CSRFToken', readCsrfCookie())
    return request
  },
}

const errorMiddleware: Middleware = {
  async onResponse({ response }) {
    if (response.ok)
      return undefined

    if (response.status === 401)
      redirectToLogin()

    const data = await response.clone().json().catch(() => undefined)

    if (response.status === 400 || response.status === 422) {
      throw new ValidationError(
        response.status,
        response.statusText,
        data,
        parseFieldErrors(data),
      )
    }

    throw new HttpError(response.status, response.statusText, data)
  },
}

const rawClient = createClient<paths>({
  baseUrl: typeof window !== 'undefined' ? window.location.origin : '',
  credentials: 'same-origin',
  fetch: (...args) => globalThis.fetch(...args),
})
rawClient.use(csrfMiddleware)
rawClient.use(errorMiddleware)

export const api = wrapWithNetworkErrors(rawClient)

type RawClient = typeof rawClient
type Method = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' | 'HEAD' | 'OPTIONS' | 'TRACE'

function wrapWithNetworkErrors(client: RawClient): RawClient {
  const methods: Method[] = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS', 'TRACE']
  const wrapped = { ...client } as RawClient
  for (const method of methods) {
    const original = client[method] as (...args: unknown[]) => Promise<unknown>
    ;(wrapped as Record<Method, unknown>)[method] = async (...args: unknown[]) => {
      try {
        return await original(...args)
      }
      catch (err) {
        if (err instanceof DOMException && err.name === 'AbortError')
          throw err
        if (err instanceof HttpError)
          throw err
        if (err instanceof Error && err.message === 'Redirecting to login')
          throw err
        throw new NetworkError(err)
      }
    }
  }
  return wrapped
}
