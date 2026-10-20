<script setup lang="ts" generic="T extends string = string">
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspTabsList from '@/components/base/CspTabs/CspTabsList.vue'
import CspTabsPanels from '@/components/base/CspTabs/CspTabsPanels.vue'

withDefaults(defineProps<{
  fill?: boolean
  width?: 'reading' | 'wide' | 'large' | 'full'
  tabs?: CspTabItem<T>[]
}>(), {
  fill: false,
  width: 'wide',
})

const activeTab = defineModel<T>('activeTab')
</script>

<template>
  <main
    class="csp-page-container"
    :class="{
      'csp-page-container--fill': fill,
      'csp-page-container--tabs': tabs && tabs.length > 0,
      'csp-page-container--reading': width === 'reading',
      'csp-page-container--wide': width === 'wide',
      'csp-page-container--large': width === 'large',
    }"
  >
    <CspTabs
      v-if="tabs && tabs.length > 0"
      v-model="activeTab"
      fill
    >
      <div class="csp-page-container__tabs">
        <CspTabsList :tabs="tabs" />
      </div>
      <div class="csp-page-container__frame">
        <div
          v-if="$slots.shared"
          class="csp-page-container__shared"
        >
          <slot name="shared" />
        </div>
        <CspTabsPanels
          :tabs="tabs"
          fill
        >
          <template
            v-if="$slots.tab"
            #default
          >
            <div class="csp-page-container__content csp-page-container__content--with-tabs">
              <slot name="tab" />
            </div>
          </template>
          <template
            v-for="tab in ($slots.tab ? [] : tabs)"
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
      </div>
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
@use '@/styles/breakpoints' as bp;
@use '@/styles/scroll-edges.scss' as edges;

.csp-page-container {
  box-sizing: border-box;
  container: page / inline-size;

  @include bp.fixed-header {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;
    overflow-y: auto;

    @include edges.scroll-edges($rule-inset: var(--csp-page-container-padding-inline), $end: false);

    // Without scroll-driven animations, the rule stays under the header of a page without tabs
    @supports not (animation-timeline: scroll()) {
      &:not(.csp-page-container--tabs)::before {
        opacity: 1;
        box-shadow: none;
      }
    }

    :deep(.csp-tabs__content) {
      overflow-y: auto;

      @include edges.scroll-edges($rule: false, $end: false);
    }
  }
}

