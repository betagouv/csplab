<script setup lang="ts">
import type { FichePoste } from '../../data/types'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import { manquesFiche } from '../../data/fiches'

// « Lancer un recrutement » depuis une fiche : nombre de postes et parcours. Une seule fenêtre,
// pas d'assistant. La règle qui impose ou non une DAR n'est pas connue : le choix est laissé, et dit.
const props = defineProps<{ fiche: FichePoste }>()
const emit = defineEmits<{ lancer: [parcours: 'dar' | 'direct', nbPostes: string] }>()
const open = defineModel<boolean>('open', { default: false })
const parcours = ref<'dar' | 'direct'>('dar')
const nbPostes = ref('1')
const erreur = computed(() => (Number(nbPostes.value) >= 1 ? '' : 'Indiquez au moins 1 poste.'))
const manques = computed(() => manquesFiche(props.fiche))

const PARCOURS = [
  { value: 'dar' as const, titre: 'Avec une demande d\'autorisation (DAR)', desc: 'La DAR reprend la fiche ; une fois validée, vous poursuivez vers l\'offre.' },
  { value: 'direct' as const, titre: 'Création directe de l\'offre', desc: 'Quand le contexte et les règles de votre organisation le permettent.' },
]

function lancer() {
  if (erreur.value) {
    return
  }
  emit('lancer', parcours.value, nbPostes.value)
  open.value = false
}
</script>

<template>
  <CspDialog
    v-model:open="open"
    title="Lancer un recrutement"
    :description="`À partir de la fiche ${fiche.id} — ${fiche.intitule}`"
    size="md"
  >
    <div class="lancer">
      <CspInput
        v-model="nbPostes"
        type="number"
        label="Nombre de postes à pourvoir"
        hint="Un seul recrutement, une seule offre, pour un ou plusieurs postes identiques."
        :error="Boolean(erreur)"
        :error-message="erreur"
      />
      <fieldset class="lancer__parcours">
        <legend class="lancer__legend">
          Parcours
        </legend>
        <label
          v-for="p in PARCOURS"
          :key="p.value"
          class="lancer__option"
          :class="{ 'lancer__option--on': parcours === p.value }"
        >
          <input
            v-model="parcours"
            type="radio"
            name="parcours"
            :value="p.value"
          >
          <span>
            <strong>{{ p.titre }}</strong>
            <small>{{ p.desc }}</small>
          </span>
        </label>
        <p class="lancer__hypo">
          Hypothèse à confirmer : les règles qui imposent une DAR (organisation, statut, type de poste…) ne sont pas connues. Le prototype laisse le choix.
        </p>
      </fieldset>
      <p
        v-if="manques.length"
        class="lancer__info"
      >
        La fiche ne précise pas encore : {{ manques.join(', ') }}. Vous pourrez compléter ces informations dans le recrutement sans modifier la fiche.
      </p>
    </div>
    <template #footer>
      <CspButton
        label="Annuler"
        variant="secondary"
        @click="open = false"
      />
      <CspButton
        :label="parcours === 'dar' ? 'Préparer la DAR' : 'Créer l\'offre'"
        icon="ri:arrow-right-line"
        @click="lancer"
      />
    </template>
  </CspDialog>
</template>

<style scoped lang="scss">
.lancer {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
}

.lancer__parcours {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  border: 0;
}

.lancer__legend {
  margin-bottom: var(--csp-space-2);
  color: var(--text-label-grey);
}

.lancer__option {
  display: flex;
  gap: var(--csp-space-3);
  align-items: flex-start;
  padding: var(--csp-space-3);
  border: 1px solid var(--border-default-grey);
  cursor: pointer;

  input {
    margin-top: 3px;
    accent-color: var(--background-action-high-blue-france);
  }

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }

  &--on {
    border-color: var(--border-active-blue-france);
    background: var(--background-alt-blue-france);
  }
}

.lancer__hypo,
.lancer__info {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}
</style>
