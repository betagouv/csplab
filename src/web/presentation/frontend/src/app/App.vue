<script setup lang="ts">
import { RouterView } from 'vue-router'
import ErrorBoundary from '@/shared/components/ErrorBoundary.vue'
</script>

<template>
  <div class="ats-app">
    <ErrorBoundary>
      <RouterView />
    </ErrorBoundary>
  </div>
</template>
