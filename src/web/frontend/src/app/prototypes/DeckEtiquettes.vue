<script setup lang="ts">
import type { Dichromacy, LinearRgb } from '@/styles/color'
import type { PaletteColor } from '@/styles/palette'
import { nextTick, onMounted, ref } from 'vue'
import { DEMO_CANDIDATURE } from '@/api/__mocks__/demo'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspLabel from '@/components/base/CspLabel/CspLabel.vue'
import CspLabelList from '@/components/base/CspLabel/CspLabelList.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import { demoCandidatureDetail, demoKanban, demoNotes, ETIQUETTES_CANDIDATURE } from '@/features/candidatures/__mocks__/demo'
import CandidatureEtiquettes from '@/features/candidatures/components/CandidatureEtiquettes.vue'
import CandidatureKanbanCard from '@/features/candidatures/components/CandidatureKanbanCard.vue'
import CandidatureNoteMessage from '@/features/candidatures/components/CandidatureNoteMessage.vue'
import { etiquettesOf } from '@/features/candidatures/etiquettes'
import { contrastRatio, deltaEOk, DICHROMACIES, hexToLinearRgb, oklchToLinearRgb, simulateDichromacy } from '@/styles/color'
import { PALETTE_COLOR_NAMES, PALETTE_COLORS } from '@/styles/palette'
import { formatDateTime } from '@/utils/date'

export type DeckPlanche
  = | 'tag-dsfr'
    | 'tag-dsfr-couleur'
    | 'badge-dsfr'
    | 'badge-dsfr-couleurs'
    | 'couleurs-dsfr'
    | 'cartes'
    | 'panneau'
    | 'note'
    | 'voisins'
    | 'palette'
    | 'contrastes'
    | 'ecarts'
    | 'daltonisme'
    | 'bordures'

const props = withDefaults(defineProps<{
  planche: DeckPlanche
  // Draws the labels as DSFR tags, with the tag colors of the DSFR families
  formeTag?: boolean
}>(), {
  formeTag: false,
})

// DSFR illustrative colors, in the order of the DSFR documentation
const FAMILLES = [
  { id: 'green-tilleul-verveine', nom: 'Tilleul verveine' },
  { id: 'green-bourgeon', nom: 'Bourgeon' },
  { id: 'green-emeraude', nom: 'Émeraude' },
  { id: 'green-menthe', nom: 'Menthe' },
  { id: 'green-archipel', nom: 'Archipel' },
  { id: 'blue-ecume', nom: 'Écume' },
  { id: 'blue-cumulus', nom: 'Cumulus' },
  { id: 'purple-glycine', nom: 'Glycine' },
  { id: 'pink-macaron', nom: 'Macaron' },
  { id: 'pink-tuile', nom: 'Tuile' },
  { id: 'yellow-tournesol', nom: 'Tournesol' },
  { id: 'yellow-moutarde', nom: 'Moutarde' },
  { id: 'orange-terre-battue', nom: 'Terre battue' },
  { id: 'brown-cafe-creme', nom: 'Café crème' },
  { id: 'brown-caramel', nom: 'Caramel' },
  { id: 'brown-opera', nom: 'Opéra' },
  { id: 'beige-gris-galet', nom: 'Gris galet' },
] as const

const FAMILLES_TAG = FAMILLES.filter(({ id }) => ['green-emeraude', 'blue-cumulus', 'purple-glycine', 'pink-tuile', 'yellow-tournesol'].includes(id))

const BADGES_SYSTEME = [
  { type: 'success', libelle: 'Acceptée', icone: 'ri:checkbox-circle-fill' },
  { type: 'error', libelle: 'Refusée', icone: 'ri:spam-fill' },
  { type: 'info', libelle: 'En cours', icone: 'ri:information-fill' },
  { type: 'warning', libelle: 'Incomplète', icone: 'ri:alert-fill' },
  { type: 'new', libelle: 'Nouvelle', icone: 'ri:flashlight-fill' },
] as const

const TAILLES = ['sm', 'md'] as const

const PREMIERE_ETAPE = demoKanban().etapes[0]!
const CARTES = [0, 2].map(index => PREMIERE_ETAPE.candidatures[index]!)
const ETIQUETTES_PANNEAU = etiquettesOf(demoCandidatureDetail(DEMO_CANDIDATURE.uuid) ?? {})
const NOTE = demoNotes(DEMO_CANDIDATURE.uuid)[0]!
const E = ETIQUETTES_CANDIDATURE
const ETIQUETTES_VOISINES = [E.titulaire, E.prioritaire, E.mobilite, E.contractuel]
const COULEURS_BORDURES: PaletteColor[] = ['grey', 'blue', 'yellow', 'orange', 'brown']

