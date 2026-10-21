<script setup lang="ts">
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { personne } from '../../data/referentiels'
import { useOffre } from '../../data/useOffre'
import { useEtapes } from './useEtapes'

// Action de fin de la vue « Besoin », selon le chemin choisi : avec DAR (soumettre, attendre) ou sans DAR.
// Une fois le besoin validé (ou sans DAR), on passe à la rédaction de l'offre.
const { state, soumettreDar, manques, afficherErreurs, journaliser, notifier, verrouille, etapeEnCours, enregistrer, dirty, saving, darFigee } = useOffre()
const { aller } = useEtapes()
const b = state.besoin

const manquesBesoin = computed(() => manques.value.filter(m => m.stepId === 'besoin' || m.stepId === 'poste'))

type Cas = 'choisir' | 'soumettre' | 'attente' | 'rediger'
const cas = computed<Cas>(() => {
  if (b.darApplicable === 'oui') {
    if (b.darStatut === 'validee') {
      return 'rediger'
    }
    return b.darStatut === 'en_cours' ? 'attente' : 'soumettre'
  }
  return b.darApplicable === 'non' ? 'rediger' : 'choisir'
})

function signalerManques() {
  afficherErreurs.value = true
  notifier(`À compléter : ${manquesBesoin.value.map(m => m.libelle.toLowerCase()).join(', ')}.`, 'info')
}

function soumettre() {
  if (!soumettreDar()) {
    signalerManques()
  }
}

function rediger() {
  if (manquesBesoin.value.length && b.darApplicable === 'non') {
    signalerManques()
    return
  }
  if (!state.offreDemarree) {
    state.offreDemarree = true
    journaliser(b.darApplicable === 'oui' ? `Offre démarrée à partir de la DAR ${b.darRef}` : 'Offre démarrée à partir du besoin (sans DAR)')
    notifier('Offre démarrée : elle reprend les informations du besoin.')
  }
  aller('offre')
}

const texte = computed(() => ({
  choisir: 'Indiquez si ce besoin passe par une demande d\'autorisation (DAR) pour continuer.',
  soumettre: 'La fiche de poste constitue la DAR. Une fois soumise, elle ne sera plus modifiée.',
  attente: `DAR soumise${etapeEnCours.value ? `, en attente de ${personne(etapeEnCours.value.personneId).nom}` : ''}. Vous pouvez préparer l'offre en attendant ; elle sera créée une fois la DAR validée.`,
  rediger: b.darApplicable === 'oui' ? 'Besoin validé par la DAR : vous pouvez rédiger l\'offre.' : 'Besoin sans DAR : vous pouvez rédiger l\'offre.',
}[cas.value]))

async function sauver() {
  await enregistrer()
  notifier('Besoin enregistré.')
}
</script>

<template>
  <div class="actions">
    <p class="actions__info">
      <CspIcon
        :name="cas === 'attente' ? 'ri:time-line' : 'ri:information-line'"
        :size="16"
      />
      {{ texte }}
    </p>
    <div class="actions__btns">
      <CspButton
        v-if="!verrouille && !darFigee && (cas === 'soumettre' || cas === 'choisir' || !state.offreDemarree)"
        label="Enregistrer"
        variant="tertiary-no-outline"
        :disabled="saving || !dirty"
        @click="sauver"
      />
      <CspButton
        v-if="cas === 'soumettre'"
        label="Soumettre la DAR à validation"
        icon="ri:send-plane-line"
        @click="soumettre"
      />
      <CspButton
        v-else-if="cas === 'attente'"
        :label="state.offreDemarree ? 'Reprendre l\'offre' : 'Préparer l\'offre en attendant'"
        variant="secondary"
        icon="ri:arrow-right-line"
        @click="rediger"
      />
      <CspButton
        v-else-if="cas === 'rediger'"
        :label="state.offreDemarree ? 'Reprendre l\'offre' : 'Rédiger l\'offre'"
        icon="ri:arrow-right-line"
        @click="rediger"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.actions {
  position: sticky;
  bottom: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-4);
  padding: var(--csp-space-3) var(--csp-space-5);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  box-shadow: var(--csp-shadow-md);
}

.actions__info {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.actions__btns {
  display: flex;
  gap: var(--csp-space-2);
  flex-shrink: 0;
}
</style>
