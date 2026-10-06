<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSidebarDropdown from '@/components/layout/CspSidebar/CspSidebarDropdown.vue'
import { RECRUTEMENTS_TAB_ROUTE_NAMES } from '@/router/names'
import { useRouteOrganisme } from '@/stores/routeOrganisme'

const router = useRouter()
const { organismes, organisme, organismeUuid } = useRouteOrganisme()

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
  <CspSidebarDropdown
    v-if="organisme"
    side="bottom"
    align="start"
    :sections="sections"
    :title="organisme.nom"
    :aria-label="`Organisme : ${organisme.nom}. Changer d'organisme`"
  >
    <template #leading>
      <span class="csp-sidebar-organisme__icon">
        <CspIcon
          name="ri:government-line"
          :size="18"
        />
      </span>
    </template>
  </CspSidebarDropdown>
</template>

<style scoped lang="scss">
.csp-sidebar-organisme__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: var(--sidebar-leading-size);
  height: var(--sidebar-leading-size);
  color: var(--text-mention-grey);
}
</style>