const FONDS = [
  { id: 'blanc', nom: 'Fond' },
  { id: 'colonne', nom: 'Colonne' },
  { id: 'note', nom: 'Note' },
  { id: 'panneau', nom: 'Panneau' },
] as const

const DICHROMASIES: Record<Dichromacy, string> = {
  protanopia: 'Protanopie',
  deuteranopia: 'Deutéranopie',
  tritanopia: 'Tritanopie',
}

function parseCssColor(value: string): LinearRgb | null {
  const oklch = value.match(/^oklch\(([^)]+)\)/)
  if (oklch) {
    const [l, c, h] = oklch[1]!.split(/[\s/]+/).map(part => part.endsWith('%') ? Number.parseFloat(part) / 100 : Number.parseFloat(part))
    return oklchToLinearRgb({ l: l!, c: c!, h: Number.isNaN(h) ? 0 : h! })
  }
  const rgb = value.match(/^rgba?\(([^)]+)\)/)
  if (rgb) {
    const hex = rgb[1]!.split(/[\s,/]+/).slice(0, 3).map(channel => Math.round(Number.parseFloat(channel)).toString(16).padStart(2, '0')).join('')
    return hexToLinearRgb(hex)
  }
  return null
}

function toHex(rgb: LinearRgb): string {
  const channels = rgb.map((channel) => {
    const encoded = channel <= 0.0031308 ? channel * 12.92 : 1.055 * channel ** (1 / 2.4) - 0.055
    return Math.round(Math.min(1, Math.max(0, encoded)) * 255).toString(16).padStart(2, '0')
  })
  return `#${channels.join('')}`
}

function formatNumber(value: number, digits: number): string {
  return value.toFixed(digits).replace('.', ',')
}

interface RenderedColor {
  background: LinearRgb
  text: LinearRgb
  dot: LinearRgb | null
}

const racine = ref<HTMLElement | null>(null)
const contrastes = ref<Partial<Record<PaletteColor, string>>>({})
const ecarts = ref<{ first: PaletteColor, second: PaletteColor, distance: string }[]>([])
const simulations = ref<Partial<Record<Dichromacy, Record<string, string>>>>({})

function renderedColors(): Partial<Record<PaletteColor, RenderedColor>> {
  const colors: Partial<Record<PaletteColor, RenderedColor>> = {}
  racine.value?.querySelectorAll<HTMLElement>('[data-mesure] .csp-label').forEach((label) => {
    const color = label.dataset.color as PaletteColor
    const style = getComputedStyle(label)
    const dot = label.querySelector<HTMLElement>('.csp-label__dot')
    const background = parseCssColor(style.backgroundColor)
    const text = parseCssColor(style.color)
    if (background && text) {
      colors[color] = { background, text, dot: dot ? parseCssColor(getComputedStyle(dot).backgroundColor) : null }
    }
  })
  return colors
}

onMounted(async () => {
  await nextTick()
  const colors = renderedColors()
  contrastes.value = Object.fromEntries(Object.entries(colors).map(([color, { background, text }]) =>
    [color, `${formatNumber(contrastRatio(background, text), 2)}∶1`]))
  ecarts.value = PALETTE_COLORS.flatMap((first, index) => PALETTE_COLORS.slice(index + 1).map(second => ({ first, second })))
    .filter(({ first, second }) => colors[first] && colors[second])
    .map(({ first, second }) => ({ first, second, value: deltaEOk(colors[first]!.background, colors[second]!.background) }))
    .sort((a, b) => a.value - b.value)
    .slice(0, 4)
    .map(({ first, second, value }) => ({ first, second, distance: formatNumber(value, 3) }))
  simulations.value = Object.fromEntries(DICHROMACIES.map(type => [type, Object.fromEntries(
    Object.entries(colors).flatMap(([color, { background, text, dot }]) => [
      [`--csp-palette-${color}-background`, toHex(simulateDichromacy(background, type))],
      [`--csp-palette-${color}-text`, toHex(simulateDichromacy(text, type))],
      ...(dot ? [[`--csp-palette-${color}-dot`, toHex(simulateDichromacy(dot, type))]] : []),
    ]),
  )]))
})
</script>

