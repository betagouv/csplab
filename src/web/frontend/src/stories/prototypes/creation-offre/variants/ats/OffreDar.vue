<script setup lang="ts">
import type { Onglet } from './nav'
import type { Fiche, Offre } from './store'
import { computed, ref } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import FieldRow from '../../shared/FieldRow.vue'
import Panel from '../../shared/Panel.vue'
import SimulationNote from '../../shared/SimulationNote.vue'
import { manquesDar } from './aide'
import { useNav } from './nav'
import { changerEtat, db, ENTITES, formulaireDarDepuis, le, maintenant, sauvegarder, TYPES_DAR } from './store'

// Onglet DAR (organismes qui l'exigent) : saisie préremplie depuis la fiche, vrai état « brouillon »
// (plus besoin d'écrire « BROUILLON » dans l'intitulé), enregistrement automatique, soumission, décision simulée.
// La DAR reprend le nombre de postes ; une fois soumise, elle est figée.
const props = defineProps<{ offre: Offre, fiche: Fiche }>()
const emit = defineEmits<{ onglet: [t: Onglet] }>()
const { notifier } = useNav()
const o = computed(() => props.offre)

// Première ouverture : la DAR est créée en brouillon, préremplie à partir de la fiche de poste.
if (!o.value.darForm && o.value.dar === 'requise') {
  o.value.darForm = { ...formulaireDarDepuis(props.fiche, o.value.nbPostes), entite: db.organisme.entite, type: db.organisme.typeDar }
  o.value.darStatut = 'brouillon'
  o.value.darRef = `DAR-2026-0${340 + db.offres.filter(x => x.darRef).length}`
  o.value.historique.push({ date: maintenant(), texte: `DAR ${o.value.darRef} créée en brouillon depuis la fiche ${props.fiche.id}` })
  sauvegarder()
}

const d = computed(() => o.value.darForm!)
const modifiable = computed(() => o.value.etat === 'redaction' && (o.value.darStatut === 'brouillon' || o.value.darStatut === 'refusee'))
const manques = computed(() => manquesDar(o.value))
const tentative = ref(false)

const STATUTS = {
  brouillon: { label: 'Brouillon', type: 'info' as const },
  soumise: { label: 'Soumise — à traiter', type: 'new' as const },
  validee: { label: 'Validée', type: 'success' as const },
  refusee: { label: 'Refusée — à corriger', type: 'warning' as const },
}

function soumettre() {
  if (manques.value.length) {
    tentative.value = true
    return
  }
  o.value.darStatut = 'soumise'
  o.value.darSoumiseLe = maintenant()
  o.value.remarqueDar = undefined
  // La DAR porte le nombre de postes : l'offre le reprend.
  o.value.nbPostes = d.value.nbPostes
  changerEtat(o.value, 'validation', `DAR ${o.value.darRef} soumise (${d.value.nbPostes} poste${Number(d.value.nbPostes) > 1 ? 's' : ''})`)
  notifier('DAR soumise. Son contenu est désormais figé.')
}

// --- Décision simulée du valideur ---
const refus = ref(false)
const motifRefus = ref('Merci de préciser le motif du recrutement et le poste remplacé.')
function valider() {
  o.value.darStatut = 'validee'
  o.value.darValideeLe = maintenant()
  changerEtat(o.value, 'a_publier', `DAR ${o.value.darRef} validée par ${db.organisme.valideur.split(',')[0]}`)
  notifier('DAR validée (simulation). L\'offre peut être préparée pour la publication.')
}
function refuser() {
  o.value.darStatut = 'refusee'
  o.value.remarqueDar = motifRefus.value
  changerEtat(o.value, 'redaction', `DAR ${o.value.darRef} refusée : correction demandée`)
  refus.value = false
  notifier('DAR refusée : elle est de nouveau modifiable.')
}

function ajouterPiece(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0]
  if (f) {
    d.value.piecesJointes = [...d.value.piecesJointes, f.name]
  }
}

const evenementsDar = computed(() => [...o.value.historique].reverse().filter(h => h.texte.includes('DAR')))
</script>

