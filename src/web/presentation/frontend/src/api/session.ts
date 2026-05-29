import { http } from '@/utils/http'

export interface Session {
  user: {
    email: string
    is_authenticated: boolean
  }
}

export const sessionApi = {
  get: () => http.get<Session>('/ats/api/session/'),
  ping: () => http.get<{ status: string }>('/ats/api/ping/'),
}
