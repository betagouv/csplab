import type { paths } from '@/types/api'
import { HttpResponse } from 'msw'
import { createOpenApiHttp } from 'openapi-msw'

export const http = createOpenApiHttp<paths>()

export function failure(status: number, body?: Record<string, unknown>) {
  return body ? HttpResponse.json(body, { status }) : new HttpResponse(null, { status })
}

export function exceptSegments<Param extends string, Info extends { params: Record<Param, string> }, Result>(
  segments: string[],
  param: Param,
  resolve: (info: Info) => Result,
) {
  return (info: Info) => segments.includes(info.params[param]) ? undefined : resolve(info)
}
