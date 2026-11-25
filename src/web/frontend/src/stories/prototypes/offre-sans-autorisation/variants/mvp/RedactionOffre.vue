<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import { manquesAnnonce } from './aide'
import ApercuCandidat from './ApercuCandidat.vue'
import { ETAPES_OFFRE } from './etapes'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import ParcoursOffre from './ParcoursOffre.vue'
import { db, heure, sauvegarder, UTILISATEUR } from './store'

// Créer une offre (retour Alice du 25/11/2026) : formulaire vide (bouton « Créer une offre ») ou pré-rempli
// (« Dupliquer » dans le menu « … » d'une offre), sans écran de choix. Une page par étape. Enregistrement automatique :
// on peut quitter à tout moment. « Publier » s'active dès que tous les champs obligatoires sont remplis.
const props = defineProps<{ id: string, etape?: number }>()
const { aller, notifier } = useNav()
const o = computed(() => db.offres.find(x => x.id === props.id)!)

// L'étape peut aussi venir de l'adresse (?etape=3) : utile pour montrer ou capturer une étape précise.
const etapeUrl = Number(new URLSearchParams(window.location.search).get('etape')) || undefined
const etape = ref(Math.min(Math.max(props.etape ?? etapeUrl ?? 1, 1), ETAPES_OFFRE.length))

const enregistre = ref(heure())
const apercu = ref(false)
watch(o, () => {
  sauvegarder()
  enregistre.value = heure()
}, { deep: true })

const reste = computed(() => manquesAnnonce(o.value).length)
const peutPublier = computed(() => db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier)
const source = computed(() => (o.value.origineContenu === 'duplication' ? db.offres.find(x => x.id === o.value.sourceOffreId) : undefined))

function quitter() {
  notifier('Brouillon enregistré. Vous pouvez le reprendre à tout moment.')
  aller({ nom: 'offres' })
}
function publier() {
  aller({ nom: 'publier', id: o.value.id })
}
</script>

<template>
  <PageAts
    actif="offres"
    largeur="full"
    :titre="o.titre || 'Nouvelle offre'"
    :sous-titre="source ? `Brouillon · copie de « ${source.titre} »` : 'Brouillon'"
    :fil="[{ label: 'Mes offres d\'emploi', to: '/offres' }, { label: 'Nouvelle offre' }]"
  >
    <template #actions>
      <span class="enregistre">Enregistré automatiquement à {{ enregistre }}</span>
      <CspButton
        label="Aperçu candidat"
        size="sm"
        variant="tertiary"
        icon="ri:eye-line"
        is-icon-left
        @click="apercu = true"
      />
      <CspButton
        label="Enregistrer et quitter"
        size="sm"
        variant="secondary"
        @click="quitter"
      />
      <CspButton
        v-if="peutPublier"
        label="Publier"
        size="sm"
        icon="ri:send-plane-line"
        is-icon-left
        :disabled="Boolean(reste)"
        :title="reste ? `Encore ${reste} champ${reste > 1 ? 's' : ''} obligatoire${reste > 1 ? 's' : ''} à remplir` : undefined"
        @click="publier"
      />
    </template>

    <p
      class="etat"
      :class="{ 'etat--ok': !reste }"
    >
      {{ reste
        ? `Encore ${reste} champ${reste > 1 ? 's' : ''} obligatoire${reste > 1 ? 's' : ''} (*) à remplir avant de pouvoir publier. Vous pouvez enregistrer et quitter à tout moment.`
        : peutPublier ? 'Tous les champs obligatoires sont remplis : vous pouvez publier l\'offre.' : 'Tous les champs obligatoires sont remplis. Vous n\'avez pas le droit « Publier » : un agent qui l\'a mettra l\'offre en ligne.' }}
    </p>

    <ParcoursOffre
      v-model:etape="etape"
      :offre="o"
    >
      <template #fin>
        <CspButton
          label="Enregistrer et quitter"
          variant="secondary"
          @click="quitter"
        />
        <CspButton
          v-if="peutPublier"
          label="Publier"
          icon="ri:send-plane-line"
          is-icon-left
          :disabled="Boolean(reste)"
          @click="publier"
        />
      </template>
    </ParcoursOffre>

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
.enregistre {
  align-self: center;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.etat {
  max-width: 80rem;
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-blue-france);
  background: var(--background-alt-blue-france);
  font-size: var(--csp-font-size-sm);

  &--ok {
    border-left-color: var(--border-plain-success);
    background: var(--background-contrast-success);
  }
}
</style>
