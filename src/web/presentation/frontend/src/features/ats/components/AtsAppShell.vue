<script setup lang="ts">
import CspAppLayout from '@/components/layout/CspAppLayout/CspAppLayout.vue'
import {
  CspSidebar,
  CspSidebarGroup,
  CspSidebarItem,
  CspSidebarLogo,
  CspSidebarProvider,
  CspSidebarTrigger,
  CspSidebarUser,
} from '@/components/layout/CspSidebar'
</script>

<template>
  <CspSidebarProvider default-expanded>
    <CspAppLayout>
      <template #sidebar>
        <CspSidebar>
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

      <template #header>
        <CspSidebarTrigger />
      </template>

      <slot />
    </CspAppLayout>
  </CspSidebarProvider>
</template>
