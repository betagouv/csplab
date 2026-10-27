<script setup lang="ts">
import {
  ListboxContent,
  ListboxFilter,
  ListboxGroup,
  ListboxGroupLabel,
  ListboxItem,
  ListboxItemIndicator,
  ListboxRoot,
} from 'reka-ui'
import { computed, ref, useId, watch } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspPopover from '@/components/base/CspPopover/CspPopover.vue'
import CspSidebarButton from '@/components/layout/CspSidebar/CspSidebarButton.vue'

export interface CspSidebarSwitcherOption {
  value: string
  label: string
  description?: string
}

export interface CspSidebarSwitcherGroup {
  label?: string
  options: CspSidebarSwitcherOption[]
}

defineOptions({
  inheritAttrs: false,
})

const props = withDefaults(defineProps<{
  title: string
  groups: CspSidebarSwitcherGroup[]
  selected?: string | null
  filterLabel?: string
  filterPlaceholder?: string
  emptyLabel?: string
}>(), {
  selected: null,
  filterLabel: undefined,
  filterPlaceholder: undefined,
  emptyLabel: 'Aucun résultat',
})

const emit = defineEmits<{
  select: [value: string]
}>()

const search = defineModel<string>('search', { default: '' })
const open = ref(false)
const filterId = useId()

const visibleGroups = computed(() => props.groups.filter(group => group.options.length > 0))
const optionCount = computed(() => visibleGroups.value.reduce((count, group) => count + group.options.length, 0))
const isStatic = computed(() => !props.filterLabel && optionCount.value <= 1)
const emptyMessage = computed(() => (open.value && optionCount.value === 0 ? props.emptyLabel : ''))

watch(open, (isOpen) => {
  if (!isOpen) {
    search.value = ''
  }
})

function select(value: string) {
  open.value = false
  emit('select', value)
}
</script>

<template>
  <CspSidebarButton
    v-if="isStatic"
    static
    :title="title"
  >
    <template #leading>
      <slot name="leading" />
    </template>
  </CspSidebarButton>

  <CspPopover
    v-else
    v-model:open="open"
    side="bottom"
    align="start"
    padding="menu"
  >
    <template #trigger>
      <CspSidebarButton
        :title="title"
        v-bind="$attrs"
      >
        <template #leading>
          <slot name="leading" />
        </template>
      </CspSidebarButton>
    </template>

    <ListboxRoot
      class="csp-sidebar-switcher"
      :model-value="selected ?? undefined"
      highlight-on-hover
    >
      <template v-if="filterLabel">
        <div class="csp-sidebar-switcher__filter">
          <label
            :for="filterId"
            class="csp-sidebar-switcher__label"
          >{{ filterLabel }}</label>
          <span class="csp-sidebar-switcher__filter-field">
            <CspIcon
              name="ri:search-line"
              class="csp-sidebar-switcher__filter-icon"
              aria-hidden="true"
            />
            <ListboxFilter
              :id="filterId"
              v-model="search"
              type="search"
              autocomplete="off"
              class="csp-sidebar-switcher__filter-input"
              :placeholder="filterPlaceholder"
              auto-focus
            />
          </span>
        </div>
        <div
          class="csp-sidebar-switcher__separator"
          aria-hidden="true"
        />
      </template>

      <ListboxContent class="csp-sidebar-switcher__content">
        <template
          v-for="(group, groupIndex) in visibleGroups"
          :key="group.label ?? groupIndex"
        >
          <div
            v-if="groupIndex > 0"
            class="csp-sidebar-switcher__separator"
            aria-hidden="true"
          />
          <ListboxGroup>
            <ListboxGroupLabel
              v-if="group.label"
              class="csp-sidebar-switcher__label csp-sidebar-switcher__group-label"
            >
              {{ group.label }}
            </ListboxGroupLabel>
            <ListboxItem
              v-for="option in group.options"
              :key="option.value"
              :value="option.value"
              class="csp-sidebar-switcher__option"
              @select="select(option.value)"
            >
              <span class="csp-sidebar-switcher__option-text">
                <span>{{ option.label }}</span>
                <span
                  v-if="option.description"
                  class="csp-sidebar-switcher__option-description"
                >{{ option.description }}</span>
              </span>
              <ListboxItemIndicator class="csp-sidebar-switcher__option-indicator">
                <CspIcon name="ri:check-line" />
              </ListboxItemIndicator>
            </ListboxItem>
          </ListboxGroup>
        </template>
      </ListboxContent>

      <p
        class="csp-sidebar-switcher__empty"
        role="status"
      >
        {{ emptyMessage }}
      </p>
    </ListboxRoot>
  </CspPopover>
</template>

<style scoped lang="scss">
@use '@/styles/menu';
@use '@/styles/search';

.csp-sidebar-switcher {
  display: flex;
  flex-direction: column;
  width: 18rem;
}

.csp-sidebar-switcher__separator {
  @include menu.separator;
}

.csp-sidebar-switcher__filter {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  padding: var(--csp-menu-item-padding);
}

.csp-sidebar-switcher__label {
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.csp-sidebar-switcher__filter-field {
  @include search.field;
}

.csp-sidebar-switcher__filter-icon {
  @include search.icon;
}

.csp-sidebar-switcher__filter-input {
  @include search.input;
}

.csp-sidebar-switcher__content {
  display: flex;
  flex-direction: column;
  max-height: 20rem;
  overflow-y: auto;
}

.csp-sidebar-switcher__group-label {
  display: block;
  padding: var(--csp-menu-item-padding);
  padding-bottom: var(--csp-space-1);
}

.csp-sidebar-switcher__option {
  @include menu.item;
}

.csp-sidebar-switcher__option-text {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.csp-sidebar-switcher__option-description {
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.csp-sidebar-switcher__option-indicator {
  display: flex;
  flex-shrink: 0;
  color: var(--text-action-high-blue-france);
}

.csp-sidebar-switcher__empty {
  margin: 0;
  padding: var(--csp-menu-item-padding);
  color: var(--text-mention-grey);

  &:empty {
    padding: 0;
  }
}
</style>
