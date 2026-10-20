<script setup lang="ts">
import type { Demo, Etape, Geste } from './boucle'
import type { KanbanPoint } from '@/composables/dnd/useKanbanDnd'
import type { Candidature } from '@/features/candidatures/types'
import { useQueryCache } from '@pinia/colada'
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import { markKanbanCardMoved } from '@/composables/dnd/useKanbanDnd'
import { DEMO_MOTIFS_REFUS, demoKanban } from '@/features/candidatures/__mocks__/demo'
import CandidatureKanbanCard from '@/features/candidatures/components/CandidatureKanbanCard.vue'
import RefusCandidatureDialog from '@/features/candidatures/components/RefusCandidatureDialog.vue'
import { useEtapeChangeMutation } from '@/features/candidatures/composables/useEtapeChangeMutation'
import { candidatureDetailQuery, candidatureNotesQuery } from '@/features/candidatures/queries'
import { boucle, GLISSER, instant, MESSAGE_ORIGINE, MESSAGE_PRET } from './boucle'

const props = withDefaults(defineProps<{
  demo?: Demo
  // Factor that slows the animations of the application down
  ralenti?: number
}>(), {
  demo: 'parcours',
  ralenti: 1,
})

const PARAMS = { organismeUuid: DEMO_ORGANISME.uuid, recrutementUuid: DEMO_RECRUTEMENT_UUID }
const RECRUTEMENT_PATH = `/organismes/${PARAMS.organismeUuid}/recrutements/${PARAMS.recrutementUuid}`
const BOARD_ID = `kanban-${PARAMS.recrutementUuid}`

const ETAPES = demoKanban().etapes
// Third card of the first column, that the panel opens
const OUVERTE = ETAPES[0]!.candidatures[2]!
// Second card of the third column, that goes between the third and the fourth columns
const DEPOSEE = ETAPES[2]!.candidatures[1]!
const COLONNES_DU_DEPOT = [2, 3]

const router = useRouter()
const queryCache = useQueryCache()
const { changeEtape } = useEtapeChangeMutation(PARAMS)

const loop = computed(() => boucle(props.demo, props.ralenti))

// The pointer stays where it was while hidden, and moves from there to its next target
const curseur = ref<KanbanPoint>({ x: -40, y: -40 })
const curseurVisible = ref(false)
const curseurGlisse = ref(false)
const dialogueOuvert = ref(false)
const fantome = ref<{ left: number, top: number, width: number, dx: number, dy: number, colonne: string } | null>(null)
const fantomeRef = ref<HTMLElement | null>(null)

function element<T extends Element = HTMLElement>(selector: string): T | null {
  return document.querySelector<T>(selector)
}

function carte(candidature: Candidature): HTMLElement | null {
  return element(`.candidature-kanban-card a[href*="${candidature.uuid}"]`)?.closest<HTMLElement>('.candidature-kanban-card') ?? null
}

function viser(cible: Element | null, decalage: KanbanPoint = { x: 0.5, y: 0.5 }): void {
  if (!cible) {
    return
  }
  const { left, top, width, height } = cible.getBoundingClientRect()
  curseur.value = { x: left + width * decalage.x, y: top + height * decalage.y }
  curseurVisible.value = true
}

function cliquer(cible: HTMLElement | null | undefined): void {
  cible?.click()
}

function pointerdown(cible: Element | null): void {
  cible?.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, cancelable: true, button: 0, pointerType: 'mouse' }))
}

const DECLENCHEUR_MENU = 'button[aria-label="Actions sur l’offre"]'
const HORS_DU_MENU = '.csp-page-header h1'
const FERMER_PANNEAU = 'button[aria-label="Fermer la candidature"]'

function colonnes(): HTMLElement[] {
  return [...document.querySelectorAll<HTMLElement>('.candidature-kanban-column')]
}

function colonneCible(): number {
  const source = carte(DEPOSEE)
  const actuelle = colonnes().findIndex(colonne => source && colonne.contains(source))
  return actuelle === COLONNES_DU_DEPOT[0] ? COLONNES_DU_DEPOT[1]! : COLONNES_DU_DEPOT[0]!
}

// The pointer picks the card up by its title, as the browser shows the drag preview under it
const PRISE = { x: 48, y: 24 }

