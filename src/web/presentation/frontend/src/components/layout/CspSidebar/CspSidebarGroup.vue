<template>
  <div class="csp-sidebar-group">
    <div class="csp-sidebar-group__items">
      <slot />
    </div>
  </div>
</template>

<style scoped lang="scss">
.csp-sidebar-group {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  min-width: 0;
}

.csp-sidebar-group__items {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  align-items: stretch;
}
</style>
