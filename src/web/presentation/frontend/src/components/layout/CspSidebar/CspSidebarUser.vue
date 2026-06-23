<script setup lang="ts">
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { useColorMode } from '@/composables/useColorMode'
import { useSidebar } from '@/composables/useSidebar'

interface CspSidebarUserProps {
  name: string
  role?: string
}

defineProps<CspSidebarUserProps>()

const { isExpanded, isMobile } = useSidebar()
const { isDark, toggle: toggleColorMode } = useColorMode()
</script>

<template>
  <CspDropdownMenu
    side="right"
    align="end"
    :sections="[
      {
        items: [
          {
            label: isDark ? 'Mode clair' : 'Mode sombre',
            icon: isDark ? 'ri:sun-line' : 'ri:moon-line',
            onSelect: toggleColorMode,
          },
        ],
      },
      {
        items: [
          {
            label: 'Mon profil',
            icon: 'ri:user-line',
          },
          {
            label: 'Paramètres',
            icon: 'ri:settings-3-line',
          },
        ],
      },
      {
        items: [
          {
            label: 'Se déconnecter',
            icon: 'ri:logout-box-r-line',
            destructive: true,
          },
        ],
      },
    ]"
  >
    <template #trigger>
      <button
        type="button"
        class="csp-sidebar-user"
        :class="{ 'csp-sidebar-user--expanded': isExpanded || isMobile }"
      >
        <CspAvatar
          :name="name"
          size="md"
        />
        <div
          v-if="isExpanded || isMobile"
          class="csp-sidebar-user__info"
        >
          <span class="csp-sidebar-user__name">{{ name }}</span>
          <span
            v-if="role"
            class="csp-sidebar-user__role"
          >{{ role }}</span>
        </div>
        <CspIcon
          v-if="isExpanded || isMobile"
          name="ri:expand-up-down-line"
          :size="16"
          class="csp-sidebar-user__chevron"
        />
      </button>
    </template>
  </CspDropdownMenu>
</template>

<style scoped lang="scss">
.csp-sidebar-user {
  --container-padding-compensation: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  margin: calc(var(--container-padding-compensation) * -1);
  min-width: 0;
  cursor: pointer;
  background-color: var(--background-alt-grey);

  &:hover {
    background-color: var(--background-alt-grey-hover);
  }

  &:active {
    background-color: var(--background-alt-grey-active);
  }

  &:focus-visible {
    outline: var(--focus-ring);
    outline-offset: var(--csp-focus-ring-offset);
  }

  &--expanded {
    justify-content: flex-start;
    min-height: var(--sidebar-item-size, 2.5rem);
    padding: calc(0.375rem + var(--container-padding-compensation))
      calc(var(--sidebar-inset-x, 0.5rem) + var(--container-padding-compensation));
  }
}

.csp-sidebar-user__info {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
  text-align: left;
  line-height: 1.2;
}

.csp-sidebar-user__name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-title-grey);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.csp-sidebar-user__role {
  font-size: 0.75rem;
  color: var(--text-mention-grey);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.csp-sidebar-user__chevron {
  flex-shrink: 0;
  color: var(--text-mention-grey);
}
</style>
