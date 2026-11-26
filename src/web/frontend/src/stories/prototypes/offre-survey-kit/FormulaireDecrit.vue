<script setup lang="ts">
import type { Description, Reponses, Valeur } from './moteur'
import { computed, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { avancementEtape } from '../offre-sans-autorisation/variants/mvp/aide'
import TexteEtoile from '../offre-sans-autorisation/variants/mvp/TexteEtoile.vue'
import ChampDecrit from './ChampDecrit.vue'
import { choixProposes, etapesDe, obligatoiresEtape, placement, repondre, visible } from './moteur'

// Formulaire en étapes produit par la description : même présentation que le formulaire de création actuel
// (ParcoursOffre du MVP) — étapes regroupées en deux parties à gauche, une étape par écran, avancement par étape.
// Les pages d'une étape s'affichent l'une sous l'autre sur le même écran (un bloc, avec son titre s'il y en a un).
const props = defineProps<{ description: Description }>()
const reponses = defineModel<Reponses>('reponses', { required: true })
const etape = defineModel<number>('etape', { default: 1 })

const etapes = computed(() => etapesDe(props.description))
watch(etapes, (l) => {
  if (etape.value > l.length) {
    etape.value = Math.max(1, l.length)
  }
})
const courante = computed(() => etapes.value[etape.value - 1])
const suivante = computed(() => etapes.value[etape.value])
const derniere = computed(() => etape.value >= etapes.value.length)
const changeDePartie = computed(() => suivante.value && courante.value && suivante.value.partie.id !== courante.value.partie.id)

function etat(i: number) {
  const c = obligatoiresEtape(props.description, etapes.value[i]!, reponses.value)
  return { total: c.length, reste: c.filter(x => !x.ok).length }
}
const parties = computed(() => props.description.questionnaire.parties.map((p, pi) => ({
  ...p,
  n: pi + 1,
  etapes: etapes.value.map((e, i) => ({ ...e, n: i + 1, ...etat(i) })).filter(e => e.partie.id === p.id),
})))
const reste = computed(() => etapes.value.reduce((s, _, i) => s + etat(i).reste, 0))

const LARGEURS = { pleine: 6, demi: 3, tiers: 2 } as const
function pages() {
  return (courante.value?.pages ?? []).map(p => ({
    ...p,
    questions: p.questions.map(placement)
      .filter(q => props.description.reponses[q.id] && visible(props.description, q.id, reponses.value))
      .map(q => ({ ...q, reponse: props.description.reponses[q.id]!, span: LARGEURS[q.largeur ?? 'pleine'] ?? 6 })),
  })).filter(p => p.questions.length)
}

function maj(id: string, v: Valeur) {
  repondre(props.description, reponses.value, id, v)
}

function aller(n: number) {
  etape.value = n
  document.querySelectorAll('.ats__main, .csp-page-container').forEach(e => e.scrollTo({ top: 0 }))
}
defineExpose({ reste })
</script>

<template>
  <div class="cadre">
    <div class="parcours">
      <nav
        class="etapes"
        aria-label="Étapes du formulaire"
      >
        <div
          v-for="p in parties"
          :key="p.id"
          class="partie"
          :class="{ 'partie--active': p.id === courante?.partie.id }"
        >
          <p class="partie__titre">
            <span class="partie__num">Partie {{ p.n }}</span>
            {{ p.titre }}
          </p>
          <ol>
            <li
              v-for="e in p.etapes"
              :key="e.id"
            >
              <button
                type="button"
                class="etape"
                :class="{ 'etape--active': etape === e.n }"
                :aria-current="etape === e.n ? 'step' : undefined"
                @click="aller(e.n)"
              >
                <span class="etape__num">{{ e.n }}</span>
                <span class="etape__corps">
                  <span class="etape__titre">{{ e.titre }}</span>
                  <span
                    class="etape__reste"
                    :class="{ 'etape__reste--ok': e.total && !e.reste }"
                  >
                    <CspIcon
                      v-if="e.total && !e.reste"
                      name="ri:checkbox-circle-fill"
                      :size="14"
                    />
                    <TexteEtoile :texte="avancementEtape(e.total, e.reste)" />
                  </span>
                </span>
              </button>
            </li>
          </ol>
        </div>
      </nav>

      <div
        v-if="courante"
        class="principal"
      >
        <div class="tete">
          <h2 class="tete__titre">
            {{ courante.titre }}
          </h2>
          <p class="tete__aide">
            Étape {{ etape }} sur {{ etapes.length }}<template v-if="courante.aide">
              · {{ courante.aide }}
            </template>
          </p>
        </div>

        <div class="corps">
          <section
            v-for="pg in pages()"
            :key="pg.id"
            class="page"
          >
            <h3
              v-if="pg.titre"
              class="page__titre"
            >
              {{ pg.titre }}
            </h3>
            <p
              v-if="pg.description"
              class="page__desc"
            >
              {{ pg.description }}
            </p>
            <div class="grille">
              <div
                v-for="q in pg.questions"
                :key="q.id"
                class="grille__case"
                :style="{ '--span': q.span }"
              >
                <ChampDecrit
                  :id="q.id"
                  :reponse="q.reponse"
                  :valeur="reponses[q.id]"
                  :choix="choixProposes(q.reponse, reponses)"
                  @repondre="(v: Valeur) => maj(q.id, v)"
                />
              </div>
            </div>
          </section>
        </div>

        <p
          v-if="changeDePartie"
          class="transition"
        >
          <CspIcon
            name="ri:information-line"
            :size="16"
          />
          {{ courante.partie.titre }} : terminé. Partie suivante : {{ suivante!.partie.titre.toLowerCase() }}.
        </p>

        <div class="nav">
          <CspButton
            v-if="etape > 1"
            label="Précédent"
            variant="secondary"
            icon="ri:arrow-left-line"
            is-icon-left
            @click="aller(etape - 1)"
          />
          <span class="nav__espace" />
          <CspButton
            v-if="!derniere"
            :label="`Suivant : ${suivante!.titre}`"
            icon="ri:arrow-right-line"
            @click="aller(etape + 1)"
          />
          <slot
            v-else
            name="fin"
            :reste="reste"
          />
        </div>
        <p
          v-if="derniere"
          class="etat"
          :class="{ 'etat--ok': !reste }"
        >
          <TexteEtoile
            :texte="reste
              ? `Encore ${reste} champ${reste > 1 ? 's' : ''} obligatoire${reste > 1 ? 's' : ''} (*) à remplir.`
              : 'Tous les champs obligatoires sont remplis.'"
          />
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
// Le formulaire s'adapte à la place dont il dispose (container query) : dans l'éditeur, il est plus étroit
// que la page, les étapes passent alors au-dessus.
.cadre {
  container-type: inline-size;
}

.parcours {
  display: grid;
  grid-template-columns: 17rem minmax(0, 1fr);
  gap: var(--csp-space-8);
  align-items: start;
  max-width: 80rem;

  @container (width <= 56rem) {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--csp-space-5);
  }
}

