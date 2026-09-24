import type { Message, PersonId, Settings } from './types'
import { PEOPLE } from '../data/scenario'
import { formatStamp, fullName } from './format'

export type Viewer = 'recruteur' | 'candidat'

export interface ThreadProps {
  messages: Message[]
  viewerId: PersonId
  viewer: Viewer
  settings: Settings
  now: Date
}

export interface AuthorLabel {
  name: string
  role: string
  isViewer: boolean
  isTeam: boolean
}

export function authorLabel(message: Message, viewerId: PersonId, viewer: Viewer): AuthorLabel {
  const author = PEOPLE[message.authorId]
  const isViewer = message.authorId === viewerId
  const role = viewer === 'candidat' && author.equipe ? author.fonction ?? author.role : author.role
  return {
    name: isViewer ? `${fullName(author)} (vous)` : fullName(author),
    role: isViewer ? '' : role,
    isViewer,
    isTeam: author.equipe,
  }
}

export function readLine(message: Message, props: ThreadProps): string | null {
  if (!props.settings.readReceipts)
    return null
  const author = PEOPLE[message.authorId]
  if (props.viewer === 'recruteur') {
    if (!author.equipe || !message.readByCandidateAt)
      return null
    return props.settings.dates === 'relatives'
      ? `Lu ${formatStamp(message.readByCandidateAt, props.now, 'relatives')}`
      : `Lu par la candidate le ${formatStamp(message.readByCandidateAt, props.now, 'absolues')}`
  }
  if (message.authorId !== props.viewerId)
    return null
  const firstRead = Object.values(message.readByTeam).sort()[0]
  if (!firstRead)
    return 'Non lu'
  return props.settings.dates === 'relatives'
    ? `Lu ${formatStamp(firstRead, props.now, 'relatives')}`
    : `Lu par l’équipe le ${formatStamp(firstRead, props.now, 'absolues')}`
}

export function receptionLine(message: Message, props: ThreadProps): string | null {
  if (props.viewer !== 'candidat' || !props.settings.progress || message.authorId !== props.viewerId)
    return null
  return 'Transmis à l’équipe de recrutement'
}

export function side(message: Message, props: ThreadProps): 'left' | 'right' {
  if (props.viewer === 'candidat' || props.settings.sideRule === 'moi')
    return message.authorId === props.viewerId ? 'right' : 'left'
  return PEOPLE[message.authorId].equipe ? 'right' : 'left'
}
