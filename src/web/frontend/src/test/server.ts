import { setupServer } from 'msw/node'
import { agentsHandlers } from './handlers/agents'
import { etapesRecrutementHandlers } from './handlers/etapes-recrutement'
import { recrutementsHandlers } from './handlers/recrutements'
import { tagsHandlers } from './handlers/tags'

export const server = setupServer(...agentsHandlers, ...etapesRecrutementHandlers, ...recrutementsHandlers, ...tagsHandlers)
