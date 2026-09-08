<script setup lang="ts">
import type { ProtoCandidature } from '../data/mock'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

defineProps<{
  candidature: ProtoCandidature
}>()
</script>

<template>
  <section class="documents">
    <h3 class="documents__title">
      {{ candidature.documents.length }} document{{ candidature.documents.length > 1 ? 's' : '' }}
    </h3>
    <ul class="documents__list">
      <li
        v-for="document in candidature.documents"
        :key="document.uuid"
        class="documents__item"
      >
        <CspIcon
          name="ri:file-list-line"
          :size="20"
          aria-hidden="true"
        />
        <div class="documents__content">
          <p class="documents__name">
            {{ document.nom }}
          </p>
          <p class="documents__meta">
            {{ document.type }} · {{ document.taille }}
          </p>
        </div>
        <CspButton
          label="Voir"
          variant="tertiary"
          size="sm"
          icon="ri:eye-line"
          is-icon-left
        />
        <CspButton
          label="Télécharger"
          variant="tertiary"
          size="sm"
          icon="ri:download-line"
          is-icon-left
        />
      </li>
    </ul>
  </section>
</template>

<style scoped lang="scss">
.documents__title {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-mention-grey);
}

.documents__list {
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  list-style: none;
  border: 1px solid var(--border-default-grey);
}

.documents__item {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);

  & + & {
    border-top: 1px solid var(--border-default-grey);
  }
}

.documents__content {
  flex: 1;
  min-width: 0;
}

.documents__name {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--text-title-grey);
}

.documents__meta {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}
</style>
