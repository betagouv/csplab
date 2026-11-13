<script setup lang="ts">
import type { Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import FieldRow from '../../shared/FieldRow.vue'
import ChampOffre from './ChampOffre.vue'
import ChampSimple from './ChampSimple.vue'
import { db, MOTIFS_DEPART, MOTIFS_RECRUTEMENT } from './store'

// Section « Informations internes » (retour PO) : séparée de l'annonce pour qu'on voie d'un coup d'œil
// ce que le candidat ne verra jamais. Ces informations alimentent le résumé pour les valideurs.
// Jamais publiées, jamais reprises d'une fiche ni d'une offre dupliquée.
const props = defineProps<{ offre: Offre }>()
const o = computed(() => props.offre)

function modele(cle: 'motifRecrutement' | 'motifDepart' | 'groupeRifseep') {
  return computed({
    get: () => o.value[cle] || 'aucun',
    set: (v: string) => (o.value[cle] = v === 'aucun' ? '' : v),
  })
}
const motif = modele('motifRecrutement')
const depart = modele('motifDepart')
const rifseep = modele('groupeRifseep')
const avecAgent = computed(() => ['Remplacement', 'Renouvellement'].includes(o.value.motifRecrutement))
// Validation : qui va valider l'offre (circuit de l'organisme). Le commentaire pour les valideurs est facultatif :
// « Ajouter un commentaire » ouvre un tiroir (commentaire, document, destinataire : tous ou un service).
const avecValidation = computed(() => db.organisme.validationActive && db.organisme.groupes.length > 0)
const TOUS = 'tous'
const OPTIONS_DESTINATAIRE = computed(() => [{ value: TOUS, label: 'Tous les services validateurs' }, ...db.organisme.groupes.map(g => ({ value: g.nom, label: g.nom }))])
const destinataires = computed(() => o.value.commentairePour?.length ? o.value.commentairePour.join(', ') : 'tous les services validateurs')

const tiroir = ref(false)
const brouillon = ref({ texte: '', document: '', pour: TOUS })
function ouvrir() {
  brouillon.value = { texte: o.value.commentaireValideurs, document: o.value.ficheJointe ?? '', pour: o.value.commentairePour?.[0] ?? TOUS }
  tiroir.value = true
}
function joindre(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0]
  if (f) {
    brouillon.value.document = f.name
  }
}
function enregistrer() {
  o.value.commentaireValideurs = brouillon.value.texte.trim()
  o.value.ficheJointe = brouillon.value.document || undefined
  o.value.commentairePour = brouillon.value.pour === TOUS ? [] : [brouillon.value.pour]
  tiroir.value = false
}
function supprimer() {
  o.value.commentaireValideurs = ''
  o.value.ficheJointe = undefined
  o.value.commentairePour = []
}
const aCommentaire = computed(() => Boolean(o.value.commentaireValideurs || o.value.ficheJointe))
const optsInternes = (l: string[]) => [{ value: 'aucun', label: 'Non renseigné' }, ...l.map(v => ({ value: v, label: v }))]
</script>

