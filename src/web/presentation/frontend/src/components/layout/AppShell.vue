<script setup lang="ts">
import type { NavGroup } from './AppShell.types'
import { storeToRefs } from 'pinia'
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CspAppLayout from '@/components/layout/CspAppLayout/CspAppLayout.vue'
import CspSidebar from '@/components/layout/CspSidebar/CspSidebar.vue'
import CspSidebarGroup from '@/components/layout/CspSidebar/CspSidebarGroup.vue'
import CspSidebarItem from '@/components/layout/CspSidebar/CspSidebarItem.vue'
import CspSidebarLogo from '@/components/layout/CspSidebar/CspSidebarLogo.vue'
import CspSidebarProvider from '@/components/layout/CspSidebar/CspSidebarProvider.vue'
import CspSidebarTrigger from '@/components/layout/CspSidebar/CspSidebarTrigger.vue'
import CspSidebarUser from '@/components/layout/CspSidebar/CspSidebarUser.vue'
import { useCurrentUserStore } from '@/stores/currentUser'

const props = defineProps<{
  navigation: NavGroup[]
}>()

const route = useRoute()
const router = useRouter()
const currentUserStore = useCurrentUserStore()
const { user, displayName } = storeToRefs(currentUserStore)

const navGroups = computed(() => {
  return props.navigation
    .map(group => ({
      ...group,
      items: group.items.filter(item => router.hasRoute(item.to)),
    }))
    .filter(group => group.items.length > 0)
})

onMounted(() => {
  currentUserStore.fetch()
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
