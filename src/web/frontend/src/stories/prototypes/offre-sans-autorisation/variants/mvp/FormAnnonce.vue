<script setup lang="ts">
import type { Fiche, Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
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
// lectureSeule : la note sur les champs obligatoires ne concerne que la personne qui rédige.
const props = defineProps<{ offre: Offre, fiche?: Fiche, lectureSeule?: boolean }>()
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
const contractuels = computed(() => o.value.ouvertA.includes('contractuel'))

// Champs du tableau de la PO (« Création manuelle des offres ») absents jusque-là.
const DIPLOMES_ETAT = ['Infirmier', 'Assistant de service social', 'Éducateur spécialisé', 'Masseur-kinésithérapeute', 'Sage-femme', 'Psychomotricien', 'Ergothérapeute', 'Manipulateur en électroradiologie médicale']
const SPECIALISATIONS = ['Administration générale', 'Droit public', 'Finances publiques', 'Ressources humaines', 'Numérique', 'Environnement', 'Urbanisme', 'Santé', 'Social']
const NIVEAUX_LANGUE = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'Langue maternelle']
const diplome = choixLibre('diplomeEtat')
const specialisation = choixLibre('specialisation')
function choixLibre(cle: 'diplomeEtat' | 'specialisation') {
  return computed({
    get: () => o.value[cle] || 'aucun',
    set: (v: string) => (o.value[cle] = v === 'aucun' ? '' : v),
  })
}
// Télétravail : liste oui / non.
const teletravail = computed({
  get: () => (!o.value.teletravail ? 'aucun' : o.value.teletravail === 'Non' ? 'Non' : 'Oui'),
  set: (v: string) => (o.value.teletravail = v === 'aucun' ? '' : v),
})
// Langues : chacune avec son niveau (obligatoire si la langue est ajoutée).
const langues = computed(() => o.value.languesListe ?? [])
function synchroLangues() {
  o.value.langues = langues.value.filter(l => l.langue.trim()).map(l => (l.niveau ? `${l.langue} (${l.niveau})` : l.langue)).join(', ')
}
function ajouterLangue() {
  o.value.languesListe = [...langues.value, { langue: '', niveau: '' }]
}
function retirerLangue(i: number) {
  o.value.languesListe = langues.value.filter((_, j) => j !== i)
  synchroLangues()
}
// Lieu : une ou plusieurs villes, ou « Pas de lieu fixe » si le poste est itinérant.
const sansLieuFixe = computed({
  get: () => Boolean(o.value.sansLieuFixe),
  set: (v: boolean) => {
    o.value.sansLieuFixe = v
    o.value.lieu = v ? 'Pas de lieu fixe' : ''
  },
})

