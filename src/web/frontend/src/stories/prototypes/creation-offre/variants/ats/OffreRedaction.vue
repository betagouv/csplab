<script setup lang="ts">
import type { Onglet } from './nav'
import type { Fiche, Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import FieldRow from '../../shared/FieldRow.vue'
import ListEditor from '../../shared/ListEditor.vue'
import Panel from '../../shared/Panel.vue'
import { aMettreEnForme, manquesCreation, mettreEnForme } from './aide'
import ApercuCandidat from './ApercuCandidat.vue'
import ChampOffre from './ChampOffre.vue'
import CircuitValidation from './CircuitValidation.vue'
import { useNav } from './nav'
import OrigineBadge from './OrigineBadge.vue'
import { CATEGORIES, CHAMPS_DETERMINANTS, changerEtat, contenuDepuisFiche, db, determinant, envoyerPourValidation, LIBELLES_CONTENU, verrouilleParDar } from './store'

// Écran 5 — formulaire unique de l'offre. Si l'organisme fait valider ses recrutements (DAR), les champs
// déterminants pour la demande y sont obligatoires et le bouton final est « Envoyer pour validation » ;
// sinon « Créer l'offre ». La fiche de poste source se consulte à côté. L'aperçu suit la saisie.
const props = defineProps<{ offre: Offre, fiche: Fiche }>()
const emit = defineEmits<{ enregistrer: [], onglet: [t: Onglet] }>()
const { notifier } = useNav()
const o = computed(() => props.offre)

// Modifiable en brouillon et pendant la relecture avant publication ; jamais pendant la validation.
// Après validation, les champs déterminants restent verrouillés pour garantir la validité de la DAR.
const modifiable = computed(() => o.value.etat === 'redaction' || o.value.etat === 'a_publier')
const avecDar = computed(() => o.value.dar === 'requise')
function bloque(champ: string) {
  return !modifiable.value || verrouilleParDar(o.value, champ)
}
function requis(champ: string) {
  return determinant(o.value, champ) && o.value.etat === 'redaction'
}
const CATEGORIES_OPTIONS = CATEGORIES.map(c => ({ value: c, label: `Catégorie ${c}` }))
const vue = ref<'apercu' | 'fiche'>('apercu')
const VUES = [
  { value: 'apercu' as const, label: 'Aperçu candidat', icon: 'ri:eye-line' },
  { value: 'fiche' as const, label: 'Fiche de poste source', icon: 'ri:file-text-line' },
]

// « Repris de la fiche » tant que le texte est identique à ce que la fiche propose (création depuis une fiche).
const source = computed(() => contenuDepuisFiche(props.fiche))
type CleTexte = 'titre' | 'presentation' | 'missions' | 'profil' | 'modalites' | 'lieu' | 'teletravail'
const avecFiche = computed(() => o.value.origineContenu === 'fiche' || o.value.origineContenu === 'fichier')
function repris(cle: CleTexte | 'indispensables') {
  const v = source.value[cle]
  return avecFiche.value && Boolean(Array.isArray(v) ? v.length : v) && JSON.stringify(o.value[cle]) === JSON.stringify(v)
}
function modifie(cle: CleTexte | 'indispensables') {
  const v = source.value[cle]
  return avecFiche.value && Boolean(Array.isArray(v) ? v.length : v) && !repris(cle)
}
function restaurer(cle: CleTexte | 'indispensables') {
  const v = source.value[cle]
  ;(o.value as unknown as Record<string, unknown>)[cle] = Array.isArray(v) ? [...v] : v
}

function formater() {
  o.value.missions = mettreEnForme(o.value.missions)
  notifier('Mise en forme appliquée : une mission par ligne. Aucun mot n\'a été changé.')
}

function enregistrer() {
  emit('enregistrer')
  notifier('Brouillon enregistré. Vous pouvez revenir à la rédaction à tout moment.')
}

// --- Fin du formulaire : le bouton dépend du paramètre DAR de l'organisme ---
const tentative = ref(false)
const manques = computed(() => manquesCreation(o.value))
const MESSAGES: Record<string, string> = {
  titre: 'Indiquez l\'intitulé.',
  categorie: 'Choisissez la catégorie.',
  nbPostes: 'Au moins 1 poste.',
  lieu: 'Indiquez le lieu.',
  missions: 'Décrivez les missions.',
}
function erreur(champ: keyof typeof CHAMPS_DETERMINANTS) {
  return tentative.value && manques.value.includes(CHAMPS_DETERMINANTS[champ]) ? MESSAGES[champ] : undefined
}

const confirmation = ref(false)
const sansValideur = computed(() => !db.organisme.valideurs.length)
function demanderEnvoi() {
  if (manques.value.length) {
    tentative.value = true
    return
  }
  confirmation.value = true
}
function envoyer() {
  confirmation.value = false
  emit('enregistrer')
  envoyerPourValidation(o.value)
  notifier('Offre envoyée pour validation. Elle n\'est plus modifiable jusqu\'à la décision des valideurs.')
}
function creer() {
  if (manques.value.length) {
    tentative.value = true
    return
  }
  emit('enregistrer')
  changerEtat(o.value, 'a_publier', 'Offre créée (pas de validation pour cet organisme)')
  notifier('Offre créée. Relisez-la et publiez-la quand vous le souhaitez.')
  emit('onglet', 'publication')
}
</script>

<template>
  <p
    v-if="!modifiable"
    class="bandeau"
  >
    <CspIcon
      name="ri:lock-line"
      :size="16"
    />
    <span v-if="o.etat === 'validation'">En attente de validation : l'offre ne peut être ni modifiée ni publiée tant que la validation n'est pas terminée.</span>
    <span v-else>Offre {{ o.etat === 'publiee' ? 'publiée' : 'archivée' }} : contenu en lecture seule.</span>
  </p>
  <p
    v-else-if="o.etat === 'a_publier'"
    class="bandeau"
  >
    <CspIcon
      name="ri:eye-line"
      :size="16"
    />
    <span>
      Relecture avant publication : l'offre ne sera publiée que lorsque vous le déciderez.
      <template v-if="o.darStatut === 'validee'">Les champs validés ({{ Object.values(CHAMPS_DETERMINANTS).join(', ') }}) ne sont plus modifiables.</template>
    </span>
  </p>
  <p
    v-else-if="o.remarqueDar"
    class="bandeau bandeau--remarque"
  >
    <CspIcon
      name="ri:chat-1-line"
      :size="16"
    />
    <span>Refusée par {{ o.remarqueDar }}. Corrigez puis renvoyez l'offre pour validation.</span>
  </p>

  <div
    v-if="o.etat === 'validation'"
    class="attente"
  >
    <p class="attente__titre">
      Validation en cours
    </p>
    <CircuitValidation :offre="o" />
  </div>

  <div class="redac">
    <fieldset
      class="form"
      :disabled="!modifiable"
    >
      <p class="origine">
        Contenu : {{ LIBELLES_CONTENU[o.origineContenu].toLowerCase() }}<template v-if="o.sourceOffreId">
          ({{ o.sourceOffreId }})
        </template>.
        Vos modifications concernent l'annonce uniquement : la fiche {{ fiche.id }} n'est pas modifiée.
      </p>
      <p
        v-if="avecDar && o.etat === 'redaction'"
        class="legende"
      >
        Votre organisme fait valider ses recrutements (DAR). Les champs <span class="legende__tag">Requis pour la validation</span>
        doivent être remplis pour envoyer l'offre ; les autres peuvent être complétés jusqu'à la publication.
        <em>Liste des champs indicative.</em>
      </p>

      <Panel titre="L'essentiel">
        <ChampOffre
          :offre="o"
          champ="titre"
          label="Titre de l'offre"
          for-id="o-titre"
          :repris="repris('titre')"
          :modifie="modifie('titre') && !bloque('titre')"
          :requis="requis('titre')"
          :valide="verrouilleParDar(o, 'titre')"
          :erreur="erreur('titre')"
          @restaurer="restaurer('titre')"
        >
          <CspInput
            id="o-titre"
            v-model="o.titre"
            :disabled="bloque('titre')"
          />
        </ChampOffre>
        <FieldRow :cols="2">
          <ChampOffre
            :offre="o"
            champ="categorie"
            label="Catégorie"
            for-id="o-categorie"
            :requis="requis('categorie')"
            :valide="verrouilleParDar(o, 'categorie')"
            :erreur="erreur('categorie')"
          >
            <div class="sans-label">
              <CspSelect
                id="o-categorie"
                v-model="o.categorie"
                label="Catégorie"
                placeholder="Choisir"
                :options="CATEGORIES_OPTIONS"
                :disabled="bloque('categorie')"
              />
            </div>
          </ChampOffre>
          <ChampOffre
            :offre="o"
            champ="nbPostes"
            label="Nombre de postes"
            for-id="o-postes"
            :requis="requis('nbPostes')"
            :valide="verrouilleParDar(o, 'nbPostes')"
            :erreur="erreur('nbPostes')"
          >
            <CspInput
              id="o-postes"
              v-model="o.nbPostes"
              type="number"
              :disabled="bloque('nbPostes')"
            />
          </ChampOffre>
        </FieldRow>
        <ChampOffre
          :offre="o"
          champ="presentation"
          label="Présentation du poste"
          for-id="o-presentation"
          :repris="repris('presentation')"
          :modifie="modifie('presentation')"
          @restaurer="restaurer('presentation')"
        >
          <CspTextarea
            id="o-presentation"
            v-model="o.presentation"
            :rows="3"
            :disabled="!modifiable"
          />
        </ChampOffre>
      </Panel>

      <Panel titre="Missions">
        <ChampOffre
          :offre="o"
          champ="missions"
          label="Vos missions"
          for-id="o-missions"
          :repris="repris('missions')"
          :modifie="modifie('missions') && !bloque('missions')"
          :requis="requis('missions')"
          :valide="verrouilleParDar(o, 'missions')"
          :erreur="erreur('missions')"
          @restaurer="restaurer('missions')"
        >
          <CspTextarea
            id="o-missions"
            v-model="o.missions"
            :rows="6"
            :disabled="bloque('missions')"
          />
        </ChampOffre>
        <div
          v-if="!bloque('missions') && aMettreEnForme(o.missions)"
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
      </Panel>

      <Panel titre="Profil recherché">
        <ChampOffre
          :offre="o"
          champ="profil"
          label="Votre profil"
          for-id="o-profil"
          :repris="repris('profil')"
          :modifie="modifie('profil')"
          @restaurer="restaurer('profil')"
        >
          <CspTextarea
            id="o-profil"
            v-model="o.profil"
            :rows="3"
            :disabled="!modifiable"
          />
        </ChampOffre>
        <ChampOffre
          :offre="o"
          champ="indispensables"
        >
          <ListEditor
            v-model="o.indispensables"
            label="Compétences indispensables"
            placeholder="Ex. : Maîtrise d'un logiciel de paie"
            :disabled="!modifiable"
          />
        </ChampOffre>
        <ChampOffre
          :offre="o"
          champ="souhaitables"
        >
          <ListEditor
            v-model="o.souhaitables"
            label="Compétences souhaitables"
            placeholder="Ex. : Première expérience en paie"
            :disabled="!modifiable"
          />
        </ChampOffre>
      </Panel>

      <Panel titre="Lieu et conditions d'exercice">
        <FieldRow :cols="2">
          <ChampOffre
            :offre="o"
            champ="lieu"
            label="Lieu"
            for-id="o-lieu"
            :repris="repris('lieu')"
            :requis="requis('lieu')"
            :valide="verrouilleParDar(o, 'lieu')"
            :erreur="erreur('lieu')"
          >
            <CspInput
              id="o-lieu"
              v-model="o.lieu"
              :disabled="bloque('lieu')"
            />
          </ChampOffre>
          <ChampOffre
            :offre="o"
            champ="remuneration"
            label="Rémunération (facultatif)"
            for-id="o-remu"
          >
            <CspInput
              id="o-remu"
              v-model="o.remuneration"
              placeholder="Ex. : selon expérience, grille indiciaire"
              :disabled="!modifiable"
            />
          </ChampOffre>
        </FieldRow>
        <FieldRow :cols="2">
          <CspInput
            v-model="o.teletravail"
            label="Télétravail (facultatif)"
            :disabled="!modifiable"
          />
          <CspInput
            v-model="o.conditions"
            label="Conditions d'exercice (facultatif)"
            placeholder="Horaires, déplacements…"
            :disabled="!modifiable"
          />
        </FieldRow>
      </Panel>

      <Panel
        v-if="avecDar"
        titre="Pour les valideurs"
        description="Ces informations accompagnent la demande ; elles ne figurent pas dans l'annonce."
      >
        <ChampOffre
          :offre="o"
          champ="motif"
          label="Motif du recrutement (facultatif)"
          for-id="o-motif"
        >
          <CspTextarea
            id="o-motif"
            v-model="o.motif"
            :rows="2"
            :disabled="!modifiable || o.darStatut === 'validee'"
          />
        </ChampOffre>
        <p class="mention">
          Circuit défini par le superviseur :
          {{ db.organisme.valideurs.map(v => `${v.nom} (${v.fonction})`).join(db.organisme.circuit === 'successif' ? ' puis ' : ' et ') || 'aucun valideur' }}.
        </p>
      </Panel>

      <div
        v-if="o.etat === 'redaction'"
        class="pied"
      >
        <CspButton
          label="Enregistrer le brouillon"
          variant="secondary"
          icon="ri:save-3-line"
          is-icon-left
          @click="enregistrer"
        />
        <p
          v-if="tentative && manques.length"
          class="manque"
          role="alert"
        >
          À compléter : {{ manques.join(', ') }}.
        </p>
        <p
          v-else-if="avecDar && sansValideur"
          class="manque"
          role="alert"
        >
          Aucun valideur n'est défini : contactez le superviseur de l'organisme.
        </p>
        <CspButton
          v-if="avecDar"
          :label="o.darStatut === 'refusee' ? 'Renvoyer pour validation' : 'Envoyer pour validation'"
          icon="ri:send-plane-line"
          is-icon-left
          :disabled="sansValideur"
          @click="demanderEnvoi"
        />
        <CspButton
          v-else
          label="Créer l'offre"
          icon="ri:check-line"
          is-icon-left
          @click="creer"
        />
      </div>
      <CspDialog
        v-model:open="confirmation"
        title="Envoyer l'offre pour validation ?"
        size="sm"
      >
        <p class="dialogue">
          Jusqu'à la fin de la validation, l'offre ne pourra être <strong>ni modifiée ni publiée</strong>.
          Après validation, les champs déterminants resteront verrouillés.
        </p>
        <p class="dialogue">
          {{ db.organisme.circuit === 'successif' ? 'Valideurs, dans l\'ordre :' : 'Valideurs, en parallèle :' }}
        </p>
        <ol class="dialogue__liste">
          <li
            v-for="v in db.organisme.valideurs"
            :key="v.nom"
          >
            {{ v.nom }} — {{ v.fonction }}
          </li>
        </ol>
        <template #footer>
          <CspButton
            label="Annuler"
            variant="secondary"
            @click="confirmation = false"
          />
          <CspButton
            label="Envoyer pour validation"
            icon="ri:send-plane-line"
            is-icon-left
            @click="envoyer"
          />
        </template>
      </CspDialog>
    </fieldset>

    <aside class="cote">
      <CspSegmentedControl
        v-model="vue"
        legend="Afficher"
        hide-legend
        size="sm"
        :options="VUES"
      />
      <ApercuCandidat
        v-if="vue === 'apercu'"
        :offre="o"
      />
      <div
        v-else
        class="source"
      >
        <p class="source__tete">
          <CspIcon
            name="ri:lock-line"
            :size="14"
          />
          {{ fiche.id }} · <OrigineBadge
            :origine="fiche.origine"
            court
          /> · consultation seule
        </p>
        <h3 class="source__titre">
          {{ fiche.intitule }}
        </h3>
        <p class="source__meta">
          {{ fiche.service }} · {{ fiche.localisation }}
        </p>
        <p class="source__label">
          Missions
        </p>
        <p class="source__texte">
          {{ fiche.missions || '—' }}
        </p>
        <ul
          v-if="fiche.activites.length"
          class="source__liste"
        >
          <li
            v-for="a in fiche.activites"
            :key="a"
          >
            {{ a }}
          </li>
        </ul>
        <p class="source__label">
          Compétences
        </p>
        <ul class="source__liste">
          <li
            v-for="c in fiche.competences"
            :key="c"
          >
            {{ c }}
          </li>
        </ul>
        <p class="source__label">
          Profil
        </p>
        <p class="source__texte">
          {{ fiche.profil || '—' }}
        </p>
        <p class="source__note">
          La fiche décrit le poste pour l'organisation ; l'annonce s'adresse aux candidats. Modifier l'une ne change pas l'autre.
        </p>
      </div>
    </aside>
  </div>
</template>

<style scoped lang="scss">
.bandeau {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-blue-france);
  background: var(--background-default-grey);
  font-size: var(--csp-font-size-sm);

  span {
    flex: 1;
  }

  &--remarque {
    background: var(--background-alt-blue-france);
  }
}