.csp-page-container--fill {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.csp-page-container__tabs {
  --csp-tabs-content-padding-inline: calc(var(--csp-page-container-padding-inline) - var(--csp-page-tabs-inset));
  --csp-tabs-list-border-width: var(--csp-page-tabs-border-width);
  --csp-tabs-trigger-background-clip: var(--csp-page-tabs-background-clip);
  --csp-tabs-trigger-background-hover: var(--csp-page-tabs-background-hover);
  --csp-tabs-trigger-background-active: var(--csp-page-tabs-background-active);
  --csp-tabs-trigger-background-current: var(--csp-page-tabs-background-current);
  --csp-tabs-trigger-background-current-hover: var(--csp-page-tabs-background-current-hover);
  --csp-tabs-trigger-border-color-current: var(--csp-page-tabs-border-color-current);

  // Positioned, the tab row paints over the border of the content below it
  position: var(--csp-page-tabs-position);
  margin-inline: var(--csp-page-tabs-inset);
  margin-bottom: var(--csp-page-tabs-margin-bottom);
  background: var(--csp-chrome-background);

  // System colors draw the active tab with its bottom border, which the border of the content must not cover
  @media (forced-colors: active) {
    margin-bottom: 0;
  }
}

.csp-page-container__frame {
  display: flex;
  flex-direction: column;
  // With framed tabs, the frame closes after its content: a page that does not fill the screen scrolls, and on a
  // page that fills it the frame shrinks to the screen height
  flex: calc(1 - var(--csp-tabs-framed)) calc(1 - var(--csp-tabs-framed)) auto;
  min-height: 0;
  background: var(--csp-page-container-frame-background);
}

.csp-page-container--fill .csp-page-container__frame {
  flex-shrink: 1;
}

/* a section that fills the page, such as the kanban, keeps the frame at the height of the screen */
.csp-page-container--fill .csp-page-container__frame:has(.csp-async-section--fill) {
  flex-grow: 1;
}

/* forced colours remove the gradient line under framed tabs */
@media (forced-colors: active) {
  .csp-page-container .csp-page-container__frame {
    border-top: calc(var(--csp-tabs-framed) * 1px) solid;
  }
}

.csp-page-container:not(.csp-page-container--tabs) {
  background: var(--csp-page-container-background);
}

/* From md, the frame takes the page margins, its sides and its bottom unless it is left open; below, it keeps the
   line under the tabs only, like the full viewport width tabs of the DSFR */
@include bp.from(bp.$md) {
  .csp-page-container__tabs {
    --csp-tabs-content-padding-inline: calc(
      var(--csp-page-container-frame-padding-inline) - var(--csp-page-tabs-inset)
    );
    --csp-tabs-list-divider-box: var(--csp-page-tabs-divider-box);

    padding-inline: var(--csp-page-container-frame-margin-inline);
  }

  .csp-page-container__frame {
    --csp-page-container-padding-inline: var(--csp-page-container-frame-padding-inline);
    // The DSFR gives the same padding to the four sides of a tab panel
    --csp-page-container-frame-padding-block: calc(
      var(--csp-tabs-framed) * var(--csp-page-container-frame-padding) + (1 - var(--csp-tabs-framed)) *
        var(--csp-page-content-padding-block)
    );

    margin: 0 var(--csp-page-container-frame-margin-inline) var(--csp-page-container-frame-margin-bottom);
    border: calc(var(--csp-tabs-framed) * var(--csp-page-container-frame-closed) * var(--csp-tabs-frame-width)) solid
      var(--csp-divider-color);
    border-top: 0;
  }

  .csp-page-container__frame > * {
    --csp-page-content-padding-block: var(--csp-page-container-frame-padding-block);
  }
}

// The content keeps the column of the page header inside its inset and its border; its children keep the width of
// the page when a surface lifts the maximum width of the content
.csp-page-container__content {
  flex-grow: var(--csp-page-content-grow);
  margin-inline: var(--csp-page-content-inset);
  margin-bottom: var(--csp-page-content-inset-bottom);
  padding-block: var(--csp-page-content-padding-block);
  padding-inline: calc(
    var(--csp-page-container-padding-inline) - var(--csp-page-content-inset) - var(--csp-page-content-border-width)
  );
  background: var(--csp-page-content-background);
  border: var(--csp-page-content-border-width) solid var(--csp-surface-border-color, var(--border-default-grey));
  box-shadow: var(--csp-page-content-shadow);
}

.csp-page-container__shared {
  padding-top: var(--csp-page-content-padding-block);
  padding-inline: var(--csp-page-container-padding-inline);
}

.csp-page-container--reading .csp-page-container__content {
  max-width: var(--csp-page-content-max-width, var(--csp-page-container-reading-width));
}

.csp-page-container--reading .csp-page-container__content > * {
  max-width: calc(var(--csp-page-container-reading-width) - 2 * var(--csp-page-container-padding-inline));
}

.csp-page-container--reading .csp-page-container__shared {
  max-width: var(--csp-page-container-reading-width);
}

.csp-page-container--wide .csp-page-container__content {
  max-width: var(--csp-page-content-max-width, var(--csp-page-container-wide-width));
}

.csp-page-container--wide .csp-page-container__content > * {
  max-width: calc(var(--csp-page-container-wide-width) - 2 * var(--csp-page-container-padding-inline));
}

.csp-page-container--wide .csp-page-container__shared {
  max-width: var(--csp-page-container-wide-width);
}

.csp-page-container--large .csp-page-container__content {
  max-width: var(--csp-page-content-max-width, var(--csp-page-container-large-width));
}

.csp-page-container--large .csp-page-container__content > * {
  max-width: calc(var(--csp-page-container-large-width) - 2 * var(--csp-page-container-padding-inline));
}

.csp-page-container--large .csp-page-container__shared {
  max-width: var(--csp-page-container-large-width);
}

.csp-page-container--fill .csp-page-container__content--with-tabs {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}
</style>
