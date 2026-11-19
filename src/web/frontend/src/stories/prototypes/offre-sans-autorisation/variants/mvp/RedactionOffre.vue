<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import Panel from '../../shared/Panel.vue'
import { manquesAnnonce, tentatives } from './aide'
import ApercuCandidat from './ApercuCandidat.vue'
import { ETAPES_OFFRE } from './etapes'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import ParcoursOffre from './ParcoursOffre.vue'
import RecapPublication from './RecapPublication.vue'
import { db, heure, sauvegarder, UTILISATEUR } from './store'

// Créer une offre : le formulaire en étapes (retour PO, F1), avec le récapitulatif des champs obligatoires à droite
// (F4). Rien n'est exigé pour enregistrer un brouillon. Processus et Équipe ne font plus partie du formulaire (F2) :
// le créateur est Responsable, et les étapes de recrutement par défaut de l'organisme s'appliquent.
const props = defineProps<{ id: string, etape?: number }>()
const { aller, notifier } = useNav()
const o = computed(() => db.offres.find(x => x.id === props.id)!)

// L'étape peut aussi venir de l'adresse (?etape=3) : utile pour montrer ou capturer une étape précise.
const etapeUrl = Number(new URLSearchParams(window.location.search).get('etape')) || undefined
const etape = ref(Math.min(Math.max(props.etape ?? etapeUrl ?? 1, 1), ETAPES_OFFRE.length))

// Enregistrement automatique.
const enregistre = ref(heure())
// Aperçu candidat (œil) : l'annonce telle que la verront les candidats, à côté du formulaire.
const apercu = ref(false)
watch(o, () => {
  sauvegarder()
  enregistre.value = heure()
}, { deep: true })

const peutPublier = computed(() => db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier)
function enregistrer() {
  notifier('Brouillon enregistré. Vous pouvez le reprendre à tout moment.')
  aller({ nom: 'offre', id: o.value.id })
}
function publier() {
  // Les erreurs s'affichent à partir de la première tentative de publication (F6).
  if (manquesAnnonce(o.value).length) {
    tentatives.add(o.value.id)
  }
  aller({ nom: 'publier', id: o.value.id })
}
</script>

<template>
  <PageAts
    actif="offres"
    largeur="full"
    :titre="o.titre || 'Nouvelle offre'"
    sous-titre="Nouvelle offre d'emploi · brouillon"
    :fil="[{ label: 'Mes offres d\'emploi', to: '/offres' }, { label: 'Nouvelle offre' }]"
    :bandeaux="['Les champs obligatoires (*) ne sont contrôlés qu\'au moment de publier : vous pouvez enregistrer une offre incomplète.']"
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

    <div class="colonnes">
      <ParcoursOffre
        v-model:etape="etape"
        :offre="o"
      >
        <template #fin>
          <CspButton
            label="Enregistrer le brouillon"
            variant="secondary"
            @click="enregistrer"
          />
          <CspButton
            v-if="peutPublier"
            label="Publier"
            icon="ri:arrow-right-line"
            @click="publier"
          />
        </template>
      </ParcoursOffre>
      <aside class="cote">
        <Panel titre="Avant de publier">
          <RecapPublication
            :offre="o"
            @aller="(n: number) => (etape = n)"
          />
          <p
            v-if="!peutPublier"
            class="sans-droit"
          >
            Vous n'avez pas le droit « Publier » : un agent qui l'a mettra l'offre en ligne.
          </p>
        </Panel>
      </aside>
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
.colonnes {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 20rem;
  gap: var(--csp-space-8);
  align-items: start;
  max-width: 80rem;
}

@media (width <= 64rem) {
  .colonnes {
    grid-template-columns: minmax(0, 1fr);
  }
}

.cote {
  position: sticky;
  top: var(--csp-space-4);
}

.enregistre {
  align-self: center;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.sans-droit {
  margin: var(--csp-space-3) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}
</style>
