<script setup lang="ts">
import type { Page } from './useApp'
import CspSidebar from '@/components/layout/CspSidebar/CspSidebar.vue'
import CspSidebarGroup from '@/components/layout/CspSidebar/CspSidebarGroup.vue'
import CspSidebarItem from '@/components/layout/CspSidebar/CspSidebarItem.vue'
import CspSidebarLogo from '@/components/layout/CspSidebar/CspSidebarLogo.vue'
import CspSidebarUser from '@/components/layout/CspSidebar/CspSidebarUser.vue'

// Navigation principale. Le référentiel des fiches de poste est le point d'entrée ; la racine suit la route.
defineProps<{ page?: Page }>()
</script>

<template>
  <aside class="app-sidebar">
    <CspSidebar>
      <template #logo>
        <CspSidebarLogo />
      </template>
      <CspSidebarGroup>
        <CspSidebarItem
          icon="ri:file-text-line"
          label="Fiches de poste"
          :to="{ path: '/fiches' }"
          :is-active="page === 'fiches'"
        />
        <CspSidebarItem
          icon="ri:route-line"
          label="Recrutements"
          :to="{ path: '/recrutements' }"
          :is-active="page === 'recrutements'"
        />
        <CspSidebarItem
          icon="ri:briefcase-line"
          label="Mes offres"
          :to="{ path: '/offres' }"
          :is-active="page === 'offres'"
        />
      </CspSidebarGroup>
      <template #footer>
        <CspSidebarUser name="Camille Moreau" />
      </template>
    </CspSidebar>
  </aside>
</template>

<style scoped lang="scss">
.app-sidebar {
  flex-shrink: 0;
  height: 100vh;
  background: var(--background-alt-grey);
  border-right: 1px solid var(--border-default-grey);
}
</style>
