<script setup lang="ts">
import type { CreateOrganismePayload, Versant } from '../types'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { SIRET_LENGTH, VERSANT_LABELS } from '../constants/organisme'
import { isSiretValid } from '../siret'

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
const gestionAts = ref<'oui' | 'non'>('oui')
const siretError = ref<string | null>(null)

watch(open, (isOpen) => {
  if (!isOpen)
    return
  nom.value = ''
  siret.value = ''
  versant.value = ''
  gestionAts.value = 'oui'
  siretError.value = null
}, { immediate: true })

watch(siret, (value) => {
  siretError.value = null
  const digits = value.replace(/\D/g, '')
  if (digits !== value)
    siret.value = digits
})

const VERSANT_OPTIONS = Object.entries(VERSANT_LABELS).map(
  ([value, label]) => ({ value, label }),
)

const GESTION_OPTIONS = [
  { value: 'oui', label: 'Oui' },
  { value: 'non', label: 'Non' },
]

const canSubmit = computed(() =>
  nom.value.trim().length > 0
  && siret.value.length > 0
  && versant.value !== '',
)

function handleSubmit(): void {
  if (!canSubmit.value || props.saving)
    return
  if (siret.value.length !== SIRET_LENGTH) {
    siretError.value = `Le SIRET doit comporter ${SIRET_LENGTH} chiffres.`
    return
  }
  if (!isSiretValid(siret.value)) {
    siretError.value = 'Ce SIRET n\'est pas valide, vérifiez votre saisie.'
    return
  }
  emit('submit', {
    nom: nom.value.trim(),
    siret: siret.value,
    versant: versant.value as Versant,
    gestion_ats: gestionAts.value === 'oui',
  })
}

function setSiretError(message: string): void {
  siretError.value = message
}

defineExpose({ setSiretError })
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
          v-model="gestionAts"
          label="Gestion des candidatures sur l'outil"
          name="gestion_ats"
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
