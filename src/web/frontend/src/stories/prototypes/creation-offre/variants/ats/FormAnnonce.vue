<script setup lang="ts">
import type { Fiche, Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import FieldRow from '../../shared/FieldRow.vue'
import Panel from '../../shared/Panel.vue'
import { aMettreEnForme, mettreEnForme } from './aide'
import ChampOffre from './ChampOffre.vue'
import { useNav } from './nav'
import ResumeValidation from './ResumeValidation.vue'
import { CATEGORIES, contenuDepuisFiche, db, metier, METIERS, MOTIFS_DEPART, MOTIFS_RECRUTEMENT, STATUTS_POSTE, TEMPS_TRAVAIL } from './store'
import SuiviInterne from './SuiviInterne.vue'

// Étape 1 — l'annonce : ce que lit le candidat sur Choisir le Service Public (article D311-8).
// Les informations de suivi interne (jamais publiées) sont rangées à côté des champs qu'elles complètent,
// dans des encadrés gris « Suivi interne ». Si l'organisme fait valider ses offres, un cadre
// « Résumé pour la validation » reprend en fin d'étape ce qui sert aux valideurs.
// Les champs sans mention « facultatif » sont contrôlés seulement au moment de publier.
// L'aperçu candidat et la fiche source s'ouvrent en panneau latéral, depuis le titre de l'étape.
const props = defineProps<{ offre: Offre, fiche: Fiche }>()
const { notifier } = useNav()
const o = computed(() => props.offre)

const opts = (l: string[], vide: string) => [{ value: 'aucun', label: vide }, ...l.map(v => ({ value: v, label: v }))]
function modele(cle: 'categorie' | 'statutPoste' | 'metier' | 'fondementJuridique' | 'motifRecrutement' | 'motifDepart' | 'groupeRifseep') {
  return computed({
    get: () => o.value[cle] || 'aucun',
    set: (v: string) => (o.value[cle] = v === 'aucun' ? '' : v),
  })
}
const categorie = modele('categorie')
const statutPoste = modele('statutPoste')
const fondement = modele('fondementJuridique')
const motif = modele('motifRecrutement')
const depart = modele('motifDepart')
const rifseep = modele('groupeRifseep')
const avecAgent = computed(() => ['Remplacement', 'Renouvellement'].includes(o.value.motifRecrutement))
const optsInternes = (l: string[]) => [{ value: 'aucun', label: 'Non renseigné' }, ...l.map(v => ({ value: v, label: v }))]

// Métier RMFP+ : ses compétences s'affichent déjà cochées ; on peut en retirer ou en ajouter.
const metierChoisi = computed({
  get: () => o.value.metier || 'aucun',
  set: (v: string) => {
    o.value.metier = v === 'aucun' ? '' : v
    const m = metier(o.value.metier)
    if (m) {
      o.value.competences = [...new Set([...m.competences, ...o.value.competences.filter(c => !METIERS.some(x => x.competences.includes(c)))])]
    }
  },
})
const OPTIONS_METIER = [{ value: 'aucun', label: 'Choisir un métier' }, ...METIERS.map(m => ({ value: m.id, label: `${m.libelle} — ${m.domaine}` }))]
const optionsCompetences = computed(() => [...new Set([...(metier(o.value.metier)?.competences ?? []), ...o.value.competences])].map(c => ({ value: c, label: c })))
const nouvelle = ref('')
function ajouterCompetence() {
  const c = nouvelle.value.trim()
  if (c && !o.value.competences.includes(c)) {
    o.value.competences = [...o.value.competences, c]
  }
  nouvelle.value = ''
}

const OUVERT = [{ value: 'titulaire', label: 'Fonctionnaires' }, { value: 'contractuel', label: 'Contractuels' }]
const FONDEMENTS = ['Article L332-2 (besoins permanents)', 'Article L332-8 (emplois de catégorie A)', 'Article L332-23 (accroissement temporaire)', 'Article L332-24 (contrat de projet)']

// « Repris de la fiche » tant que le texte est identique à ce que la fiche propose.
const source = computed(() => contenuDepuisFiche(props.fiche))
type CleTexte = 'titre' | 'presentation' | 'missions' | 'profil' | 'lieu'
const avecFiche = computed(() => o.value.origineContenu === 'fiche' || o.value.origineContenu === 'fichier')
function repris(cle: CleTexte) {
  return avecFiche.value && Boolean(source.value[cle]) && o.value[cle] === source.value[cle]
}
function modifie(cle: CleTexte) {
  return avecFiche.value && Boolean(source.value[cle]) && !repris(cle)
}
function restaurer(cle: CleTexte) {
  o.value[cle] = source.value[cle]
}
function formater() {
  o.value.missions = mettreEnForme(o.value.missions)
  notifier('Mise en forme appliquée : une mission par ligne. Aucun mot n\'a été changé.')
}
</script>

<template>
  <div class="redac">
    <div class="form">
      <Panel titre="Le poste">
        <ChampOffre
          :offre="o"
          champ="titre"
          label="Intitulé"
          for-id="a-titre"
          :repris="repris('titre')"
          :modifie="modifie('titre')"
          @restaurer="restaurer('titre')"
        >
          <CspInput
            id="a-titre"
            v-model="o.titre"
          />
        </ChampOffre>
        <FieldRow :cols="3">
          <CspSelect
            v-model="categorie"
            label="Catégorie"
            :options="opts(CATEGORIES.map(c => `${c}`), 'Choisir')"
          />
          <CspSelect
            v-model="statutPoste"
            label="Statut du poste"
            :options="opts(STATUTS_POSTE, 'Choisir')"
          />
          <CspInput
            v-model="o.nbPostes"
            type="number"
            label="Nombre de postes"
          />
        </FieldRow>
        <FieldRow :cols="2">
          <CspInput
            v-model="o.dateVacance"
            label="Date de vacance"
            placeholder="AAAA-MM-JJ"
          />
          <CspCheckboxGroup
            v-model="o.ouvertA"
            label="Emploi ouvert aux"
            :options="OUVERT"
          />
        </FieldRow>
        <CspSelect
          v-if="o.ouvertA.includes('contractuel')"
          v-model="fondement"
          label="Fondement juridique (emploi ouvert aux contractuels)"
          :options="opts(FONDEMENTS, 'Choisir')"
        />
        <SuiviInterne>
          <FieldRow :cols="2">
            <CspInput
              v-model="o.referenceInterne"
              label="Référence interne (facultatif)"
            />
            <CspInput
              v-model="o.codePoste"
              label="Code poste (facultatif)"
            />
          </FieldRow>
          <FieldRow :cols="2">
            <CspSelect
              v-model="motif"
              label="Motif de recrutement (facultatif)"
              :options="optsInternes(MOTIFS_RECRUTEMENT)"
            />
            <CspSelect
              v-model="depart"
              label="Motif de départ (facultatif)"
              :options="optsInternes(MOTIFS_DEPART)"
            />
          </FieldRow>
          <CspInput
            v-if="avecAgent"
            v-model="o.agentRemplace"
            label="Agent remplacé ou renouvelé (facultatif)"
          />
        </SuiviInterne>
      </Panel>

      <Panel titre="Métier et compétences">
        <ChampOffre
          :offre="o"
          champ="metier"
          label="Métier (référentiel RMFP+)"
          for-id="a-metier"
        >
          <CspSelect
            id="a-metier"
            v-model="metierChoisi"
            label="Métier"
            class="sans-label"
            :options="OPTIONS_METIER"
          />
        </ChampOffre>
        <ChampOffre
          v-if="optionsCompetences.length"
          :offre="o"
          champ="competences"
          label="Compétences (facultatif)"
        >
          <CspCheckboxGroup
            v-model="o.competences"
            label="Compétences"
            class="sans-label"
            :options="optionsCompetences"
          />
        </ChampOffre>
        <div class="ajout">
          <CspInput
            v-model="nouvelle"
            label="Ajouter une compétence hors métier"
            size="sm"
            @keydown.enter.prevent="ajouterCompetence"
          />
          <CspButton
            label="Ajouter"
            size="sm"
            variant="secondary"
            icon="ri:add-line"
            is-icon-left
            @click="ajouterCompetence"
          />
        </div>
      </Panel>

      <Panel titre="Présentation et missions">
        <CspTextarea
          v-model="o.descriptifEmployeur"
          label="Descriptif de l'employeur (facultatif)"
          :rows="2"
        />
        <ChampOffre
          :offre="o"
          champ="presentation"
          label="Descriptif du service (facultatif)"
          for-id="a-presentation"
          :repris="repris('presentation')"
          :modifie="modifie('presentation')"
          @restaurer="restaurer('presentation')"
        >
          <CspTextarea
            id="a-presentation"
            v-model="o.presentation"
            :rows="3"
          />
        </ChampOffre>
        <ChampOffre
          :offre="o"
          champ="missions"
          label="Missions"
          for-id="a-missions"
          :repris="repris('missions')"
          :modifie="modifie('missions')"
          @restaurer="restaurer('missions')"
        >
          <CspTextarea
            id="a-missions"
            v-model="o.missions"
            :rows="6"
          />
        </ChampOffre>
        <div
          v-if="aMettreEnForme(o.missions)"
          class="outil"
        >
          <CspButton
            label="Mettre en forme (une mission par ligne)"
            variant="tertiary-no-outline"
            size="sm"
            icon="ri:list-unordered"
            is-icon-left
            @click="formater"
          />
        </div>
        <ChampOffre
          :offre="o"
          champ="profil"
          label="Profil recherché"
          for-id="a-profil"
          :repris="repris('profil')"
          :modifie="modifie('profil')"
          @restaurer="restaurer('profil')"
        >
          <CspTextarea
            id="a-profil"
            v-model="o.profil"
            :rows="3"
          />
        </ChampOffre>
      </Panel>

      <Panel titre="Conditions d'exercice">
        <CspRadioGroup
          v-model="o.tempsTravail"
          label="Temps de travail"
          :options="TEMPS_TRAVAIL"
        />
        <ChampOffre
          :offre="o"
          champ="conditions"
          label="Conditions particulières (facultatif)"
          for-id="a-conditions"
        >
          <CspTextarea
            id="a-conditions"
            v-model="o.conditions"
            :rows="2"
          />
        </ChampOffre>
        <FieldRow :cols="2">
          <ChampOffre
            :offre="o"
            champ="lieu"
            label="Lieu"
            for-id="a-lieu"
            :repris="repris('lieu')"
          >
            <CspInput
              id="a-lieu"
              v-model="o.lieu"
              placeholder="Ville, ou « Pas de lieu fixe »"
            />
          </ChampOffre>
          <ChampOffre
            :offre="o"
            champ="remuneration"
            label="Rémunération (facultatif)"
            for-id="a-remu"
          >
            <CspInput
              id="a-remu"
              v-model="o.remuneration"
              placeholder="Ex. : selon expérience, grille indiciaire"
            />
          </ChampOffre>
        </FieldRow>
        <FieldRow :cols="2">
          <CspInput
            v-model="o.teletravail"
            label="Télétravail (facultatif)"
          />
          <CspInput
            v-model="o.contact"
            label="Contact (facultatif)"
          />
        </FieldRow>
        <SuiviInterne>
          <FieldRow :cols="2">
            <CspSelect
              v-model="rifseep"
              label="Groupe RIFSEEP (facultatif)"
              :options="optsInternes(['Groupe 1', 'Groupe 2', 'Groupe 3', 'Groupe 4'])"
            />
            <ChampOffre
              :offre="o"
              champ="cycleTravail"
              label="Cycle de travail (facultatif)"
              for-id="a-cycle"
            >
              <CspInput
                id="a-cycle"
                v-model="o.cycleTravail"
                placeholder="Ex. : 38 h 30 sur 5 jours"
              />
            </ChampOffre>
          </FieldRow>
        </SuiviInterne>
      </Panel>

      <ResumeValidation
        v-if="db.organisme.validationActive"
        :offre="o"
        :fiche="fiche"
        editable
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.redac {
  max-width: 60rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  min-width: 0;
}

.sans-label :deep(.csp-select-group__label),
.sans-label :deep(legend) {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}

.ajout {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--csp-space-3);
  align-items: end;
}

.outil {
  margin: calc(-1 * var(--csp-space-3)) 0 0 calc(-1 * var(--csp-space-2));
}
</style>
