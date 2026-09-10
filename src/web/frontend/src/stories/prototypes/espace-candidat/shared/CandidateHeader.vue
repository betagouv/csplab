<script setup lang="ts">
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

export type CandidatePage = 'accueil' | 'conversations' | 'documents'

withDefaults(defineProps<{
  variant?: 'public' | 'connected'
  userName?: string
  currentPage?: CandidatePage
  unreadCount?: number
}>(), {
  variant: 'public',
  userName: 'Camille Rousseau',
  currentPage: 'accueil',
  unreadCount: 0,
})

defineEmits<{
  navigate: [page: CandidatePage]
}>()
</script>

<template>
  <header class="candidate-header">
    <div class="candidate-header__brand">
      <span class="candidate-header__title">CSPLab</span>
      <span class="candidate-header__subtitle">Espace candidat</span>
    </div>

    <nav
      v-if="variant === 'connected'"
      class="candidate-header__nav"
      aria-label="Navigation espace candidat"
    >
      <button
        type="button"
        class="candidate-header__nav-item"
        :class="{ 'candidate-header__nav-item--active': currentPage === 'accueil' }"
        @click="$emit('navigate', 'accueil')"
      >
        Mes candidatures
      </button>
      <button
        type="button"
        class="candidate-header__nav-item"
        :class="{ 'candidate-header__nav-item--active': currentPage === 'conversations' }"
        @click="$emit('navigate', 'conversations')"
      >
        Messages
        <CspBadge
          v-if="unreadCount > 0"
          :label="String(unreadCount)"
          type="info"
          size="sm"
        />
      </button>
      <button
        type="button"
        class="candidate-header__nav-item"
        :class="{ 'candidate-header__nav-item--active': currentPage === 'documents' }"
        @click="$emit('navigate', 'documents')"
      >
        Documents
      </button>
    </nav>

    <div class="candidate-header__end">
      <CspDropdownMenu
        v-if="variant === 'connected'"
        :sections="[{ items: [
          { label: 'Mon profil', icon: 'ri:user-line' },
          { label: 'Se déconnecter', icon: 'ri:logout-box-line' },
        ] }]"
        align="end"
        side="bottom"
      >
        <template #trigger>
          <button
            type="button"
            class="candidate-header__user"
          >
            <CspAvatar
              :name="userName"
              size="sm"
            />
            <span class="candidate-header__user-name">{{ userName }}</span>
            <CspIcon
              name="ri:arrow-down-s-line"
              :size="16"
            />
          </button>
        </template>
      </CspDropdownMenu>
      <span
        v-else
        class="candidate-header__hint"
      >
        Pas besoin de compte pour candidater
      </span>
    </div>
  </header>
</template>

<style scoped lang="scss">
.candidate-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-4);
  padding: var(--csp-space-3) var(--csp-space-6);
  background-color: var(--background-default-grey);
  box-shadow: inset 0 -1px 0 var(--border-default-grey);
}

.candidate-header__brand {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
  min-width: 0;
}

.candidate-header__title {
  font-size: 1.125rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--text-action-high-blue-france);
  white-space: nowrap;
}

.candidate-header__subtitle {
  margin-top: 0.125rem;
  font-size: 0.6875rem;
  font-weight: 500;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.candidate-header__nav {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
}

.candidate-header__nav-item {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-2);
  border: none;
  background: none;
  cursor: pointer;
  padding: var(--csp-space-2) var(--csp-space-3);
  border-radius: 0.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-mention-grey);

  &:hover {
    background-color: var(--background-alt-grey);
    color: var(--text-default-grey);
  }

  &--active {
    color: var(--text-action-high-blue-france);
    background-color: var(--background-alt-blue-france);
  }
}

.candidate-header__end {
  display: flex;
  align-items: center;
}

.candidate-header__hint {
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.candidate-header__user {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  border: none;
  background: none;
  cursor: pointer;
  padding: var(--csp-space-1) var(--csp-space-2);
  border-radius: 0.25rem;
  color: var(--text-default-grey);

  &:hover {
    background-color: var(--background-alt-grey);
  }
}

.candidate-header__user-name {
  font-size: 0.875rem;
  font-weight: 500;
}
</style>
