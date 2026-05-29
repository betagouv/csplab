export interface AppUser {
  is_authenticated: boolean
  email?: string
}

export interface AppConfig {
  csrfToken: string
  user: AppUser
}

declare global {
  interface Window {
    __APP_CONFIG__: AppConfig
  }
}

export function getCsrfToken(): string {
  return window.__APP_CONFIG__.csrfToken
}
