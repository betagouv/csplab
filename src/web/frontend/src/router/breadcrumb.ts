import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { HOME_ROUTE_NAME, recrutementsListLocation } from './names'

export const HOME_BREADCRUMB_ITEM: CspBreadcrumbItem = { label: 'Accueil', to: { name: HOME_ROUTE_NAME } }

export const RECRUTEMENTS_BREADCRUMB_LABEL = 'Recrutements'

export function recrutementsBreadcrumbItem(organismeUuid: string, archive: boolean | undefined): CspBreadcrumbItem {
  return { label: RECRUTEMENTS_BREADCRUMB_LABEL, to: recrutementsListLocation(organismeUuid, archive) }
}
