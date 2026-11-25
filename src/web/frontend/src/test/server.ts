import { setupServer } from 'msw/node'
import { agentsHandlers } from './handlers/agents'
import { recrutementsHandlers } from './handlers/recrutements'
import { tagsHandlers } from './handlers/tags'

export const server = setupServer(...agentsHandlers, ...recrutementsHandlers, ...tagsHandlers)
