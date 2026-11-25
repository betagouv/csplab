import type { paths } from '@/types/api'
import { HttpResponse } from 'msw'
import { createOpenApiHttp } from 'openapi-msw'

export const http = createOpenApiHttp<paths>()

export function failure(status: number, body?: Record<string, unknown>) {
  return body ? HttpResponse.json(body, { status }) : new HttpResponse(null, { status })
}