<template>
  <div
    ref="racine"
    class="deck"
    :class="{ 'deck--tag': props.formeTag }"
  >
    <div
      v-if="planche === 'tag-dsfr'"
      class="deck__grille deck__grille--tailles"
    >
      <template
        v-for="taille in TAILLES"
        :key="taille"
      >
        <span class="deck__legende">{{ taille }}</span>
        <span
          class="deck-tag deck-tag--statique"
          :class="`deck-tag--${taille}`"
        >Non cliquable</span>
        <span
          class="deck-tag deck-tag--cliquable"
          :class="`deck-tag--${taille}`"
        >Cliquable</span>
        <span
          class="deck-tag deck-tag--selectionne"
          :class="`deck-tag--${taille}`"
        >Sélectionné</span>
        <span
          class="deck-tag deck-tag--supprimable"
          :class="`deck-tag--${taille}`"
        >Supprimable<CspIcon
          name="ri:close-line"
          :size="taille === 'sm' ? 12 : 16"
        /></span>
      </template>
    </div>

    <div
      v-else-if="planche === 'tag-dsfr-couleur'"
      class="deck__grille deck__grille--couleur"
    >
      <span class="deck__legende">Non cliquable</span>
      <span
        v-for="famille in FAMILLES_TAG"
        :key="`statique-${famille.id}`"
        class="deck-tag deck-tag--md deck-tag--statique"
      >{{ famille.nom }}</span>
      <span class="deck__legende">Cliquable</span>
      <span
        v-for="famille in FAMILLES_TAG"
        :key="`cliquable-${famille.id}`"
        class="deck-tag deck-tag--md"
        :style="{ backgroundColor: `var(--background-action-low-${famille.id})`, color: `var(--text-action-high-${famille.id})` }"
      >{{ famille.nom }}</span>
    </div>

    <div
      v-else-if="planche === 'badge-dsfr'"
      class="deck__grille deck__grille--badges"
    >
      <template
        v-for="taille in TAILLES"
        :key="taille"
      >
        <span class="deck__legende">{{ taille }}</span>
        <span
          class="deck-badge"
          :class="`deck-badge--${taille}`"
        >Brouillon</span>
        <span
          class="deck-badge deck-badge--success"
          :class="`deck-badge--${taille}`"
        ><CspIcon
          name="ri:checkbox-circle-fill"
          :size="taille === 'sm' ? 12 : 16"
        />Acceptée</span>
      </template>
    </div>

    <div
      v-else-if="planche === 'badge-dsfr-couleurs'"
      class="deck__grille deck__grille--couleur"
    >
      <span class="deck__legende">Système</span>
      <span
        v-for="badge in BADGES_SYSTEME"
        :key="badge.type"
        class="deck-badge deck-badge--md"
        :class="`deck-badge--${badge.type}`"
      ><CspIcon
        :name="badge.icone"
        :size="16"
      />{{ badge.libelle }}</span>
      <span class="deck__legende">Illustrative</span>
      <span
        v-for="famille in FAMILLES_TAG"
        :key="famille.id"
        class="deck-badge deck-badge--md"
        :style="{ backgroundColor: `var(--background-contrast-${famille.id})`, color: `var(--text-label-${famille.id})` }"
      >{{ famille.nom }}</span>
    </div>

    <div
      v-else-if="planche === 'couleurs-dsfr'"
      class="deck__familles"
    >
      <span
        v-for="famille in FAMILLES"
        :key="famille.id"
        class="deck-tag deck-tag--md"
        :style="{ backgroundColor: `var(--background-action-low-${famille.id})`, color: `var(--text-action-high-${famille.id})` }"
      >{{ famille.nom }}</span>
    </div>

    <div
      v-else-if="planche === 'cartes'"
      class="deck__cartes"
    >
      <CandidatureKanbanCard
        v-for="(candidature, index) in CARTES"
        :key="candidature.uuid"
        :candidature="candidature"
        board-id="deck"
        :column-id="PREMIERE_ETAPE.uuid"
        :card-index="index"
      />
    </div>

    <div
      v-else-if="planche === 'panneau'"
      class="deck__panneau"
    >
      <CandidatureEtiquettes :etiquettes="ETIQUETTES_PANNEAU" />
    </div>

    <CspCard
      v-else-if="planche === 'note'"
      as="div"
      variant="alt"
      class="deck__note"
    >
      <template #start>
        <span class="deck__note-auteur">{{ NOTE.publie_par_prenom }} {{ NOTE.publie_par_nom }}</span>
        <span
          class="deck__note-separateur"
          aria-hidden="true"
        >•</span>
        <time
          :datetime="NOTE.publie_le"
          class="deck__note-horodatage"
        >
          {{ formatDateTime(NOTE.publie_le) }}
        </time>
      </template>
      <CspLabelList
        class="deck__note-etiquettes"
        :labels="etiquettesOf(NOTE)"
        removable
      />
      <CandidatureNoteMessage :message="NOTE.message" />
    </CspCard>

    <div
      v-else-if="planche === 'voisins'"
      class="deck__voisins"
    >
      <div class="deck__groupe">
        <CspLabel
          v-for="etiquette in ETIQUETTES_VOISINES"
          :key="etiquette.libelle"
          :label="etiquette.libelle"
          :color="etiquette.couleur"
          size="md"
        />
      </div>
      <div class="deck__groupe">
        <CspBadge
          type="success"
          label="Acceptée"
        />
        <CspBadge
          type="error"
          label="Refusée"
        />
        <CspBadge
          type="info"
          label="En cours"
        />
      </div>
      <div class="deck__groupe">
        <CspTag
          variant="clickable"
          label="Présélection"
        />
        <CspTag
          variant="selectable"
          label="Entretien RH"
          :pressed="true"
        />
        <CspButton
          variant="secondary"
          label="Ajouter une note"
        />
      </div>
    </div>

    <div
      v-else-if="planche === 'palette'"
      class="deck__palette"
    >
      <CspLabel
        v-for="couleur in PALETTE_COLORS"
        :key="couleur"
        :label="PALETTE_COLOR_NAMES[couleur]"
        :color="couleur"
        size="md"
      />
    </div>

    <div
      v-else-if="planche === 'contrastes'"
      class="deck__contrastes"
      data-mesure
    >
      <div
        v-for="couleur in PALETTE_COLORS"
        :key="couleur"
        class="deck__contraste"
      >
        <CspLabel
          :label="PALETTE_COLOR_NAMES[couleur]"
          :color="couleur"
          size="md"
        />
        <span class="deck__valeur">{{ contrastes[couleur] }}</span>
      </div>
    </div>

    <div
      v-else-if="planche === 'ecarts'"
      class="deck__ecarts"
    >
      <div
        class="deck__mesure-cachee"
        data-mesure
        aria-hidden="true"
      >
        <CspLabel
          v-for="couleur in PALETTE_COLORS"
          :key="couleur"
          :label="PALETTE_COLOR_NAMES[couleur]"
          :color="couleur"
          size="md"
        />
      </div>
      <div
        v-for="ecart in ecarts"
        :key="`${ecart.first}-${ecart.second}`"
        class="deck__ecart"
      >
        <CspLabel
          :label="PALETTE_COLOR_NAMES[ecart.first]"
          :color="ecart.first"
          size="md"
        />
        <CspLabel
          :label="PALETTE_COLOR_NAMES[ecart.second]"
          :color="ecart.second"
          size="md"
        />
        <span class="deck__valeur">{{ ecart.distance }}</span>
      </div>
    </div>

    <div
      v-else-if="planche === 'daltonisme'"
      class="deck__grille deck__grille--daltonisme"
    >
      <span class="deck__legende">Vision ordinaire</span>
      <div
        class="deck__groupe"
        data-mesure
      >
        <CspLabel
          v-for="couleur in PALETTE_COLORS"
          :key="couleur"
          :label="PALETTE_COLOR_NAMES[couleur]"
          :color="couleur"
          size="md"
        />
      </div>
      <template
        v-for="type in DICHROMACIES"
        :key="type"
      >
        <span class="deck__legende">{{ DICHROMASIES[type] }}</span>
        <div
          class="deck__groupe"
          :style="simulations[type]"
        >
          <CspLabel
            v-for="couleur in PALETTE_COLORS"
            :key="couleur"
            :label="PALETTE_COLOR_NAMES[couleur]"
            :color="couleur"
            size="md"
          />
        </div>
      </template>
    </div>

    <div
      v-else-if="planche === 'bordures'"
      class="deck__grille deck__grille--bordures"
    >
      <span />
      <span class="deck__legende">Sans filet</span>
      <span class="deck__legende">Avec filet</span>
      <template
        v-for="fond in FONDS"
        :key="fond.id"
      >
        <span class="deck__legende">{{ fond.nom }}</span>
        <div
          v-for="filet in [false, true]"
          :key="String(filet)"
          class="deck__cellule"
          :class="[`deck__cellule--${fond.id}`, { 'deck__cellule--filet': filet }]"
        >
          <CspLabel
            v-for="couleur in COULEURS_BORDURES"
            :key="couleur"
            :label="PALETTE_COLOR_NAMES[couleur]"
            :color="couleur"
            size="md"
          />
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped lang="scss">
.deck {
  display: grid;
  place-items: center;
  min-height: 100vh;
  padding: var(--csp-space-8);
  background-color: var(--background-default-grey);
  color: var(--text-default-grey);
}

