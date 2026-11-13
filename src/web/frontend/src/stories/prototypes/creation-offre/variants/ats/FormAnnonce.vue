<script setup lang="ts">
import type { Fiche, Offre } from './store'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import FieldRow from '../../shared/FieldRow.vue'
import { aMettreEnForme, mettreEnForme } from './aide'
import ChampOffre from './ChampOffre.vue'
import ChampSimple from './ChampSimple.vue'
import { useNav } from './nav'
import { CATEGORIES, contenuDepuisFiche, db, metier, METIERS, STATUTS_POSTE, TEMPS_TRAVAIL, VERSANTS } from './store'

// Section « Annonce » de la page de l'offre : ce que lit le candidat sur Choisir le Service Public (D311-8).
// Groupes : titre · Le poste · L'organisme · Le rôle · Profil recherché. Les informations internes (jamais
// publiées) sont dans leur propre section (FormInterne). Le résumé pour la validation est en haut de la page.
// Seuls les champs obligatoires portent une mention (« Champ obligatoire », aide grise DSFR) ; ils ne sont
// contrôlés qu'au moment de publier. Les aides vont sous le champ (message d'information) ou en exemple dans le champ.
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
const temps = computed({ get: () => o.value.tempsTravail || 'aucun', set: (v: string) => (o.value.tempsTravail = v === 'aucun' ? '' : v) })
const OPTIONS_TEMPS = [{ value: 'aucun', label: 'Choisir' }, ...TEMPS_TRAVAIL]
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

// Métier RMFP+ (à gauche) : ses compétences s'affichent à droite, déjà cochées ; on peut en décocher.
// Pas d'ajout manuel : les compétences viennent du référentiel.
const metierChoisi = computed({
  get: () => o.value.metier || 'aucun',
  set: (v: string) => {
    o.value.metier = v === 'aucun' ? '' : v
    o.value.competences = [...(metier(o.value.metier)?.competences ?? [])]
  },
})
const OPTIONS_METIER = [{ value: 'aucun', label: 'Choisir un métier' }, ...METIERS.map(m => ({ value: m.id, label: `${m.libelle} — ${m.domaine}` }))]
const optionsCompetences = computed(() => (metier(o.value.metier)?.competences ?? []).map(c => ({ value: c, label: c })))

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
    <p class="note">
      Les champs obligatoires ne sont contrôlés qu'au moment de publier : vous pouvez enregistrer une annonce incomplète.
    </p>
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
        hint="Champ obligatoire"
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
          label="Nombre de postes"
        />
        <ChampOffre
          :offre="o"
          champ="lieu"
          label="Lieu"
          hint="Champ obligatoire"
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
          hint="Champ obligatoire"
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
          hint="Champ obligatoire"
          :options="opts(FONDEMENTS, 'Choisir')"
        />
        <CspSelect
          v-model="natureContrat"
          label="Nature du contrat"
          :options="opts(CONTRATS, 'Non renseigné')"
        />
      </FieldRow>
      <FieldRow :cols="2">
        <CspSelect
          v-model="statutPoste"
          label="Statut du poste"
          hint="Champ obligatoire"
          :options="opts(STATUTS_POSTE, 'Choisir')"
        />
        <CspInput
          v-model="o.dateVacance"
          label="Date de vacance"
          hint="Champ obligatoire"
          placeholder="AAAA-MM-JJ"
        />
      </FieldRow>
      <FieldRow :cols="2">
        <CspInput
          v-model="o.corps"
          label="Corps"
          placeholder="Ex. : attachés d'administration de l'État"
        />
        <CspInput
          v-model="o.grade"
          label="Grade"
        />
      </FieldRow>
      <FieldRow :cols="3">
        <CspSelect
          v-model="temps"
          label="Temps de travail"
          hint="Champ obligatoire"
          :options="OPTIONS_TEMPS"
        />
        <CspInput
          v-model="o.teletravail"
          label="Télétravail"
          placeholder="Ex. : 2 jours par semaine"
        />
        <CspSelect
          v-model="management"
          label="Management"
          :options="opts(MANAGEMENT, 'Non renseigné')"
        />
      </FieldRow>
      <FieldRow :cols="2">
        <ChampOffre
          :offre="o"
          champ="remuneration"
          label="Rémunération des fonctionnaires"
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
          label="Rémunération des contractuels"
          placeholder="Ex. : 2 600 à 3 200 € brut mensuel"
        />
      </FieldRow>
      <ChampOffre
        :offre="o"
        champ="conditions"
        label="Conditions particulières d'exercice"
        for-id="a-conditions"
      >
        <CspTextarea
          id="a-conditions"
          v-model="o.conditions"
          :rows="2"
        />
      </ChampOffre>
    </div>

    <div class="groupe">
      <h3 class="groupe__titre">
        L'organisme
      </h3>
      <ChampSimple
        label="Description de l'employeur"
      >
        <CspTextarea
          v-model="o.descriptifEmployeur"
          label="Description de l'employeur"
          :rows="2"
        />
      </ChampSimple>
      <ChampOffre
        :offre="o"
        champ="presentation"
        label="Descriptif du service"
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
        hint="Champ obligatoire"
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
      <div class="metier">
        <ChampOffre
          :offre="o"
          champ="metier"
          label="Métier (référentiel RMFP+)"
          hint="Champ obligatoire"
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
          :offre="o"
          champ="competences"
          label="Compétences du métier"
        >
          <CspCheckboxGroup
            v-if="optionsCompetences.length"
            v-model="o.competences"
            label="Compétences"
            class="sans-label"
            :options="optionsCompetences"
          />
          <p
            v-else
            class="metier__vide"
          >
            Choisissez un métier pour afficher ses compétences du RMFP+.
          </p>
        </ChampOffre>
      </div>
      <ChampOffre
        :offre="o"
        champ="profil"
        label="Expérience et diplômes attendus"
        hint="Champ obligatoire"
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
          label="Niveau d'expérience"
          :options="opts(EXPERIENCES, 'Non renseigné')"
        />
        <CspSelect
          v-model="etudes"
          label="Niveau d'études"
          :options="opts(ETUDES, 'Non renseigné')"
        />
        <CspInput
          v-model="o.langues"
          label="Langues"
          placeholder="Ex. : anglais, niveau B2"
        />
      </FieldRow>
    </div>

    <div class="groupe">
      <h3 class="groupe__titre">
        Informations complémentaires
      </h3>
      <ChampSimple
        label="Informations complémentaires"
      >
        <CspTextarea
          v-model="o.infosComplementaires"
          label="Informations complémentaires"
          placeholder="Ex. : accessibilité du poste aux personnes en situation de handicap, avantages sociaux."
          :rows="2"
        />
      </ChampSimple>
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

.note {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.metier {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: var(--csp-space-6);
  align-items: start;
}

.metier__vide {
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-alt-grey);
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.outil {
  margin: calc(-1 * var(--csp-space-3)) 0 0 calc(-1 * var(--csp-space-2));
}
</style>
