<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

export type OngletCandidat = 'candidatures' | 'messages' | 'documents' | 'profil'

withDefaults(defineProps<{
  actif: OngletCandidat
  messagesNonLus?: number
}>(), {
  messagesNonLus: 0,
})

defineEmits<{
  changer: [onglet: OngletCandidat]
}>()

const onglets: { key: OngletCandidat, label: string, icon: string }[] = [
  { key: 'candidatures', label: 'Candidatures', icon: 'ri:briefcase-line' },
  { key: 'messages', label: 'Messages', icon: 'ri:message-3-line' },
  { key: 'documents', label: 'Documents', icon: 'ri:folder-line' },
  { key: 'profil', label: 'Profil', icon: 'ri:user-line' },
]
</script>

<template>
  <nav
    class="tabbar"
    aria-label="Navigation espace candidat"
  >
    <button
      v-for="onglet in onglets"
      :key="onglet.key"
      type="button"
      class="tabbar__item"
      :class="{ 'tabbar__item--actif': actif === onglet.key }"
      @click="$emit('changer', onglet.key)"
    >
      <span class="tabbar__icon-wrap">
        <CspIcon
          :name="onglet.icon"
          :size="20"
        />
        <span
          v-if="onglet.key === 'messages' && messagesNonLus > 0"
          class="tabbar__badge"
        >{{ messagesNonLus }}</span>
      </span>
      <span class="tabbar__label">{{ onglet.label }}</span>
    </button>
  </nav>
</template>

<style scoped lang="scss">
.tabbar {
  position: sticky;
  bottom: 0;
  z-index: 10;
  display: flex;
  background-color: var(--background-default-grey);
  box-shadow: inset 0 1px 0 var(--border-default-grey), 0 -2px 8px rgb(0 0 0 / 6%);
  padding-bottom: env(safe-area-inset-bottom);
}

.tabbar__item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.1875rem;
  border: none;
  background: none;
  cursor: pointer;
  padding: var(--csp-space-2) var(--csp-space-1);
  min-height: 3.25rem;
  color: var(--text-mention-grey);

  &--actif {
    color: var(--text-action-high-blue-france);
  }
}

.tabbar__icon-wrap {
  position: relative;
  display: flex;
}

.tabbar__badge {
  position: absolute;
  top: -0.25rem;
  right: -0.5rem;
  min-width: 1rem;
  height: 1rem;
  padding: 0 0.25rem;
  border-radius: 999px;
  background-color: var(--background-action-high-blue-france);
  color: var(--text-inverted-blue-france);
  font-size: 0.625rem;
  font-weight: 700;
  line-height: 1rem;
  text-align: center;
}

.tabbar__label {
  font-size: 0.6875rem;
  font-weight: 600;
}
</style>
