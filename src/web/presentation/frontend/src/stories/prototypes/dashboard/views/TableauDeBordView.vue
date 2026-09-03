<script setup lang="ts">
import type { RecrutementDashboard, TacheDashboard } from '../data/dashboardMock'
import type { AtsPage } from '../shared/AtsShell.vue'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import RecrutementCard from '../shared/RecrutementCard.vue'
import TacheRow from '../shared/TacheRow.vue'

const props = defineProps<{
  userFirstName: string
  recrutements: RecrutementDashboard[]
  taches: TacheDashboard[]
  layout: 'colonnes' | 'empile'
}>()

const emit = defineEmits<{
  navigate: [page: AtsPage]
  openRecrutement: [id: string]
  openTache: [id: string]
  toggleFait: [id: string]
}>()

function accord(count: number, singulier: string, pluriel: string): string {
  return count > 1 ? pluriel : singulier
}

const nouveauxCVTotal = computed(() => props.recrutements.reduce((acc, r) => acc + r.nouveauxCV, 0))
const candidaturesTotal = computed(() => props.recrutements.reduce((acc, r) => acc + r.candidaturesTotal, 0))
const candidaturesEnAttenteTotal = computed(() => props.recrutements.reduce((acc, r) => acc + r.candidaturesEnAttente, 0))
const entretiensAPreparerTotal = computed(() => props.recrutements.reduce((acc, r) => acc + r.entretiensAPreparer, 0))

const tachesActives = computed(() => props.taches.filter(t => !t.fait))
const tachesEnRetardTotal = computed(() => tachesActives.value.filter(t => t.echeanceStatut === 'retard').length)
const tachesAujourdhuiTotal = computed(() => tachesActives.value.filter(t => t.echeanceStatut === 'aujourdhui').length)

const nouveauxCVLabel = computed(() =>
  accord(nouveauxCVTotal.value, 'nouveau CV à traiter', 'nouveaux CV à traiter'),
)

interface RowATraiter {
  key: string
  page: AtsPage
  urgent: boolean
  count: number
  label: string
}

const secondaryRows = computed<RowATraiter[]>(() => {
  const rows: RowATraiter[] = []
  if (tachesEnRetardTotal.value > 0) {
    rows.push({
      key: 'retard',
      page: 'taches',
      urgent: true,
      count: tachesEnRetardTotal.value,
      label: accord(tachesEnRetardTotal.value, 'tâche en retard', 'tâches en retard'),
    })
  }
  if (candidaturesEnAttenteTotal.value > 0) {
    rows.push({
      key: 'attente',
      page: 'recrutements',
      urgent: false,
      count: candidaturesEnAttenteTotal.value,
      label: accord(candidaturesEnAttenteTotal.value, 'candidature en attente', 'candidatures en attente'),
    })
  }
  if (entretiensAPreparerTotal.value > 0) {
    rows.push({
      key: 'entretiens',
      page: 'recrutements',
      urgent: false,
      count: entretiensAPreparerTotal.value,
      label: accord(entretiensAPreparerTotal.value, 'entretien à préparer', 'entretiens à préparer'),
    })
  }
  if (tachesAujourdhuiTotal.value > 0) {
    rows.push({
      key: 'aujourdhui',
      page: 'taches',
      urgent: false,
      count: tachesAujourdhuiTotal.value,
      label: accord(tachesAujourdhuiTotal.value, 'tâche à échéance aujourd\'hui', 'tâches à échéance aujourd\'hui'),
    })
  }
  return rows
})

const recrutementsASurveiller = computed(() => {
  return [...props.recrutements]
    .sort((a, b) => (b.nouveauxCV - a.nouveauxCV) || (b.candidaturesEnAttente - a.candidaturesEnAttente))
    .slice(0, 3)
})

const ORDRE_ECHEANCE = { retard: 0, aujourdhui: 1, venir: 2 } as const

