<script setup lang="ts">
import type { Description, Reponses, TypeReponse } from './moteur'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import FormulaireDecrit from './FormulaireDecrit.vue'
import { etapesDe, lireDescription, nombreConditions, reponsesInitiales, reponsesVisibles } from './moteur'
import origine from './offre.formulaire.json'

// Éditeur à la façon de la page « Écrire un questionnaire » de survey-kit : la description à gauche (modifiable),
// le formulaire produit à droite, les réponses en JSON dessous. On modifie la description, le formulaire suit.
// Si le texte n'est plus valable, le formulaire garde la dernière version valable et la liste des problèmes s'affiche.
const TEXTE_ORIGINE = JSON.stringify(origine, null, 2)

const texte = ref(TEXTE_ORIGINE)
const description = ref<Description>(lireDescription(TEXTE_ORIGINE).description!)
const erreurs = ref<string[]>([])
const reponses = ref<Reponses>(reponsesInitiales(description.value))
const etape = ref(1)

let minuterie: ReturnType<typeof setTimeout> | undefined
watch(texte, (t) => {
  clearTimeout(minuterie)
  minuterie = setTimeout(() => {
    const lu = lireDescription(t)
    erreurs.value = lu.erreurs
    if (lu.description) {
      const types: Record<string, TypeReponse> = Object.fromEntries(Object.entries(description.value.reponses).map(([k, r]) => [k, r.type]))
      description.value = lu.description
      reponses.value = reponsesInitiales(lu.description, reponses.value, types)
    }
  }, 300)
})

const stats = computed(() => {
  const d = description.value
  return `${Object.keys(d.reponses).length} réponses · ${d.questionnaire.parties.length} parties · ${etapesDe(d).length} étapes · ${nombreConditions(d)} conditions ou dépendances`
})
const sortie = computed(() => JSON.stringify(reponsesVisibles(description.value, reponses.value), null, 2))

function retablir() {
  texte.value = TEXTE_ORIGINE
}
function viderReponses() {
  reponses.value = reponsesInitiales(description.value)
}
</script>

<template>
  <div class="editeur">
    <header class="editeur__tete">
      <div>
        <h1 class="editeur__titre">
          Formulaire décrit en données — éditeur
        </h1>
        <p class="editeur__sous-titre">
          Variante « survey-kit » sans dépendance : la description ci-dessous produit le formulaire de création d'offre.
          Listes de choix fictives (extraits du proto MVP).
        </p>
      </div>
      <div class="editeur__actions">
        <CspButton
          label="Rétablir la description d'origine"
          variant="secondary"
          size="sm"
          icon="ri:restart-line"
          is-icon-left
          :disabled="texte === TEXTE_ORIGINE"
          @click="retablir"
        />
        <CspButton
          label="Vider les réponses"
          variant="tertiary"
          size="sm"
          icon="ri:delete-bin-line"
          is-icon-left
          @click="viderReponses"
        />
      </div>
    </header>

    <div class="editeur__colonnes">
      <section
        class="panneau panneau--source"
        aria-labelledby="titre-description"
      >
        <div class="panneau__tete">
          <h2
            id="titre-description"
            class="panneau__titre"
          >
            Description (JSON)
          </h2>
          <span class="panneau__info">{{ stats }}</span>
        </div>
        <CspCallout
          v-if="erreurs.length"
          variant="error"
          title="La description a un problème : le formulaire garde la dernière version valable."
        >
          <ul class="erreurs">
            <li
              v-for="e in erreurs.slice(0, 6)"
              :key="e"
            >
              {{ e }}
            </li>
          </ul>
        </CspCallout>
        <textarea
          v-model="texte"
          class="source"
          spellcheck="false"
          aria-labelledby="titre-description"
        />
      </section>

      <section
        class="panneau"
        aria-labelledby="titre-formulaire"
      >
        <div class="panneau__tete">
          <h2
            id="titre-formulaire"
            class="panneau__titre"
          >
            Formulaire produit
          </h2>
        </div>
        <FormulaireDecrit
          v-model:reponses="reponses"
          v-model:etape="etape"
          :description="description"
        />
      </section>
    </div>

    <section
      class="panneau"
      aria-labelledby="titre-reponses"
    >
      <div class="panneau__tete">
        <h2
          id="titre-reponses"
          class="panneau__titre"
        >
          Réponses (JSON)
        </h2>
        <span class="panneau__info">Seules les questions affichées ont une réponse.</span>
      </div>
      <pre class="sortie">{{ sortie }}</pre>
    </section>
  </div>
</template>

<style scoped lang="scss">
.editeur {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
  min-height: 100vh;
  padding: var(--csp-space-6);
  background: var(--background-alt-grey);

  @media (width <= 40rem) {
    padding: var(--csp-space-4);
  }
}

.editeur__tete {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--csp-space-4);
}

.editeur__titre {
  margin: 0;
  font-size: 1.5rem;
  line-height: 1.3;
}

.editeur__sous-titre {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.editeur__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
}

.editeur__colonnes {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(0, 3fr);
  gap: var(--csp-space-6);
  align-items: start;

  @media (width <= 64rem) {
    grid-template-columns: minmax(0, 1fr);
  }
}

.panneau {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  min-width: 0;
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.panneau--source {
  position: sticky;
  top: var(--csp-space-4);

  @media (width <= 64rem) {
    position: static;
  }
}

.panneau__tete {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: var(--csp-space-2);
}

.panneau__titre {
  margin: 0;
  font-size: 1rem;
}

.panneau__info {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.source,
.sortie {
  margin: 0;
  padding: var(--csp-space-3);
  border: 1px solid var(--border-default-grey);
  background: var(--background-alt-grey);
  font-family: ui-monospace, 'SFMono-Regular', Menlo, monospace;
  font-size: 0.75rem;
  line-height: 1.5;
  color: var(--text-default-grey);
}

.source {
  width: 100%;
  height: calc(100vh - 14rem);
  min-height: 24rem;
  resize: vertical;
  tab-size: 2;

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.sortie {
  max-height: 28rem;
  overflow: auto;
  white-space: pre-wrap;
}

.erreurs {
  margin: 0;
  padding-left: var(--csp-space-5);
  font-size: var(--csp-font-size-sm);
}
</style>
