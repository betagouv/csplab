import { setupServer } from 'msw/node'
import { agentsHandlers } from './handlers/agents'
import { equipeRecrutementHandlers } from './handlers/equipe-recrutement'
import { etapesRecrutementHandlers } from './handlers/etapes-recrutement'
import { recrutementsHandlers } from './handlers/recrutements'
import { tagsHandlers } from './handlers/tags'

export const server = setupServer(...agentsHandlers, ...equipeRecrutementHandlers, ...etapesRecrutementHandlers, ...recrutementsHandlers, ...tagsHandlers)
