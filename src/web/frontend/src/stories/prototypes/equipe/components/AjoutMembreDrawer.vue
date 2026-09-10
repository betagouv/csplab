<script setup lang="ts">
import type { ProtoAgent, RoleOffre } from '../data/mock'
import type { InvitationPayload } from '../shared/useEquipePrototype'
import type { CspComboboxOption } from '@/components/base/CspCombobox/CspCombobox.vue'
import type { CspRadioGroupOption } from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import type { CspSelectOption } from '@/components/base/CspSelect/CspSelect.vue'
import { computed, ref, watch } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspCombobox from '@/components/base/CspCombobox/CspCombobox.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import { pluralize } from '@/utils/format'
import { normalizeSearchText } from '@/utils/search'
import { FONCTIONS, ROLE_OFFRE_DESCRIPTIONS, ROLE_OFFRE_LABELS } from '../data/mock'
import { useEquipePrototypeContext } from '../shared/context'
import { formatAgentNom } from '../shared/format'

export type AjoutContexte = 'equipe' | 'responsable'

export type AjoutMembreResultat
  = | { type: 'agent', agentUuid: string, roleOffre: RoleOffre, fonction: string | null }
    | { type: 'invitation', invitation: InvitationPayload, roleOffre: RoleOffre, fonction: string | null }

const props = withDefaults(defineProps<{
  contexte: AjoutContexte
  exclus?: string[]
  peutInviter?: boolean
}>(), {
  exclus: () => [],
  peutInviter: false,
})

const emit = defineEmits<{
  submit: [resultat: AjoutMembreResultat]
}>()

const open = defineModel<boolean>('open', { required: true })
const recrutementUuids = defineModel<string[]>('recrutementUuids', { default: () => [] })

const proto = useEquipePrototypeContext()

