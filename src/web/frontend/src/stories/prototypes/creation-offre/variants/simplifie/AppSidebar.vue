<script setup lang="ts">
import CspSidebar from '@/components/layout/CspSidebar/CspSidebar.vue'
import CspSidebarGroup from '@/components/layout/CspSidebar/CspSidebarGroup.vue'
import CspSidebarItem from '@/components/layout/CspSidebar/CspSidebarItem.vue'
import CspSidebarLogo from '@/components/layout/CspSidebar/CspSidebarLogo.vue'
import CspSidebarUser from '@/components/layout/CspSidebar/CspSidebarUser.vue'

// Navigation principale : les deux pages du parcours. La racine du prototype suit la route.
defineProps<{ page?: 'besoins' | 'offres' }>()
</script>

<template>
  <aside class="app-sidebar">
    <CspSidebar>
      <template #logo>
        <CspSidebarLogo />
      </template>
      <CspSidebarGroup>
        <CspSidebarItem
          icon="ri:file-list-3-line"
          label="Mes besoins en recrutement"
          :to="{ path: '/besoins' }"
          :is-active="page === 'besoins'"
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
