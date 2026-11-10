<script setup lang="ts">
import { PiniaColadaDevtools } from '@pinia/colada-devtools'
import { useHead } from '@unhead/vue'
import { computed } from 'vue'
import { RouterView } from 'vue-router'
import { navigationFor } from '@/app/navigation'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import ErrorBoundary from '@/components/ErrorBoundary.vue'
import CspAppShell from '@/components/layout/CspAppShell/CspAppShell.vue'
import OrganismeSwitcher from '@/features/organismes/components/OrganismeSwitcher.vue'
import { useCurrentUser } from '@/stores/currentUser'
import { useRouteOrganisme } from '@/stores/routeOrganisme'
import { can } from '@/utils/authorizedActions'

const LOADING_TITLE = document.title

useHead({ titleTemplate: title => (title ? `${title} | CSPLab` : LOADING_TITLE) })

const { user, error: userError, refetch: refetchUser } = useCurrentUser()
const { organismeUuid, actionsPending, canOnOrganisme } = useRouteOrganisme()

const navigation = computed(() => navigationFor({
  canListOrganismes: can(user.value?.authorized_actions, 'list_organismes'),
  organismeUuid: organismeUuid.value,
  organismeActionsPending: actionsPending.value,
  canAccessOrganismeSettings: canOnOrganisme('get_organisme'),
}))

const userLoadFailed = computed(() => !user.value && Boolean(userError.value))
</script>

<template>
  <div class="ats-app">
    <CspToaster>
      <main
        v-if="userLoadFailed"
        class="ats-app__error"
      >
        <CspErrorState title="Une erreur est survenue lors du chargement de votre compte.">
          <template #action>
            <CspButton
              label="Réessayer"
              variant="secondary"
              @click="refetchUser()"
            />
          </template>
        </CspErrorState>
      </main>
      <CspAppShell
        v-else
        :navigation="navigation"
      >
        <template #context>
          <OrganismeSwitcher />
        </template>
        <ErrorBoundary>
          <RouterView />
        </ErrorBoundary>
      </CspAppShell>
    </CspToaster>
    <PiniaColadaDevtools />
  </div>
</template>

<style scoped lang="scss">
.ats-app__error {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100dvh;
}
</style>