.deck__legende {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.deck__grille {
  display: grid;
  align-items: center;
  justify-items: start;
  gap: var(--csp-space-6) var(--csp-space-6);
}

.deck__grille--tailles {
  grid-template-columns: auto repeat(4, auto);
}

.deck__grille--couleur {
  grid-template-columns: auto repeat(5, auto);
  justify-items: start;
}

.deck__grille--badges {
  grid-template-columns: auto repeat(2, auto);
  justify-items: start;
}

.deck__grille--daltonisme {
  grid-template-columns: auto auto;
  gap: var(--csp-space-5) var(--csp-space-6);
}

.deck__grille--bordures {
  grid-template-columns: auto repeat(2, auto);
  gap: var(--csp-space-3) var(--csp-space-4);
}

.deck__groupe {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-2);
}

/* DSFR tag, fr-tag and fr-tag--sm of DSFR 1.15.4 */
.deck-tag {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  min-width: 2.25rem;
  min-height: 2rem;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: var(--csp-font-weight-regular);
  line-height: 1.5rem;
  white-space: nowrap;
}

.deck-tag--sm {
  gap: 0.125rem;
  min-height: 1.5rem;
  padding: 0.125rem 0.5rem;
  border-radius: 0.75rem;
  font-size: 0.75rem;
  line-height: 1.25rem;
}

