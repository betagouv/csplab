<script setup lang="ts">
import type { TacheDashboard } from '../data/dashboardMock'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { computed } from 'vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import TacheRow from '../shared/TacheRow.vue'

const props = defineProps<{
  taches: TacheDashboard[]
}>()

const emit = defineEmits<{
  open: [id: string]
  toggleFait: [id: string]
}>()

const BREADCRUMB: CspBreadcrumbItem[] = [
  { label: 'Accueil' },
  { label: 'Mes tâches' },
]

const groupes = computed(() => {
  const actives = props.taches.filter(t => !t.fait)
  return [
    { key: 'retard', title: 'En retard', items: actives.filter(t => t.echeanceStatut === 'retard') },
    { key: 'aujourdhui', title: 'Aujourd\'hui', items: actives.filter(t => t.echeanceStatut === 'aujourdhui') },
    { key: 'venir', title: 'À venir', items: actives.filter(t => t.echeanceStatut === 'venir') },
  ].filter(groupe => groupe.items.length > 0)
})

const tachesFaites = computed(() => props.taches.filter(t => t.fait))
</script>

<template>
  <CspPageHeader
    title="Mes tâches"
    :breadcrumb="BREADCRUMB"
  >
    <template #subtitle>
      <p class="mtv__subtitle">
        Ce qu'il reste à faire, avec l'échéance et le recrutement concerné.
      </p>
    </template>
  </CspPageHeader>

  <CspPageContainer width="reading">
    <template v-if="groupes.length > 0">
      <div
        v-for="groupe in groupes"
        :key="groupe.key"
        class="mtv__groupe"
      >
        <h2 class="mtv__groupe-title">
          {{ groupe.title }}
        </h2>
        <ul class="mtv__list">
          <TacheRow
            v-for="tache in groupe.items"
            :key="tache.id"
            :tache="tache"
            @open="emit('open', $event)"
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

    <div
      v-if="tachesFaites.length > 0"
      class="mtv__groupe"
    >
      <h2 class="mtv__groupe-title">
        Faites
      </h2>
      <ul class="mtv__list">
        <TacheRow
          v-for="tache in tachesFaites"
          :key="tache.id"
          :tache="tache"
          @open="emit('open', $event)"
          @toggle-fait="emit('toggleFait', $event)"
        />
      </ul>
    </div>
  </CspPageContainer>
</template>

<style scoped lang="scss">
.mtv__subtitle {
  margin: 0;
  color: var(--text-mention-grey);
}

.mtv__groupe {
  margin-bottom: 2rem;
}

.mtv__groupe-title {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.mtv__list {
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  list-style: none;
}
</style>
