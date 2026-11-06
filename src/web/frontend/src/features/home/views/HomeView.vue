<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useDocumentTitle } from '@/composables/ui/useDocumentTitle'
import { HOME_BREADCRUMB_LABEL } from '@/router/breadcrumb'
import { useCurrentUser } from '@/stores/currentUser'
import { useRouteOrganisme } from '@/stores/routeOrganisme'
import ForbiddenView from '@/views/ForbiddenView.vue'
import { HELP_LABEL, HELP_URL, WELCOME_TEXTS } from '../constants/home'

const props = defineProps<{
  organismeUuid?: string
}>()

const breadcrumb: CspBreadcrumbItem[] = [{ label: HOME_BREADCRUMB_LABEL }]

const { user } = useCurrentUser()
const { organisme, canBrowseOrganismes, canOnOrganisme } = useRouteOrganisme()

const forbidden = computed(() => !!props.organismeUuid && !!user.value && !canBrowseOrganismes.value && !organisme.value)

const canAccessOrganismeSettings = computed(() => canOnOrganisme('get_organisme'))

const welcome = computed(() => WELCOME_TEXTS[canAccessOrganismeSettings.value ? 'superviseur' : 'agent'])

useDocumentTitle(HOME_BREADCRUMB_LABEL)
</script>

<template>
  <ForbiddenView v-if="forbidden" />
  <template v-else>
    <CspPageHeader
      :breadcrumb="breadcrumb"
      :title="`Bonjour ${user?.prenom}`"
      :show-title-skeleton="!user"
      subtitle="Votre espace de recrutement"
    />
    <CspPageContainer>
      <CspCard
        v-if="user && organismeUuid"
        as="section"
        size="lg"
        title-as="h2"
        :title="welcome.title"
        :description="welcome.description"
      >
        <div class="home-view">
          <ol class="home-view__steps">
            <li
              v-for="(step, index) in welcome.steps"
              :key="step.title"
              class="home-view__row"
            >
              <span
                class="home-view__marker"
                aria-hidden="true"
              >{{ index + 1 }}</span>
              <div class="home-view__row-text">
                <h3>{{ step.title }}</h3>
                <p>{{ step.description }}</p>
              </div>
              <CspButton
                v-if="step.action"
                class="home-view__action"
                :as="RouterLink"
                :to="{ name: step.action.to, params: { organismeUuid } }"
                :variant="index === 0 ? 'primary' : 'secondary'"
                :label="step.action.label"
              />
            </li>
          </ol>
          <div class="home-view__row home-view__row--help">
            <span
              class="home-view__marker"
              aria-hidden="true"
            >
              <CspIcon
                name="ri:question-line"
                :size="20"
              />
            </span>
            <div class="home-view__row-text">
              <h3>Besoin d’aide pour bien démarrer ?</h3>
              <p>Découvrez nos guides et conseils pour prendre en main cet ATS.</p>
            </div>
            <CspButton
              class="home-view__action"
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
          </div>
        </div>
      </CspCard>
      <CspEmptyState
        v-else-if="user"
        icon="ri:government-line"
        title="Vous n’êtes rattaché à aucun organisme"
        description="Demandez au superviseur de votre organisme de vous inviter dans l’ATS."
      />
    </CspPageContainer>
  </template>
</template>

<style scoped lang="scss">
@use '@/styles/breakpoints' as bp;

.home-view {
  --home-view-marker-size: 2.5rem;

  display: grid;
  grid-template-columns: var(--home-view-marker-size) 1fr;
  column-gap: var(--csp-space-5);

  @include bp.from(bp.$md) {
    grid-template-columns: var(--home-view-marker-size) 1fr auto;
  }
}

.home-view__steps {
  display: grid;
  grid-column: 1 / -1;
  grid-template-columns: subgrid;
  margin: 0;
  padding: 0;
  list-style: none;
}

.home-view__row {
  display: grid;
  grid-column: 1 / -1;
  grid-template-columns: subgrid;
  align-items: start;
  row-gap: var(--csp-space-4);
  padding-block: var(--csp-space-5);
  border-top: 1px solid var(--border-default-grey);

  @include bp.from(bp.$md) {
    align-items: center;
  }
}

.home-view__row--help {
  padding-bottom: 0;
}

.home-view__marker {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: var(--home-view-marker-size);
  height: var(--home-view-marker-size);
  border-radius: 9999px;
  background-color: var(--background-contrast-blue-france);
  color: var(--text-action-high-blue-france);
  font-weight: var(--csp-font-weight-bold);
}

.home-view .home-view__action {
  grid-column: 2;
  width: 100%;

  @include bp.from(bp.$md) {
    grid-column: 3;
  }
}

.home-view__row-text {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);

  h3 {
    margin: 0;
    color: var(--text-title-grey);
    font-size: var(--csp-font-size-md);
    font-weight: var(--csp-font-weight-bold);
    line-height: var(--csp-line-height-base);
  }

  p {
    margin: 0;
    color: var(--text-mention-grey);
    font-size: var(--csp-font-size-base);
    line-height: var(--csp-line-height-base);
  }
}
</style>
