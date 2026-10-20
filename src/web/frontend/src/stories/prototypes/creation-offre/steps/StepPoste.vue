<script setup lang="ts">
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspSwitch from '@/components/base/CspSwitch/CspSwitch.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { personne, PERSONNES } from '../data/referentiels'
import { useOffre } from '../data/useOffre'
import Field from '../shared/Field.vue'
import FormSection from '../shared/FormSection.vue'
import ListEditor from '../shared/ListEditor.vue'
import SimulationNote from '../shared/SimulationNote.vue'
import StepFooter from '../shared/StepFooter.vue'
import StepHeader from '../shared/StepHeader.vue'

// Écran 3 — décrire le poste (fiche de poste). Contenu interne : il nourrit l'offre
// destinée aux candidats mais ne se confond pas avec elle.
const { state, verrouille, afficherErreurs, demanderContribution, simulerContribution, completerAvecFiche } = useOffre()
const ficheDisponible = computed(() => !state.besoin.ficheRef && !state.poste.missions && !verrouille.value)
const p = state.poste

const contributions = computed(() => state.contributions.filter(c => c.stepId === 'poste'))
const demande = ref(false)
const destinataire = ref('julien')
const message = ref('Compléter les compétences attendues et le profil recherché')
const destinataires = PERSONNES.filter(x => x.id !== 'camille').map(x => ({ value: x.id, label: `${x.nom} — ${x.role}` }))

function envoyer() {
  demanderContribution({ personneId: destinataire.value, stepId: 'poste', demande: message.value })
  demande.value = false
}
</script>

<template>
  <StepHeader
    id="poste"
    description="La fiche de poste décrit le poste pour l'organisation. Elle sert de matière à l'offre (étape suivante), rédigée pour les candidats : modifier ici ne change pas le texte de l'offre déjà rédigé."
  />

  <CspCallout
    v-if="ficheDisponible"
    variant="info"
    title="Une fiche de poste existe pour ce service"
    description="FP-SECL-2024-012 — Chargé·e de mission PTRE (SIRH, mai 2024). Reprenez-la pour éviter de ressaisir : seuls les champs vides seront remplis, vous pourrez tout modifier."
  >
    <CspButton
      label="Reprendre la fiche de poste"
      variant="secondary"
      size="sm"
      icon="ri:download-2-line"
      is-icon-left
      @click="completerAvecFiche"
    />
  </CspCallout>

  <section
    class="collab"
    aria-label="Contributions"
  >
    <div class="collab__head">
      <p class="collab__title">
        Besoin d'aide pour compléter ?
      </p>
      <CspButton
        v-if="!demande && !verrouille"
        label="Demander une contribution"
        variant="secondary"
        size="sm"
        icon="ri:user-shared-line"
        is-icon-left
        @click="demande = true"
      />
    </div>
    <form
      v-if="demande"
      class="collab__form"
      @submit.prevent="envoyer"
    >
      <CspSelect
        v-model="destinataire"
        label="À qui ?"
        size="sm"
        :options="destinataires"
      />
      <CspTextarea
        v-model="message"
        label="Que lui demandez-vous ?"
        :rows="2"
      />
      <div class="collab__actions">
        <CspButton
          type="submit"
          label="Envoyer la demande"
          size="sm"
          :disabled="!message.trim()"
        />
        <CspButton
          label="Annuler"
          variant="tertiary-no-outline"
          size="sm"
          @click="demande = false"
        />
      </div>
    </form>
    <ul
      v-if="contributions.length"
      class="collab__list"
    >
      <li
        v-for="c in contributions"
        :key="c.id"
        :class="{ collab__done: c.statut === 'faite' }"
      >
        <span>
          <strong>{{ personne(c.personneId).nom }}</strong> — {{ c.demande }}
          <small>{{ c.statut === 'faite' ? 'Contribution reçue' : 'En attente de réponse' }}</small>
        </span>
        <SimulationNote v-if="c.statut === 'en_attente'">
          <CspButton
            :label="`Simuler la réponse de ${personne(c.personneId).nom.split(' ')[0]}`"
            variant="tertiary"
            size="sm"
            @click="simulerContribution(c.id)"
          />
        </SimulationNote>
      </li>
    </ul>
  </section>

  <fieldset
    class="step-fields"
    :disabled="verrouille"
  >
    <FormSection
      titre="Missions et activités"
      description="Ce que fait la personne sur ce poste."
    >
      <Field path="poste.missions">
        <CspTextarea
          v-model="p.missions"
          label="Missions principales *"
          :rows="5"
          :disabled="verrouille"
          :error="afficherErreurs && !p.missions"
          error-message="Décrivez au moins les missions principales."
        />
      </Field>
      <ListEditor
        v-model="p.activites"
        label="Activités"
        path="poste.activites"
        hint="Une activité par ligne. Vous pouvez les modifier directement."
        placeholder="Ex. : Instruire les demandes de subvention"
        :disabled="verrouille"
      />
      <Field path="poste.environnement">
        <CspTextarea
          v-model="p.environnement"
          label="Environnement professionnel"
          :rows="3"
          :disabled="verrouille"
        />
      </Field>
    </FormSection>

    <FormSection
      titre="Compétences et profil"
      description="Ce que l'organisation attend. Les critères de sélection se précisent à l'étape « Conditions de candidature »."
    >
      <ListEditor
        v-model="p.competences"
        label="Compétences attendues"
        path="poste.competences"
        placeholder="Ex. : Conduite de projet partenarial"
        :disabled="verrouille"
      />
      <Field path="poste.qualifications">
        <CspTextarea
          v-model="p.qualifications"
          label="Qualifications, diplômes"
          :rows="2"
          :disabled="verrouille"
        />
      </Field>
      <Field path="poste.profil">
        <CspTextarea
          v-model="p.profil"
          label="Profil recherché"
          :rows="2"
          :disabled="verrouille"
        />
      </Field>
    </FormSection>

    <FormSection
      titre="Conditions particulières"
      facultatif
    >
      <CspSwitch
        v-model="p.aDesConditions"
        label="Le poste comporte des conditions particulières (astreintes, déplacements, horaires…)"
        :disabled="verrouille"
      />
      <Field
        v-if="p.aDesConditions"
        path="poste.conditionsParticulieres"
      >
        <CspTextarea
          v-model="p.conditionsParticulieres"
          label="Précisez"
          :rows="2"
          :disabled="verrouille"
        />
      </Field>
    </FormSection>
  </fieldset>

  <StepFooter id="poste" />
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

.collab {
  padding: var(--csp-space-3) var(--csp-space-4);
  border: 1px dashed var(--border-default-grey);
  background: var(--background-default-grey);
}

.collab__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-3);
}

.collab__title {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
}

.collab__form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin-top: var(--csp-space-3);
}

.collab__actions {
  display: flex;
  gap: var(--csp-space-2);
}

.collab__list {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: var(--csp-space-3) 0 0;
  padding: 0;
  list-style: none;
  font-size: var(--csp-font-size-sm);

  li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: var(--csp-space-3);
    padding-top: var(--csp-space-2);
    border-top: 1px solid var(--border-default-grey);
  }

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-default-warning);
  }
}

.collab__done small {
  color: var(--text-default-success);
}
</style>
