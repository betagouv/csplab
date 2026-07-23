<script setup lang="ts">
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspTabsList from '@/components/base/CspTabs/CspTabsList.vue'
import CspTabsPanels from '@/components/base/CspTabs/CspTabsPanels.vue'

withDefaults(defineProps<{
  fill?: boolean
  width?: 'reading' | 'wide' | 'full'
  tabs?: CspTabItem[]
}>(), {
  fill: false,
  width: 'wide',
})

const activeTab = defineModel<string>('activeTab')
</script>

<template>
  <main
    class="csp-page-container"
    :class="{
      'csp-page-container--fill': fill,
      'csp-page-container--reading': width === 'reading',
      'csp-page-container--wide': width === 'wide',
    }"
  >
    <CspTabs
      v-if="tabs && tabs.length > 0"
      v-model="activeTab"
      :fill="fill"
    >
      <div class="csp-page-container__tabs">
        <CspTabsList :tabs="tabs" />
      </div>
      <div
        v-if="$slots.shared"
        class="csp-page-container__shared"
      >
        <slot name="shared" />
      </div>
      <CspTabsPanels
        :tabs="tabs"
        :fill="fill"
      >
        <template
          v-for="tab in tabs"
          #[tab.value]
          :key="tab.value"
        >
          <div
            class="csp-page-container__content csp-page-container__content--with-tabs"
          >
            <slot
              :name="`tab-${tab.value}`"
            />
          </div>
        </template>
      </CspTabsPanels>
    </CspTabs>
    <div
      v-else
      class="csp-page-container__content"
    >
      <slot />
    </div>
  </main>
</template>

<style scoped lang="scss">
.csp-page-container {
  box-sizing: border-box;
  container: page / inline-size;
}

.csp-page-container--fill {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.csp-page-container__tabs {
  padding-inline: calc(var(--csp-page-container-padding-inline) - 1rem);
  border-bottom: 1px solid var(--border-default-grey);
}

.csp-page-container__content {
  padding-block: var(--csp-page-content-padding-block);
  padding-inline: var(--csp-page-container-padding-inline);
}

.csp-page-container__shared {
  padding-top: var(--csp-page-content-padding-block);
  padding-inline: var(--csp-page-container-padding-inline);
}

.csp-page-container--reading .csp-page-container__content,
.csp-page-container--reading .csp-page-container__shared {
  max-width: var(--csp-page-container-reading-width);
}

.csp-page-container--wide .csp-page-container__content,
.csp-page-container--wide .csp-page-container__shared {
  max-width: var(--csp-page-container-wide-width);
}

.csp-page-container--fill .csp-page-container__content--with-tabs {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}
</style>