function saisir(): void {
  const source = carte(DEPOSEE)
  const cible = colonnes()[colonneCible()]?.querySelector('.candidature-kanban-column__cards')
  if (!source || !cible) {
    return
  }
  const depart = source.getBoundingClientRect()
  const derniere = cible.lastElementChild?.getBoundingClientRect()
  const arriveeTop = derniere ? derniere.bottom + 56 : cible.getBoundingClientRect().top + 40
  source.setAttribute('data-mouvement-saisie', '')
  fantome.value = {
    left: depart.left,
    top: depart.top,
    width: depart.width,
    dx: 0,
    dy: 0,
    colonne: ETAPES[colonneCible()]!.uuid,
  }
  curseurGlisse.value = true
  // The preview leaves the card a bit off its place in the other column, as a hand does
  const dx = cible.getBoundingClientRect().left + 40 - depart.left
  const dy = arriveeTop - depart.top
  requestAnimationFrame(() => requestAnimationFrame(() => {
    if (fantome.value) {
      fantome.value = { ...fantome.value, dx, dy }
      curseur.value = { x: depart.left + dx + PRISE.x, y: depart.top + dy + PRISE.y }
    }
  }))
}

function deposer(): void {
  const lache = fantomeRef.value?.getBoundingClientRect()
  const colonne = fantome.value?.colonne
  fantome.value = null
  curseurGlisse.value = false
  carte(DEPOSEE)?.removeAttribute('data-mouvement-saisie')
  if (!lache || !colonne) {
    return
  }
  markKanbanCardMoved(BOARD_ID, DEPOSEE.uuid, { x: lache.left, y: lache.top })
  void changeEtape({ etapeCibleUuid: colonne, candidatureUuids: [DEPOSEE.uuid] })
}

const ACTIONS: Record<Geste, Partial<Record<Etape['action'], (etape: Etape, index: number) => void>>> = {
  menu: {
    viser: (_, index) => viser(element(index === 0 ? DECLENCHEUR_MENU : HORS_DU_MENU), index === 0 ? undefined : { x: 0.3, y: 0.5 }),
    ouvrir: () => cliquer(element(DECLENCHEUR_MENU)),
    fermer: () => pointerdown(element(HORS_DU_MENU)),
  },
  panneau: {
    viser: (_, index) => viser(index === 0 ? carte(OUVERTE)?.querySelector('a') ?? null : element(FERMER_PANNEAU), index === 0 ? { x: 0.3, y: 0.5 } : undefined),
    ouvrir: () => void router.push(`${RECRUTEMENT_PATH}/candidatures/${OUVERTE.uuid}/notes`),
    fermer: () => cliquer(element(FERMER_PANNEAU)),
  },
  depot: {
    viser: () => {
      const depart = carte(DEPOSEE)?.getBoundingClientRect()
      if (depart) {
        curseur.value = { x: depart.left + PRISE.x, y: depart.top + PRISE.y }
        curseurVisible.value = true
      }
    },
    saisir,
    deposer,
  },
  dialogue: {
    viser: () => viser([...document.querySelectorAll('.csp-dialog button')].find(button => button.textContent?.trim() === 'Annuler') ?? null),
    ouvrir: () => {
      dialogueOuvert.value = true
    },
    fermer: () => cliquer([...document.querySelectorAll<HTMLElement>('.csp-dialog button')].find(button => button.textContent?.trim() === 'Annuler')),
  },
}

function jouer(etape: Etape): void {
  const etapesDuGeste = loop.value.etapes.filter(({ geste, action }) => geste === etape.geste && action === etape.action)
  ACTIONS[etape.geste][etape.action]?.(etape, etapesDuGeste.indexOf(etape))
}

// A gesture plays from its start only, so that a frame opened in the middle of a loop waits for the next one
const armes = new Set<Geste>()
let precedent = -1
let frame = 0

// A screen framed by a plate waits for the origin that the plate gives all its screens; a screen alone starts its loop
// as soon as the kanban shows its cards
const dansUnePlanche = window.frameElement?.classList.contains('mouvement-cadre__ecran') ?? false
const origine = ref<number | null>(null)
let pret = false

function signalerPret(): void {
  pret = true
  if (dansUnePlanche) {
    window.parent.postMessage({ type: MESSAGE_PRET }, window.location.origin)
  }
  else {
    origine.value = Date.now()
  }
}

function recevoir(event: MessageEvent): void {
  if (event.source === window.parent && event.data?.type === MESSAGE_ORIGINE) {
    origine.value = event.data.origine
  }
}

function franchi(at: number, t: number): boolean {
  return precedent <= t ? at > precedent && at <= t : at > precedent || at <= t
}

function ralentir(): void {
  if (props.ralenti === 1) {
    return
  }
  for (const animation of document.getAnimations()) {
    const cible = (animation.effect as KeyframeEffect | null)?.target
    if (!cible?.closest('.mouvement-scene__dessus') && animation.playbackRate !== 1 / props.ralenti) {
      animation.playbackRate = 1 / props.ralenti
    }
  }
}

