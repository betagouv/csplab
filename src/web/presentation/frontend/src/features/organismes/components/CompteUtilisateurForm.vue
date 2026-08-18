<script setup lang="ts">
import type { CompteUtilisateurType, CreateCompteUtilisateurPayload } from '../types'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'

const props = withDefaults(defineProps<{
  initialEmail?: string
  lockedType?: CompteUtilisateurType | null
  submitLabel: string
  saving?: boolean
}>(), {
  initialEmail: '',
  lockedType: null,
  saving: false,
})

const emit = defineEmits<{
  submit: [payload: CreateCompteUtilisateurPayload]
  cancel: []
}>()

const email = ref(props.initialEmail)
const nom = ref('')
const prenom = ref('')
const poste = ref('')
const type = ref<string>(props.lockedType ?? 'agent')

const TYPE_OPTIONS = [
  { value: 'gestionnaire', label: 'Gestionnaire' },
  { value: 'agent', label: 'Agent' },
]

const TYPE_DESCRIPTIONS: Record<string, string> = {
  gestionnaire: 'Administre son organisme, invite des utilisateurs, attribue les responsables des recrutements.',
  agent: 'Accède à l\'espace de l\'organisme sur l\'ATS et participe aux recrutements sur les offres auxquelles il est rattaché.',
}

const emailValid = computed(() => /^[^\s@]+@[^\s@][^\s.@]*\.[^\s@]+$/.test(email.value))

const canSubmit = computed(() =>
  emailValid.value
  && nom.value.trim().length > 0
  && prenom.value.trim().length > 0
  && type.value !== '',
)

function handleSubmit(): void {
  if (!canSubmit.value || props.saving)
    return
  emit('submit', {
    email: email.value.trim(),
    nom: nom.value.trim(),
    prenom: prenom.value.trim(),
    poste: poste.value.trim(),
    type: type.value as CompteUtilisateurType,
  })
}
</script>

<template>
  <form
    class="compte-form"
    @submit.prevent="handleSubmit"
  >
    <p class="compte-form__section-title">
      Détail de l'utilisateur
      <span class="compte-form__required-hint">Champs obligatoires</span>
    </p>

    <div>
      <CspInput
        v-model="email"
        type="email"
        label="Courriel"
        name="email"
      />
      <p class="compte-form__hint">
        Invitation envoyée sur son mail dès la création du compte
      </p>
    </div>

    <CspInput
      v-model="nom"
      label="Nom"
      name="nom"
    />

    <CspInput
      v-model="prenom"
      label="Prénom"
      name="prenom"
    />

    <CspInput
      v-model="poste"
      label="Poste occupé"
      name="poste"
    />

    <div>
      <CspRadioGroup
        v-model="type"
        label="Type d'utilisateur"
        name="type"
        :options="TYPE_OPTIONS"
        :disabled="lockedType !== null"
      />
      <p class="compte-form__hint">
        {{ TYPE_DESCRIPTIONS[type] }}
      </p>
    </div>

    <div class="compte-form__actions">
      <CspButton
        type="submit"
        :label="submitLabel"
        icon="ri:user-add-line"
        is-icon-left
        :disabled="!canSubmit || saving"
      />
      <CspButton
        variant="secondary"
        type="button"
        label="Annuler"
        @click="emit('cancel')"
      />
    </div>
  </form>
</template>

<style scoped lang="scss">
.compte-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  height: 100%;
}

.compte-form__section-title {
  margin: 0;
  font-weight: 700;
  display: flex;
  align-items: baseline;
  gap: var(--csp-space-3);
}

.compte-form__required-hint {
  font-size: 0.75rem;
  font-weight: 400;
  color: var(--text-mention-grey);
}

.compte-form__hint {
  margin: var(--csp-space-1) 0 0;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.compte-form__actions {
  margin-top: auto;
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
  padding-top: var(--csp-space-4);
  border-top: 1px solid var(--border-default-grey);
}
</style>
