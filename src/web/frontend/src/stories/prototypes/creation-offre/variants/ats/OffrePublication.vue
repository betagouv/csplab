<script setup lang="ts">
import type { Fiche, Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import Panel from '../../shared/Panel.vue'
import SimulationNote from '../../shared/SimulationNote.vue'
import { manquesPublication, manquesRedaction } from './aide'
import CycleOffre from './CycleOffre.vue'
import { useNav } from './nav'
import { CANAUX_DIFFUSION, changerEtat, le, maintenant, sauvegarder } from './store'

// Écran 6 — validation et publication : état administratif, DAR quand elle est nécessaire,
// passage à « À publier », puis publication (action distincte), et archivage.
const props = defineProps<{ offre: Offre, fiche: Fiche }>()
const emit = defineEmits<{ onglet: [t: 'suivi' | 'redaction' | 'publication'] }>()
const { aller, notifier } = useNav()
const o = computed(() => props.offre)

const manques = computed(() => manquesRedaction(o.value))
const manquesPub = computed(() => manquesPublication(o.value))
const tentative = ref(false)

const DAR = [
  { value: 'requise', label: 'Oui, une DAR doit être validée avant la publication' },
  { value: 'non_requise', label: 'Non, pas de DAR pour ce recrutement' },
]

function soumettreDar() {
  if (manques.value.length) {
    tentative.value = true
    return
  }
  o.value.darRef = o.value.darRef ?? `DAR-2026-0${330 + Math.floor(Math.random() * 60)}`
  o.value.darSoumiseLe = maintenant()
  o.value.darContenu = { intitule: props.fiche.intitule, service: props.fiche.service, nbPostes: o.value.nbPostes, missions: props.fiche.missions }
  o.value.remarqueDar = undefined
  changerEtat(o.value, 'validation', `DAR ${o.value.darRef} soumise`)
  notifier('DAR soumise. L\'offre est en cours de validation.')
}

function passerAPublier() {
  if (manques.value.length) {
    tentative.value = true
    return
  }
  changerEtat(o.value, 'a_publier', 'Rédaction terminée, pas de DAR nécessaire')
  notifier('L\'offre est prête à publier. Elle n\'est pas encore visible des candidats.')
}

// --- Simulation de la décision sur la DAR ---
const correction = ref(false)
const texteCorrection = ref('Merci de préciser le nombre de postes et les codes correspondants.')
function validerDar() {
  o.value.darValideeLe = maintenant()
  changerEtat(o.value, 'a_publier', `DAR ${o.value.darRef} validée par Hélène Robert`)
  notifier('DAR validée (simulation). L\'offre peut être publiée.')
}
function corrigerDar() {
  o.value.remarqueDar = texteCorrection.value
  changerEtat(o.value, 'redaction', `Correction demandée sur la DAR ${o.value.darRef}`)
  correction.value = false
  notifier('Correction demandée : l\'offre revient en rédaction.')
}

function basculerCanal(id: string) {
  o.value.canaux = o.value.canaux.includes(id) ? o.value.canaux.filter(c => c !== id) : [...o.value.canaux, id]
}
function publier() {
  if (manquesPub.value.length) {
    tentative.value = true
    return
  }
  o.value.publieeLe = maintenant()
  const noms = CANAUX_DIFFUSION.filter(c => o.value.canaux.includes(c.id)).map(c => c.nom).join(', ')
  changerEtat(o.value, 'publiee', `Offre publiée sur ${noms}`)
  notifier('Offre publiée (simulation : rien n\'est envoyé).')
}
function archiver() {
  changerEtat(o.value, 'archivee', 'Offre archivée')
  notifier('Offre archivée. Elle reste consultable et peut être dupliquée.')
}
function retour() {
  changerEtat(o.value, 'redaction', 'Retour en rédaction')
  emit('onglet', 'redaction')
}
</script>

<template>
  <CycleOffre :offre="o" />

  <div class="grille">
    <div class="col">
      <!-- Rédaction : DAR ou non -->
      <Panel
        v-if="o.etat === 'redaction'"
        titre="Validation administrative"
        description="Selon votre organisation et ce recrutement, une demande d'autorisation (DAR) peut être nécessaire avant la publication."
      >
        <CspRadioGroup
          :model-value="o.dar === 'non_definie' ? '' : o.dar"
          label="Ce recrutement nécessite-t-il une DAR ?"
          :options="DAR"
          @update:model-value="v => { o.dar = v as Offre['dar']; sauvegarder() }"
        />
        <p class="mention">
          Hypothèse à confirmer : les règles qui imposent une DAR varient selon les organisations ; le prototype laisse le choix.
        </p>
        <div
          v-if="tentative && manques.length"
          class="manques"
          role="alert"
        >
          Avant de continuer, complétez : {{ manques.join(', ') }}.
          <button
            type="button"
            class="lien"
            @click="emit('onglet', 'redaction')"
          >
            Revenir à la rédaction
          </button>
        </div>
        <div class="actions">
          <CspButton
            v-if="o.dar === 'requise'"
            label="Soumettre la DAR"
            icon="ri:send-plane-line"
            is-icon-left
            @click="soumettreDar"
          />
          <CspButton
            v-else-if="o.dar === 'non_requise'"
            label="Passer à « À publier »"
            icon="ri:arrow-right-line"
            @click="passerAPublier"
          />
        </div>
      </Panel>

      <!-- Validation en cours -->
      <Panel
        v-else-if="o.etat === 'validation'"
        :titre="`DAR ${o.darRef} — en cours de validation`"
        :description="`Soumise ${le(o.darSoumiseLe)}. En attente de Hélène Robert, autorité de validation.`"
      >
        <dl
          v-if="o.darContenu"
          class="dl"
        >
          <dt>Intitulé</dt>
          <dd>{{ o.darContenu.intitule }}</dd>
          <dt>Service</dt>
          <dd>{{ o.darContenu.service }}</dd>
          <dt>Postes</dt>
          <dd>{{ o.darContenu.nbPostes }}</dd>
          <dt>Missions</dt>
          <dd>{{ o.darContenu.missions }}</dd>
        </dl>
        <p class="mention">
          Contenu de la DAR figé à la soumission, repris de la fiche de poste. Le texte de l'annonce est distinct.
        </p>
        <SimulationNote titre="Décision du valideur">
          <CspButton
            label="Valider la DAR"
            size="sm"
            @click="validerDar"
          />
          <CspButton
            label="Demander une correction"
            size="sm"
            variant="secondary"
            @click="correction = !correction"
          />
        </SimulationNote>
        <div
          v-if="correction"
          class="correction"
        >
          <CspTextarea
            v-model="texteCorrection"
            label="Remarque"
            :rows="2"
          />
          <div>
            <CspButton
              label="Envoyer la demande de correction"
              size="sm"
              @click="corrigerDar"
            />
          </div>
        </div>
      </Panel>

      <!-- À publier -->
      <Panel
        v-else-if="o.etat === 'a_publier'"
        titre="Publication"
        description="L'offre est prête mais pas encore visible des candidats. Publier est une action distincte."
      >
        <p class="mention">
          <CspIcon
            name="ri:checkbox-circle-line"
            :size="14"
          />
          {{ o.dar === 'requise' ? `DAR ${o.darRef} validée ${le(o.darValideeLe)}` : 'Pas de DAR nécessaire pour ce recrutement' }}.
        </p>
        <fieldset class="canaux">
          <legend class="legende">
            Où publier ?
          </legend>
          <label
            v-for="c in CANAUX_DIFFUSION"
            :key="c.id"
            class="canal"
          >
            <input
              type="checkbox"
              :checked="o.canaux.includes(c.id)"
              @change="basculerCanal(c.id)"
            >
            <span>{{ c.nom }}<small>{{ c.detail }}</small></span>
          </label>
        </fieldset>
        <CspInput
          v-model="o.dateLimite"
          label="Date limite de candidature"
          placeholder="AAAA-MM-JJ"
          class="date"
          :error="tentative && !o.dateLimite"
          :error-message="tentative && !o.dateLimite ? 'Indiquez la date limite pour publier.' : undefined"
        />
        <p
          v-if="tentative && !o.canaux.length"
          class="manques"
          role="alert"
        >
          Choisissez au moins un canal.
        </p>
        <div class="actions">
          <CspButton
            label="Revenir en rédaction"
            variant="tertiary-no-outline"
            @click="retour"
          />
          <CspButton
            label="Publier l'offre"
            icon="ri:send-plane-line"
            is-icon-left
            @click="publier"
          />
        </div>
      </Panel>

      <!-- Publiée -->
      <Panel
        v-else-if="o.etat === 'publiee'"
        titre="Offre publiée"
        :description="`Publiée ${le(o.publieeLe)} — candidatures jusqu'au ${o.dateLimite}.`"
      >
        <ul class="liste">
          <li
            v-for="c in CANAUX_DIFFUSION.filter(x => o.canaux.includes(x.id))"
            :key="c.id"
          >
            {{ c.nom }} <small>— {{ c.detail.toLowerCase() }}</small>
          </li>
        </ul>
        <div class="actions">
          <CspButton
            label="Archiver l'offre"
            variant="secondary"
            icon="ri:archive-line"
            is-icon-left
            @click="archiver"
          />
        </div>
      </Panel>

      <!-- Archivée -->
      <Panel
        v-else
        titre="Offre archivée"
        description="Elle n'est plus visible des candidats. Son contenu peut servir de base à une nouvelle offre."
      >
        <div class="actions">
          <CspButton
            label="Dupliquer cette offre"
            variant="secondary"
            icon="ri:file-copy-2-line"
            is-icon-left
            @click="aller({ nom: 'creation', mode: 'duplication', offreId: o.id })"
          />
        </div>
      </Panel>
    </div>

    <aside class="col">
      <Panel titre="Rappel">
        <dl class="dl">
          <dt>Fiche</dt>
          <dd>{{ fiche.intitule }} ({{ fiche.id }})</dd>
          <dt>Postes</dt>
          <dd>{{ o.nbPostes }}</dd>
          <dt>Lieu</dt>
          <dd>{{ o.lieu || '—' }}</dd>
          <dt>Date limite</dt>
          <dd>{{ o.dateLimite || '—' }}</dd>
        </dl>
        <CspButton
          label="Voir l'aperçu candidat"
          variant="tertiary-no-outline"
          size="sm"
          @click="emit('onglet', 'redaction')"
        />
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

.mention {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.manques {
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-error);
  background: var(--background-default-grey);
  font-size: var(--csp-font-size-sm);
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-2);
}

.dl {
  display: grid;
  grid-template-columns: 6rem 1fr;
  gap: var(--csp-space-1) var(--csp-space-3);
  margin: 0;
  font-size: var(--csp-font-size-sm);

  dt {
    color: var(--text-mention-grey);
  }

  dd {
    margin: 0;
  }
}

.correction {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.canaux {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  border: 0;
}

.legende {
  margin-bottom: var(--csp-space-2);
  color: var(--text-label-grey);
}

.canal {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-2);
  font-size: var(--csp-font-size-sm);
  cursor: pointer;

  input {
    margin-top: 3px;
    accent-color: var(--background-action-high-blue-france);
  }

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.date {
  max-width: 16rem;
}

.liste {
  margin: 0;
  padding-left: var(--csp-space-5);
  list-style: disc;
  font-size: var(--csp-font-size-sm);

  small {
    color: var(--text-mention-grey);
  }
}

.lien {
  margin-left: var(--csp-space-1);
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}
</style>
