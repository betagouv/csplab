<script setup lang="ts">
import type { Preset } from '../../data/scenario'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspCombobox from '@/components/base/CspCombobox/CspCombobox.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspSwitch from '@/components/base/CspSwitch/CspSwitch.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { CATEGORIES, libelleMetier, METIERS, MOTIFS, ORGANISMES, personne, SERVICES, STATUTS, versantDe } from '../../data/referentiels'
import { FICHES } from '../../data/scenario'
import { useOffre } from '../../data/useOffre'
import Disclosure from '../../shared/Disclosure.vue'
import Field from '../../shared/Field.vue'
import FieldRow from '../../shared/FieldRow.vue'
import ListEditor from '../../shared/ListEditor.vue'
import Panel from '../../shared/Panel.vue'
import SimulationNote from '../../shared/SimulationNote.vue'
import EtapeFooter from './EtapeFooter.vue'
import RemarquesSection from './RemarquesSection.vue'
import SourcePanel from './SourcePanel.vue'

// Étape 1 — définir le poste. L'essentiel d'abord ; la fiche de poste et les compléments
// sont repliés, et les champs conditionnels n'apparaissent que si la situation les rend utiles.
const emit = defineEmits<{ reprendre: [preset: Preset] }>()

const { state, verrouille, afficherErreurs, demanderContribution, simulerContribution, completerAvecFiche } = useOffre()
const b = state.besoin
const p = state.poste

const err = (vide: boolean, message: string) => (afficherErreurs.value && vide ? message : undefined)

const organismes = ORGANISMES.map(o => ({ value: o.value, label: o.label }))
const services = computed(() => (SERVICES[b.organisme] ?? []).map(s => ({ value: s, label: s })))
const territoriale = computed(() => versantDe(b.organisme).includes('territoriale'))

// --- DAR : uniquement si l'organisation en utilise (paramétrage), jamais comme question réglementaire ---
const organisationAvecDar = computed(() => state.organisation === 'avec_dar')
const darObtenue = computed(() => b.darStatut === 'validee' && Boolean(b.darRef))
watch(() => b.darRef, (ref) => {
  if (darObtenue.value) {
    return
  }
  b.darApplicable = ref.trim() ? 'oui' : 'nsp'
  b.darStatut = ref.trim() ? 'en_cours' : ''
})

// --- Fiche de poste ---
const ficheOuverte = ref(Boolean(p.missions) && state.statut === 'a_corriger')
const ficheDispo = computed(() => !p.missions && !b.ficheRef && !verrouille.value)
const resumeFiche = computed(() => {
  if (!p.missions && !p.competences.length) {
    return 'Non renseignée. Elle facilite la rédaction de l\'offre et des critères.'
  }
  const src = state.origines['poste.missions']
  return `${p.activites.length} activité(s), ${p.competences.length} compétence(s)${src ? ' · reprise de la fiche de poste' : ''}`
})
const contributions = computed(() => state.contributions.filter(c => c.stepId === 'poste'))
function demanderAuManager() {
  demanderContribution({ personneId: 'julien', stepId: 'poste', demande: 'Compléter les missions et les compétences attendues' })
}

// --- Compléments ---
const complementsOuverts = ref(false)
const recherche = ref(libelleMetier(b.metier))
const metiersFiltres = computed(() => {
  const q = recherche.value.toLowerCase().trim()
  if (!q || q === libelleMetier(b.metier).toLowerCase()) {
    return METIERS
  }
  return METIERS.filter(m => m.label.toLowerCase().includes(q) || m.description.toLowerCase().includes(q))
})
const horsRepertoire = ref(Boolean(b.metierHorsReferentiel && !b.metier))
function passerHorsRepertoire() {
  horsRepertoire.value = true
  b.metierHorsReferentiel = recherche.value
  b.metier = null
}
const resumeComplements = computed(() => {
  const faits = [
    (b.metier || b.metierHorsReferentiel) && 'métier',
    b.motif && 'motif',
    b.datePriseDePoste && 'prise de poste',
    b.corps && (territoriale.value ? 'cadre d\'emplois' : 'corps'),
  ].filter(Boolean)
  return faits.length ? `Renseigné : ${faits.join(', ')}` : 'Métier du répertoire, motif, date de prise de poste, quotité…'
})

const CONTRATS = [
  { value: 'cdd', label: 'CDD' },
  { value: 'cdi', label: 'CDI' },
  { value: 'a_definir', label: 'Selon le profil' },
]
const QUOTITES = ['100 %', '90 %', '80 %', '50 %'].map(q => ({ value: q, label: q }))
const intituleTropLong = computed(() => b.intitule.length > 120)
</script>

