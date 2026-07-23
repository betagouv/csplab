<script setup lang="ts">
import { PiniaColadaDevtools } from '@pinia/colada-devtools'
import { RouterView } from 'vue-router'
import { APP_NAVIGATION } from '@/app/navigation'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import ErrorBoundary from '@/components/ErrorBoundary.vue'
import CspAppShell from '@/components/layout/CspAppShell/CspAppShell.vue'
</script>

<template>
  <div class="ats-app">
    <CspToaster>
      <CspAppShell :navigation="APP_NAVIGATION">
        <ErrorBoundary>
          <RouterView />
        </ErrorBoundary>
      </CspAppShell>
    </CspToaster>
    <PiniaColadaDevtools />
  </div>
</template>
