import type { components } from '@/types/api'

export type RecrutementsActifs = components['schemas']['RecrutementsActifs']

export type RecrutementsArchives = components['schemas']['RecrutementsArchives']

export type RecrutementBase = RecrutementsActifs | RecrutementsArchives

export type RecrutementKey = 'actifs' | 'archives'

export type TypeContrat = components['schemas']['TypeContratEnum']
