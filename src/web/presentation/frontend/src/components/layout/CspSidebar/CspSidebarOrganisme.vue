<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { useSidebar } from '@/composables/ui/useSidebar'
import { RECRUTEMENTS_TAB_ROUTE_NAMES } from '@/features/recrutements/routes'
import { useRouteOrganisme } from '@/stores/routeOrganisme'

const router = useRouter()
const { isExpanded, isMobile } = useSidebar()
const { organismes, organisme, organismeUuid } = useRouteOrganisme()

const showLabel = computed(() => isExpanded.value || isMobile.value)

function selectOrganisme(uuid: string) {
  if (uuid === organismeUuid.value) {
    return
  }
  void router.push({
    name: RECRUTEMENTS_TAB_ROUTE_NAMES.actifs,
    params: { organismeUuid: uuid },
  })
}

const sections = computed(() => [{
  items: organismes.value.map(candidat => ({
    label: candidat.nom,
    icon: candidat.organisme_uuid === organismeUuid.value
      ? 'ri:check-line'
      : 'ri:government-line',
    onSelect: () => selectOrganisme(candidat.organisme_uuid),
  })),
}])
</script>

<template>
  <CspDropdownMenu
    v-if="organisme"
    side="bottom"
    align="start"
    :sections="sections"
  >
    <template #trigger>
      <button
        type="button"
        class="csp-sidebar-organisme"
        :class="{ 'csp-sidebar-organisme--expanded': showLabel }"
        :aria-label="`Organisme : ${organisme.nom}. Changer d'organisme`"
      >
        <CspIcon
          name="ri:government-line"
          :size="18"
          class="csp-sidebar-organisme__icon"
        />
        <span
          v-if="showLabel"
          class="csp-sidebar-organisme__nom"
        >
          {{ organisme.nom }}
        </span>
        <CspIcon
          v-if="showLabel"
          name="ri:expand-up-down-line"
          :size="16"
          class="csp-sidebar-organisme__chevron"
        />
      </button>
    </template>
  </CspDropdownMenu>
</template>

<style scoped lang="scss">
.csp-sidebar-organisme {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  width: 100%;
  min-width: 0;
  padding: 0;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  background-color: var(--background-alt-grey);
  color: var(--text-default-grey);

  &:hover {
    background-color: var(--background-alt-grey-hover);
  }

  &:focus-visible {
    outline: var(--focus-ring);
    outline-offset: var(--csp-focus-ring-offset);
  }

  &--expanded {
    justify-content: flex-start;
    min-height: var(--sidebar-item-size, 2.5rem);
    padding: 0.375rem var(--sidebar-inset-x, 0.5rem);
  }
}

.csp-sidebar-organisme__icon {
  flex-shrink: 0;
  color: var(--text-mention-grey);
}

.csp-sidebar-organisme__nom {
  flex: 1;
  min-width: 0;
  font-size: 0.875rem;
  font-weight: 600;
  text-align: left;
  color: var(--text-title-grey);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.csp-sidebar-organisme__chevron {
  flex-shrink: 0;
  color: var(--text-mention-grey);
}
</style>
