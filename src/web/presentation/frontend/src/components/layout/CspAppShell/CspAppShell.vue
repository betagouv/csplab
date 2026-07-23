<script setup lang="ts">
import type { NavGroup } from './CspAppShell.types'
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CspSidebar from '@/components/layout/CspSidebar/CspSidebar.vue'
import CspSidebarGroup from '@/components/layout/CspSidebar/CspSidebarGroup.vue'
import CspSidebarItem from '@/components/layout/CspSidebar/CspSidebarItem.vue'
import CspSidebarLogo from '@/components/layout/CspSidebar/CspSidebarLogo.vue'
import CspSidebarProvider from '@/components/layout/CspSidebar/CspSidebarProvider.vue'
import CspSidebarTrigger from '@/components/layout/CspSidebar/CspSidebarTrigger.vue'
import CspSidebarUser from '@/components/layout/CspSidebar/CspSidebarUser.vue'
import { useCurrentUser } from '@/stores/currentUser'

const props = defineProps<{
  navigation: NavGroup[]
}>()

const route = useRoute()
const router = useRouter()
const { user, displayName } = useCurrentUser()

const navGroups = computed(() => {
  return props.navigation
    .map(group => ({
      ...group,
      items: group.items.filter(item => router.hasRoute(item.to)),
    }))
    .filter(group => group.items.length > 0)
})
</script>

<template>
  <div class="csp-app-shell">
    <CspSidebarProvider
      v-if="user"
      default-expanded
    >
      <aside class="csp-app-shell__sidebar">
        <CspSidebar>
          <template #logo>
            <CspSidebarLogo />
          </template>

          <CspSidebarGroup
            v-for="group in navGroups"
            :key="group.label"
            :label="group.label"
          >
            <CspSidebarItem
              v-for="item in group.items"
              :key="item.to"
              :icon="item.icon"
              :label="item.label"
              :to="{ name: item.to }"
              :is-active="route.name === item.to"
            />
          </CspSidebarGroup>

          <template #footer>
            <CspSidebarUser :name="displayName" />
          </template>
        </CspSidebar>
      </aside>
      <div class="csp-app-shell__content">
        <header class="csp-app-shell__header">
          <CspSidebarTrigger />
        </header>
        <div class="csp-app-shell__main">
          <slot />
        </div>
      </div>
    </CspSidebarProvider>
  </div>
</template>

<style scoped lang="scss">
.csp-app-shell {
  display: flex;
  min-height: 100vh;
}

.csp-app-shell__sidebar {
  flex-shrink: 0;
  min-height: 100vh;
  overflow: hidden;
  background: var(--background-alt-grey);
  border-right: 1px solid var(--border-default-grey);

  @media (width <= 768px) {
    display: none;
  }
}

.csp-app-shell__content {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.csp-app-shell__header {
  display: none;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
  padding: 0.75rem 1rem;
  background: var(--background-default-grey);
  border-bottom: 1px solid var(--border-default-grey);

  @media (width <= 768px) {
    display: flex;
  }
}

.csp-app-shell__main {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow-x: auto;
}
</style>
