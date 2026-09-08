<script setup lang="ts">
import type { ProtoCandidature } from '../data/mock'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import { ACTIVITE_ICONS, formatRelative } from '../shared/format'

defineProps<{
  candidature: ProtoCandidature
}>()
</script>

<template>
  <section class="historique">
    <h3 class="historique__title">
      Activités récentes ({{ candidature.activites.length }})
    </h3>
    <ol class="historique__list">
      <li
        v-for="activite in candidature.activites"
        :key="activite.uuid"
        class="historique__item"
      >
        <span class="historique__icon">
          <CspIcon
            :name="ACTIVITE_ICONS[activite.type]"
            :size="16"
            aria-hidden="true"
          />
        </span>
        <div class="historique__content">
          <p class="historique__text">
            <span
              v-if="activite.auteur"
              class="historique__auteur"
            >{{ activite.auteur }}</span>
            {{ activite.libelle }}
          </p>
          <div
            v-if="activite.tags?.length"
            class="historique__tags"
          >
            <CspTag
              v-for="tag in activite.tags"
              :key="tag"
              size="sm"
              :label="tag"
            />
          </div>
        </div>
        <time class="historique__time">{{ formatRelative(activite.date) }}</time>
      </li>
    </ol>
  </section>
</template>

<style scoped lang="scss">
.historique__title {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-mention-grey);
}

.historique__list {
  position: relative;
  margin: 0;
  padding: 0;
  list-style: none;

  &::before {
    position: absolute;
    top: 1rem;
    bottom: 1rem;
    left: 1rem;
    width: 1px;
    content: '';
    background: var(--border-default-grey);
  }
}

.historique__item {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) 0;
}

.historique__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 2rem;
  height: 2rem;
  color: var(--text-action-high-grey);
  background: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
}

.historique__content {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: var(--csp-space-2);
  min-width: 0;
  padding-top: 0.375rem;
}

.historique__text {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-default-grey);
}

.historique__auteur {
  color: var(--text-mention-grey);
}

.historique__tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
}

.historique__time {
  flex-shrink: 0;
  padding-top: 0.375rem;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}
</style>
