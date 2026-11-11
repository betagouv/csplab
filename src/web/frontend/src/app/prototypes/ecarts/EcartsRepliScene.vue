<script setup lang="ts">
import { onMounted, useTemplateRef } from 'vue'
import CspSidebar from '@/components/layout/CspSidebar/CspSidebar.vue'
import CspSidebarGroup from '@/components/layout/CspSidebar/CspSidebarGroup.vue'
import CspSidebarItem from '@/components/layout/CspSidebar/CspSidebarItem.vue'
import CspSidebarLogo from '@/components/layout/CspSidebar/CspSidebarLogo.vue'
import CspSidebarProvider from '@/components/layout/CspSidebar/CspSidebarProvider.vue'
import CspSidebarUser from '@/components/layout/CspSidebar/CspSidebarUser.vue'

const root = useTemplateRef<HTMLElement>('root')

const HOVERED = ['.csp-sidebar__toggle', '.csp-sidebar-item:not(.csp-sidebar-item--active)', '.csp-sidebar-button']

onMounted(() => {
  for (const selector of HOVERED) {
    root.value?.querySelector(selector)?.classList.add('ecarts-survol')
  }
})
</script>

<template>
  <div
    ref="root"
    class="ecarts-repli"
  >
    <CspSidebarProvider
      :default-expanded="true"
      :persist-state="false"
    >
      <aside class="ecarts-repli__aside">
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
              icon="ri:home-line"
              label="Accueil"
              :to="{ path: '/accueil' }"
              :is-active="true"
            />
            <CspSidebarItem
              icon="ri:mail-line"
              label="Messages"
              :to="{ path: '/messages' }"
            />
          </CspSidebarGroup>

          <CspSidebarGroup>
            <CspSidebarItem
              icon="ri:settings-3-line"
              label="Paramètres"
              :to="{ path: '/parametres' }"
            />
          </CspSidebarGroup>

          <template #footer>
            <CspSidebarUser
              name="Camille Martin"
              role="Administratrice"
            />
          </template>
        </CspSidebar>
      </aside>
    </CspSidebarProvider>
  </div>
</template>

<style scoped lang="scss">
.ecarts-repli {
  display: flex;
  height: 100vh;
}

.ecarts-repli__aside {
  flex-shrink: 0;
  border-right: 1px solid var(--border-default-grey);
}
</style>
