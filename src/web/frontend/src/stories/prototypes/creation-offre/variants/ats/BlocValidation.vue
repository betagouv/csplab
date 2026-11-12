<script setup lang="ts">
import type { Offre } from './store'
import { computed, ref } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { useNav } from './nav'
import { db, forcerValidation, le, repondre } from './store'

// Bloc « Validation » : une ligne par validation, avec ses valideurs, l'état, la date et le commentaire.
// Les validations se font en parallèle ; l'accord d'un seul valideur suffit pour chacune.
// Les réponses des valideurs et le forçage par le superviseur sont simulés : regroupés sous un lien replié
// « Simuler la réponse des valideurs (proto) », pour que l'encart montre ce que voit vraiment le demandeur.
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
const simuOuverte = ref(false)
const enAttente = computed(() => (o.value.validations ?? []).map((v, i) => ({ v, i })).filter(x => x.v.decision === 'attente'))

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
        v-for="v in o.validations"
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
      </li>
    </ul>

    <div
      v-if="simulation && enCours"
      class="simu"
    >
      <button
        type="button"
        class="simu__lien"
        :aria-expanded="simuOuverte"
        @click="simuOuverte = !simuOuverte"
      >
        <CspIcon
          name="ri:flask-line"
          :size="14"
        />
        Simuler la réponse des valideurs (proto)
        <CspIcon
          :name="simuOuverte ? 'ri:arrow-up-s-line' : 'ri:arrow-down-s-line'"
          :size="16"
        />
      </button>
      <div
        v-if="simuOuverte"
        class="simu__corps"
      >
        <p class="simu__explication">
          N'existe pas dans le produit : chaque valideur répond depuis son propre compte. Ces boutons servent seulement à faire avancer le scénario.
        </p>
        <template
          v-for="x in enAttente"
          :key="x.v.nom"
        >
          <div class="simu__ligne">
            <span>Jouer <strong>{{ x.v.valideurs[0] ?? x.v.nom }}</strong> ({{ x.v.nom }})</span>
            <span class="simu__boutons">
              <CspButton
                label="Valider"
                size="sm"
                @click="accorder(x.i)"
              />
              <CspButton
                label="Refuser"
                size="sm"
                variant="secondary"
                @click="refusEn = refusEn === x.i ? null : x.i"
              />
            </span>
          </div>
          <div
            v-if="refusEn === x.i"
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
                @click="refuser(x.i)"
              />
            </div>
          </div>
        </template>
        <div class="simu__ligne">
          <span>Jouer <strong>{{ db.organisme.superviseur }}</strong> (superviseur)</span>
          <span class="simu__boutons">
            <CspButton
              label="Forcer la validation"
              size="sm"
              variant="tertiary"
              @click="forcer"
            />
          </span>
        </div>
      </div>
    </div>
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

.simu {
  margin-top: var(--csp-space-2);
  padding: var(--csp-space-3);
  border: 1px dashed var(--border-plain-purple-glycine, #a558a0);
  background: var(--background-alt-purple-glycine, #fbf5fa);
}

.simu__lien {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-label-purple-glycine, #6e445a);
  cursor: pointer;

  &:hover {
    text-decoration: underline;
  }
}

.simu__corps {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin-top: var(--csp-space-3);
}

.simu__explication {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.simu__ligne {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-2);
  font-size: var(--csp-font-size-sm);
}

.simu__boutons {
  display: flex;
  gap: var(--csp-space-2);
}

.refus {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}
</style>
