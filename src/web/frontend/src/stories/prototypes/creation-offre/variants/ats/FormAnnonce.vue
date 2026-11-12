<script setup lang="ts">
import type { Fiche, Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import FieldRow from '../../shared/FieldRow.vue'
import { aMettreEnForme, mettreEnForme } from './aide'
import ChampOffre from './ChampOffre.vue'
import { useNav } from './nav'
import { CATEGORIES, contenuDepuisFiche, db, metier, METIERS, MOTIFS_DEPART, MOTIFS_RECRUTEMENT, STATUTS_POSTE, TEMPS_TRAVAIL, VERSANTS } from './store'
import SuiviInterne from './SuiviInterne.vue'

// Section « Annonce » de la page de l'offre : ce que lit le candidat sur Choisir le Service Public (D311-8).
// Groupes : titre · Le poste · L'organisme · Le rôle · Profil recherché. Le suivi interne (jamais publié)
// est dans un encadré gris du bloc « Le poste ». Le résumé pour la validation est en haut de la page.
// Les champs sans mention « facultatif » sont contrôlés seulement au moment de publier.
const props = defineProps<{ offre: Offre, fiche?: Fiche }>()
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
const temps = computed({ get: () => o.value.tempsTravail || 'aucun', set: (v: string) => (o.value.tempsTravail = v === 'aucun' ? '' : v) })
const OPTIONS_TEMPS = [{ value: 'aucun', label: 'Choisir' }, ...TEMPS_TRAVAIL]
const rifseep = modele('groupeRifseep')
// Champs facultatifs à liste : « aucun » = non renseigné.
function choix(cle: 'versant' | 'natureContrat' | 'niveauExperience' | 'niveauEtudes' | 'management') {
  return computed({
    get: () => o.value[cle] || 'aucun',
    set: (v: string) => (o.value[cle] = v === 'aucun' ? '' : v),
  })
}
const versant = choix('versant')
const natureContrat = choix('natureContrat')
const experience = choix('niveauExperience')
const etudes = choix('niveauEtudes')
const management = choix('management')
const OPTIONS_VERSANT = VERSANTS.map(v => ({ value: v, label: v }))
const CONTRATS = ['Contrat à durée déterminée (CDD)', 'Contrat à durée indéterminée (CDI)', 'Contrat de projet']
const EXPERIENCES = ['Débutant accepté', 'Confirmé (2 à 5 ans)', 'Expert (plus de 5 ans)']
const ETUDES = ['Sans diplôme', 'CAP, BEP', 'Baccalauréat', 'Bac + 2', 'Bac + 3', 'Bac + 5 et plus']
const MANAGEMENT = ['Pas d\'encadrement', 'Encadrement d\'une équipe', 'Encadrement de plusieurs équipes']
const contractuels = computed(() => o.value.ouvertA.includes('contractuel'))
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
const source = computed(() => (props.fiche ? contenuDepuisFiche(props.fiche) : undefined))
type CleTexte = 'titre' | 'presentation' | 'missions' | 'profil' | 'lieu'
const avecFiche = computed(() => Boolean(props.fiche) && (o.value.origineContenu === 'fiche' || o.value.origineContenu === 'fichier'))
function repris(cle: CleTexte) {
  return avecFiche.value && Boolean(source.value?.[cle]) && o.value[cle] === source.value?.[cle]
}
function modifie(cle: CleTexte) {
  return avecFiche.value && Boolean(source.value?.[cle]) && !repris(cle)
}
function restaurer(cle: CleTexte) {
  o.value[cle] = source.value?.[cle] ?? o.value[cle]
}
function formater() {
  o.value.missions = mettreEnForme(o.value.missions)
  notifier('Mise en forme appliquée : une mission par ligne. Aucun mot n\'a été changé.')
}
</script>

<template>
  <div class="annonce">
    <div class="groupe">
      <FieldRow :cols="2">
        <CspInput
          :model-value="db.organisme.nom"
          label="Organisme"
          disabled
        />
        <CspSelect
          v-model="versant"
          label="Versant"
          :options="OPTIONS_VERSANT"
        />
      </FieldRow>
      <ChampOffre
        :offre="o"
        champ="titre"
        label="Titre de l'offre"
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
    </div>

    <div class="groupe">
      <h3 class="groupe__titre">
        Le poste
      </h3>
      <FieldRow :cols="2">
        <CspInput
          v-model="o.nbPostes"
          type="number"
          label="Nombre de postes (facultatif)"
        />
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
      </FieldRow>
      <FieldRow :cols="2">
        <CspCheckboxGroup
          v-model="o.ouvertA"
          label="Nature de l'emploi : ouvert aux"
          :options="OUVERT"
        />
        <CspSelect
          v-model="categorie"
          label="Catégorie"
          :options="opts(CATEGORIES.map(c => `${c}`), 'Choisir')"
        />
      </FieldRow>
      <FieldRow
        v-if="contractuels"
        :cols="2"
      >
        <CspSelect
          v-model="fondement"
          label="Fondement juridique"
          :options="opts(FONDEMENTS, 'Choisir')"
        />
        <CspSelect
          v-model="natureContrat"
          label="Nature du contrat (facultatif)"
          :options="opts(CONTRATS, 'Non renseigné')"
        />
      </FieldRow>
      <FieldRow :cols="2">
        <CspSelect
          v-model="statutPoste"
          label="Statut du poste"
          :options="opts(STATUTS_POSTE, 'Choisir')"
        />
        <CspInput
          v-model="o.dateVacance"
          label="Date de vacance"
          placeholder="AAAA-MM-JJ"
        />
      </FieldRow>
      <FieldRow :cols="2">
        <CspInput
          v-model="o.corps"
          label="Corps (facultatif)"
          placeholder="Ex. : attachés d'administration de l'État"
        />
        <CspInput
          v-model="o.grade"
          label="Grade (facultatif)"
        />
      </FieldRow>
      <FieldRow :cols="3">
        <CspSelect
          v-model="temps"
          label="Temps de travail"
          :options="OPTIONS_TEMPS"
        />
        <CspInput
          v-model="o.teletravail"
          label="Télétravail (facultatif)"
          placeholder="Ex. : 2 jours par semaine"
        />
        <CspSelect
          v-model="management"
          label="Management (facultatif)"
          :options="opts(MANAGEMENT, 'Non renseigné')"
        />
      </FieldRow>
      <FieldRow :cols="2">
        <ChampOffre
          :offre="o"
          champ="remuneration"
          label="Rémunération des fonctionnaires (facultatif)"
          for-id="a-remu"
        >
          <CspInput
            id="a-remu"
            v-model="o.remuneration"
            placeholder="Ex. : grille indiciaire, selon expérience"
          />
        </ChampOffre>
        <CspInput
          v-if="contractuels"
          v-model="o.remunerationContractuels"
          label="Rémunération des contractuels (facultatif)"
          placeholder="Ex. : 2 600 à 3 200 € brut mensuel"
        />
      </FieldRow>
      <ChampOffre
        :offre="o"
        champ="conditions"
        label="Conditions particulières d'exercice (facultatif)"
        for-id="a-conditions"
      >
        <CspTextarea
          id="a-conditions"
          v-model="o.conditions"
          :rows="2"
        />
      </ChampOffre>

      <SuiviInterne>
        <FieldRow :cols="2">
          <CspInput
            v-model="o.referenceInterne"
            label="Référence interne (facultatif)"
          />
          <CspInput
            v-model="o.referenceFranceTravail"
            label="Référence France Travail (facultatif)"
          />
        </FieldRow>
        <FieldRow :cols="2">
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
    </div>

    <div class="groupe">
      <h3 class="groupe__titre">
        L'organisme
      </h3>
      <CspTextarea
        v-model="o.descriptifEmployeur"
        label="Description de l'employeur (facultatif)"
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
    </div>

    <div class="groupe">
      <h3 class="groupe__titre">
        Le rôle
      </h3>
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
    </div>

    <div class="groupe">
      <h3 class="groupe__titre">
        Profil recherché
      </h3>
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
          label="Ajouter une compétence"
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
      <ChampOffre
        :offre="o"
        champ="profil"
        label="Expérience et diplômes attendus"
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
      <FieldRow :cols="3">
        <CspSelect
          v-model="experience"
          label="Niveau d'expérience (facultatif)"
          :options="opts(EXPERIENCES, 'Non renseigné')"
        />
        <CspSelect
          v-model="etudes"
          label="Niveau d'études (facultatif)"
          :options="opts(ETUDES, 'Non renseigné')"
        />
        <CspInput
          v-model="o.langues"
          label="Langues (facultatif)"
          placeholder="Ex. : anglais, niveau B2"
        />
      </FieldRow>
    </div>

    <div class="groupe">
      <h3 class="groupe__titre">
        Informations complémentaires
      </h3>
      <CspTextarea
        v-model="o.infosComplementaires"
        label="Informations complémentaires (facultatif)"
        hint="Ex. : accessibilité du poste aux personnes en situation de handicap, avantages sociaux."
        :rows="2"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.annonce {
  display: flex;
  flex-direction: column;
  max-width: 60rem;
}

.groupe {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  min-width: 0;

  & + & {
    margin-top: var(--csp-space-8, 2.5rem);
    padding-top: var(--csp-space-6);
    border-top: 1px solid var(--border-default-grey);
  }
}

.groupe__titre {
  margin: 0;
  font-size: 1.125rem;
  font-weight: var(--csp-font-weight-bold);
  line-height: 1.4;
  color: var(--text-title-grey);
}

.mention {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
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
