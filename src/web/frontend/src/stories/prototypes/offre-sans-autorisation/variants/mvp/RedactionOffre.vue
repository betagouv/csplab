<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import ApercuCandidat from './ApercuCandidat.vue'
import FormAnnonce from './FormAnnonce.vue'
import FormCandidature from './FormCandidature.vue'
import FormEquipe from './FormEquipe.vue'
import FormInterne from './FormInterne.vue'
import FormProcessus from './FormProcessus.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { db, heure, sauvegarder, UTILISATEUR } from './store'

// Créer une offre : un parcours en 5 étapes. Rien n'est exigé pour enregistrer un brouillon ; Processus et Équipe
// sont facultatifs et ne bloquent pas la publication. « Publier » ouvre le parcours de publication (date de fin).
const props = defineProps<{ id: string, etape?: number }>()
const { aller, notifier } = useNav()
const o = computed(() => db.offres.find(x => x.id === props.id)!)

const ETAPES = [
  { titre: 'Annonce', aide: 'Ce que liront les candidats sur Choisir le Service Public, avec les mentions obligatoires de l\'article D311-8.' },
  { titre: 'Informations internes', aide: 'Ce qui sert à l\'organisme et n\'est jamais publié.' },
  { titre: 'Formulaire de candidature', aide: 'Ce que vous demandez aux candidats quand ils postulent. Les candidatures arrivent dans l\'ATS.' },
  { titre: 'Processus', facultatif: true, aide: 'Facultatif. Sans adaptation, c\'est le processus de recrutement de l\'organisme qui s\'applique.' },
  { titre: 'Équipe', facultatif: true, aide: 'Facultatif. Vous êtes Responsable de l\'offre ; ajoutez d\'autres membres si besoin.' },
]
// L'étape peut aussi venir de l'adresse (?etape=3) : utile pour montrer ou capturer une étape précise.
const etapeUrl = Number(new URLSearchParams(window.location.search).get('etape')) || undefined
const etape = ref(Math.min(Math.max(props.etape ?? etapeUrl ?? 1, 1), ETAPES.length))
const courante = computed(() => ETAPES[etape.value - 1]!)
const derniere = computed(() => etape.value === ETAPES.length)

// Enregistrement automatique.
const enregistre = ref(heure())
// Aperçu candidat (œil) : l'annonce telle que la verront les candidats, à côté du formulaire.
const apercu = ref(false)
watch(o, () => {
  sauvegarder()
  enregistre.value = heure()
}, { deep: true })

function allerEtape(n: number) {
  etape.value = n
  document.querySelector('.csp-page-container')?.scrollTo({ top: 0 })
}
const peutPublier = computed(() => db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier)
function enregistrer() {
  notifier('Brouillon enregistré. Vous pouvez le reprendre à tout moment.')
  aller({ nom: 'offre', id: o.value.id })
}
</script>

<template>
  <PageAts
    actif="offres"
    :titre="o.titre || 'Nouvelle offre'"
    sous-titre="Nouvelle offre d'emploi · brouillon"
    :fil="[{ label: 'Mes offres d\'emploi', to: '/offres' }, { label: 'Nouvelle offre' }]"
  >
    <template #actions>
      <span class="enregistre">Enregistré automatiquement à {{ enregistre }}</span>
      <CspButton
        label="Aperçu candidat"
        size="sm"
        variant="secondary"
        icon="ri:eye-line"
        is-icon-left
        @click="apercu = true"
      />
      <CspButton
        label="Enregistrer et quitter"
        size="sm"
        variant="secondary"
        @click="enregistrer"
      />
    </template>

    <div class="redaction">
      <!-- Indicateur d'étapes (modèle DSFR) -->
      <div class="stepper">
        <h2 class="stepper__titre">
          {{ courante.titre }}
          <span class="stepper__etat">Étape {{ etape }} sur {{ ETAPES.length }}</span>
        </h2>
        <div
          class="stepper__barre"
          aria-hidden="true"
        >
          <span
            v-for="n in ETAPES.length"
            :key="n"
            :class="{ faite: n <= etape }"
          />
        </div>
        <p
          v-if="!derniere"
          class="stepper__suivante"
        >
          <strong>Étape suivante :</strong> {{ ETAPES[etape]!.titre }}{{ ETAPES[etape]!.facultatif ? ' (facultative)' : '' }}
        </p>
      </div>

      <p class="aide">
        {{ courante.aide }}
      </p>

      <div class="corps">
        <FormAnnonce
          v-if="etape === 1"
          :offre="o"
        />
        <FormInterne
          v-else-if="etape === 2"
          :offre="o"
        />
        <FormCandidature
          v-else-if="etape === 3"
          :offre="o"
        />
        <FormProcessus
          v-else-if="etape === 4"
          :offre="o"
        />
        <FormEquipe
          v-else
          :offre="o"
        />
      </div>

      <div class="nav">
        <CspButton
          v-if="etape > 1"
          label="Précédent"
          variant="secondary"
          icon="ri:arrow-left-line"
          is-icon-left
          @click="allerEtape(etape - 1)"
        />
        <span class="nav__espace" />
        <CspButton
          v-if="courante.facultatif && !derniere"
          label="Passer cette étape"
          variant="tertiary-no-outline"
          @click="allerEtape(etape + 1)"
        />
        <CspButton
          v-if="!derniere"
          label="Suivant"
          icon="ri:arrow-right-line"
          @click="allerEtape(etape + 1)"
        />
        <template v-else>
          <CspButton
            label="Enregistrer le brouillon"
            variant="secondary"
            @click="enregistrer"
          />
          <CspButton
            v-if="peutPublier"
            label="Publier"
            icon="ri:arrow-right-line"
            @click="aller({ nom: 'publier', id: o.id })"
          />
        </template>
      </div>
      <p
        v-if="derniere && !peutPublier"
        class="sans-droit"
      >
        Vous n'avez pas le droit « Publier » : un agent qui l'a mettra l'offre en ligne.
      </p>
    </div>

    <CspDrawer
      :open="apercu"
      title="Aperçu candidat"
      description="Mise en page indicative ; elle suit votre saisie."
      size="lg"
      :modal="false"
      :overlay="false"
      @update:open="(v: boolean) => (apercu = v)"
    >
      <ApercuCandidat
        :offre="o"
        :organisme="db.organisme.nom"
      />
    </CspDrawer>
  </PageAts>
</template>

<style scoped lang="scss">
.redaction {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
  max-width: 52rem;
}

.enregistre {
  align-self: center;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.stepper__titre {
  display: flex;
  flex-direction: column-reverse;
  gap: var(--csp-space-1);
  margin: 0 0 var(--csp-space-3);
  font-size: 1.375rem;
  line-height: 1.3;
}

.stepper__etat {
  font-size: var(--csp-font-size-sm);
  font-weight: 400;
  color: var(--text-mention-grey);
}

.stepper__barre {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: 1fr;
  gap: var(--csp-space-2);

  span {
    height: 6px;
    background: var(--background-contrast-grey);

    &.faite {
      background: var(--background-action-high-blue-france);
    }
  }
}

.stepper__suivante {
  margin: var(--csp-space-3) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.aide {
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-contrast-info);
  font-size: var(--csp-font-size-sm);
}

.corps {
  padding: var(--csp-space-6) var(--csp-space-8);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.nav {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
}

.nav__espace {
  flex: 1;
}

.sans-droit {
  margin: calc(-1 * var(--csp-space-3)) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
  text-align: right;
}
</style>
