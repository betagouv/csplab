import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { organismeHomeLocation, recrutementsListLocation } from './names'

export const HOME_BREADCRUMB_LABEL = 'Accueil'

export function homeBreadcrumbItem(organismeUuid: string): CspBreadcrumbItem {
  return { label: HOME_BREADCRUMB_LABEL, to: organismeHomeLocation(organismeUuid) }
}

export const RECRUTEMENTS_BREADCRUMB_LABEL = 'Recrutements'

export function recrutementsBreadcrumbItem(organismeUuid: string, archive: boolean | undefined): CspBreadcrumbItem {
  return { label: RECRUTEMENTS_BREADCRUMB_LABEL, to: recrutementsListLocation(organismeUuid, archive) }
}