.attente {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.attente__titre {
  margin: 0;
  font-weight: var(--csp-font-weight-bold);
}

.legende {
  margin: 0;
  font-size: var(--csp-font-size-sm);
}

.legende__tag {
  padding: 0 var(--csp-space-1);
  background: var(--background-alt-blue-france);
  font-size: var(--csp-font-size-xs);
  color: var(--text-action-high-blue-france);
  white-space: nowrap;
}

.sans-label :deep(.csp-select-group__label) {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}

.mention {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.dialogue {
  margin: 0 0 var(--csp-space-2);
  font-size: var(--csp-font-size-sm);
}

.dialogue__liste {
  margin: 0;
  padding-left: var(--csp-space-5);
  font-size: var(--csp-font-size-sm);
}

.redac {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: var(--csp-space-5);
  align-items: start;
}

.form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  margin: 0;
  padding: 0;
  border: 0;
  min-width: 0;
}

.origine {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.court {
  max-width: 8rem;
}

.outil {
  margin: calc(-1 * var(--csp-space-3)) 0 0 calc(-1 * var(--csp-space-2));
}

.manque {
  flex: 1;
  margin: 0;
  align-self: center;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-error);
}

.pied {
  position: sticky;
  bottom: 0;
  display: flex;
  justify-content: space-between;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  box-shadow: var(--csp-shadow-md);
}

.cote {
  position: sticky;
  top: 9rem;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  max-height: calc(100vh - 11rem);
  overflow-y: auto;
}

.source {
  padding: var(--csp-space-5);
  border: 1px dashed var(--border-plain-grey);
  background: var(--background-alt-grey);
  font-size: var(--csp-font-size-sm);

  p {
    margin: 0;
  }
}

.source__tete {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.source__titre {
  margin: var(--csp-space-2) 0 0;
  font-size: var(--csp-font-size-lg);
}

.source__meta {
  color: var(--text-mention-grey);
}

.source__label {
  margin-top: var(--csp-space-3) !important;
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.source__liste {
  margin: 0;
  padding-left: var(--csp-space-5);
  list-style: disc;
}

.source__note {
  margin-top: var(--csp-space-4) !important;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}
</style>
