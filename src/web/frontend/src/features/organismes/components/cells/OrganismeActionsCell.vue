<script setup lang="ts">
import type { OrganismesList } from '../../types'
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { organismeHomeLocation } from '@/router/names'
import { useCurrentUser } from '@/stores/currentUser'
import { can } from '@/utils/authorizedActions'
import { useOrganismeEdition } from '../../composables/useOrganismeEdition'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: OrganismesList
}>()

const router = useRouter()
const edition = useOrganismeEdition()
const { user } = useCurrentUser()

const items = computed(() => [
  ...(can(props.row.authorized_actions, 'list_recrutements')
    ? [{
        label: 'Se connecter à l’organisme',
        icon: 'ri:login-box-line',
        onSelect: () => void router.push(organismeHomeLocation(props.row.uuid)),
      }]
    : []),
  ...(can(user.value?.authorized_actions, 'update_organisme')
    ? [{
        label: 'Modifier l’organisme',
        icon: 'ri:pencil-line',
        onSelect: () => edition.request(props.row),
      }]
    : []),
])
</script>

<template>
  <div class="organisme-actions-cell">
    <CspDropdownMenu
      v-if="items.length > 0"
      :sections="[{ items }]"
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