<template>
  <div class="interne">
    <FieldRow :cols="2">
      <CspInput
        v-model="o.referenceInterne"
        label="Référence interne"
        hint="Facultatif"
      />
      <CspInput
        v-model="o.referenceFranceTravail"
        label="Référence France Travail"
        hint="Facultatif"
      />
    </FieldRow>
    <FieldRow :cols="2">
      <CspInput
        v-model="o.codePoste"
        label="Code poste"
        hint="Facultatif"
      />
    </FieldRow>
    <FieldRow :cols="2">
      <CspSelect
        v-model="motif"
        label="Motif de recrutement"
        hint="Facultatif"
        :options="optsInternes(MOTIFS_RECRUTEMENT)"
      />
      <CspSelect
        v-model="depart"
        label="Motif de départ"
        hint="Facultatif"
        :options="optsInternes(MOTIFS_DEPART)"
      />
    </FieldRow>
    <CspInput
      v-if="avecAgent"
      v-model="o.agentRemplace"
      label="Agent remplacé ou renouvelé"
      hint="Facultatif"
    />
    <FieldRow :cols="2">
      <CspSelect
        v-model="rifseep"
        label="Groupe RIFSEEP"
        hint="Facultatif"
        :options="optsInternes(['Groupe 1', 'Groupe 2', 'Groupe 3', 'Groupe 4'])"
      />
      <ChampOffre
        :offre="o"
        champ="cycleTravail"
        label="Cycle de travail"
        hint="Facultatif"
        for-id="a-cycle"
      >
        <CspInput
          id="a-cycle"
          v-model="o.cycleTravail"
          placeholder="Ex. : 38 h 30 sur 5 jours"
        />
      </ChampOffre>
    </FieldRow>

    <div
      v-if="avecValidation"
      class="validation"
    >
      <h3 class="validation__titre">
        Validation
      </h3>
      <div>
        <p class="validation__label">
          Qui va valider l'offre
        </p>
        <ul class="validation__liste">
          <li
            v-for="g in db.organisme.groupes"
            :key="g.nom"
          >
            <strong>{{ g.nom }}</strong> : {{ g.valideurs.join(', ') || 'aucun valideur désigné' }}
          </li>
        </ul>
        <p class="validation__aide">
          Circuit défini dans les paramètres de l'organisme. L'accord d'un seul valideur suffit pour chaque service.
        </p>
      </div>
      <div
        v-if="aCommentaire"
        class="commentaire"
      >
        <p class="validation__label">
          Commentaire pour {{ destinataires }}
        </p>
        <p
          v-if="o.commentaireValideurs"
          class="commentaire__texte"
        >
          {{ o.commentaireValideurs }}
        </p>
        <p
          v-if="o.ficheJointe"
          class="commentaire__doc"
        >
          <CspIcon
            name="ri:attachment-2"
            :size="14"
          /> {{ o.ficheJointe }}
        </p>
        <div class="commentaire__actions">
          <CspButton
            label="Modifier"
            size="sm"
            variant="tertiary-no-outline"
            icon="ri:edit-line"
            is-icon-left
            @click="ouvrir"
          />
          <CspButton
            label="Supprimer"
            size="sm"
            variant="tertiary-no-outline"
            icon="ri:delete-bin-line"
            is-icon-left
            @click="supprimer"
          />
        </div>
      </div>
      <div v-else>
        <CspButton
          label="Ajouter un commentaire"
          size="sm"
          variant="secondary"
          icon="ri:chat-3-line"
          is-icon-left
          @click="ouvrir"
        />
      </div>

      <CspDrawer
        v-model:open="tiroir"
        title="Commentaire pour les valideurs"
        description="Facultatif. Visible des valideurs choisis, jamais publié."
        size="md"
      >
        <div class="tiroir">
          <ChampSimple
            label="Commentaire"
            hint="Contexte utile pour décider, par ex. « Remplacement à l'identique, poste budgété »."
          >
            <CspTextarea
              v-model="brouillon.texte"
              label="Commentaire"
              :rows="5"
            />
          </ChampSimple>
          <div>
            <p class="validation__label">
              Document
              <span class="validation__hint">Facultatif</span>
            </p>
            <p
              v-if="brouillon.document"
              class="commentaire__doc"
            >
              <CspIcon
                name="ri:attachment-2"
                :size="14"
              /> {{ brouillon.document }}
              <button
                type="button"
                class="lien"
                @click="brouillon.document = ''"
              >
                Retirer
              </button>
            </p>
            <label class="ajout">
              <CspIcon
                name="ri:upload-2-line"
                :size="14"
              /> {{ brouillon.document ? 'Remplacer le document' : 'Joindre un document' }}
              <input
                type="file"
                class="sr-only"
                @change="joindre"
              >
            </label>
          </div>
          <CspRadioGroup
            v-model="brouillon.pour"
            label="Destinataire"
            :options="OPTIONS_DESTINATAIRE"
          />
        </div>
        <template #footer>
          <CspButton
            label="Annuler"
            variant="secondary"
            @click="tiroir = false"
          />
          <CspButton
            label="Enregistrer le commentaire"
            :disabled="!brouillon.texte.trim() && !brouillon.document"
            @click="enregistrer"
          />
        </template>
      </CspDrawer>
    </div>
  </div>
</template>

<style scoped lang="scss">
.interne {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  max-width: 48rem;
}
.validation {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  padding-top: var(--csp-space-5);
  border-top: 1px solid var(--border-default-grey);
}

.validation__titre {
  margin: 0;
  font-size: var(--csp-font-size-lg);
}

.validation__label {
  margin: 0 0 var(--csp-space-2);
  font-weight: var(--csp-font-weight-bold);
  font-size: var(--csp-font-size-sm);
}

.validation__liste {
  margin: 0;
  padding-left: var(--csp-space-5);
  font-size: var(--csp-font-size-sm);
}

.validation__hint {
  display: block;
  margin-top: var(--csp-space-1);
  font-size: 0.75rem;
  font-weight: 400;
  color: var(--text-mention-grey);
}

.validation__aide {
  margin: var(--csp-space-2) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.commentaire {
  padding: var(--csp-space-4);
  border-left: 3px solid var(--border-plain-blue-france);
  background: var(--background-alt-grey);
}

.commentaire__texte {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  white-space: pre-line;
}

.commentaire__doc {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: var(--csp-space-2) 0 0;
  font-size: var(--csp-font-size-sm);
}

.commentaire__actions {
  display: flex;
  gap: var(--csp-space-2);
  margin: var(--csp-space-2) 0 0 calc(-1 * var(--csp-space-2));
}

.tiroir {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
}

.lien {
  margin-left: var(--csp-space-2);
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}

.ajout {
  margin-top: var(--csp-space-2);
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-sm);
  color: var(--text-action-high-blue-france);
  cursor: pointer;

  &:has(:focus-visible) {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
  }
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
