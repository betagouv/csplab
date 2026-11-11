<script setup lang="ts">
import { nextTick, onMounted, ref, useTemplateRef } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCombobox from '@/components/base/CspCombobox/CspCombobox.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspPopover from '@/components/base/CspPopover/CspPopover.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspToast from '@/components/base/CspToast/CspToast.vue'
import CspToastProvider from '@/components/base/CspToast/CspToastProvider.vue'
import CspTooltip from '@/components/base/CspTooltip/CspTooltip.vue'

const MENU_SECTIONS = [
  {
    items: [
      { label: 'Modifier', icon: 'ri:pencil-line' },
      { label: 'Dupliquer', icon: 'ri:file-copy-line' },
    ],
  },
  {
    items: [
      { label: 'Supprimer', icon: 'ri:delete-bin-line', destructive: true },
    ],
  },
]

const SORT_OPTIONS = [
  { value: 'date', label: 'Date de création' },
  { value: 'nom', label: 'Nom' },
  { value: 'modification', label: 'Dernière modification' },
]

const CITY_OPTIONS = [
  { value: 'paris', label: 'Paris' },
  { value: 'lyon', label: 'Lyon' },
  { value: 'marseille', label: 'Marseille' },
]

const sort = ref('date')
const city = ref<string | null>(null)
const cityQuery = ref('')

function keepOpen() {}

const root = useTemplateRef<HTMLElement>('root')

// CspSelect and CspTooltip expose no open prop: open them as a user would, once the controlled layers have taken focus
onMounted(async () => {
  await nextTick()
  window.setTimeout(() => {
    root.value?.querySelector('.ecarts-couches__tooltip')?.dispatchEvent(
      new PointerEvent('pointermove', { pointerType: 'mouse', bubbles: true }),
    )
    const selectTrigger = root.value?.querySelector<HTMLElement>('.csp-select')
    selectTrigger?.focus()
    selectTrigger?.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }))
  }, 150)
  // The select focuses and highlights its selected option on open
  window.setTimeout(() => {
    if (document.activeElement instanceof HTMLElement) {
      document.activeElement.blur()
    }
  }, 400)
})
</script>

<template>
  <CspToastProvider>
    <div
      ref="root"
      class="ecarts-couches"
    >
      <div class="ecarts-couches__cell ecarts-couches__cell--menu">
        <CspDropdownMenu
          :sections="MENU_SECTIONS"
          side="bottom"
          align="start"
          :side-offset="8"
          :open="true"
          @update:open="keepOpen"
        >
          <template #trigger>
            <CspButton
              label="Actions"
              icon="ri:more-2-line"
              variant="tertiary"
            />
          </template>
        </CspDropdownMenu>
      </div>

      <div class="ecarts-couches__cell ecarts-couches__cell--popover">
        <CspPopover
          :open="true"
          @update:open="keepOpen"
        >
          <template #trigger>
            <CspButton
              label="Filtres"
              icon="ri:filter-3-line"
              variant="tertiary"
            />
          </template>
          <p class="ecarts-couches__popover-text">
            Aucun filtre actif.
          </p>
        </CspPopover>
      </div>

      <div class="ecarts-couches__cell ecarts-couches__cell--select">
        <CspSelect
          v-model="sort"
          label="Trier par"
          :options="SORT_OPTIONS"
        />
      </div>

      <div class="ecarts-couches__cell ecarts-couches__cell--combobox">
        <CspCombobox
          v-model="city"
          v-model:search-term="cityQuery"
          label="Ville"
          placeholder="Rechercher"
          :options="CITY_OPTIONS"
          :open="true"
          @update:open="keepOpen"
        />
      </div>

      <div class="ecarts-couches__cell ecarts-couches__cell--tooltip">
        <CspTooltip
          content="Exporter au format CSV"
          side="right"
          :delay-duration="0"
        >
          <CspButton
            class="ecarts-couches__tooltip"
            label="Exporter"
            variant="secondary"
          />
        </CspTooltip>
      </div>
    </div>

    <CspToast
      :open="true"
      :duration="Infinity"
      variant="success"
      title="Modifications enregistrées"
      @update:open="keepOpen"
    />
  </CspToastProvider>
</template>

<style scoped lang="scss">
.ecarts-couches {
  box-sizing: border-box;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 13rem 13rem auto;
  grid-template-areas:
    'menu popover'
    'select combobox'
    'tooltip tooltip';
  column-gap: var(--csp-space-6);
  padding: 7rem var(--csp-space-6) var(--csp-space-6);
}

.ecarts-couches__cell--menu {
  grid-area: menu;
}
.ecarts-couches__cell--popover {
  grid-area: popover;
}
.ecarts-couches__cell--select {
  grid-area: select;
}
.ecarts-couches__cell--combobox {
  grid-area: combobox;
}
.ecarts-couches__cell--tooltip {
  grid-area: tooltip;
}

.ecarts-couches__popover-text {
  margin: 0;
  color: var(--text-default-grey);
  font-size: var(--csp-font-size-sm);
}
</style>
