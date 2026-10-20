<script setup lang="ts">
import type { EtapeCircuit } from '../../data/types'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { personne, PERSONNES } from '../../data/referentiels'
import { LIBELLES_STATUT, useOffre } from '../../data/useOffre'
import SimulationNote from '../../shared/SimulationNote.vue'
import { ETAPE_DE, ETAPES, useEtapes } from './useEtapes'

// Volet « Suivi » : la validation vit ici, dans le fonctionnement global de l'offre,
// et non comme une étape de création. Le circuit vient du paramétrage de l'organisation.
const open = defineModel<boolean>('open', { default: false })

const { state, circuit, etapeEnCours, repondre, simulerContribution } = useOffre()
const { aller } = useEtapes()

const ICONES: Record<EtapeCircuit['statut'], { icon: string, label: string, cls: string }> = {
  a_venir: { icon: 'ri:checkbox-blank-circle-line', label: 'À venir', cls: 'todo' },
  en_attente: { icon: 'ri:time-line', label: 'En attente', cls: 'wait' },
  approuve: { icon: 'ri:checkbox-circle-fill', label: 'Validé', cls: 'ok' },
  corrections: { icon: 'ri:chat-1-line', label: 'Corrections demandées', cls: 'ko' },
}

const remarques = computed(() => [...state.remarques].reverse())
const correction = ref('')
const ouvrirCorrection = ref(false)

function demanderCorrection() {
  if (!correction.value.trim() || !etapeEnCours.value) {
    return
  }
  repondre(etapeEnCours.value.id, 'corrections', { texte: correction.value, stepId: 'offre' })
  correction.value = ''
  ouvrirCorrection.value = false
}

function voir(stepId: keyof typeof ETAPE_DE) {
  open.value = false
  aller(stepId)
}

const ROLES = { gestion: 'Gère le recrutement', evaluation: 'Évalue les candidatures', lecture: 'Consulte' }
const ajoutables = computed(() => PERSONNES.filter(p => !state.equipe.some(m => m.personneId === p.id)))
</script>

