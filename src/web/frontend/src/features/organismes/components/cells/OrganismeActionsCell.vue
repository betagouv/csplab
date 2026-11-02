<script setup lang="ts">
import type { OrganismesList } from '../../types'
import { useRouter } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { RECRUTEMENTS_TAB_ROUTE_NAMES } from '@/router/names'
import { useOrganismeEdition } from '../../composables/useOrganismeEdition'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: OrganismesList
}>()

const router = useRouter()
const edition = useOrganismeEdition()

const sections = [{
  items: [{
    label: 'Se connecter à l’organisme',
    icon: 'ri:login-box-line',
    onSelect: () => void router.push({
      name: RECRUTEMENTS_TAB_ROUTE_NAMES.actifs,
      params: { organismeUuid: props.row.uuid },
    }),
  }, {
    label: 'Modifier l’organisme',
    icon: 'ri:pencil-line',
    onSelect: () => edition.request(props.row),
  }],
}]
</script>

<template>
  <div class="organisme-actions-cell">
    <CspDropdownMenu
      :sections="sections"
      side="bottom"
      align="end"
    >
      <template #trigger>
        <CspButton
          icon="ri:more-2-fill"
          variant="tertiary-no-outline"
          size="sm"
          :aria-label="`Actions pour ${row.nom}`"
        />
      </template>
    </CspDropdownMenu>
  </div>
</template>

<style scoped lang="scss">
.organisme-actions-cell {
  display: flex;
  justify-content: flex-end;
}
</style>
