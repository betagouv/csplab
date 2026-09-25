<script setup lang="ts">
import { logout } from '@/api/utilisateur'
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'
import CspSidebarDropdown from '@/components/layout/CspSidebar/CspSidebarDropdown.vue'
import { useColorMode } from '@/composables/ui/useColorMode'

interface CspSidebarUserProps {
  name: string
  role?: string
}

defineProps<CspSidebarUserProps>()

const { isDark, toggle: toggleColorMode } = useColorMode()
</script>

<template>
  <CspSidebarDropdown
    align="end"
    side="right"
    :title="name"
    :description="role"
    :aria-label="`Compte : ${name}`"
    :sections="[
      {
        items: [
          {
            label: isDark ? 'Mode clair' : 'Mode sombre',
            icon: isDark ? 'ri:sun-line' : 'ri:moon-line',
            onSelect: toggleColorMode,
          },
        ],
      },
      {
        items: [
          {
            label: 'Mon profil',
            icon: 'ri:user-line',
          },
          {
            label: 'Paramètres',
            icon: 'ri:settings-3-line',
          },
        ],
      },
      {
        items: [
          {
            label: 'Se déconnecter',
            icon: 'ri:logout-box-r-line',
            destructive: true,
            onSelect: logout,
          },
        ],
      },
    ]"
  >
    <template #leading>
      <CspAvatar :name="name" />
    </template>
  </CspSidebarDropdown>
</template>
