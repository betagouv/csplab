<script setup lang="ts">
import type { PartieOffre } from './etapes'
import type { Fiche, Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspCombobox from '@/components/base/CspCombobox/CspCombobox.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import FieldRow from '../../shared/FieldRow.vue'
import { aMettreEnForme, mettreEnForme } from './aide'
import ChampDate from './ChampDate.vue'
import ChampOffre from './ChampOffre.vue'
import ChampSimple from './ChampSimple.vue'
import ChoixMultiple from './ChoixMultiple.vue'
import LieuxPoste from './LieuxPoste.vue'
import { useNav } from './nav'
import { CATEGORIES, COMPETENCES_RMFP, contenuDepuisFiche, CORPS, FAMILLES, LANGUES, metier, METIERS, STATUTS_POSTE, TEMPS_TRAVAIL, typeCompetence } from './store'

// Champs de l'annonce (ce que lit le candidat sur Choisir le Service Public, D311-8), découpés en étapes (retour PO, F1) :
// `partie` choisit l'étape affichée. Les champs obligatoires portent un astérisque (F5) et ne sont contrôlés qu'au moment
// de publier. Versant et organisme de rattachement ne sont plus demandés : ils viennent de l'organisme (F7).
const props = defineProps<{ offre: Offre, partie: PartieOffre, fiche?: Fiche, lectureSeule?: boolean }>()
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
function choix(cle: 'natureContrat' | 'niveauExperience' | 'niveauEtudes' | 'management') {
  return computed({
    get: () => o.value[cle] || 'aucun',
    set: (v: string) => (o.value[cle] = v === 'aucun' ? '' : v),
  })
}
const natureContrat = choix('natureContrat')
const experience = choix('niveauExperience')
const etudes = choix('niveauEtudes')
const management = choix('management')
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
// Langue choisie dans une liste fixe (retour PO) ; une langue déjà ajoutée n'est plus proposée.
function optionsLangue(actuelle: string) {
  return opts(LANGUES.filter(x => x === actuelle || !langues.value.some(y => y.langue === x)), 'Choisir une langue')
}
function ajouterLangue() {
  o.value.languesListe = [...langues.value, { langue: '', niveau: '' }]
}
function retirerLangue(i: number) {
  o.value.languesListe = langues.value.filter((_, j) => j !== i)
  synchroLangues()
}

// Famille puis métier du RMFP+ (retour PO, 26/11/2026) : les compétences du métier s'affichent déjà cochées ;
// on peut en retirer, et en ajouter seulement depuis la liste des compétences du RMFP.
const famille = computed({
  get: () => o.value.famille || metier(o.value.metier)?.domaine || 'aucun',
  set: (v: string) => {
    o.value.famille = v === 'aucun' ? '' : v
    if (metier(o.value.metier)?.domaine !== o.value.famille) {
      o.value.metier = ''
      o.value.competences = []
    }
  },
})
const OPTIONS_FAMILLE = [{ value: 'aucun', label: 'Choisir une famille' }, ...FAMILLES.map(f => ({ value: f, label: f }))]
const metierChoisi = computed({
  get: () => o.value.metier || 'aucun',
  set: (v: string) => {
    o.value.metier = v === 'aucun' ? '' : v
    o.value.competences = [...(metier(o.value.metier)?.competences ?? [])]
  },
})
const OPTIONS_METIER = computed(() => [{ value: 'aucun', label: famille.value === 'aucun' ? 'Choisissez d\'abord une famille' : 'Choisir un métier' }, ...METIERS.filter(m => m.domaine === famille.value).map(m => ({ value: m.id, label: m.libelle }))])
const optionsCompetences = computed(() => [...new Set([...(metier(o.value.metier)?.competences ?? []), ...o.value.competences])].map(c => ({ value: c, label: c })))
const rechercheCompetence = ref('')
const competencesProposees = computed(() => COMPETENCES_RMFP
  .filter(c => !o.value.competences.includes(c) && c.toLowerCase().includes(rechercheCompetence.value.trim().toLowerCase()))
  .map(c => ({ value: c, label: `${c} (${typeCompetence(c).toLowerCase()})` })))
function cocherCompetence(c: string, v: boolean) {
  o.value.competences = v ? [...o.value.competences, c] : o.value.competences.filter(x => x !== c)
}
function ajouterCompetence(c: string | null) {
  if (c && !o.value.competences.includes(c)) {
    o.value.competences = [...o.value.competences, c]
  }
  rechercheCompetence.value = ''
}

// Corps et grades : plusieurs choix dans une liste fixe ; les grades proposés sont ceux des corps choisis (retour PO).
const optionsCorps = computed(() => CORPS.filter(c => !o.value.categorie || c.categorie === o.value.categorie).map(c => c.nom))
const corpsActuels = computed(() => o.value.corpsListe ?? (o.value.corps ? [o.value.corps] : []))
const optionsGrades = computed(() => [...new Set(CORPS.filter(c => corpsActuels.value.includes(c.nom)).flatMap(c => c.grades))])
const gradesChoisis = computed({
  get: () => o.value.gradesListe ?? (o.value.grade ? [o.value.grade] : []),
  set: (v: string[]) => {
    o.value.gradesListe = v
    o.value.grade = v.join(', ')
  },
})
const corpsChoisis = computed({
  get: () => corpsActuels.value,
  set: (v: string[]) => {
    o.value.corpsListe = v
    o.value.corps = v.join(', ')
    gradesChoisis.value = gradesChoisis.value.filter(g => optionsGrades.value.includes(g))
  },
})

// Nature de l'emploi (retour PO, F8) : un seul choix parmi trois, plutôt que deux cases à cocher.
const OUVERT = [
  { value: 'titulaire', label: 'Fonctionnaires uniquement' },
  { value: 'les_deux', label: 'Fonctionnaires et contractuels' },
  { value: 'contractuel', label: 'Contractuels uniquement' },
]
const ouvertA = computed({
  get: () => (o.value.ouvertA.length === 2 ? 'les_deux' : o.value.ouvertA[0] ?? ''),
  set: (v: string) => (o.value.ouvertA = v === 'les_deux' ? ['titulaire', 'contractuel'] : v ? [v] : []),
})
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
    <!-- Étape « Le poste » -->
    <div
      v-if="partie === 'poste'"
      class="groupe"
    >
      <ChampOffre
        :offre="o"
        champ="titre"
        label="Intitulé de l'offre"
        obligatoire
        hint="Compréhensible hors de l'administration, sans sigle · 150 caractères maximum"
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
        <ChampSimple
          label="Nombre de postes"
          obligatoire
          hint="10 au maximum"
        >
          <CspInput
            v-model="o.nbPostes"
            type="number"
            min="1"
            max="10"
            label="Nombre de postes"
          />
        </ChampSimple>
      </FieldRow>
      <ChampOffre
        :offre="o"
        champ="missions"
        label="Descriptif du poste"
        obligatoire
        hint="Une mission par ligne, en commençant par un verbe"
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

    <!-- Étape « Le métier » : page dédiée au métier et aux compétences -->
    <div
      v-else-if="partie === 'metier'"
      class="groupe"
    >
      <div class="metier">
        <FieldRow :cols="2">
          <ChampSimple
            label="Famille (référentiel RMFP+)"
            obligatoire
          >
            <CspSelect
              v-model="famille"
              label="Famille"
              :options="OPTIONS_FAMILLE"
            />
          </ChampSimple>
          <ChampOffre
            :offre="o"
            champ="metier"
            label="Métier"
            obligatoire
            for-id="a-metier"
          >
            <CspSelect
              id="a-metier"
              v-model="metierChoisi"
              label="Métier"
              class="sans-label"
              :options="OPTIONS_METIER"
              :disabled="famille === 'aucun'"
            />
          </ChampOffre>
        </FieldRow>
        <ChampOffre
          :offre="o"
          champ="competences"
          label="Compétences"
          hint="Pré-remplies avec les compétences du métier, modifiables"
        >
          <!-- Savoir-faire ou connaissance, en texte secondaire à côté de chaque compétence (revue UI, 27/11/2026) -->
          <fieldset
            v-if="optionsCompetences.length"
            class="competences"
          >
            <legend class="sr-only">
              Compétences
            </legend>
            <div
              v-for="c in optionsCompetences"
              :key="c.value"
              class="competence"
            >
              <CspCheckbox
                :model-value="o.competences.includes(c.value)"
                :label="c.label"
                @update:model-value="(v?: boolean) => cocherCompetence(c.value, Boolean(v))"
              />
              <span class="competence__type">{{ typeCompetence(c.value) }}</span>
            </div>
          </fieldset>
          <p
            v-else
            class="metier__vide"
          >
            Choisissez un métier pour afficher ses compétences du RMFP+.
          </p>
          <div class="ajout">
            <CspCombobox
              v-model:search-term="rechercheCompetence"
              :model-value="null"
              :options="competencesProposees"
              label="Ajouter une compétence du RMFP"
              placeholder="Rechercher une compétence"
              empty-label="Aucune compétence du RMFP ne correspond"
              @update:model-value="ajouterCompetence"
            />
          </div>
        </ChampOffre>
      </div>
    </div>

    <!-- Étape « Cadre du recrutement » : Catégorie, Corps puis Grade (le grade dépend du corps, F8) -->
    <div
      v-else-if="partie === 'cadre'"
      class="groupe"
    >
      <ChampSimple
        label="Nature de l'emploi"
        obligatoire
      >
        <CspRadioGroup
          v-model="ouvertA"
          label="Nature de l'emploi"
          name="ouvert-a"
          :options="OUVERT"
        />
      </ChampSimple>
      <FieldRow
        v-if="contractuels"
        :cols="2"
      >
        <CspSelect
          v-model="natureContrat"
          label="Nature du contrat"
          :options="opts(CONTRATS, 'Non renseigné')"
        />
      </FieldRow>
      <!-- Un champ avec texte d'aide est seul sur sa ligne (retour Alice du 25/11/2026) -->
      <FieldRow
        v-if="contractuels"
        :cols="2"
      >
        <ChampSimple
          label="Fondement juridique"
          obligatoire
          hint="Pour les contractuels"
        >
          <CspSelect
            v-model="fondement"
            label="Fondement juridique"
            :options="opts(FONDEMENTS, 'Choisir')"
          />
        </ChampSimple>
      </FieldRow>
      <FieldRow :cols="2">
        <ChampSimple
          label="Statut du poste"
          obligatoire
        >
          <CspSelect
            v-model="statutPoste"
            label="Statut du poste"
            :options="opts(STATUTS_POSTE, 'Choisir')"
          />
        </ChampSimple>
        <ChampSimple
          label="Date de vacance"
          obligatoire
        >
          <ChampDate
            v-model="o.dateVacance"
            label="Date de vacance"
          />
        </ChampSimple>
      </FieldRow>
      <FieldRow :cols="2">
        <ChampSimple
          label="Catégorie"
          obligatoire
        >
          <CspSelect
            v-model="categorie"
            label="Catégorie"
            :options="opts(CATEGORIES.map(c => `${c}`), 'Choisir')"
          />
        </ChampSimple>
      </FieldRow>
      <FieldRow :cols="2">
        <ChoixMultiple
          v-model="corpsChoisis"
          label="Corps"
          :hint="o.categorie ? `Corps de catégorie ${o.categorie} · plusieurs choix possibles` : 'Plusieurs choix possibles'"
          :options="optionsCorps"
          placeholder="Rechercher un corps"
        />
      </FieldRow>
      <FieldRow :cols="2">
        <ChoixMultiple
          v-if="corpsChoisis.length"
          v-model="gradesChoisis"
          label="Grade"
          hint="Grades des corps choisis · plusieurs choix possibles"
          :options="optionsGrades"
          placeholder="Rechercher un grade"
        />
        <ChampSimple
          v-else
          label="Grade"
          hint="Choisissez d'abord un corps"
        >
          <CspSelect
            model-value="aucun"
            label="Grade"
            :options="[{ value: 'aucun', label: 'Choisissez d\'abord un corps' }]"
            disabled
          />
        </ChampSimple>
      </FieldRow>
      <CspInput
        v-model="o.lienJO"
        type="url"
        label="Lien vers l'avis de vacance au Journal officiel"
        placeholder="Ex. : https://www.legifrance.gouv.fr/jorf/id/…"
      />
    </div>

    <!-- Étape « Le profil recherché » (les conditions de travail sont passées à l'étape 5, revue UI du 27/11/2026) -->
    <template v-else-if="partie === 'profil'">
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
            <CspSelect
              :model-value="l.langue || 'aucun'"
              :label="`Langue ${i + 1}`"
              :options="optionsLangue(l.langue)"
              @update:model-value="(v?: string) => { l.langue = !v || v === 'aucun' ? '' : v; synchroLangues() }"
            />
            <ChampSimple
              label="Niveau"
              obligatoire
            >
              <CspSelect
                :model-value="l.niveau || 'aucun'"
                label="Niveau"
                :options="opts(NIVEAUX_LANGUE, 'Choisir')"
                @update:model-value="(v?: string) => { l.niveau = !v || v === 'aucun' ? '' : v; synchroLangues() }"
              />
            </ChampSimple>
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
    </template>

    <!-- Étape 5 « L'environnement de travail » : employeur, lieux, conditions de travail -->
    <template v-else-if="partie === 'lieu'">
      <div class="groupe">
        <h3 class="groupe__titre">
          Employeur
        </h3>
        <ChampSimple
          label="Descriptif de l'employeur"
          obligatoire
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
          Lieux
        </h3>
        <LieuxPoste :offre="o" />
      </div>
      <div class="groupe">
        <h3 class="groupe__titre">
          Conditions de travail
        </h3>
        <FieldRow :cols="2">
          <ChampSimple
            label="Temps de travail"
            obligatoire
          >
            <CspSelect
              v-model="temps"
              label="Temps de travail"
              :options="OPTIONS_TEMPS"
            />
          </ChampSimple>
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
        <CspTextarea
          v-model="o.infosComplementaires"
          label="Informations complémentaires"
          placeholder="Ex. : accessibilité du poste aux personnes en situation de handicap, avantages sociaux."
          :rows="2"
        />
      </div>
    </template>
  </div>
</template>

<style scoped lang="scss">
.competences {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  border: 0;
}

.competence {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-1) var(--csp-space-3);
}

.competence__type {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}

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

.metier {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
}

.ajout {
  max-width: 30rem;
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
