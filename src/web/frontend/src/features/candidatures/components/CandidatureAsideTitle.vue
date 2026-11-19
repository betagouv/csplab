<template>
  <h3 class="candidature-aside-title">
    <slot />
  </h3>
</template>

<style scoped lang="scss">
.candidature-aside-title {
  margin: 0;
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}
</style>
