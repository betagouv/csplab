<script setup lang="ts">
import { RouterView } from 'vue-router'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import ErrorBoundary from '@/shared/components/ErrorBoundary.vue'
</script>

<template>
  <div class="ats-app">
    <CspToaster>
      <ErrorBoundary>
        <RouterView />
      </ErrorBoundary>
    </CspToaster>
  </div>
</template>
