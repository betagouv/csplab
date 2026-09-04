<script setup lang="ts">
import type { NavItem } from './CspAppShell.types'
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { isNavItemActive } from '@/app/navigation'
import CspSidebar from '@/components/layout/CspSidebar/CspSidebar.vue'
import CspSidebarItem from '@/components/layout/CspSidebar/CspSidebarItem.vue'
import CspSidebarLogo from '@/components/layout/CspSidebar/CspSidebarLogo.vue'
import CspSidebarOrganisme from '@/components/layout/CspSidebar/CspSidebarOrganisme.vue'
import CspSidebarProvider from '@/components/layout/CspSidebar/CspSidebarProvider.vue'
import CspSidebarTrigger from '@/components/layout/CspSidebar/CspSidebarTrigger.vue'
import CspSidebarUser from '@/components/layout/CspSidebar/CspSidebarUser.vue'
import { useCurrentUser } from '@/stores/currentUser'

const props = defineProps<{
  navigation: NavItem[]
}>()

const route = useRoute()
const router = useRouter()
const { user, displayName } = useCurrentUser()

const navItems = computed(() => {
  return props.navigation.filter((item) => {
    if (!router.hasRoute(item.to)) {
      console.warn(`Route "${item.to}" does not exist. Please check your navigation configuration.`)
      return false
    }
    return true
  })
})

function isItemActive(item: NavItem): boolean {
  const matchedNames = route.matched
    .map(record => record.name)
    .filter((name): name is string => typeof name === 'string')
  return isNavItemActive(item, matchedNames)
}
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

          <CspSidebarOrganisme />

          <CspSidebarItem
            v-for="item in navItems"
            :key="item.to"
            :icon="item.icon"
            :label="item.label"
            :to="{ name: item.to, params: item.params }"
            :is-active="isItemActive(item)"
          />

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