.deck-tag--statique {
  background-color: var(--background-contrast-grey);
  color: var(--text-label-grey);
}

.deck-tag--cliquable {
  background-color: var(--background-action-low-blue-france);
  color: var(--text-action-high-blue-france);
}

.deck-tag--selectionne {
  background-color: var(--background-active-blue-france);
  color: var(--text-inverted-blue-france);
}

.deck-tag--supprimable {
  background-color: var(--background-action-high-blue-france);
  color: var(--text-inverted-blue-france);
}

/* DSFR badge, fr-badge and fr-badge--sm of DSFR 1.15.4 */
.deck-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  min-height: 1.5rem;
  padding: 0 0.5rem;
  border-radius: 0.25rem;
  background-color: var(--background-contrast-grey);
  color: var(--text-label-grey);
  font-size: 0.875rem;
  font-weight: var(--csp-font-weight-bold);
  line-height: 1.5rem;
  text-transform: uppercase;
  white-space: nowrap;
}

.deck-badge--sm {
  min-height: 1.125rem;
  padding: 0 0.375rem;
  font-size: 0.75rem;
  line-height: 1.25rem;
}

.deck-badge--success {
  background-color: var(--background-contrast-success);
  color: var(--text-default-success);
}

.deck-badge--error {
  background-color: var(--background-contrast-error);
  color: var(--text-default-error);
}

.deck-badge--info {
  background-color: var(--background-contrast-info);
  color: var(--text-default-info);
}

.deck-badge--warning {
  background-color: var(--background-contrast-warning);
  color: var(--text-default-warning);
}

.deck-badge--new {
  background-color: var(--background-contrast-yellow-moutarde);
  color: var(--text-label-yellow-moutarde);
}

.deck__familles {
  display: grid;
  grid-template-columns: repeat(6, auto);
  justify-items: start;
  gap: var(--csp-space-4);
}

.deck__cartes {
  display: grid;
  grid-template-columns: repeat(2, var(--csp-kanban-column-width));
  align-items: start;
  gap: var(--csp-space-6);
  padding: var(--csp-space-6);
  background-color: var(--background-alt-grey);
}

.deck__panneau {
  width: 20rem;
  padding: var(--csp-space-6);
  background-color: var(--background-overlap-grey);
}

.deck__note {
  --csp-card-border: transparent;

  width: 44rem;
}

