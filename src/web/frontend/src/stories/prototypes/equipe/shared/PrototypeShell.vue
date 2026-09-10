<script setup lang="ts">
import { computed } from 'vue'
import CspSidebar from '@/components/layout/CspSidebar/CspSidebar.vue'
import CspSidebarItem from '@/components/layout/CspSidebar/CspSidebarItem.vue'
import CspSidebarLogo from '@/components/layout/CspSidebar/CspSidebarLogo.vue'
import CspSidebarProvider from '@/components/layout/CspSidebar/CspSidebarProvider.vue'
import CspSidebarTrigger from '@/components/layout/CspSidebar/CspSidebarTrigger.vue'
import CspSidebarUser from '@/components/layout/CspSidebar/CspSidebarUser.vue'
import { useEquipePrototypeContext } from './context'

const proto = useEquipePrototypeContext()

const recrutementsActifs = computed(() => proto.page.value.name !== 'parametres-organisme')
</script>

<template>
  <div class="proto-shell">
    <CspSidebarProvider>
      <aside class="proto-shell__sidebar">
        <CspSidebar>
          <template #logo>
            <CspSidebarLogo />
          </template>
          <CspSidebarItem
            icon="ri:dashboard-line"
            label="Tableau de bord"
          />
          <CspSidebarItem
            icon="ri:briefcase-line"
            label="Recrutements"
            :is-active="recrutementsActifs"
            @click="proto.goRecrutements()"
          />
          <CspSidebarItem
            v-if="proto.peutGererOrganisme.value"
            icon="ri:settings-3-line"
            label="Paramètres de l'organisme"
            :is-active="!recrutementsActifs"
            @click="proto.goParametresOrganisme()"
          />
          <template #footer>
            <CspSidebarUser
              :name="proto.utilisateur.value.nom"
              :role="proto.utilisateur.value.role"
            />
          </template>
        </CspSidebar>
      </aside>
      <div class="proto-shell__content">
        <header class="proto-shell__mobile-header">
          <CspSidebarTrigger />
        </header>
        <div class="proto-shell__main">
          <slot />
        </div>
      </div>
    </CspSidebarProvider>
  </div>
</template>

<style scoped lang="scss">
.proto-shell {
  display: flex;
  min-height: 100vh;
  background: var(--background-default-grey);
}

.proto-shell__sidebar {
  flex-shrink: 0;
  min-height: 100vh;
  background: var(--background-alt-grey);
  border-right: 1px solid var(--border-default-grey);

  @media (width <= 768px) {
    display: none;
  }
}

.proto-shell__content {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.proto-shell__mobile-header {
  display: none;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-default-grey);

  @media (width <= 768px) {
    display: flex;
  }
}

.proto-shell__main {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}
</style>
