<script setup lang="ts">
import type { RouteLocationRaw } from 'vue-router'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { computed } from 'vue'
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useDocumentTitle } from '@/composables/ui/useDocumentTitle'
import { HOME_BREADCRUMB_LABEL } from '@/router/breadcrumb'
import { ORGANISME_TAB_ROUTE_NAMES, RECRUTEMENTS_TAB_ROUTE_NAMES } from '@/router/names'
import { useCurrentUser } from '@/stores/currentUser'
import { useRouteOrganisme } from '@/stores/routeOrganisme'
import { HELP_LABEL, HELP_URL, WELCOME_TEXTS } from '../constants/home'

const props = defineProps<{
  organismeUuid?: string
}>()

const breadcrumb: CspBreadcrumbItem[] = [{ label: HOME_BREADCRUMB_LABEL }]

const { user } = useCurrentUser()
const { canManageOrganisme } = useRouteOrganisme()

const welcome = computed(() => WELCOME_TEXTS[canManageOrganisme.value ? 'superviseur' : 'agent'])

const tiles = computed<{ label: string, icon: string, to: RouteLocationRaw }[]>(() => {
  if (!canManageOrganisme.value) {
    return []
  }
  const params = { organismeUuid: props.organismeUuid }
  return [
    { label: 'Équipe de recrutement', icon: 'ri:account-circle-line', to: { name: ORGANISME_TAB_ROUTE_NAMES.membres, params } },
    { label: 'Processus de recrutement', icon: 'ri:table-line', to: { name: ORGANISME_TAB_ROUTE_NAMES.etapes, params } },
    { label: 'Recrutements', icon: 'ri:briefcase-line', to: { name: RECRUTEMENTS_TAB_ROUTE_NAMES.actifs, params } },
  ]
})

useDocumentTitle(HOME_BREADCRUMB_LABEL)
</script>

<template>
  <CspPageHeader
    :breadcrumb="breadcrumb"
    :title="`Bonjour ${user?.prenom}`"
    :show-title-skeleton="!user"
    subtitle="Votre espace de recrutement"
  />
  <CspPageContainer>
    <div
      v-if="organismeUuid"
      class="home-view"
    >
      <CspCard
        as="section"
        size="lg"
        title-as="h2"
        :title="welcome.title"
        :description="welcome.description"
      >
        <template #start>
          <CspIcon
            name="ri:briefcase-line"
            :size="24"
          />
        </template>
        <ul class="home-view__steps">
          <li
            v-for="step in welcome.steps"
            :key="step"
          >
            {{ step }}
          </li>
        </ul>
      </CspCard>

      <ul
        v-if="tiles.length"
        class="home-view__tiles"
      >
        <li
          v-for="tile in tiles"
          :key="tile.label"
        >
          <CspCard
            as="div"
            class="home-view__tile"
            :title="tile.label"
            :to="tile.to"
          >
            <template #start>
              <CspIcon
                :name="tile.icon"
                :size="24"
              />
            </template>
          </CspCard>
        </li>
      </ul>

      <CspCard
        as="section"
        class="home-view__help"
        title-as="h2"
        title="Besoin d’aide pour bien démarrer ?"
        description="Découvrez nos guides et conseils pour prendre en main cet ATS."
      >
        <template #start>
          <CspAvatar
            icon="ri:question-line"
            size="lg"
          />
        </template>
        <template #footer>
          <CspButton
            as="a"
            :href="HELP_URL"
            target="_blank"
            rel="noopener"
            :title="`${HELP_LABEL} - nouvelle fenêtre`"
            variant="secondary"
            icon="ri:external-link-line"
            is-icon-left
            :label="HELP_LABEL"
          />
        </template>
      </CspCard>
    </div>
  </CspPageContainer>
</template>

<style scoped lang="scss">
@use '@/styles/breakpoints' as bp;

.home-view {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
}

.home-view__steps {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding-left: var(--csp-space-5);
  list-style-type: disc;
}

.home-view__tiles {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--csp-space-6);
  margin: 0;
  padding: 0;
  list-style: none;

  @include bp.from(bp.$md) {
    grid-template-columns: repeat(3, 1fr);
  }
}

.home-view__tile {
  height: 100%;
  align-items: center;
  text-align: center;
  color: var(--text-action-high-blue-france);
  box-shadow:
    inset 0 0 0 1px var(--csp-card-border),
    inset 0 -0.25rem 0 0 var(--border-active-blue-france);
}

.home-view__help {
  @include bp.from(bp.$md) {
    flex-direction: row;
    align-items: center;

    :deep(.csp-card__header) {
      flex: 1;
    }
  }
}
</style>