.deck__note-auteur {
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.deck__note-separateur,
.deck__note-horodatage {
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
}

.deck__note-etiquettes {
  margin-bottom: var(--csp-space-3);
}

.deck__voisins {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--csp-space-6);
}

.deck__palette {
  display: grid;
  grid-template-columns: repeat(5, auto);
  justify-items: start;
  gap: var(--csp-space-5) var(--csp-space-6);
}

.deck__contrastes {
  display: grid;
  grid-template-columns: repeat(5, auto);
  gap: var(--csp-space-6) var(--csp-space-8);
}

.deck__contraste {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-2);
}

.deck__valeur {
  font-size: var(--csp-font-size-base);
  font-variant-numeric: tabular-nums;
  color: var(--text-default-grey);
}

.deck__ecarts {
  display: grid;
  gap: var(--csp-space-4);
}

.deck__ecart {
  display: grid;
  grid-template-columns: 8rem 8rem auto;
  align-items: center;
  justify-items: start;
  gap: var(--csp-space-4);
}

.deck__mesure-cachee {
  position: absolute;
  visibility: hidden;
}

.deck__cellule {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  padding: var(--csp-space-5);
}

.deck__cellule--blanc {
  background-color: var(--background-default-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
}

.deck__cellule--colonne,
.deck__cellule--note {
  background-color: var(--background-alt-grey);
}

.deck__cellule--colonne {
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
}

.deck__cellule--panneau {
  background-color: var(--background-overlap-grey);
  box-shadow: inset 1px 0 0 var(--border-default-grey);
}

.deck .deck__cellule :deep(.csp-label.csp-label) {
  --csp-label-border-color: transparent;
}

/* the rule of the « libre » scenario */
.deck .deck__cellule--filet :deep(.csp-label.csp-label) {
  --csp-label-border-color: color-mix(in oklab, var(--csp-label-dot) 26%, transparent);
}

/* Labels drawn as DSFR tags, with the tag colors of the DSFR family that the « dsfr » scenario gives each key */
.deck--tag {
  --csp-palette-grey-background: var(--background-contrast-grey);
  --csp-palette-grey-text: var(--text-label-grey);
  --csp-palette-blue-background: var(--background-action-low-blue-cumulus);
  --csp-palette-blue-text: var(--text-action-high-blue-cumulus);
  --csp-palette-teal-background: var(--background-action-low-green-archipel);
  --csp-palette-teal-text: var(--text-action-high-green-archipel);
  --csp-palette-green-background: var(--background-action-low-green-emeraude);
  --csp-palette-green-text: var(--text-action-high-green-emeraude);
  --csp-palette-yellow-background: var(--background-action-low-green-tilleul-verveine);
  --csp-palette-yellow-text: var(--text-action-high-green-tilleul-verveine);
  --csp-palette-orange-background: var(--background-action-low-orange-terre-battue);
  --csp-palette-orange-text: var(--text-action-high-orange-terre-battue);
  --csp-palette-red-background: var(--background-action-low-pink-tuile);
  --csp-palette-red-text: var(--text-action-high-pink-tuile);
  --csp-palette-pink-background: var(--background-action-low-pink-macaron);
  --csp-palette-pink-text: var(--text-action-high-pink-macaron);
  --csp-palette-purple-background: var(--background-action-low-purple-glycine);
  --csp-palette-purple-text: var(--text-action-high-purple-glycine);
  --csp-palette-brown-background: var(--background-action-low-brown-opera);
  --csp-palette-brown-text: var(--text-action-high-brown-opera);
}

.deck--tag :deep(.csp-label.csp-label--sm),
.deck--tag :deep(.csp-label-list__more.csp-label-list__more) {
  gap: 0.125rem;
  min-height: 1.5rem;
  padding: 0.125rem 0.5rem;
  border-radius: 0.75rem;
  font-size: 0.75rem;
  font-weight: var(--csp-font-weight-regular);
  line-height: 1.25rem;
}

.deck--tag :deep(.csp-label.csp-label--md),
.deck--tag :deep(.csp-label-list__more.csp-label-list__more--md) {
  gap: 0.25rem;
  min-height: 2rem;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: var(--csp-font-weight-regular);
  line-height: 1.5rem;
}

.deck--tag :deep(.csp-label .csp-label__remove) {
  margin-block: 0;
  padding: 0;
}

.deck--tag :deep(.csp-label .csp-label__dot) {
  display: none;
}
</style>
