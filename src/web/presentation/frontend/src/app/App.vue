<script setup lang="ts">
import { PiniaColadaDevtools } from '@pinia/colada-devtools'
import { RouterView } from 'vue-router'
import { APP_NAVIGATION } from '@/app/navigation'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import ErrorBoundary from '@/components/ErrorBoundary.vue'
import AppShell from '@/components/layout/AppShell.vue'
</script>

<template>
  <div class="ats-app">
    <CspToaster>
      <AppShell :navigation="APP_NAVIGATION">
        <ErrorBoundary>
          <RouterView />
        </ErrorBoundary>
      </AppShell>
    </CspToaster>
  </div>

  <PiniaColadaDevtools />
</template>
