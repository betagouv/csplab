import { setupServer } from 'msw/node'
import { recrutementsHandlers } from './handlers/recrutements'
import { tagsHandlers } from './handlers/tags'

export const server = setupServer(...recrutementsHandlers, ...tagsHandlers)
