<script setup lang="ts">
import { RouterView } from 'vue-router'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import ErrorBoundary from '@/components/ErrorBoundary.vue'
import AppShell from '@/components/layout/AppShell.vue'
</script>

<template>
  <div class="ats-app">
    <CspToaster>
      <AppShell>
        <ErrorBoundary>
          <RouterView />
        </ErrorBoundary>
      </AppShell>
    </CspToaster>
  </div>
</template>
