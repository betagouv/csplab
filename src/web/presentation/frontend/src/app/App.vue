<script setup lang="ts">
import { PiniaColadaDevtools } from '@pinia/colada-devtools'
import { computed } from 'vue'
import { RouterView } from 'vue-router'
import { navigationFor } from '@/app/navigation'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import ErrorBoundary from '@/components/ErrorBoundary.vue'
import CspAppShell from '@/components/layout/CspAppShell/CspAppShell.vue'
import { useCurrentUser } from '@/stores/currentUser'

const { user } = useCurrentUser()
const navigation = computed(() => navigationFor(user.value?.is_staff ?? false))
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