const EMAIL_PATTERN = /^[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+$/
const MAX_SUGGESTIONS = 8
const SANS_FONCTION = 'aucune'

const ROLE_OPTIONS: CspRadioGroupOption[] = [
  { value: 'recruteur', label: ROLE_OFFRE_LABELS.recruteur },
  { value: 'contributeur', label: ROLE_OFFRE_LABELS.contributeur },
]

const FONCTION_OPTIONS: CspSelectOption[] = [
  { value: SANS_FONCTION, label: 'Aucune' },
  ...FONCTIONS.map(fonction => ({ value: fonction, label: fonction })),
]

type Mode = 'recherche' | 'selection' | 'invitation'

const mode = ref<Mode>('recherche')
const searchTerm = ref('')
const selectedValue = ref<string | null>(null)
const comboOpen = ref(false)
const agentChoisi = ref<ProtoAgent | null>(null)
const roleOffre = ref<RoleOffre>('recruteur')
const fonction = ref(SANS_FONCTION)
const invitation = ref<InvitationPayload>({ prenom: '', nom: '', email: '', poste: '' })
const invitationErrors = ref<Partial<Record<keyof InvitationPayload, string>>>({})

const isResponsable = computed(() => props.contexte === 'responsable')
const roleRetenu = computed<RoleOffre>(() => (isResponsable.value ? 'responsable' : roleOffre.value))

const title = computed(() => (isResponsable.value ? 'Assigner un responsable' : 'Ajouter un membre'))

const offres = computed(() =>
  recrutementUuids.value
    .map(uuid => proto.recrutementOf(uuid))
    .filter((r): r is NonNullable<typeof r> => r !== null),
)

const offresLabel = computed(() => {
  const count = offres.value.length
  return `${count} ${pluralize(count, 'offre sélectionnée', 'offres sélectionnées')}`
})

const emailSaisi = computed(() => {
  const value = searchTerm.value.trim().toLowerCase()
  return EMAIL_PATTERN.test(value) ? value : null
})

const agentParEmail = computed(() =>
  emailSaisi.value ? proto.scenario.agents.find(a => a.email.toLowerCase() === emailSaisi.value) ?? null : null,
)

const options = computed<CspComboboxOption[]>(() => {
  const term = normalizeSearchText(searchTerm.value.trim())
  return proto.scenario.agents
    .filter(agent => !props.exclus.includes(agent.uuid))
    .filter(agent => !term || normalizeSearchText(`${agent.prenom} ${agent.nom} ${agent.nom} ${agent.prenom} ${agent.email}`).includes(term))
    .slice(0, MAX_SUGGESTIONS)
    .map(agent => ({
      value: agent.uuid,
      label: formatAgentNom(agent),
      description: agent.statut === 'en_attente' ? `${agent.poste} · ${agent.email} · invitation en attente` : `${agent.poste} · ${agent.email}`,
    }))
})

const actionLabel = computed(() => {
  if (!props.peutInviter || !emailSaisi.value || agentParEmail.value || options.value.length > 0)
    return null
  return `Inviter ${emailSaisi.value}`
})

const emptyLabel = computed(() => {
  if (agentParEmail.value && props.exclus.includes(agentParEmail.value.uuid))
    return 'Cette personne fait déjà partie de l\'équipe.'
  if (emailSaisi.value && !props.peutInviter)
    return 'Aucun compte ne correspond à ce courriel. Seul un responsable de l\'offre peut inviter une nouvelle personne.'
  return searchTerm.value.trim() ? 'Aucun membre de l\'organisme ne correspond.' : 'Saisissez un nom ou un courriel.'
})

const submitLabel = computed(() => {
  if (mode.value === 'invitation')
    return isResponsable.value ? 'Créer le compte et assigner' : 'Créer le compte et ajouter'
  return isResponsable.value ? 'Assigner le responsable' : 'Ajouter à l\'équipe'
})

const submitDisabled = computed(() => mode.value === 'recherche' || offres.value.length === 0)

watch(selectedValue, (value) => {
  if (!value)
    return
  agentChoisi.value = proto.agentOf(value)
  if (agentChoisi.value)
    mode.value = 'selection'
})

function changerPersonne(): void {
  agentChoisi.value = null
  selectedValue.value = null
  searchTerm.value = ''
  mode.value = 'recherche'
}

function demarrerInvitation(): void {
  invitation.value = { prenom: '', nom: '', email: emailSaisi.value ?? '', poste: '' }
  invitationErrors.value = {}
  comboOpen.value = false
  mode.value = 'invitation'
}

function retirerOffre(uuid: string): void {
  recrutementUuids.value = recrutementUuids.value.filter(value => value !== uuid)
}

function reset(): void {
  mode.value = 'recherche'
  searchTerm.value = ''
  selectedValue.value = null
  agentChoisi.value = null
  roleOffre.value = 'recruteur'
  fonction.value = SANS_FONCTION
  invitation.value = { prenom: '', nom: '', email: '', poste: '' }
  invitationErrors.value = {}
}

watch(open, (isOpen) => {
  if (!isOpen)
    reset()
})

function fonctionRetenue(): string | null {
  return fonction.value === SANS_FONCTION ? null : fonction.value
}

function validerInvitation(): boolean {
  const errors: typeof invitationErrors.value = {}
  if (!invitation.value.prenom.trim())
    errors.prenom = 'Renseignez le prénom.'
  if (!invitation.value.nom.trim())
    errors.nom = 'Renseignez le nom.'
  if (!EMAIL_PATTERN.test(invitation.value.email.trim()))
    errors.email = 'Renseignez une adresse électronique valide.'
  if (!invitation.value.poste.trim())
    errors.poste = 'Renseignez le poste.'
  invitationErrors.value = errors
  return Object.keys(errors).length === 0
}

function handleSubmit(): void {
  if (mode.value === 'selection' && agentChoisi.value) {
    emit('submit', { type: 'agent', agentUuid: agentChoisi.value.uuid, roleOffre: roleRetenu.value, fonction: fonctionRetenue() })
    return
  }
  if (mode.value === 'invitation' && validerInvitation()) {
    emit('submit', { type: 'invitation', invitation: { ...invitation.value }, roleOffre: roleRetenu.value, fonction: fonctionRetenue() })
  }
}
</script>

<template>
  <CspDrawer
    v-model:open="open"
    :title="title"
    size="md"
  >
    <form
      class="ajout-membre"
      novalidate
      @submit.prevent="handleSubmit"
    >
      <section
        v-if="isResponsable"
        class="ajout-membre__offres"
      >
        <p class="ajout-membre__offres-title">
          {{ offresLabel }}
        </p>
        <p class="ajout-membre__hint">
          Le responsable choisi pilotera {{ offres.length > 1 ? 'chacune de ces offres' : 'cette offre' }} et pourra constituer son équipe.
        </p>
        <ul class="ajout-membre__offres-list">
          <li
            v-for="offre in offres"
            :key="offre.uuid"
          >
            <CspTag
              v-if="offres.length > 1"
              variant="dismissible"
              :label="offre.intitule"
              :dismiss-label="`Retirer ${offre.intitule} de la sélection`"
              @dismiss="retirerOffre(offre.uuid)"
            />
            <CspTag
              v-else
              :label="offre.intitule"
              icon="ri:briefcase-line"
            />
          </li>
        </ul>
      </section>

      <template v-if="mode === 'invitation'">
        <CspCallout
          variant="info"
          title="Un compte agent sera créé dans l'organisme."
          description="La personne recevra un courriel d'invitation. Son accès s'activera à sa première connexion, sur cette offre uniquement."
        />
        <div class="ajout-membre__fields">
          <CspInput
            v-model="invitation.email"
            label="Adresse électronique"
            name="email"
            type="email"
            autocomplete="off"
            :error="Boolean(invitationErrors.email)"
            :error-message="invitationErrors.email"
          />
          <div class="ajout-membre__row">
            <CspInput
              v-model="invitation.prenom"
              label="Prénom"
              name="prenom"
              autocomplete="off"
              :error="Boolean(invitationErrors.prenom)"
              :error-message="invitationErrors.prenom"
            />
            <CspInput
              v-model="invitation.nom"
              label="Nom"
              name="nom"
              autocomplete="off"
              :error="Boolean(invitationErrors.nom)"
              :error-message="invitationErrors.nom"
            />
          </div>
          <CspInput
            v-model="invitation.poste"
            label="Poste"
            name="poste"
            placeholder="Chargé·e de mission, cheffe de bureau…"
            autocomplete="off"
            :error="Boolean(invitationErrors.poste)"
            :error-message="invitationErrors.poste"
          />
        </div>
      </template>

      <template v-else>
        <div
          v-if="mode === 'selection' && agentChoisi"
          class="ajout-membre__selection"
        >
          <p class="ajout-membre__label">
            Personne
          </p>
          <div class="ajout-membre__agent">
            <div class="ajout-membre__agent-body">
              <p class="ajout-membre__agent-name">
                {{ formatAgentNom(agentChoisi) }}
                <CspBadge
                  v-if="agentChoisi.statut === 'en_attente'"
                  size="sm"
                  variant="soft"
                  type="warning"
                  label="Invitation en attente"
                />
              </p>
              <p class="ajout-membre__agent-detail">
                {{ agentChoisi.poste }}
              </p>
              <p class="ajout-membre__agent-detail">
                {{ agentChoisi.email }}
              </p>
            </div>
            <CspButton
              label="Changer"
              variant="tertiary-no-outline"
              size="sm"
              type="button"
              @click="changerPersonne"
            />
          </div>
        </div>
        <CspCombobox
          v-else
          v-model="selectedValue"
          v-model:search-term="searchTerm"
          v-model:open="comboOpen"
          label="Personne"
          hint="Recherchez parmi les membres de l'organisme par nom ou courriel."
          placeholder="Nom, prénom ou courriel"
          :options="options"
          :empty-label="emptyLabel"
          :action-label="actionLabel"
          action-icon="ri:user-add-line"
          @action="demarrerInvitation"
        />
      </template>

      <template v-if="mode !== 'recherche'">
        <div
          v-if="!isResponsable"
          class="ajout-membre__role"
        >
          <CspRadioGroup
            v-model="roleOffre"
            label="Rôle sur l'offre"
            name="role-offre"
            :options="ROLE_OPTIONS"
          />
          <p class="ajout-membre__hint">
            {{ ROLE_OFFRE_DESCRIPTIONS[roleOffre] }}
          </p>
        </div>
        <CspSelect
          v-model="fonction"
          label="Fonction dans le recrutement (facultatif)"
          :options="FONCTION_OPTIONS"
        />
      </template>
    </form>

    <template #footer>
      <div class="ajout-membre__actions">
        <CspButton
          label="Annuler"
          variant="secondary"
          type="button"
          @click="open = false"
        />
        <CspButton
          :label="submitLabel"
          icon="ri:user-add-line"
          is-icon-left
          type="button"
          :disabled="submitDisabled"
          @click="handleSubmit"
        />
      </div>
    </template>
  </CspDrawer>
</template>

<style scoped lang="scss">
.ajout-membre {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
}

.ajout-membre__offres {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  padding-bottom: var(--csp-space-5);
  border-bottom: 1px solid var(--border-default-grey);
}

.ajout-membre__offres-title {
  margin: 0;
  font-weight: var(--csp-font-weight-medium);
  color: var(--text-title-grey);
}

.ajout-membre__offres-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: var(--csp-space-1) 0 0;
  padding: 0;
  list-style: none;
}

.ajout-membre__hint {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.ajout-membre__fields {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.ajout-membre__row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--csp-space-4);
}

.ajout-membre__selection {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.ajout-membre__label {
  margin: 0;
  font-weight: var(--csp-font-weight-medium);
  color: var(--text-title-grey);
}

.ajout-membre__agent {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--csp-space-3);
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  border-radius: 0.25rem;
}

.ajout-membre__agent-body {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  min-width: 0;
}

.ajout-membre__agent-name {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  font-weight: 600;
  color: var(--text-title-grey);
}

.ajout-membre__agent-detail {
  margin: 0;
  font-size: var(--csp-font-size-base);
  color: var(--text-mention-grey);
}

.ajout-membre__role {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.ajout-membre__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
}
</style>
