<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import CspAppLayout from '@/components/layout/CspAppLayout/CspAppLayout.vue'
import CspSidebar from '@/components/layout/CspSidebar/CspSidebar.vue'
import CspSidebarGroup from '@/components/layout/CspSidebar/CspSidebarGroup.vue'
import CspSidebarItem from '@/components/layout/CspSidebar/CspSidebarItem.vue'
import CspSidebarLogo from '@/components/layout/CspSidebar/CspSidebarLogo.vue'
import CspSidebarProvider from '@/components/layout/CspSidebar/CspSidebarProvider.vue'
import CspSidebarTrigger from '@/components/layout/CspSidebar/CspSidebarTrigger.vue'
import CspSidebarUser from '@/components/layout/CspSidebar/CspSidebarUser.vue'
import { useCurrentUser } from '@/composables/useCurrentUser'

const route = useRoute()
const { user, displayName, fetch: fetchUser } = useCurrentUser()

onMounted(() => {
  fetchUser()
})
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
              :as="RouterLink"
              to="/"
              icon="ri:briefcase-line"
              label="Mes offres"
              :is-active="route.name === 'home'"
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
              :as="RouterLink"
              to="/parametres"
              icon="ri:settings-3-line"
              label="Paramètres"
              :is-active="route.name === 'parametres'"
            />
          </CspSidebarGroup>

          <template #footer>
            <CspSidebarUser
              v-if="user"
              :name="displayName"
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
