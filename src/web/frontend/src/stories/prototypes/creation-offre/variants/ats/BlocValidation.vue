<script setup lang="ts">
import type { Offre } from './store'
import { computed, ref } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import SimulationNote from '../../shared/SimulationNote.vue'
import { useNav } from './nav'
import { db, forcerValidation, le, repondre } from './store'

// Bloc « Validation » : une ligne par validation, avec ses valideurs, l'état, la date et le commentaire.
// Les validations se font en parallèle ; l'accord d'un seul valideur suffit pour chacune.
// Les réponses des valideurs et le forçage par le superviseur sont simulés (encadrés violets).
const props = defineProps<{ offre: Offre, simulation?: boolean }>()
const { notifier } = useNav()
const o = computed(() => props.offre)

const ETATS = {
  attente: { label: 'En attente', type: 'info' as const },
  accord: { label: 'Accord', type: 'success' as const },
  refus: { label: 'Refusée', type: 'warning' as const },
}

const refusEn = ref<number | null>(null)
const commentaire = ref('')
const enCours = computed(() => o.value.validationEtat === 'en_attente')

function accorder(i: number) {
  const v = o.value.validations![i]!
  repondre(o.value, i, 'accord', v.valideurs[0] ?? v.nom)
  notifier(o.value.validationEtat === 'validee' ? 'Validation obtenue (simulation).' : `Accord du ${v.nom} (simulation).`)
}
function refuser(i: number) {
  if (!commentaire.value.trim()) {
    return
  }
  const v = o.value.validations![i]!
  repondre(o.value, i, 'refus', v.valideurs[0] ?? v.nom, commentaire.value.trim())
  refusEn.value = null
  commentaire.value = ''
  notifier('Offre refusée (simulation) : le demandeur la complète puis refait la demande.')
}
function forcer() {
  forcerValidation(o.value)
  notifier('Validation forcée par le superviseur (simulation).')
}
</script>

<template>
  <div class="bloc">
    <ul class="lignes">
      <li
        v-for="(v, i) in o.validations"
        :key="v.nom"
        class="ligne"
      >
        <div class="ligne__tete">
          <span>
            <strong>{{ v.nom }}</strong>
            <small>{{ v.valideurs.join(', ') || 'Aucun valideur désigné' }}</small>
          </span>
          <CspBadge
            :label="v.forcee ? 'Validation forcée' : ETATS[v.decision].label"
            :type="ETATS[v.decision].type"
            variant="soft"
            size="sm"
          />
        </div>
        <p
          v-if="v.decision !== 'attente'"
          class="ligne__detail"
        >
          {{ v.decision === 'accord' ? 'Accord' : 'Refus' }} de {{ v.par }} {{ le(v.le) }}<template v-if="v.commentaire">
            : « {{ v.commentaire }} »
          </template>
        </p>

        <template v-if="simulation && enCours && v.decision === 'attente'">
          <SimulationNote :titre="`Réponse du ${v.nom}`">
            <CspButton
              label="Valider"
              size="sm"
              @click="accorder(i)"
            />
            <CspButton
              label="Refuser"
              size="sm"
              variant="secondary"
              @click="refusEn = refusEn === i ? null : i"
            />
          </SimulationNote>
          <div
            v-if="refusEn === i"
            class="refus"
          >
            <CspTextarea
              v-model="commentaire"
              label="Commentaire (obligatoire) : ce qui manque ou le motif du refus"
              :rows="2"
            />
            <div>
              <CspButton
                label="Envoyer le refus"
                size="sm"
                :disabled="!commentaire.trim()"
                @click="refuser(i)"
              />
            </div>
          </div>
        </template>
      </li>
    </ul>
    <SimulationNote
      v-if="simulation && enCours"
      :titre="`Superviseur (${db.organisme.superviseur})`"
    >
      <CspButton
        label="Forcer la validation"
        size="sm"
        variant="tertiary"
        @click="forcer"
      />
    </SimulationNote>
  </div>
</template>

<style scoped lang="scss">
.bloc {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.lignes {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  list-style: none;
}

.ligne {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  padding-bottom: var(--csp-space-3);
  border-bottom: 1px solid var(--border-default-grey);
  font-size: var(--csp-font-size-sm);

  &:last-child {
    border-bottom: 0;
    padding-bottom: 0;
  }
}

.ligne__tete {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--csp-space-2);

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.ligne__detail {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.refus {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}
</style>
