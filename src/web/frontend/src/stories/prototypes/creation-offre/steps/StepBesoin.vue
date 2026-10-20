<script setup lang="ts">
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspCombobox from '@/components/base/CspCombobox/CspCombobox.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { CATEGORIES, libelleMetier, METIERS, MOTIFS, ORGANISMES, SERVICES, STATUTS, versantDe } from '../data/referentiels'
import { useOffre } from '../data/useOffre'
import Field from '../shared/Field.vue'
import FieldRow from '../shared/FieldRow.vue'
import FormSection from '../shared/FormSection.vue'
import StepFooter from '../shared/StepFooter.vue'
import StepHeader from '../shared/StepHeader.vue'

// Écran 2 — qualifier le besoin et le poste : données administratives, à usage interne.
const { state, verrouille, afficherErreurs } = useOffre()
const b = state.besoin

const erreur = (vide: boolean, message: string) => (afficherErreurs.value && vide ? message : undefined)

// --- Organisme et service ---
const organismes = ORGANISMES.map(o => ({ value: o.value, label: o.label }))
const services = computed(() => (SERVICES[b.organisme] ?? []).map(s => ({ value: s, label: s })))
const versant = computed(() => versantDe(b.organisme))
const libelleCorps = computed(() => {
  if (versant.value.includes('territoriale')) {
    return 'Cadre d\'emplois'
  }
  return 'Corps'
})

// --- Métier : recherche dans le répertoire, avec échappatoire « hors répertoire » ---
const recherche = ref(libelleMetier(b.metier))
const metiersFiltres = computed(() => {
  const q = recherche.value.toLowerCase().trim()
  if (!q || q === libelleMetier(b.metier).toLowerCase()) {
    return METIERS
  }
  return METIERS.filter(m => m.label.toLowerCase().includes(q) || m.description.toLowerCase().includes(q))
})
const horsReferentiel = ref(Boolean(b.metierHorsReferentiel && !b.metier))
function passerHorsReferentiel() {
  horsReferentiel.value = true
  b.metierHorsReferentiel = recherche.value
  b.metier = null
}
function revenirAuReferentiel() {
  horsReferentiel.value = false
  b.metierHorsReferentiel = ''
}

const associeAAjouter = ref<string>()
const metiersAssociables = computed(() => METIERS.filter(m => m.value !== b.metier && !b.metiersAssocies.includes(m.value)).map(m => ({ value: m.value, label: m.label })))
function ajouterAssocie() {
  if (associeAAjouter.value) {
    b.metiersAssocies.push(associeAAjouter.value)
    associeAAjouter.value = undefined
  }
}

const motifRemplacement = computed(() => b.motif === 'vacance' || b.motif === 'remplacement')
const dateInvalide = computed(() => Boolean(b.datePriseDePoste) && b.datePriseDePoste < '2026-10-20')

const DAR_OPTIONS = [
  { value: 'oui', label: 'Oui' },
  { value: 'non', label: 'Non' },
  { value: 'nsp', label: 'Je ne sais pas encore' },
]
const DAR_STATUTS = [
  { value: 'validee', label: 'Déjà validée' },
  { value: 'en_cours', label: 'En cours de validation' },
  { value: 'a_demander', label: 'À demander' },
]
const CONTRATS = [
  { value: 'cdd', label: 'CDD' },
  { value: 'cdi', label: 'CDI' },
  { value: 'a_definir', label: 'À définir selon le profil' },
]
const QUOTITES = ['100 %', '90 %', '80 %', '50 %'].map(q => ({ value: q, label: q }))
</script>