<template>
  <header class="head">
    <h2 class="head__title">
      Définir le poste
    </h2>
  </header>

  <SourcePanel @reprendre="pr => emit('reprendre', pr)" />
  <RemarquesSection :step-ids="['besoin', 'poste']" />

  <fieldset
    class="fields"
    :disabled="verrouille"
  >
    <Panel
      titre="Le poste"
      description="Ces informations suffisent pour avancer. Le reste est facultatif et regroupé plus bas."
    >
      <Field
        id="champ-intitule"
        path="besoin.intitule"
      >
        <CspInput
          v-model="b.intitule"
          label="Intitulé du poste"
          :disabled="verrouille"
          :error="intituleTropLong || Boolean(err(!b.intitule, 'x'))"
          :error-message="intituleTropLong ? `${b.intitule.length} caractères : raccourcissez à 120 au maximum pour rester lisible sur les sites d'emploi.` : err(!b.intitule, 'Indiquez l\'intitulé du poste.')"
        />
      </Field>
      <FieldRow :cols="2">
        <Field path="besoin.organisme">
          <CspSelect
            v-model="b.organisme"
            label="Organisme"
            :options="organismes"
            :disabled="verrouille"
          />
        </Field>
        <Field
          id="champ-service"
          path="besoin.service"
        >
          <CspSelect
            v-model="b.service"
            label="Service"
            :options="services"
            :disabled="verrouille"
            :error="Boolean(err(!b.service, 'x'))"
            :error-message="err(!b.service, 'Choisissez le service qui recrute.')"
          />
        </Field>
      </FieldRow>
      <FieldRow :cols="2">
        <Field
          id="champ-localisation"
          path="besoin.localisation"
        >
          <CspInput
            v-model="b.localisation"
            label="Localisation"
            placeholder="Ville (département)"
            :disabled="verrouille"
            :error="Boolean(err(!b.localisation, 'x'))"
            :error-message="err(!b.localisation, 'Indiquez où se situe le poste.')"
          />
        </Field>
        <Field path="besoin.teletravail">
          <CspInput
            v-model="b.teletravail"
            label="Télétravail (facultatif)"
            placeholder="Ex. : 2 jours par semaine"
            :disabled="verrouille"
          />
        </Field>
      </FieldRow>
      <FieldRow :cols="2">
        <Field
          id="champ-categories"
          path="besoin.categories"
        >
          <CspCheckboxGroup
            v-model="b.categories"
            label="Catégorie(s)"
            :options="CATEGORIES"
            :disabled="verrouille"
            :error="Boolean(err(!b.categories.length, 'x'))"
            :error-message="err(!b.categories.length, 'Cochez au moins une catégorie.')"
          />
        </Field>
        <Field
          id="champ-statuts"
          path="besoin.statuts"
        >
          <CspCheckboxGroup
            v-model="b.statuts"
            label="Ouvert aux"
            :options="STATUTS"
            :disabled="verrouille"
            :error="Boolean(err(!b.statuts.length, 'x'))"
            :error-message="err(!b.statuts.length, 'Indiquez à qui le poste est ouvert.')"
          />
        </Field>
      </FieldRow>

      <FieldRow
        v-if="b.statuts.includes('contractuel')"
        id="champ-contrat"
        :cols="2"
        class="conditional"
      >
        <CspRadioGroup
          v-model="b.typeContrat"
          label="Contrat proposé aux contractuels"
          :options="CONTRATS"
          :disabled="verrouille"
          :error="Boolean(err(!b.typeContrat, 'x'))"
          :error-message="err(!b.typeContrat, 'Choisissez le type de contrat.')"
        />
        <CspInput
          v-if="b.typeContrat === 'cdd'"
          v-model="b.dureeContrat"
          label="Durée (facultatif)"
          placeholder="Ex. : 3 ans"
          :disabled="verrouille"
        />
      </FieldRow>

      <template v-if="organisationAvecDar">
        <p
          v-if="darObtenue"
          class="dar-line"
        >
          Autorisation de recrutement : <strong>{{ b.darRef }}</strong>, validée le 2 octobre 2026.
        </p>
        <Field
          v-else
          path="besoin.darRef"
          class="dar-field"
        >
          <CspInput
            v-model="b.darRef"
            label="Référence de la DAR (si votre recrutement en nécessite une)"
            placeholder="DAR-AAAA-0000"
            :disabled="verrouille"
          />
        </Field>
      </template>
    </Panel>

    <Panel>
      <Disclosure
        v-model:ouvert="ficheOuverte"
        titre="Fiche de poste"
        :resume="resumeFiche"
        icon="ri:lock-line"
        facultatif
      >
        <p class="hint">
          Usage interne, non publiée. Elle sert de matière à l'offre : la modifier ne change pas le texte déjà rédigé pour les candidats.
        </p>
        <div
          v-if="ficheDispo || !verrouille"
          class="fiche-actions"
        >
          <CspButton
            v-if="ficheDispo"
            :label="`Reprendre la fiche ${FICHES[0]!.id}`"
            variant="secondary"
            size="sm"
            icon="ri:download-2-line"
            is-icon-left
            @click="completerAvecFiche"
          />
          <CspButton
            v-if="!contributions.length && !verrouille"
            :label="`Demander à ${personne('julien').nom} de compléter`"
            variant="tertiary-no-outline"
            size="sm"
            icon="ri:user-shared-line"
            is-icon-left
            @click="demanderAuManager"
          />
        </div>
        <div
          v-for="c in contributions"
          :key="c.id"
          class="contrib"
        >
          <span>{{ personne(c.personneId).nom }} — {{ c.statut === 'faite' ? 'a complété la fiche' : 'demande envoyée, en attente' }}</span>
          <SimulationNote v-if="c.statut === 'en_attente'">
            <CspButton
              label="Simuler sa réponse"
              size="sm"
              variant="tertiary"
              @click="simulerContribution(c.id)"
            />
          </SimulationNote>
        </div>
        <Field path="poste.missions">
          <CspTextarea
            v-model="p.missions"
            label="Missions principales"
            :rows="4"
            :disabled="verrouille"
          />
        </Field>
        <ListEditor
          v-model="p.activites"
          label="Activités"
          path="poste.activites"
          placeholder="Ex. : Instruire les demandes de subvention"
          :disabled="verrouille"
        />
        <ListEditor
          v-model="p.competences"
          label="Compétences attendues"
          path="poste.competences"
          placeholder="Ex. : Conduite de projet partenarial"
          :disabled="verrouille"
        />
        <FieldRow :cols="2">
          <Field path="poste.environnement">
            <CspTextarea
              v-model="p.environnement"
              label="Environnement de travail"
              :rows="3"
              :disabled="verrouille"
            />
          </Field>
          <Field path="poste.qualifications">
            <CspTextarea
              v-model="p.qualifications"
              label="Diplômes, qualifications"
              :rows="3"
              :disabled="verrouille"
            />
          </Field>
        </FieldRow>
        <CspSwitch
          v-model="p.aDesConditions"
          label="Conditions particulières (astreintes, déplacements…)"
          :disabled="verrouille"
        />
        <CspTextarea
          v-if="p.aDesConditions"
          v-model="p.conditionsParticulieres"
          label="Précisez"
          :rows="2"
          :disabled="verrouille"
        />
      </Disclosure>

      <Disclosure
        v-model:ouvert="complementsOuverts"
        titre="Informations complémentaires"
        :resume="resumeComplements"
        icon="ri:list-settings-line"
        facultatif
      >
        <Field
          v-if="!horsRepertoire"
          path="besoin.metier"
        >
          <CspCombobox
            v-model="b.metier"
            v-model:search-term="recherche"
            label="Métier du répertoire"
            hint="Sert au classement et à certains canaux de diffusion."
            placeholder="Ex. : énergie, ressources humaines…"
            :options="metiersFiltres"
            empty-label="Aucun métier ne correspond"
            action-label="Le métier n'est pas dans le répertoire"
            action-icon="ri:edit-line"
            @action="passerHorsRepertoire"
          />
        </Field>
        <div
          v-else
          class="libre"
        >
          <CspInput
            v-model="b.metierHorsReferentiel"
            label="Métier (hors répertoire)"
            :disabled="verrouille"
          />
          <CspButton
            label="Rechercher dans le répertoire"
            variant="tertiary-no-outline"
            size="sm"
            @click="horsRepertoire = false; b.metierHorsReferentiel = ''"
          />
        </div>
        <FieldRow :cols="2">
          <Field path="besoin.motif">
            <CspSelect
              v-model="b.motif"
              label="Motif du recrutement"
              :options="MOTIFS"
              :disabled="verrouille"
            />
          </Field>
          <Field
            v-if="b.motif === 'vacance' || b.motif === 'remplacement'"
            path="besoin.posteRemplace"
          >
            <CspInput
              v-model="b.posteRemplace"
              label="Poste remplacé"
              :disabled="verrouille"
            />
          </Field>
        </FieldRow>
        <FieldRow :cols="3">
          <Field path="besoin.datePriseDePoste">
            <CspInput
              v-model="b.datePriseDePoste"
              label="Prise de poste"
              placeholder="AAAA-MM-JJ"
              :disabled="verrouille"
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
          <Field path="besoin.nbPostes">
            <CspInput
              v-model="b.nbPostes"
              type="number"
              label="Nombre de postes"
              :disabled="verrouille"
            />
          </Field>
        </FieldRow>
        <Field path="besoin.corps">
          <CspInput
            v-model="b.corps"
            :label="territoriale ? 'Cadre(s) d\'emplois' : 'Corps'"
            hint="Plusieurs possibles, séparés par « / »."
            :disabled="verrouille"
          />
        </Field>
      </Disclosure>
    </Panel>
  </fieldset>

  <EtapeFooter />
</template>

<style scoped lang="scss">
.head__title {
  margin: 0;
  font-size: var(--csp-font-size-2xl);
}

.fields {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  margin: 0;
  padding: 0;
  border: 0;
  min-width: 0;
}

.conditional {
  padding-left: var(--csp-space-4);
  border-left: 2px solid var(--border-default-blue-france);
}

.dar-line {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.dar-field {
  max-width: 28rem;
}

.hint {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.fiche-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
}

.contrib {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-3);
  font-size: var(--csp-font-size-sm);
}

.libre {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-2);

  > :first-child {
    width: 100%;
  }
}
</style>
