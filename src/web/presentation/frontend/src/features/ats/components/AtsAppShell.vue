<script setup lang="ts">
import CspAppLayout from '@/components/layout/CspAppLayout/CspAppLayout.vue'
import CspSidebar from '@/components/layout/CspSidebar/CspSidebar.vue'
import CspSidebarGroup from '@/components/layout/CspSidebar/CspSidebarGroup.vue'
import CspSidebarItem from '@/components/layout/CspSidebar/CspSidebarItem.vue'
import CspSidebarLogo from '@/components/layout/CspSidebar/CspSidebarLogo.vue'
import CspSidebarUser from '@/components/layout/CspSidebar/CspSidebarUser.vue'
</script>

<template>
  <CspAppLayout>
    <template #sidebar>
      <CspSidebar default-expanded>
        <template #logo>
          <CspSidebarLogo />
        </template>

        <CspSidebarGroup label="Pilotage">
          <CspSidebarItem
            icon="ri:dashboard-line"
            label="Tableau de bord"
          />
          <CspSidebarItem
            icon="ri:briefcase-line"
            label="Mes offres"
            is-active
          />
        </CspSidebarGroup>

        <CspSidebarGroup label="Candidatures">
          <CspSidebarItem
            icon="ri:group-line"
            label="Toutes les candidatures"
          />
          <CspSidebarItem
            icon="ri:layout-column-line"
            label="Pipeline"
          />
        </CspSidebarGroup>

        <CspSidebarGroup label="Entretiens">
          <CspSidebarItem
            icon="ri:calendar-line"
            label="Mes entretiens"
          />
        </CspSidebarGroup>

        <CspSidebarGroup label="Paramètres">
          <CspSidebarItem
            icon="ri:settings-3-line"
            label="Paramètres"
          />
        </CspSidebarGroup>

        <template #footer>
          <CspSidebarUser
            name="Marie Dupont"
            role="RH"
          />
        </template>
      </CspSidebar>
    </template>

    <slot />
  </CspAppLayout>
</template>
