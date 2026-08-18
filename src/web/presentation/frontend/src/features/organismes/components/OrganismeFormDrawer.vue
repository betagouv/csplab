<script setup lang="ts">
import type { CreateOrganismePayload, Versant } from '../types'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { SiretConflictError } from '../api'
import { SIRET_LENGTH, VERSANT_LABELS } from '../constants/organisme'

const props = defineProps<{
  saving?: boolean
}>()

const emit = defineEmits<{
  submit: [payload: CreateOrganismePayload]
}>()

const open = defineModel<boolean>('open', { required: true })

const nom = ref('')
const siret = ref('')
const versant = ref<string>('')
const gestionCandidatures = ref<'oui' | 'non'>('oui')
const siretError = ref<string | null>(null)

watch(open, (isOpen) => {
  if (!isOpen)
    return
  nom.value = ''
  siret.value = ''
  versant.value = ''
  gestionCandidatures.value = 'oui'
  siretError.value = null
}, { immediate: true })

watch(siret, () => {
  siretError.value = null
})

const VERSANT_OPTIONS = Object.entries(VERSANT_LABELS).map(
  ([value, label]) => ({ value, label }),
)

const GESTION_OPTIONS = [
  { value: 'oui', label: 'Oui' },
  { value: 'non', label: 'Non' },
]

const siretValid = computed(() =>
  new RegExp(`^\\d{${SIRET_LENGTH}}$`).test(siret.value),
)

const canSubmit = computed(() =>
  nom.value.trim().length > 0
  && siretValid.value
  && versant.value !== '',
)

function handleSubmit(): void {
  if (!canSubmit.value || props.saving)
    return
  emit('submit', {
    nom: nom.value.trim(),
    siret: siret.value,
    versant: versant.value as Versant,
    gestion_candidatures: gestionCandidatures.value === 'oui',
  })
}

function setSiretConflict(error: unknown): void {
  if (error instanceof SiretConflictError) {
    siretError.value = error.message
  }
}

defineExpose({ setSiretConflict })
</script>

<template>
  <CspDrawer
    v-model:open="open"
    title="Ajouter un organisme"
    size="md"
  >
    <form
      class="organisme-form"
      @submit.prevent="handleSubmit"
    >
      <p class="organisme-form__section-title">
        Détail de l'organisme
        <span class="organisme-form__required-hint">Champs obligatoires</span>
      </p>

      <CspInput
        v-model="nom"
        label="Nom de l'organisme"
        name="nom"
      />

      <CspInput
        v-model="siret"
        label="SIRET de l'organisme"
        name="siret"
        :error="Boolean(siretError)"
        :error-message="siretError ?? undefined"
      />

      <CspRadioGroup
        v-model="versant"
        label="Versant"
        name="versant"
        :options="VERSANT_OPTIONS"
      />

      <div>
        <CspRadioGroup
          v-model="gestionCandidatures"
          label="Gestion des candidatures sur l'outil"
          name="gestion_candidatures"
          :options="GESTION_OPTIONS"
        />
        <p class="organisme-form__hint">
          L'organisme reçoit ses candidatures et traite ses recrutements sur l'outil
        </p>
      </div>

      <div class="organisme-form__actions">
        <CspButton
          type="submit"
          label="Créer l'organisme"
          icon="ri:add-line"
          is-icon-left
          :disabled="!canSubmit || saving"
        />
        <CspButton
          variant="secondary"
          type="button"
          label="Annuler"
          @click="open = false"
        />
      </div>
    </form>
  </CspDrawer>
</template>

<style scoped lang="scss">
.organisme-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  height: 100%;
}

.organisme-form__section-title {
  margin: 0;
  font-weight: 700;
  display: flex;
  align-items: baseline;
  gap: var(--csp-space-3);
}

.organisme-form__required-hint {
  font-size: 0.75rem;
  font-weight: 400;
  color: var(--text-mention-grey);
}

.organisme-form__hint {
  margin: var(--csp-space-1) 0 0;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.organisme-form__actions {
  margin-top: auto;
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
  padding-top: var(--csp-space-4);
  border-top: 1px solid var(--border-default-grey);
}
</style>