<template>
  <CspDrawer
    v-model:open="open"
    title="Suivi de l'offre"
    :description="`${state.reference} · ${LIBELLES_STATUT[state.statut].label}`"
    size="md"
  >
    <div class="suivi">
      <section>
        <h3 class="suivi__h">
          Validation
        </h3>
        <p
          v-if="!circuit.length"
          class="suivi__muted"
        >
          Votre organisation ne prévoit pas de validation pour ce type de recrutement : l'offre peut être publiée directement.
        </p>
        <template v-else>
          <p class="suivi__muted">
            Circuit appliqué selon le paramétrage de votre organisation.
          </p>
          <ol class="circuit">
            <li
              v-for="e in circuit"
              :key="e.id"
              :class="`circuit--${ICONES[e.statut].cls}`"
            >
              <CspIcon
                :name="ICONES[e.statut].icon"
                :size="16"
                class="circuit__icon"
              />
              <div class="circuit__body">
                <strong>{{ e.libelle }}</strong>
                <small>{{ personne(e.personneId).nom }} · {{ ICONES[e.statut].label }}<template v-if="e.externe"> avant la création de l'offre</template><template v-else-if="e.date"> · {{ e.date }}</template></small>
                <SimulationNote
                  v-if="etapeEnCours?.id === e.id && state.statut === 'a_valider'"
                  :titre="`Réponse de ${personne(e.personneId).nom.split(' ')[0]}`"
                >
                  <CspButton
                    label="Valider"
                    size="sm"
                    @click="repondre(e.id, 'approuve')"
                  />
                  <CspButton
                    label="Demander une correction"
                    size="sm"
                    variant="secondary"
                    @click="ouvrirCorrection = !ouvrirCorrection"
                  />
                </SimulationNote>
                <form
                  v-if="ouvrirCorrection && etapeEnCours?.id === e.id && state.statut === 'a_valider'"
                  class="circuit__form"
                  @submit.prevent="demanderCorrection"
                >
                  <CspTextarea
                    v-model="correction"
                    label="Remarque sur l'offre"
                    :rows="2"
                  />
                  <div>
                    <CspButton
                      type="submit"
                      label="Envoyer"
                      size="sm"
                      :disabled="!correction.trim()"
                    />
                  </div>
                </form>
              </div>
            </li>
          </ol>
        </template>
      </section>

      <section v-if="remarques.length">
        <h3 class="suivi__h">
          Remarques
        </h3>
        <ul class="list">
          <li
            v-for="r in remarques"
            :key="r.id"
          >
            <small>{{ personne(r.auteurId).nom }} · {{ r.date }}<template v-if="r.resolue"> · traitée</template></small>
            <p :class="{ list__done: r.resolue }">
              {{ r.texte }}
            </p>
            <button
              v-if="!r.resolue"
              type="button"
              class="link"
              @click="voir(r.stepId)"
            >
              Aller à « {{ ETAPES.find(x => x.id === ETAPE_DE[r.stepId])?.libelle }} »
            </button>
          </li>
        </ul>
      </section>

      <section v-if="state.contributions.length">
        <h3 class="suivi__h">
          Contributions
        </h3>
        <ul class="list">
          <li
            v-for="c in state.contributions"
            :key="c.id"
          >
            <small>{{ personne(c.personneId).nom }} · {{ c.statut === 'faite' ? 'reçue' : 'en attente' }}</small>
            <p>{{ c.demande }}</p>
            <SimulationNote v-if="c.statut === 'en_attente'">
              <CspButton
                label="Simuler sa réponse"
                size="sm"
                variant="tertiary"
                @click="simulerContribution(c.id)"
              />
            </SimulationNote>
          </li>
        </ul>
      </section>

      <section>
        <h3 class="suivi__h">
          Équipe de recrutement
        </h3>
        <p class="suivi__muted">
          Accès aux candidatures après publication.
        </p>
        <ul class="team">
          <li
            v-for="m in state.equipe"
            :key="m.personneId"
          >
            <span>{{ personne(m.personneId).nom }}<template v-if="m.personneId === 'camille'"> (vous)</template></span>
            <select
              v-model="m.acces"
              class="team__select"
              :aria-label="`Rôle de ${personne(m.personneId).nom}`"
              :disabled="m.personneId === 'camille'"
            >
              <option
                v-for="(l, v) in ROLES"
                :key="v"
                :value="v"
              >
                {{ l }}
              </option>
            </select>
          </li>
        </ul>
        <select
          v-if="ajoutables.length"
          class="team__select team__add"
          aria-label="Ajouter un membre à l'équipe"
          @change="e => { const v = (e.target as HTMLSelectElement).value; if (v) { state.equipe.push({ personneId: v, acces: 'lecture' }); (e.target as HTMLSelectElement).value = '' } }"
        >
          <option value="">
            + Ajouter un membre…
          </option>
          <option
            v-for="p in ajoutables"
            :key="p.id"
            :value="p.id"
          >
            {{ p.nom }} — {{ p.role }}
          </option>
        </select>
      </section>

      <section>
        <h3 class="suivi__h">
          Historique
        </h3>
        <ol class="journal">
          <li
            v-for="(j, i) in [...state.journal].reverse()"
            :key="i"
          >
            <small>{{ j.date }}</small>{{ j.texte }}
          </li>
        </ol>
      </section>
    </div>
  </CspDrawer>
</template>

<style scoped lang="scss">
.suivi {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
  font-size: var(--csp-font-size-sm);

  section {
    display: flex;
    flex-direction: column;
    gap: var(--csp-space-2);
  }

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }

  p {
    margin: 0;
  }
}

.suivi__h {
  margin: 0;
  font-size: var(--csp-font-size-base);
}

.suivi__muted {
  color: var(--text-mention-grey);
}

.circuit,
.list,
.team,
.journal {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  list-style: none;
}

.circuit li {
  display: flex;
  gap: var(--csp-space-2);
}

.circuit__icon {
  flex-shrink: 0;
  margin-top: 2px;
  color: var(--text-mention-grey);

  .circuit--ok & {
    color: var(--text-default-success);
  }

  .circuit--wait & {
    color: var(--text-action-high-blue-france);
  }
}

.circuit__body {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-1);
}

.circuit__form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  width: 100%;
}

.list li {
  padding-left: var(--csp-space-3);
  border-left: 2px solid var(--border-default-grey);
}

.list__done {
  color: var(--text-mention-grey);
}

.team li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-2);
}

.team__select {
  padding: var(--csp-space-1) var(--csp-space-2);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  font: inherit;
  font-size: var(--csp-font-size-xs);
  color: var(--text-default-grey);
}

.team__add {
  align-self: stretch;
  max-width: 100%;
}

.journal li {
  padding-left: var(--csp-space-3);
  border-left: 2px solid var(--border-default-grey);
}

.link {
  align-self: flex-start;
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  font-size: var(--csp-font-size-xs);
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}
</style>
