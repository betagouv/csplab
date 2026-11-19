import { setupServer } from 'msw/node'
import { recrutementsHandlers } from './handlers/recrutements'

export const server = setupServer(...recrutementsHandlers)
