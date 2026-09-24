<template>
  <div class="phone-frame">
    <div class="phone-frame__screen">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.phone-frame {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: var(--csp-space-6);
  background: var(--background-alt-grey);
}

.phone-frame__screen {
  width: 375px;
  height: 740px;
  max-height: calc(100vh - 2 * var(--csp-space-6));
  overflow-y: auto;
  background: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
  box-shadow: var(--csp-shadow-lg);
}
</style>
