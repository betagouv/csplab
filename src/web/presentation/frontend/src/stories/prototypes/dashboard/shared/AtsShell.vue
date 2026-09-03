<script setup lang="ts">
import CspSidebar from '@/components/layout/CspSidebar/CspSidebar.vue'
import CspSidebarGroup from '@/components/layout/CspSidebar/CspSidebarGroup.vue'
import CspSidebarItem from '@/components/layout/CspSidebar/CspSidebarItem.vue'
import CspSidebarLogo from '@/components/layout/CspSidebar/CspSidebarLogo.vue'
import CspSidebarProvider from '@/components/layout/CspSidebar/CspSidebarProvider.vue'
import CspSidebarTrigger from '@/components/layout/CspSidebar/CspSidebarTrigger.vue'
import CspSidebarUser from '@/components/layout/CspSidebar/CspSidebarUser.vue'

export type AtsPage = 'dashboard' | 'recrutements' | 'taches'

withDefaults(defineProps<{
  userName?: string
  userRole?: string
}>(), {
  userName: 'Alice Gourbat',
  userRole: 'Chargée de recrutement',
})

const page = defineModel<AtsPage>('page', { default: 'dashboard' })
</script>

<template>
  <div class="ats-shell">
    <CspSidebarProvider default-expanded>
      <aside class="ats-shell__sidebar">
        <CspSidebar>
          <template #logo>
            <CspSidebarLogo />
          </template>

          <CspSidebarGroup label="Navigation">
            <CspSidebarItem
              icon="ri:dashboard-line"
              label="Tableau de bord"
              :is-active="page === 'dashboard'"
              @click="page = 'dashboard'"
            />
            <CspSidebarItem
              icon="ri:briefcase-line"
              label="Mes recrutements"
              :is-active="page === 'recrutements'"
              @click="page = 'recrutements'"
            />
            <CspSidebarItem
              icon="ri:checkbox-line"
              label="Mes tâches"
              :is-active="page === 'taches'"
              @click="page = 'taches'"
            />
          </CspSidebarGroup>

          <template #footer>
            <CspSidebarUser
              :name="userName"
              :role="userRole"
            />
          </template>
        </CspSidebar>
      </aside>

      <div class="ats-shell__content">
        <header class="ats-shell__mobile-header">
          <CspSidebarTrigger />
        </header>
        <div class="ats-shell__main">
          <slot :page="page" />
        </div>
      </div>
    </CspSidebarProvider>
  </div>
</template>

<style scoped lang="scss">
.ats-shell {
  display: flex;
  min-height: 100vh;
  background: var(--background-default-grey);
}

.ats-shell__sidebar {
  flex-shrink: 0;
  min-height: 100vh;
  background: var(--background-alt-grey);
  border-right: 1px solid var(--border-default-grey);

  @media (width <= 768px) {
    display: none;
  }
}

.ats-shell__content {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.ats-shell__mobile-header {
  display: none;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-default-grey);

  @media (width <= 768px) {
    display: flex;
  }
}

.ats-shell__main {
  flex: 1;
  min-width: 0;
}
</style>
