import type { paths } from '@/types/api'
import { HttpResponse } from 'msw'
import { createOpenApiHttp } from 'openapi-msw'

export const http = createOpenApiHttp<paths>()

export function failure(status: number) {
  return new HttpResponse(null, { status })
}
