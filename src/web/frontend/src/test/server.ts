import { setupServer } from 'msw/node'
import { agentsHandlers } from './handlers/agents'
import { candidaturesHandlers } from './handlers/candidatures'
import { equipeRecrutementHandlers } from './handlers/equipe-recrutement'
import { etapesRecrutementHandlers } from './handlers/etapes-recrutement'
import { messagesHandlers } from './handlers/messages'
import { organismesHandlers } from './handlers/organismes'
import { recrutementsHandlers } from './handlers/recrutements'
import { tagsHandlers } from './handlers/tags'

export const server = setupServer(...agentsHandlers, ...candidaturesHandlers, ...equipeRecrutementHandlers, ...etapesRecrutementHandlers, ...messagesHandlers, ...organismesHandlers, ...recrutementsHandlers, ...tagsHandlers)
