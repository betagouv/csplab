<script setup lang="ts">
import { PiniaColadaDevtools } from '@pinia/colada-devtools'
import { computed } from 'vue'
import { RouterView } from 'vue-router'
import { navigationFor } from '@/app/navigation'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import ErrorBoundary from '@/components/ErrorBoundary.vue'
import CspAppShell from '@/components/layout/CspAppShell/CspAppShell.vue'
import { useCurrentUser } from '@/stores/currentUser'
import { useRouteOrganisme } from '@/stores/routeOrganisme'

const { user } = useCurrentUser()
const { organismeUuid, canManageOrganisme } = useRouteOrganisme()

const navigation = computed(() => navigationFor({
  isStaff: user.value?.is_staff ?? false,
  organismeUuid: organismeUuid.value,
  canManageOrganisme: canManageOrganisme.value,
}))
</script>

<template>
  <div class="ats-app">
    <CspToaster>
      <CspAppShell :navigation="navigation">
        <ErrorBoundary>
          <RouterView />
        </ErrorBoundary>
      </CspAppShell>
    </CspToaster>
    <PiniaColadaDevtools />
  </div>
</template>
