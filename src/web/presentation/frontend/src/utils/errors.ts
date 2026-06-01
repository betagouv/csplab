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

export class NetworkError extends Error {
  constructor(public readonly cause: unknown) {
    super('Network request failed')
    this.name = 'NetworkError'
  }
}

export class ValidationError extends HttpError {
  constructor(
    status: number,
    statusText: string,
    data: unknown,
    public readonly fieldErrors: Record<string, string[]>,
  ) {
    super(status, statusText, data)
    this.name = 'ValidationError'
  }
}

const META_KEYS = new Set(['detail', 'status', 'message', 'type'])

/** Extracts per-field errors from a DRF native or custom-handler payload. */
export function parseFieldErrors(payload: unknown): Record<string, string[]> {
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
    return {}
  }
  const obj = payload as Record<string, unknown>
  const isCustomHandler
    = obj.status === 'error'
      && obj.details
      && typeof obj.details === 'object'
      && !Array.isArray(obj.details)
  const source = isCustomHandler
    ? (obj.details as Record<string, unknown>)
    : obj

  const out: Record<string, string[]> = {}
  for (const [key, value] of Object.entries(source)) {
    if (source === obj && META_KEYS.has(key))
      continue
    if (Array.isArray(value)) {
      const strings = value.filter((v): v is string => typeof v === 'string')
      if (strings.length > 0)
        out[key] = strings
    }
    else if (typeof value === 'string') {
      out[key] = [value]
    }
  }
  return out
}
