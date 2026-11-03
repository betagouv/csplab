import type * as Api from '@/api/utilisateur'
import { DEMO_UTILISATEUR } from '@/api/__mocks__/demo'

export const getMe: typeof Api.getMe = async () => DEMO_UTILISATEUR

export const logout: typeof Api.logout = () => undefined