<template>
  <StepHeader
    id="besoin"
    description="Les informations administratives qui cadrent le recrutement. Elles ne sont pas publiées telles quelles : elles alimentent l'offre, la validation et le pilotage. Seuls les champs marqués d'un astérisque sont requis pour soumettre."
  />

  <fieldset
    class="step-fields"
    :disabled="verrouille"
  >
    <FormSection
      titre="Le poste"
      description="Identification du poste et rattachement."
    >
      <Field path="besoin.intitule">
        <CspInput
          v-model="b.intitule"
          label="Intitulé du poste *"
          hint="Tel qu'il apparaîtra dans l'offre. Vous pourrez l'ajuster plus tard."
          :disabled="verrouille"
          :error="Boolean(erreur(!b.intitule, 'x')) || b.intitule.length > 120"
          :error-message="b.intitule.length > 120 ? `L'intitulé fait ${b.intitule.length} caractères : 120 maximum pour rester lisible sur les sites d'emploi.` : erreur(!b.intitule, 'Renseignez l\'intitulé du poste.')"
        />
      </Field>
      <FieldRow :cols="2">
        <Field path="besoin.organisme">
          <CspSelect
            v-model="b.organisme"
            label="Organisme recruteur"
            :hint="versant"
            :options="organismes"
            :disabled="verrouille"
          />
        </Field>
        <Field path="besoin.service">
          <CspSelect
            v-model="b.service"
            label="Service recruteur *"
            :options="services"
            :disabled="verrouille"
            :error="Boolean(erreur(!b.service, 'x'))"
            :error-message="erreur(!b.service, 'Choisissez le service qui recrute.')"
          />
        </Field>
      </FieldRow>
      <FieldRow :cols="3">
        <Field path="besoin.localisation">
          <CspInput
            v-model="b.localisation"
            label="Localisation *"
            placeholder="Ville (département)"
            :disabled="verrouille"
            :error="Boolean(erreur(!b.localisation, 'x'))"
            :error-message="erreur(!b.localisation, 'Indiquez où se situe le poste.')"
          />
        </Field>
        <Field path="besoin.quotite">
          <CspSelect
            v-model="b.quotite"
            label="Quotité"
            :options="QUOTITES"
            :disabled="verrouille"
          />
        </Field>
        <Field path="besoin.teletravail">
          <CspInput
            v-model="b.teletravail"
            label="Télétravail"
            placeholder="Ex. : 2 jours par semaine"
            :disabled="verrouille"
          />
        </Field>
      </FieldRow>

      <div class="metier">
        <Field
          v-if="!horsReferentiel"
          path="besoin.metier"
        >
          <CspCombobox
            v-model="b.metier"
            v-model:search-term="recherche"
            label="Métier du répertoire"
            hint="Recherchez par intitulé ou domaine. Sert au classement et à la diffusion sur certains canaux."
            placeholder="Ex. : énergie, ressources humaines…"
            :options="metiersFiltres"
            empty-label="Aucun métier ne correspond"
            action-label="Ce métier n'est pas dans le répertoire"
            action-icon="ri:edit-line"
            @action="passerHorsReferentiel"
          />
        </Field>
        <div
          v-else
          class="metier__libre"
        >
          <CspInput
            v-model="b.metierHorsReferentiel"
            label="Métier (hors répertoire)"
            hint="Décrivez le métier avec vos mots. Il sera signalé aux gestionnaires du répertoire (hypothèse)."
            :disabled="verrouille"
          />
          <CspButton
            label="Rechercher dans le répertoire"
            variant="tertiary-no-outline"
            size="sm"
            @click="revenirAuReferentiel"
          />
        </div>

        <div class="metier__associes">
          <p class="metier__label">
            Métiers associés <span class="muted">— facultatif, si le poste couvre plusieurs profils</span>
          </p>
          <div
            v-if="b.metiersAssocies.length"
            class="metier__tags"
          >
            <CspTag
              v-for="m in b.metiersAssocies"
              :key="m"
              variant="dismissible"
              size="sm"
              :label="libelleMetier(m)"
              :dismiss-label="`Retirer ${libelleMetier(m)}`"
              :disabled="verrouille"
              @dismiss="b.metiersAssocies = b.metiersAssocies.filter(x => x !== m)"
            />
          </div>
          <div
            v-if="!verrouille"
            class="metier__add"
          >
            <CspSelect
              v-model="associeAAjouter"
              label="Ajouter un métier associé"
              placeholder="Choisir un métier…"
              size="sm"
              :options="metiersAssociables"
            />
            <CspButton
              label="Ajouter"
              variant="secondary"
              size="sm"
              :disabled="!associeAAjouter"
              @click="ajouterAssocie"
            />
          </div>
        </div>
      </div>
    </FormSection>

    <FormSection
      titre="Le besoin"
      description="Pourquoi ce recrutement, pour quand, combien de postes."
    >
      <FieldRow :cols="2">
        <Field path="besoin.motif">
          <CspSelect
            v-model="b.motif"
            label="Motif du recrutement *"
            :options="MOTIFS"
            :disabled="verrouille"
            :error="Boolean(erreur(!b.motif, 'x'))"
            :error-message="erreur(!b.motif, 'Précisez le motif du recrutement.')"
          />
        </Field>
        <Field
          v-if="motifRemplacement"
          path="besoin.posteRemplace"
        >
          <CspInput
            v-model="b.posteRemplace"
            label="Poste ou agent remplacé"
            hint="Numéro de poste ou référence SIRH, si connu."
            :disabled="verrouille"
          />
        </Field>
        <CspTextarea
          v-else-if="b.motif"
          v-model="b.motifPrecision"
          label="Précisions sur le besoin"
          :rows="2"
          :disabled="verrouille"
        />
      </FieldRow>
      <FieldRow :cols="2">
        <Field path="besoin.datePriseDePoste">
          <CspInput
            v-model="b.datePriseDePoste"
            type="text"
            label="Prise de poste souhaitée"
            placeholder="AAAA-MM-JJ"
            :disabled="verrouille"
            :error="dateInvalide"
            :error-message="dateInvalide ? 'Cette date est déjà passée.' : undefined"
          />
        </Field>
        <Field path="besoin.nbPostes">
          <CspInput
            v-model="b.nbPostes"
            type="number"
            label="Nombre de postes"
            :disabled="verrouille"
          />
        </Field>
      </FieldRow>
    </FormSection>

    <FormSection
      titre="Catégorie et statut"
      description="Un poste peut être ouvert à plusieurs catégories et à plusieurs statuts."
    >
      <FieldRow :cols="2">
        <Field path="besoin.categories">
          <CspCheckboxGroup
            v-model="b.categories"
            label="Catégorie(s) *"
            :options="CATEGORIES"
            :disabled="verrouille"
            :error="Boolean(erreur(!b.categories.length, 'x'))"
            :error-message="erreur(!b.categories.length, 'Cochez au moins une catégorie.')"
          />
        </Field>
        <Field path="besoin.statuts">
          <CspCheckboxGroup
            v-model="b.statuts"
            label="Statut(s) ouverts *"
            :options="STATUTS"
            :disabled="verrouille"
            :error="Boolean(erreur(!b.statuts.length, 'x'))"
            :error-message="erreur(!b.statuts.length, 'Indiquez à qui le poste est ouvert.')"
          />
        </Field>
      </FieldRow>
      <Field path="besoin.corps">
        <CspInput
          v-model="b.corps"
          :label="`${libelleCorps} (facultatif)`"
          :hint="`Pour les fonctionnaires. Plusieurs ${libelleCorps.toLowerCase()}s possibles, séparés par « / ».`"
          :disabled="verrouille"
        />
      </Field>
      <div
        v-if="b.statuts.includes('contractuel')"
        class="conditional"
      >
        <p class="conditional__label">
          Pour les candidats contractuels
        </p>
        <FieldRow :cols="2">
          <CspRadioGroup
            v-model="b.typeContrat"
            label="Type de contrat proposé *"
            :options="CONTRATS"
            :disabled="verrouille"
            :error="Boolean(erreur(!b.typeContrat, 'x'))"
            :error-message="erreur(!b.typeContrat, 'Choisissez le type de contrat.')"
          />
          <CspInput
            v-if="b.typeContrat === 'cdd'"
            v-model="b.dureeContrat"
            label="Durée du contrat"
            placeholder="Ex. : 3 ans"
            :disabled="verrouille"
          />
        </FieldRow>
      </div>
    </FormSection>

    <FormSection
      titre="Validation du besoin"
      description="Selon les organisations, le recrutement doit ou non être autorisé avant publication."
    >
      <CspRadioGroup
        v-model="b.darApplicable"
        label="Ce recrutement nécessite-t-il une demande d'autorisation de recrutement (DAR) ?"
        :options="DAR_OPTIONS"
        :disabled="verrouille"
      />
      <div
        v-if="b.darApplicable === 'oui'"
        class="conditional"
      >
        <FieldRow :cols="2">
          <Field path="besoin.darRef">
            <CspInput
              v-model="b.darRef"
              label="Référence de la DAR *"
              placeholder="DAR-AAAA-0000"
              :disabled="verrouille"
              :error="Boolean(erreur(!b.darRef, 'x'))"
              :error-message="erreur(!b.darRef, 'Indiquez la référence, ou choisissez « À demander ».')"
            />
          </Field>
          <Field path="besoin.darStatut">
            <CspRadioGroup
              v-model="b.darStatut"
              label="État de la DAR"
              :options="DAR_STATUTS"
              :disabled="verrouille"
            />
          </Field>
        </FieldRow>
        <p
          v-if="b.darStatut !== 'validee'"
          class="muted"
        >
          La DAR apparaîtra comme première étape du circuit de validation : l'offre ne pourra pas être publiée avant.
        </p>
      </div>
      <CspCallout
        v-else-if="b.darApplicable === 'nsp'"
        variant="info"
        description="Pas de blocage : la responsable recrutement pourra le préciser lors de la validation."
      />
      <Field path="besoin.ficheRef">
        <CspInput
          v-model="b.ficheRef"
          label="Référence de la fiche de poste (facultatif)"
          placeholder="Ex. : FP-SECL-2024-012"
          :disabled="verrouille"
        />
      </Field>
    </FormSection>
  </fieldset>

  <StepFooter id="besoin" />
</template>

<style scoped lang="scss">
.step-fields {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  margin: 0;
  padding: 0;
  border: 0;
  min-width: 0;
}

.metier {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.metier__libre {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-2);

  > :first-child {
    width: 100%;
  }
}

.metier__label {
  margin: 0 0 var(--csp-space-2);
  font-size: var(--csp-font-size-base);
  color: var(--text-label-grey);
}

.metier__tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin-bottom: var(--csp-space-2);
}

.metier__add {
  display: flex;
  align-items: flex-end;
  gap: var(--csp-space-2);
  max-width: 32rem;

  > :first-child {
    flex: 1;
  }
}

.muted {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-regular);
  color: var(--text-mention-grey);
}

.conditional {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-4);
  border-left: 2px solid var(--border-default-blue-france);
  background: var(--background-alt-grey);
}

.conditional__label {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
}
</style>