<template>
  <div
    v-if="o.darForm"
    class="grille"
  >
    <div class="col">
      <div class="tete">
        <div>
          <p class="tete__ref">
            Demande d'autorisation de recrutement · {{ o.darRef }}
          </p>
          <h2 class="tete__titre">
            {{ d.intitule || 'Intitulé à renseigner' }}
          </h2>
        </div>
        <CspBadge
          :label="STATUTS[o.darStatut ?? 'brouillon'].label"
          :type="STATUTS[o.darStatut ?? 'brouillon'].type"
          variant="soft"
          size="sm"
        />
      </div>

      <p
        v-if="o.darStatut === 'refusee'"
        class="bandeau bandeau--refus"
      >
        <CspIcon
          name="ri:chat-1-line"
          :size="16"
        />
        Refusée : « {{ o.remarqueDar }} »
      </p>
      <p
        v-else-if="modifiable"
        class="note"
      >
        Préremplie depuis la fiche {{ fiche.id }}. Brouillon enregistré automatiquement : vous pouvez quitter et revenir.
        Ces informations concernent la DAR ; elles ne modifient ni la fiche ni l'annonce.
      </p>
      <p
        v-else
        class="note"
      >
        <CspIcon
          name="ri:lock-line"
          :size="14"
        />
        Soumise {{ le(o.darSoumiseLe) }} : contenu figé, validé tel qu'il a été renseigné.
      </p>

      <fieldset
        class="form"
        :disabled="!modifiable"
      >
        <Panel titre="Informations administratives">
          <FieldRow :cols="2">
            <CspSelect
              v-model="d.entite"
              label="Entité"
              :options="ENTITES.map(e => ({ value: e, label: e }))"
              :disabled="!modifiable"
            />
            <CspSelect
              v-model="d.type"
              label="Type de DAR"
              :options="TYPES_DAR.map(t => ({ value: t, label: t }))"
              :disabled="!modifiable"
            />
          </FieldRow>
          <CspInput
            v-model="d.employeur"
            label="Employeur"
            :disabled="!modifiable"
          />
        </Panel>

        <Panel titre="Description du poste">
          <CspTextarea
            v-model="d.descriptifEmployeur"
            label="Descriptif de l'employeur"
            :rows="2"
            :disabled="!modifiable"
          />
          <CspInput
            v-model="d.descriptifService"
            label="Descriptif du service"
            :disabled="!modifiable"
          />
          <FieldRow :cols="3">
            <CspInput
              v-model="d.intitule"
              label="Intitulé du poste"
              :disabled="!modifiable"
              :error="tentative && !d.intitule.trim()"
              :error-message="tentative && !d.intitule.trim() ? 'Indiquez l\'intitulé.' : undefined"
            />
            <CspInput
              v-model="d.categorie"
              label="Catégorie"
              :disabled="!modifiable"
              :error="tentative && !d.categorie.trim()"
              :error-message="tentative && !d.categorie.trim() ? 'Indiquez la catégorie.' : undefined"
            />
            <CspInput
              v-model="d.nbPostes"
              type="number"
              label="Nombre de postes"
              :disabled="!modifiable"
              :error="Number(d.nbPostes) < 1"
              :error-message="Number(d.nbPostes) < 1 ? 'Au moins 1 poste.' : undefined"
            />
          </FieldRow>
          <CspTextarea
            v-model="d.description"
            label="Description du poste"
            :rows="6"
            :disabled="!modifiable"
          />
          <CspTextarea
            v-model="d.motif"
            label="Motif et contexte de la demande (facultatif)"
            :rows="2"
            :disabled="!modifiable"
          />
          <p
            v-if="modifiable"
            class="mention"
          >
            Le motif aide les valideurs à comprendre la demande sans appeler le service (vacance, remplacement, création…).
          </p>
        </Panel>

        <Panel titre="Pièces jointes">
          <ul
            v-if="d.piecesJointes.length"
            class="pieces"
          >
            <li
              v-for="p in d.piecesJointes"
              :key="p"
            >
              <CspIcon
                name="ri:attachment-2"
                :size="14"
              />{{ p }}
            </li>
          </ul>
          <p
            v-else
            class="mention"
          >
            Aucune pièce jointe.
          </p>
          <label
            v-if="modifiable"
            class="ajout"
          >
            <CspIcon
              name="ri:add-line"
              :size="14"
            /> Ajouter une pièce jointe (simulation)
            <input
              type="file"
              class="sr-only"
              @change="ajouterPiece"
            >
          </label>
        </Panel>
      </fieldset>

      <div
        v-if="modifiable"
        class="pied"
      >
        <p
          v-if="tentative && manques.length"
          class="manque"
          role="alert"
        >
          À compléter : {{ manques.join(', ') }}.
        </p>
        <CspButton
          :label="o.darStatut === 'refusee' ? 'Soumettre à nouveau' : 'Soumettre la DAR'"
          icon="ri:send-plane-line"
          is-icon-left
          @click="soumettre"
        />
      </div>
    </div>

    <aside class="col">
      <Panel
        v-if="o.darStatut === 'soumise'"
        titre="Validation"
        :description="`En attente de ${db.organisme.valideur}.`"
      >
        <SimulationNote titre="Décision du valideur">
          <CspButton
            label="Valider"
            size="sm"
            @click="valider"
          />
          <CspButton
            label="Refuser"
            size="sm"
            variant="secondary"
            @click="refus = !refus"
          />
        </SimulationNote>
        <template v-if="refus">
          <CspTextarea
            v-model="motifRefus"
            label="Motif du refus"
            :rows="3"
          />
          <div>
            <CspButton
              label="Envoyer le refus"
              size="sm"
              @click="refuser"
            />
          </div>
        </template>
      </Panel>
      <Panel
        v-else-if="o.darStatut === 'validee'"
        titre="DAR validée"
        :description="`Validée ${le(o.darValideeLe)}.`"
      >
        <CspButton
          label="Préparer la publication"
          size="sm"
          icon="ri:arrow-right-line"
          @click="emit('onglet', 'publication')"
        />
      </Panel>
      <Panel titre="Historique de la DAR">
        <ol class="histo">
          <li
            v-for="(h, i) in evenementsDar"
            :key="i"
          >
            <small>{{ h.date }}</small>{{ h.texte }}
          </li>
        </ol>
      </Panel>
    </aside>
  </div>
</template>

<style scoped lang="scss">
.grille {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 20rem;
  gap: var(--csp-space-5);
  align-items: start;
}

.col {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.tete {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--csp-space-3);
}

.tete__ref {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.tete__titre {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-lg);
}

.note,
.bandeau {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-blue-france);
  background: var(--background-default-grey);
  font-size: var(--csp-font-size-sm);
}

.bandeau--refus {
  border-left-color: var(--border-plain-warning);
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

.mention {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.pieces {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: var(--csp-font-size-sm);

  li {
    display: flex;
    align-items: center;
    gap: var(--csp-space-1);
  }
}

.ajout {
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

.pied {
  position: sticky;
  bottom: 0;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  box-shadow: var(--csp-shadow-md);
}

.manque {
  flex: 1;
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-error);
}

.histo {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: var(--csp-font-size-sm);

  li {
    padding-left: var(--csp-space-3);
    border-left: 2px solid var(--border-default-grey);
  }

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
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