// Métier RMFP+ (à gauche) : ses compétences s'affichent à droite, déjà cochées ; on peut en retirer
// ou en ajouter librement (doc « Création manuelle des offres »).
const metierChoisi = computed({
  get: () => o.value.metier || 'aucun',
  set: (v: string) => {
    o.value.metier = v === 'aucun' ? '' : v
    o.value.competences = [...(metier(o.value.metier)?.competences ?? [])]
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
    <p
      v-if="!lectureSeule"
      class="note"
    >
      Les champs obligatoires ne sont contrôlés qu'au moment de publier : vous pouvez enregistrer une annonce incomplète.
    </p>

    <!-- Métadonnées : pré-remplies depuis l'organisme -->
    <div class="groupe">
      <FieldRow :cols="2">
        <CspSelect
          v-model="versant"
          label="Versant"
          hint="Champ obligatoire"
          :options="OPTIONS_VERSANT"
        />
        <CspInput
          :model-value="db.organisme.nom"
          label="Organisme de rattachement"
          hint="Champ obligatoire"
          disabled
        />
      </FieldRow>
    </div>

    <div class="groupe">
      <h3 class="groupe__titre">
        Le poste
      </h3>
      <ChampOffre
        :offre="o"
        champ="titre"
        label="Intitulé de l'offre"
        hint="Champ obligatoire · 150 caractères maximum"
        for-id="a-titre"
        :repris="repris('titre')"
        :modifie="modifie('titre')"
        @restaurer="restaurer('titre')"
      >
        <CspInput
          id="a-titre"
          v-model="o.titre"
          maxlength="150"
        />
      </ChampOffre>
      <FieldRow :cols="3">
        <CspInput
          v-model="o.nbPostes"
          type="number"
          min="1"
          max="10"
          label="Nombre de postes"
          hint="Champ obligatoire · 10 au maximum"
        />
      </FieldRow>
      <div class="metier">
        <ChampOffre
          :offre="o"
          champ="metier"
          label="Métier (référentiel RMFP+)"
          hint="Champ obligatoire · le domaine et le sous-domaine en sont déduits"
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
          label="Compétences"
          hint="Pré-remplies avec les compétences du métier, modifiables"
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
        </ChampOffre>
      </div>
      <ChampOffre
        :offre="o"
        champ="missions"
        label="Descriptif du poste"
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
      <FieldRow :cols="3">
        <CspSelect
          v-model="management"
          label="Management"
          :options="opts(['Oui', 'Non'], 'Non renseigné')"
        />
      </FieldRow>
    </div>

    <div class="groupe">
      <h3 class="groupe__titre">
        Cadre du recrutement
      </h3>
      <FieldRow :cols="2">
        <ChampSimple
          label="Nature de l'emploi : ouvert aux"
          hint="Champ obligatoire"
        >
          <CspCheckboxGroup
            v-model="o.ouvertA"
            label="Nature de l'emploi : ouvert aux"
            class="sans-label"
            :options="OUVERT"
          />
        </ChampSimple>
        <CspSelect
          v-if="contractuels"
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
      <FieldRow :cols="3">
        <CspSelect
          v-model="categorie"
          label="Catégorie"
          hint="Champ obligatoire"
          :options="opts(CATEGORIES.map(c => `${c}`), 'Choisir')"
        />
        <CspInput
          v-model="o.grade"
          label="Grade"
        />
        <CspInput
          v-model="o.corps"
          label="Corps"
          placeholder="Ex. : attachés d'administration de l'État"
        />
      </FieldRow>
      <FieldRow :cols="2">
        <CspSelect
          v-if="contractuels"
          v-model="fondement"
          label="Fondement juridique"
          hint="Champ obligatoire si l'emploi est ouvert aux contractuels"
          :options="opts(FONDEMENTS, 'Choisir')"
        />
        <CspInput
          v-model="o.lienJO"
          type="url"
          label="Lien vers l'avis de vacance au Journal officiel"
          placeholder="Ex. : https://www.legifrance.gouv.fr/jorf/id/…"
        />
      </FieldRow>
    </div>

    <div class="groupe">
      <h3 class="groupe__titre">
        Profil recherché
      </h3>
      <ChampOffre
        :offre="o"
        champ="profil"
        label="Descriptif du profil recherché"
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
      <FieldRow :cols="2">
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
      </FieldRow>
      <FieldRow :cols="2">
        <CspSelect
          v-model="diplome"
          label="Diplôme d'État requis"
          :options="opts(DIPLOMES_ETAT, 'Aucun')"
        />
        <CspSelect
          v-model="specialisation"
          label="Spécialisation"
          :options="opts(SPECIALISATIONS, 'Non renseigné')"
        />
      </FieldRow>
      <ChampSimple
        label="Langues"
        info="Pour chaque langue ajoutée, le niveau est obligatoire."
      >
        <div
          v-for="(l, i) in langues"
          :key="i"
          class="langue"
        >
          <CspInput
            v-model="l.langue"
            :label="`Langue ${i + 1}`"
            placeholder="Ex. : anglais"
            @update:model-value="synchroLangues"
          />
          <CspSelect
            :model-value="l.niveau || 'aucun'"
            label="Niveau"
            hint="Champ obligatoire"
            :options="opts(NIVEAUX_LANGUE, 'Choisir')"
            @update:model-value="(v?: string) => { l.niveau = !v || v === 'aucun' ? '' : v; synchroLangues() }"
          />
          <CspButton
            label="Retirer"
            variant="tertiary-no-outline"
            size="sm"
            icon="ri:delete-bin-line"
            is-icon-left
            @click="retirerLangue(i)"
          />
        </div>
        <CspButton
          label="Ajouter une langue"
          variant="secondary"
          size="sm"
          icon="ri:add-line"
          is-icon-left
          @click="ajouterLangue"
        />
      </ChampSimple>
    </div>

    <div class="groupe">
      <h3 class="groupe__titre">
        Conditions de travail
      </h3>
      <FieldRow :cols="2">
        <CspSelect
          v-model="temps"
          label="Temps de travail"
          hint="Champ obligatoire"
          :options="OPTIONS_TEMPS"
        />
        <CspSelect
          v-model="teletravail"
          label="Télétravail"
          :options="opts(['Oui', 'Non'], 'Non renseigné')"
        />
      </FieldRow>
      <ChampOffre
        :offre="o"
        champ="conditions"
        label="Conditions particulières"
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

    <div class="groupe">
      <h3 class="groupe__titre">
        Employeur
      </h3>
      <ChampSimple
        label="Descriptif de l'employeur"
        hint="Champ obligatoire"
      >
        <CspTextarea
          v-model="o.descriptifEmployeur"
          label="Descriptif de l'employeur"
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
        Localisation
      </h3>
      <ChampOffre
        :offre="o"
        champ="lieu"
        label="Lieu"
        hint="Champ obligatoire · plusieurs lieux possibles, séparés par une virgule"
        for-id="a-lieu"
        :repris="repris('lieu')"
      >
        <CspInput
          id="a-lieu"
          v-model="o.lieu"
          :disabled="sansLieuFixe"
          placeholder="Ex. : Montpellier, Nîmes"
        />
      </ChampOffre>
      <CspCheckbox
        v-model="sansLieuFixe"
        label="Pas de lieu fixe (poste itinérant)"
      />
      <FieldRow
        v-if="!sansLieuFixe"
        :cols="2"
      >
        <CspInput
          v-model="o.adresse"
          label="Géolocalisation : adresse du poste"
          hint="Champ obligatoire"
          placeholder="Numéro, rue, code postal, ville"
        />
        <CspInput
          v-model="o.lieuAffectation"
          label="Lieu d'affectation"
          placeholder="Ex. : site de la Pompignane, bâtiment B"
        />
      </FieldRow>
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

.ajout {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--csp-space-3);
  align-items: end;
  margin-top: var(--csp-space-3);
}

.metier__vide {
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-alt-grey);
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.langue {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 12rem auto;
  gap: var(--csp-space-3);
  align-items: end;
  margin-bottom: var(--csp-space-3);
}

.outil {
  margin: calc(-1 * var(--csp-space-3)) 0 0 calc(-1 * var(--csp-space-2));
}
</style>