const tachesApercu = computed(() => {
  return [...tachesActives.value]
    .sort((a, b) => ORDRE_ECHEANCE[a.echeanceStatut] - ORDRE_ECHEANCE[b.echeanceStatut])
    .slice(0, 4)
})

const tachesGroupes = computed(() => {
  return [
    { key: 'retard', title: 'En retard', items: tachesApercu.value.filter(t => t.echeanceStatut === 'retard') },
    { key: 'aujourdhui', title: 'Aujourd\'hui', items: tachesApercu.value.filter(t => t.echeanceStatut === 'aujourdhui') },
    { key: 'venir', title: 'À venir', items: tachesApercu.value.filter(t => t.echeanceStatut === 'venir') },
  ].filter(groupe => groupe.items.length > 0)
})
</script>

<template>
  <div class="tdb">
    <header class="tdb__header">
      <h1 class="tdb__title">
        Bonjour {{ userFirstName }}
      </h1>
      <p class="tdb__subtitle">
        Voici ce qui mérite votre attention aujourd'hui.
      </p>
    </header>

    <section
      class="tdb__a-traiter"
      aria-labelledby="tdb-a-traiter-title"
    >
      <h2
        id="tdb-a-traiter-title"
        class="sr-only"
      >
        À traiter
      </h2>

      <button
        type="button"
        class="tdb__nouveaux-cv"
        :class="{ 'tdb__nouveaux-cv--calme': nouveauxCVTotal === 0 }"
        @click="emit('navigate', 'recrutements')"
      >
        <span class="tdb__nouveaux-cv-main">
          <span class="tdb__nouveaux-cv-number">{{ nouveauxCVTotal }}</span>
          <span class="tdb__nouveaux-cv-label">{{ nouveauxCVLabel }}</span>
        </span>
        <span class="tdb__nouveaux-cv-side">
          <span class="tdb__nouveaux-cv-total">{{ candidaturesTotal }} candidatures au total</span>
          <span class="tdb__nouveaux-cv-cta">
            Voir les candidatures
            <CspIcon
              name="ri:arrow-right-line"
              :size="16"
            />
          </span>
        </span>
      </button>

      <ul
        v-if="secondaryRows.length > 0"
        class="tdb__rows"
      >
        <li
          v-for="row in secondaryRows"
          :key="row.key"
        >
          <button
            type="button"
            class="tdb__row"
            :class="{ 'tdb__row--urgent': row.urgent }"
            @click="emit('navigate', row.page)"
          >
            <span class="tdb__row-text">
              <strong>{{ row.count }}</strong> {{ row.label }}
            </span>
            <CspIcon
              name="ri:arrow-right-s-line"
              :size="16"
            />
          </button>
        </li>
      </ul>
      <p
        v-else
        class="tdb__a-jour"
      >
        <CspIcon
          name="ri:checkbox-circle-line"
          :size="16"
        />
        Vous êtes à jour sur le reste.
      </p>
    </section>

    <div
      class="tdb__blocks"
      :class="`tdb__blocks--${layout}`"
    >
      <section
        class="tdb__block"
        aria-labelledby="tdb-recrutements-title"
      >
        <div class="tdb__block-header">
          <h2
            id="tdb-recrutements-title"
            class="tdb__block-title"
          >
            Mes recrutements
          </h2>
          <CspButton
            variant="tertiary-no-outline"
            size="sm"
            label="Voir tous mes recrutements"
            icon="ri:arrow-right-line"
            @click="emit('navigate', 'recrutements')"
          />
        </div>
        <div class="tdb__recrutements-list">
          <RecrutementCard
            v-for="recrutement in recrutementsASurveiller"
            :key="recrutement.id"
            :recrutement="recrutement"
            @open="emit('openRecrutement', $event)"
          />
        </div>
      </section>

      <section
        class="tdb__block"
        aria-labelledby="tdb-taches-title"
      >
        <div class="tdb__block-header">
          <h2
            id="tdb-taches-title"
            class="tdb__block-title"
          >
            Mes tâches
          </h2>
          <CspButton
            variant="tertiary-no-outline"
            size="sm"
            label="Voir toutes les tâches"
            icon="ri:arrow-right-line"
            @click="emit('navigate', 'taches')"
          />
        </div>

        <template v-if="tachesGroupes.length > 0">
          <div
            v-for="groupe in tachesGroupes"
            :key="groupe.key"
            class="tdb__taches-groupe"
          >
            <h3 class="tdb__taches-groupe-title">
              {{ groupe.title }}
            </h3>
            <ul class="tdb__taches-list">
              <TacheRow
                v-for="tache in groupe.items"
                :key="tache.id"
                :tache="tache"
                @open="emit('openTache', $event)"
                @toggle-fait="emit('toggleFait', $event)"
              />
            </ul>
          </div>
        </template>
        <CspEmptyState
          v-else
          title="Aucune tâche en attente"
          description="Vous êtes à jour."
          icon="ri:checkbox-circle-line"
        />
      </section>
    </div>
  </div>
