// Copies of the pictograms of the DSFR 1.14.2 (dist/artwork/pictograms), MIT licence of the DSFR. A file holds three
// symbols, artwork-decorative, artwork-minor and artwork-major, that CspPictogram colours with the artwork tokens.
export type CspPictogramName
  = | 'buildings/city-hall'
    | 'buildings/companie'
    | 'digital/application'
    | 'digital/calendar'
    | 'digital/mail-send'
    | 'digital/search'
    | 'document/archive'
    | 'document/binders'
    | 'document/conclusion'
    | 'document/contract'
    | 'document/document'
    | 'document/document-add'
    | 'document/document-search'
    | 'leisure/community'
    | 'system/flow-settings'
    | 'system/padlock'
    | 'system/technical-error'

// Never inlined: a <use> element ignores a symbol of a data URL
const urls = import.meta.glob<string>('./artwork/*/*.svg', { query: '?url&no-inline', import: 'default', eager: true })

export function pictogramUrl(name: CspPictogramName): string {
  return urls[`./artwork/${name}.svg`]!
}
