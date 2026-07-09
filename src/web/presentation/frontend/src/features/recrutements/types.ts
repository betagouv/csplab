import type { components } from '@/types/api'

export type PaginatedRecrutementsActifsResponse = components['schemas']['PaginatedRecrutementsActifsResponse']

export type PaginatedRecrutementsArchivesResponse = components['schemas']['PaginatedRecrutementsArchivesResponse']

export type RecrutementsActifs = components['schemas']['RecrutementsActifs']

export type RecrutementsArchives = components['schemas']['RecrutementsArchives']

export type RecrutementBase = RecrutementsActifs | RecrutementsArchives

export type RecrutementKey = 'actifs' | 'archives'

export type TypeContrat = components['schemas']['TypeContratEnum']

export type PaginatedCandidatureListeResponse = components['schemas']['PaginatedCandidatureListeResponse']

export type CandidatureListe = components['schemas']['CandidatureListe']

export type EtapeRecrutement = components['schemas']['EtapeRecrutement']

export type RecrutementDetail = components['schemas']['RecrutementDetailKanban']