.etapes {
  position: sticky;
  top: var(--csp-space-4);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);

  @container (width <= 56rem) {
    position: static;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: var(--csp-space-6);
  }
}

.partie {
  ol {
    display: flex;
    flex-direction: column;
    gap: 2px;
    margin: var(--csp-space-2) 0 0;
    padding: 0 0 0 var(--csp-space-3);
    border-left: 2px solid var(--border-default-grey);
    list-style: none;
  }

  &--active ol {
    border-left-color: var(--border-plain-blue-france);
  }
}

.partie__titre {
  margin: 0;
  font-weight: 700;
  font-size: var(--csp-font-size-sm);
  line-height: 1.3;
  color: var(--text-title-grey);
}

.partie__num {
  display: block;
  font-weight: 400;
  font-size: var(--csp-font-size-xs);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-mention-grey);
}

.etape {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  width: 100%;
  padding: var(--csp-space-2);
  border: 0;
  background: none;
  font: inherit;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
  text-align: left;
  cursor: pointer;

  &:hover {
    background: var(--background-default-grey-hover);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.etape--active {
  background: var(--background-alt-blue-france);
  font-weight: 700;
  color: var(--text-action-high-blue-france);
}

.etape__num {
  display: inline-grid;
  flex-shrink: 0;
  place-items: center;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: var(--background-contrast-grey);
  font-size: var(--csp-font-size-xs);
  font-weight: 700;
}

.etape--active .etape__num {
  background: var(--background-action-high-blue-france);
  color: var(--text-inverted-blue-france);
}

.etape__corps {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
}

.etape__reste {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-weight: 400;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);

  &--ok {
    color: var(--text-default-success);
  }
}

.principal {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  min-width: 0;
}

.tete__titre {
  margin: 0;
  font-size: 1.5rem;
  line-height: 1.3;
}

.tete__aide {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.corps {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-8);
  padding: var(--csp-space-6) var(--csp-space-8);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);

  @container (width <= 40rem) {
    padding: var(--csp-space-5);
  }
}

.page {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.page__titre {
  margin: 0;
  font-size: 1.125rem;
  line-height: 1.4;
}

.page__desc {
  margin: calc(-1 * var(--csp-space-2)) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

// Grille de 6 colonnes : pleine largeur (6), moitié (3) ou tiers (2), comme les FieldRow du MVP.
.grille {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: var(--csp-space-5);
}

.grille__case {
  grid-column: span var(--span, 6);

  @container (width <= 40rem) {
    grid-column: span 6;
  }
}

.transition {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.nav {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-3);
}

.nav__espace {
  flex: 1;
}

.etat {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);

  &--ok {
    color: var(--text-default-success);
  }
}
</style>
