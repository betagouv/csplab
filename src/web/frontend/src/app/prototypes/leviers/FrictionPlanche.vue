<script setup lang="ts">
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspToast from '@/components/base/CspToast/CspToast.vue'
import CspToastProvider from '@/components/base/CspToast/CspToastProvider.vue'

// etiquette: removal undone from the toast; equipe: confirmation; etape, etape-saisie: deletion that cannot be undone
// degre: how much colour and icon the confirmation takes, from the blue of the kit to a full red button
const props = withDefaults(defineProps<{
  cas: 'etiquette' | 'equipe' | 'etape' | 'etape-saisie'
  degre?: 'neutre' | 'picto' | 'contour-rouge' | 'plein-rouge'
  nomSaisi?: boolean
}>(), { degre: 'neutre', nomSaisi: false })

const ETAPE = 'Entretien RH'
const saisie = ref(props.nomSaisi ? ETAPE : '')
const nomConfirme = computed(() => saisie.value.trim() === ETAPE)
const ouvert = computed(() => props.cas !== 'etiquette')
</script>

<template>
  <CspToastProvider>
    <div class="friction-planche" />
    <CspToast
      v-if="cas === 'etiquette'"
      variant="success"
      title="Étiquette «&nbsp;Point de vigilance&nbsp;» retirée de la note"
      action-label="Annuler"
      :default-open="true"
      :duration="86400000"
    />
    <CspDialog
      v-if="cas === 'equipe'"
      :open="ouvert"
      title="Retirer de l’équipe"
      size="sm"
    >
      Julien Moreau perdra l'accès aux candidatures de ce recrutement. Son compte reste rattaché à l'organisme et pourra
      être réintégré à l'équipe plus tard.
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
        />
        <CspButton label="Retirer de l’équipe" />
      </template>
    </CspDialog>
    <CspDialog
      v-if="cas === 'etape'"
      :open="ouvert"
      title="Supprimer l'étape"
      size="sm"
    >
      Voulez-vous vraiment supprimer l'étape «&nbsp;{{ ETAPE }}&nbsp;»&nbsp;? Cette action est irréversible.
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
        />
        <CspButton
          label="Supprimer"
          variant="primary"
        />
      </template>
    </CspDialog>
    <CspDialog
      v-if="cas === 'etape-saisie'"
      :open="ouvert"
      title="Supprimer l'étape"
      size="md"
    >
      <template
        v-if="degre === 'plein-rouge'"
        #title
      >
        <span class="friction-planche__titre">
          <CspIcon
            name="ri:error-warning-line"
            class="friction-planche__alerte"
          />
          Supprimer l'étape
        </span>
      </template>
      <div class="friction-planche__corps">
        <p>Voulez-vous vraiment supprimer l'étape «&nbsp;{{ ETAPE }}&nbsp;»&nbsp;? Cette action est irréversible.</p>
        <CspInput
          v-model="saisie"
          label="Saisissez le nom de l'étape pour confirmer"
          :hint="ETAPE"
        />
      </div>
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
        />
        <CspButton
          label="Supprimer définitivement"
          :variant="degre === 'contour-rouge' ? 'secondary' : 'primary'"
          :icon="degre === 'neutre' ? undefined : 'ri:delete-bin-line'"
          :is-icon-left="degre !== 'neutre'"
          :class="`friction-planche__confirmer--${degre}`"
          :disabled="!nomConfirme"
        />
      </template>
    </CspDialog>
  </CspToastProvider>
</template>

<style scoped lang="scss">
.friction-planche {
  min-height: 35rem;
  background-color: var(--background-default-grey);
}

.friction-planche__titre {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-2);
}

.friction-planche__alerte {
  color: var(--text-default-error);
}

.friction-planche__confirmer--contour-rouge:not(:disabled) {
  color: var(--text-default-error);
  box-shadow: inset 0 0 0 1px var(--border-action-high-error);
}

.friction-planche__confirmer--plein-rouge:not(:disabled) {
  background-color: var(--background-action-high-error);
  color: var(--text-inverted-error);

  &:hover {
    background-color: var(--background-action-high-error-hover);
  }

  &:active {
    background-color: var(--background-action-high-error-active);
  }
}

.friction-planche__corps {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);

  p {
    margin: 0;
  }
}
</style>
