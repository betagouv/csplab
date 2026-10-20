import type * as Api from '@/features/etapes-recrutement/api'
import { DEMO_ETAPES } from '@/features/recrutements/__mocks__/demo'

export const getEtapesRecrutement: typeof Api.getEtapesRecrutement = async () => DEMO_ETAPES

export const updateEtapesRecrutement: typeof Api.updateEtapesRecrutement = async () => DEMO_ETAPES

export const initEtapesRecrutement: typeof Api.initEtapesRecrutement = async () => DEMO_ETAPES

export const getEtapesOffre: typeof Api.getEtapesOffre = async () => DEMO_ETAPES

export const updateEtapesOffre: typeof Api.updateEtapesOffre = async () => DEMO_ETAPES

export const initEtapesOffre: typeof Api.initEtapesOffre = async () => DEMO_ETAPES
