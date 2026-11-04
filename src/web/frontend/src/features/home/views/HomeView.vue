<script setup lang="ts">
import type { RouteLocationRaw } from 'vue-router'
import type { HomeDestination, HomeLayout } from '../constants/home'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
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

const DESTINATIONS = {
  membres: ORGANISME_TAB_ROUTE_NAMES.membres,
  etapes: ORGANISME_TAB_ROUTE_NAMES.etapes,
  recrutements: RECRUTEMENTS_TAB_ROUTE_NAMES.actifs,
} satisfies Record<HomeDestination, string>

const breadcrumb: CspBreadcrumbItem[] = [{ label: HOME_BREADCRUMB_LABEL }]

const route = useRoute()
const { user } = useCurrentUser()
const { canManageOrganisme } = useRouteOrganisme()

const layout = computed<HomeLayout>(() => route.query.piste === 'parcours' ? 'steps' : 'tiles')

const welcome = computed(() => WELCOME_TEXTS[canManageOrganisme.value ? 'superviseur' : 'agent'])

function locationOf(destination: HomeDestination): RouteLocationRaw {
  return { name: DESTINATIONS[destination], params: { organismeUuid: props.organismeUuid } }
}

const tiles = computed(() => welcome.value.steps.flatMap(step => step.to
  ? [{ label: step.label, icon: step.icon, description: step.tileDescription ?? step.title, to: locationOf(step.to) }]
  : []))

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
      <section
        v-if="layout === 'tiles'"
        class="home-view__section"
        aria-labelledby="home-welcome"
      >
        <div class="home-view__intro">
          <h2 id="home-welcome">
            {{ welcome.title }}
          </h2>
          <p>{{ welcome.description }}</p>
        </div>
        <ul class="home-view__tiles">
          <li
            v-for="tile in tiles"
            :key="tile.label"
          >
            <CspCard
              as="div"
              class="home-view__tile"
              :title="tile.label"
              :description="tile.description"
              :to="tile.to"
            >
              <template #start>
                <CspIcon
                  :name="tile.icon"
                  :size="32"
                />
              </template>
            </CspCard>
          </li>
        </ul>
      </section>

      <CspCard
        v-else
        as="section"
        size="lg"
        title-as="h2"
        :title="welcome.title"
        :description="welcome.description"
      >
        <div class="home-view__guide">
          <ol class="home-view__steps">
            <li
              v-for="(step, index) in welcome.steps"
              :key="step.title"
              class="home-view__row"
            >
              <span
                class="home-view__step-number"
                aria-hidden="true"
              >{{ index + 1 }}</span>
              <div class="home-view__row-text">
                <h3>{{ step.title }}</h3>
                <p v-if="step.description">
                  {{ step.description }}
                </p>
              </div>
              <CspButton
                v-if="step.to && step.action"
                class="home-view__action"
                :as="RouterLink"
                :to="locationOf(step.to)"
                variant="secondary"
                size="sm"
                :label="step.action"
              />
            </li>
          </ol>
          <div class="home-view__row home-view__guide-help">
            <CspIcon
              class="home-view__help-icon"
              name="ri:question-line"
              :size="24"
            />
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
              size="sm"
              icon="ri:external-link-line"
              is-icon-left
              :label="HELP_LABEL"
            />
          </div>
        </div>
      </CspCard>

      <CspCard
        v-if="layout === 'tiles'"
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
  gap: var(--csp-space-8);
}

.home-view__section {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
}

.home-view__intro {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);

  h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 700;
    line-height: 1.4;
  }

  p {
    margin: 0;
    color: var(--text-mention-grey);
  }
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
  box-shadow:
    inset 0 0 0 1px var(--csp-card-border),
    inset 0 -0.25rem 0 0 var(--border-active-blue-france);
}

.home-view__guide {
  display: grid;
  grid-template-columns: 2rem 1fr;
  column-gap: var(--csp-space-4);

  @include bp.from(bp.$md) {
    grid-template-columns: 2rem 1fr auto;
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
  row-gap: var(--csp-space-3);

  @include bp.from(bp.$md) {
    align-items: center;
  }
  padding-block: var(--csp-space-4);
  border-top: 1px solid var(--border-default-grey);
}

.home-view__guide .home-view__action {
  grid-column: 2;
  width: 100%;

  @include bp.from(bp.$md) {
    grid-column: 3;
  }
}

.home-view__guide-help {
  --home-view-help-inset: calc(var(--csp-card-padding) - 1px);

  margin: var(--csp-space-2) calc(-1 * var(--home-view-help-inset)) calc(-1 * var(--home-view-help-inset));
  padding: var(--csp-space-5) var(--home-view-help-inset);
  border-top: none;
  background-color: var(--background-alt-grey);
}

.home-view__help-icon {
  justify-self: center;
  color: var(--text-action-high-blue-france);
}

.home-view__step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 9999px;
  background-color: var(--background-action-low-blue-france);
  color: var(--text-action-high-blue-france);
  font-weight: 700;
}

.home-view__row-text {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);

  h3 {
    margin: 0;
    font-size: 1rem;
    line-height: 1.5;
  }

  p {
    margin: 0;
    color: var(--text-mention-grey);
    font-size: 0.875rem;
  }
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
