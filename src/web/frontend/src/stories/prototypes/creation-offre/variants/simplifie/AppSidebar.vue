<script setup lang="ts">
import CspSidebar from '@/components/layout/CspSidebar/CspSidebar.vue'
import CspSidebarGroup from '@/components/layout/CspSidebar/CspSidebarGroup.vue'
import CspSidebarItem from '@/components/layout/CspSidebar/CspSidebarItem.vue'
import CspSidebarLogo from '@/components/layout/CspSidebar/CspSidebarLogo.vue'
import CspSidebarUser from '@/components/layout/CspSidebar/CspSidebarUser.vue'

// Navigation principale de l'ATS (décor : seule l'entrée « Offres » est active dans le prototype).
</script>

<template>
  <aside class="app-sidebar">
    <CspSidebar>
      <template #logo>
        <CspSidebarLogo />
      </template>
      <CspSidebarGroup>
        <CspSidebarItem
          icon="ri:dashboard-line"
          label="Tableau de bord"
          :to="{ path: '/tableau-de-bord' }"
        />
        <CspSidebarItem
          icon="ri:briefcase-line"
          label="Offres"
          :to="{ path: '/offres' }"
          :is-active="true"
        />
        <CspSidebarItem
          icon="ri:team-line"
          label="Candidatures"
          :to="{ path: '/candidatures' }"
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
