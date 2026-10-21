<script setup lang="ts">
import CspSidebar from '@/components/layout/CspSidebar/CspSidebar.vue'
import CspSidebarGroup from '@/components/layout/CspSidebar/CspSidebarGroup.vue'
import CspSidebarItem from '@/components/layout/CspSidebar/CspSidebarItem.vue'
import CspSidebarLogo from '@/components/layout/CspSidebar/CspSidebarLogo.vue'
import CspSidebarUser from '@/components/layout/CspSidebar/CspSidebarUser.vue'

// Navigation principale : tableau de bord, fiches de poste, offres d'emploi. La racine suit la route.
defineProps<{ actif: 'accueil' | 'fiches' | 'offres' }>()
</script>

<template>
  <aside class="ats-sidebar">
    <CspSidebar>
      <template #logo>
        <CspSidebarLogo />
      </template>
      <CspSidebarGroup>
        <CspSidebarItem
          icon="ri:home-4-line"
          label="Tableau de bord"
          :to="{ path: '/accueil' }"
          :is-active="actif === 'accueil'"
        />
        <CspSidebarItem
          icon="ri:file-text-line"
          label="Fiches de poste"
          :to="{ path: '/fiches' }"
          :is-active="actif === 'fiches'"
        />
        <CspSidebarItem
          icon="ri:megaphone-line"
          label="Offres d'emploi"
          :to="{ path: '/offres' }"
          :is-active="actif === 'offres'"
        />
      </CspSidebarGroup>
      <template #footer>
        <CspSidebarUser name="Camille Moreau" />
      </template>
    </CspSidebar>
  </aside>
</template>

<style scoped lang="scss">
.ats-sidebar {
  flex-shrink: 0;
  height: 100vh;
  background: var(--background-alt-grey);
  border-right: 1px solid var(--border-default-grey);
}
</style>