</template>

<style scoped lang="scss">
.tdb {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  max-width: 64rem;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 3rem;
}

.tdb__title {
  margin: 0 0 0.25rem;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.tdb__subtitle {
  margin: 0;
  font-size: 1rem;
  color: var(--text-mention-grey);
}

.tdb__a-traiter {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-default-grey);
  border-radius: 0.5rem;
  overflow: hidden;
}

.tdb__nouveaux-cv {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  width: 100%;
  padding: 1.75rem 2rem;
  background: var(--background-alt-blue-france);
  border: none;
  cursor: pointer;
  text-align: left;

  &:hover {
    background: var(--background-alt-blue-france-hover);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: -2px;
  }

  &--calme {
    background: var(--background-alt-grey);

    &:hover {
      background: var(--background-alt-grey-hover);
    }

    .tdb__nouveaux-cv-number {
      color: var(--text-title-grey);
    }
  }
}

.tdb__nouveaux-cv-main {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
}

.tdb__nouveaux-cv-number {
  font-size: 3rem;
  font-weight: 700;
  line-height: 1;
  color: var(--text-active-blue-france);
  font-variant-numeric: tabular-nums;
}

.tdb__nouveaux-cv-label {
  font-size: 1.125rem;
  font-weight: 500;
  color: var(--text-title-grey);
}

.tdb__nouveaux-cv-side {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.tdb__nouveaux-cv-total {
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}

.tdb__nouveaux-cv-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--text-action-high-blue-france);
}

.tdb__rows {
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  list-style: none;
}

.tdb__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  width: 100%;
  padding: 1rem 2rem;
  background: none;
  border: none;
  border-top: 1px solid var(--border-default-grey);
  cursor: pointer;
  text-align: left;
  color: var(--text-mention-grey);

  &:hover {
    background: var(--background-alt-grey-hover);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: -2px;
  }
}

.tdb__row-text {
  font-size: 1rem;
  color: var(--text-title-grey);

  strong {
    font-weight: 700;
  }
}

.tdb__row--urgent .tdb__row-text strong {
  color: var(--text-default-error);
}

.tdb__a-jour {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
  padding: 1rem 2rem;
  border-top: 1px solid var(--border-default-grey);
  color: var(--text-mention-grey);
  font-size: 0.9375rem;
}

.tdb__blocks {
  display: grid;
  gap: 2rem;
}

.tdb__blocks--colonnes {
  grid-template-columns: repeat(2, 1fr);

  @media (width <= 900px) {
    grid-template-columns: 1fr;
  }
}

.tdb__blocks--empile {
  grid-template-columns: 1fr;
}

.tdb__block {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tdb__block-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.tdb__block-title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.tdb__recrutements-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.tdb__taches-groupe {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.tdb__taches-groupe-title {
  margin: 0.5rem 0 0;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--text-mention-grey);
}

.tdb__taches-list {
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  list-style: none;
}
</style>
