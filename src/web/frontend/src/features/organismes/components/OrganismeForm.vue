<script setup lang="ts">
import type { CreateOrganismePayload, OrganismesList, UpdateOrganismePayload, Versant } from '../types'
import { computed, ref, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawerFooter from '@/components/base/CspDrawer/CspDrawerFooter.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { SIRET_LENGTH, VERSANT_LABELS } from '../constants/organisme'
import { isSiretValid } from '../siret'

const props = defineProps<{
  organisme?: OrganismesList | null
  saving?: boolean
  rejectedSiret?: string | null
}>()

const emit = defineEmits<{
  create: [payload: CreateOrganismePayload]
  update: [payload: UpdateOrganismePayload]
  cancel: []
}>()

const isEdition = computed(() => Boolean(props.organisme))

const nom = ref(props.organisme?.nom ?? '')
const siret = ref(props.organisme?.siret ?? '')
const versant = ref<string>(props.organisme?.versant ?? '')
const gestionAts = ref<'oui' | 'non'>((props.organisme?.gestion_ats ?? true) ? 'oui' : 'non')
const siretValidationError = ref<string | null>(null)

const siretError = computed(() => {
  if (siretValidationError.value) {
    return siretValidationError.value
  }
  if (props.rejectedSiret && props.rejectedSiret === siret.value) {
    return 'Ce SIRET est déjà utilisé ou n\'est pas valide.'
  }
  return null
})

function handleSiretInput(value: string): void {
  siretValidationError.value = null
  siret.value = value.replace(/\D/g, '')
}

const VERSANT_OPTIONS = Object.entries(VERSANT_LABELS).map(
  ([value, label]) => ({ value, label }),
)

const GESTION_OPTIONS = [
  { value: 'oui', label: 'Oui' },
  { value: 'non', label: 'Non' },
]

const canSubmit = computed(() =>
  nom.value.trim().length > 0
  && (isEdition.value || siret.value.length > 0)
  && versant.value !== '',
)

function handleSubmit(): void {
  if (!canSubmit.value || props.saving) {
    return
  }
  const commonFields = {
    nom: nom.value.trim(),
    versant: versant.value as Versant,
    gestion_ats: gestionAts.value === 'oui',
  }
  if (isEdition.value) {
    emit('update', commonFields)
    return
  }
  if (siret.value.length !== SIRET_LENGTH) {
    siretValidationError.value = `Le SIRET doit comporter ${SIRET_LENGTH} chiffres.`
    return
  }
  if (!isSiretValid(siret.value)) {
    siretValidationError.value = 'Ce SIRET n\'est pas valide, vérifiez votre saisie.'
    return
  }
  emit('create', { ...commonFields, siret: siret.value })
}

const formId = useId()
</script>

<template>
  <form
    :id="formId"
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
      :model-value="siret"
      label="SIRET de l'organisme"
      name="siret"
      :disabled="isEdition"
      :error="Boolean(siretError)"
      :error-message="siretError ?? undefined"
      @update:model-value="handleSiretInput"
    />

    <CspRadioGroup
      v-model="versant"
      label="Versant"
      name="versant"
      :options="VERSANT_OPTIONS"
    />

    <div>
      <CspRadioGroup
        v-model="gestionAts"
        label="Gestion des candidatures sur l'outil"
        name="gestion_ats"
        :options="GESTION_OPTIONS"
      />
      <p class="organisme-form__hint">
        L'organisme reçoit ses candidatures et traite ses recrutements sur l'outil
      </p>
    </div>
  </form>

  <CspDrawerFooter>
    <CspButton
      variant="secondary"
      type="button"
      label="Annuler"
      @click="emit('cancel')"
    />
    <CspButton
      type="submit"
      :form="formId"
      :label="isEdition ? 'Enregistrer les modifications' : 'Créer l\'organisme'"
      :icon="isEdition ? undefined : 'ri:add-line'"
      is-icon-left
      :disabled="!canSubmit || saving"
    />
  </CspDrawerFooter>
</template>

<style scoped lang="scss">
.organisme-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-drawer-body-gap);
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
</style>