function tick(): void {
  frame = requestAnimationFrame(tick)
  if (!pret && carte(OUVERTE)) {
    signalerPret()
  }
  if (origine.value === null || Date.now() < origine.value) {
    return
  }
  const t = instant(loop.value, origine.value)
  // The first frame plays the loop from its start when it comes at the start, and waits for the next start otherwise
  if (precedent < 0) {
    precedent = t < 100 ? loop.value.duree - 1 : t
  }
  const saut = precedent <= t ? t - precedent : t + loop.value.duree - precedent
  // A hidden page stops its frames: the gestures wait for their next start
  if (saut > 500) {
    armes.clear()
  }
  else {
    for (const { at, geste } of loop.value.debuts) {
      if (franchi(at, t)) {
        armes.add(geste)
        curseurVisible.value = false
      }
    }
    for (const etape of loop.value.etapes) {
      if (armes.has(etape.geste) && franchi(etape.at, t)) {
        jouer(etape)
      }
    }
  }
  precedent = t
  ralentir()
}

// The demo moves the focus by script, which the browser shows as a keyboard focus; a mouse user sees no ring
function sansAnneau(event: FocusEvent): void {
  const cible = event.target as HTMLElement
  if (cible.matches(':focus-visible')) {
    cible.blur()
    cible.focus({ focusVisible: false } as FocusOptions)
  }
}

onMounted(() => {
  window.addEventListener('message', recevoir)
  document.addEventListener('focusin', sansAnneau)
  void nextTick(() => {
    const candidature = { ...PARAMS, candidatureUuid: OUVERTE.uuid }
    void queryCache.fetch(queryCache.ensure(candidatureDetailQuery(candidature)))
    void queryCache.fetch(queryCache.ensure(candidatureNotesQuery(candidature)))
  })
  frame = requestAnimationFrame(tick)
})

onBeforeUnmount(() => {
  cancelAnimationFrame(frame)
  window.removeEventListener('message', recevoir)
  document.removeEventListener('focusin', sansAnneau)
})
</script>

<template>
  <App />

  <RefusCandidatureDialog
    :open="dialogueOuvert"
    :candidats="[OUVERTE.candidat]"
    :motifs="DEMO_MOTIFS_REFUS"
    @cancel="dialogueOuvert = false"
    @confirm="dialogueOuvert = false"
  />

  <div
    class="mouvement-scene__dessus"
    aria-hidden="true"
  >
    <div
      v-if="fantome"
      ref="fantomeRef"
      class="mouvement-scene__fantome"
      :style="{
        left: `${fantome.left}px`,
        top: `${fantome.top}px`,
        width: `${fantome.width}px`,
        transform: `translate(${fantome.dx}px, ${fantome.dy}px)`,
        transitionDuration: `${GLISSER}ms`,
      }"
    >
      <CandidatureKanbanCard
        :candidature="DEPOSEE"
        board-id="fantome"
        :column-id="fantome.colonne"
        :card-index="0"
      />
    </div>
    <svg
      class="mouvement-scene__curseur"
      :class="{ 'mouvement-scene__curseur--visible': curseurVisible }"
      :style="{
        transform: `translate(${curseur.x}px, ${curseur.y}px)`,
        transitionDuration: curseurGlisse ? `${GLISSER}ms` : undefined,
      }"
      width="20"
      height="24"
      viewBox="0 0 20 24"
    >
      <path
        d="M2 2 L2 19 L6.5 15 L9.5 22 L12.5 20.8 L9.6 14 L16 14 Z"
        fill="#161616"
        stroke="#fff"
        stroke-width="1.5"
        stroke-linejoin="round"
      />
    </svg>
  </div>
</template>

<style lang="scss">
.candidature-kanban-card[data-mouvement-saisie] {
  opacity: var(--csp-raised-opacity-drag);
}

.mouvement-scene__dessus {
  position: fixed;
  inset: 0;
  z-index: 2000;
  pointer-events: none;
}

/* The drag preview of the browser, carried by the pointer */
.mouvement-scene__fantome {
  position: fixed;
  opacity: 0.8;
  transition-property: transform;
  transition-timing-function: ease-in-out;
}

.mouvement-scene__curseur {
  position: fixed;
  top: 0;
  left: 0;
  opacity: 0;
  transition: transform 350ms ease-in-out;
}

.mouvement-scene__curseur--visible {
  opacity: 1;
}
</style>
