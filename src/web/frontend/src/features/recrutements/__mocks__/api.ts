import type * as Api from '@/features/recrutements/api'
import { paginated } from '@/api/__mocks__/demo'
import { DEMO_RECRUTEMENT_DETAIL, DEMO_RECRUTEMENTS_ACTIFS } from '@/features/recrutements/__mocks__/demo'

export const getRecrutementDetail: typeof Api.getRecrutementDetail = async () => DEMO_RECRUTEMENT_DETAIL

export const getRecrutementsActifs: typeof Api.getRecrutementsActifs = async () => paginated(DEMO_RECRUTEMENTS_ACTIFS)

export const getRecrutementsArchives: typeof Api.getRecrutementsArchives = async () => paginated([])

export const setRecrutementsResponsable: typeof Api.setRecrutementsResponsable = async () => ({ reussites: [], echecs: [] })
