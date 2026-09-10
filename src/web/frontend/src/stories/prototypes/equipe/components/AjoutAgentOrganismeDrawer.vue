<script setup lang="ts">
import type { RoleOrganisme } from '../data/mock'
import type { InvitationPayload } from '../shared/useEquipePrototype'
import type { CspRadioGroupOption } from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { ROLE_ORGANISME_LABELS } from '../data/mock'
import { useEquipePrototypeContext } from '../shared/context'

const emit = defineEmits<{
  submit: [invitation: InvitationPayload, roleOrganisme: RoleOrganisme]
}>()

const open = defineModel<boolean>('open', { required: true })

const proto = useEquipePrototypeContext()

const EMAIL_PATTERN = /^[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+$/

const roleOptions = computed<CspRadioGroupOption[]>(() => [
  { value: 'agent', label: ROLE_ORGANISME_LABELS.agent },
  { value: 'gestionnaire', label: ROLE_ORGANISME_LABELS.gestionnaire, disabled: !proto.peutPromouvoirGestionnaire.value },
])

const invitation = ref<InvitationPayload>({ prenom: '', nom: '', email: '', poste: '' })
const roleOrganisme = ref<RoleOrganisme>('agent')
const errors = ref<Partial<Record<keyof InvitationPayload, string>>>({})

const emailExistant = computed(() => {
  const email = invitation.value.email.trim().toLowerCase()
  return proto.scenario.agents.some(agent => agent.email.toLowerCase() === email)
})

watch(open, (isOpen) => {
  if (!isOpen) {
    invitation.value = { prenom: '', nom: '', email: '', poste: '' }
    roleOrganisme.value = 'agent'
    errors.value = {}
  }
})

function valider(): boolean {
  const next: typeof errors.value = {}
  if (!EMAIL_PATTERN.test(invitation.value.email.trim()))
    next.email = 'Renseignez une adresse électronique valide.'
  else if (emailExistant.value)
    next.email = 'Cette personne fait déjà partie de l\'organisme.'
  if (!invitation.value.prenom.trim())
    next.prenom = 'Renseignez le prénom.'
  if (!invitation.value.nom.trim())
    next.nom = 'Renseignez le nom.'
  if (!invitation.value.poste.trim())
    next.poste = 'Renseignez le poste.'
  errors.value = next
  return Object.keys(next).length === 0
}

function handleSubmit(): void {
  if (valider())
    emit('submit', { ...invitation.value }, roleOrganisme.value)
}
</script>

<template>
  <CspDrawer
    v-model:open="open"
    title="Créer un compte"
    size="md"
  >
    <form
      class="ajout-agent"
      novalidate
      @submit.prevent="handleSubmit"
    >
      <CspCallout
        variant="info"
        title="La personne recevra un courriel d'invitation."
        description="Son compte s'activera à sa première connexion. Elle accédera ensuite aux recrutements auxquels elle sera rattachée."
      />
      <div class="ajout-agent__fields">
        <CspInput
          v-model="invitation.email"
          label="Adresse électronique"
          name="email"
          type="email"
          placeholder="prenom.nom@exemple.gouv.fr"
          autocomplete="off"
          :error="Boolean(errors.email)"
          :error-message="errors.email"
        />
        <div class="ajout-agent__row">
          <CspInput
            v-model="invitation.prenom"
            label="Prénom"
            name="prenom"
            autocomplete="off"
            :error="Boolean(errors.prenom)"
            :error-message="errors.prenom"
          />
          <CspInput
            v-model="invitation.nom"
            label="Nom"
            name="nom"
            autocomplete="off"
            :error="Boolean(errors.nom)"
            :error-message="errors.nom"
          />
        </div>
        <CspInput
          v-model="invitation.poste"
          label="Poste"
          name="poste"
          autocomplete="off"
          :error="Boolean(errors.poste)"
          :error-message="errors.poste"
        />
      </div>
      <div class="ajout-agent__role">
        <CspRadioGroup
          v-model="roleOrganisme"
          label="Rôle dans l'organisme"
          name="role-organisme"
          :options="roleOptions"
        />
        <p class="ajout-agent__hint">
          {{ roleOrganisme === 'gestionnaire'
            ? 'Administre l\'organisme, invite des membres et attribue les responsables des recrutements.'
            : 'Participe aux recrutements auxquels un responsable ou un gestionnaire le rattache.' }}
        </p>
        <p
          v-if="!proto.peutPromouvoirGestionnaire.value"
          class="ajout-agent__hint"
        >
          Seul l'administrateur de la plateforme peut créer un compte gestionnaire.
        </p>
      </div>
    </form>
    <template #footer>
      <div class="ajout-agent__actions">
        <CspButton
          label="Annuler"
          variant="secondary"
          type="button"
          @click="open = false"
        />
        <CspButton
          label="Créer le compte"
          icon="ri:user-add-line"
          is-icon-left
          type="button"
          @click="handleSubmit"
        />
      </div>
    </template>
  </CspDrawer>
</template>

<style scoped lang="scss">
.ajout-agent {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
}

.ajout-agent__fields {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.ajout-agent__row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--csp-space-4);
}

.ajout-agent__role {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.ajout-agent__hint {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.ajout-agent__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
}
</style>
