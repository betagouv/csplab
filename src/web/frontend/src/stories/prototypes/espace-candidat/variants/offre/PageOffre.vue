<script setup lang="ts">
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSeparator from '@/components/base/CspSeparator/CspSeparator.vue'
import { offrePrincipale } from '../../data/candidatMock'
import CandidateHeader from '../../shared/CandidateHeader.vue'

defineEmits<{
  postuler: []
}>()

const offre = offrePrincipale
</script>

<template>
  <div class="page-offre">
    <CandidateHeader variant="public" />

    <main class="page-offre__main">
      <div class="page-offre__layout">
        <div class="page-offre__content">
          <p class="page-offre__breadcrumb">
            <CspIcon
              name="ri:arrow-left-line"
              :size="16"
            />
            Toutes les offres
          </p>

          <div class="page-offre__header">
            <CspBadge
              label="Offre ouverte"
              type="success"
              variant="soft"
            />
            <h1 class="page-offre__title">
              {{ offre.intitule }}
            </h1>
            <p class="page-offre__organisme">
              <CspIcon
                name="ri:government-line"
                :size="18"
              />
              {{ offre.organisme }}
              <span
                v-if="offre.service"
                class="page-offre__service"
              >— {{ offre.service }}</span>
            </p>

            <ul class="page-offre__meta">
              <li>
                <CspIcon
                  name="ri:map-pin-line"
                  :size="16"
                />
                {{ offre.localisation }}
              </li>
              <li>
                <CspIcon
                  name="ri:briefcase-line"
                  :size="16"
                />
                {{ offre.typeContrat }}
              </li>
              <li>
                <CspIcon
                  name="ri:money-euro-circle-line"
                  :size="16"
                />
                {{ offre.remunerationDetail }}
              </li>
            </ul>
          </div>

          <section class="page-offre__section">
            <h2>Description du poste</h2>
            <p>{{ offre.description }}</p>
          </section>

          <section class="page-offre__section">
            <h2>Vos missions</h2>
            <ul class="page-offre__list">
              <li
                v-for="mission in offre.missions"
                :key="mission"
              >
                {{ mission }}
              </li>
            </ul>
          </section>

          <section class="page-offre__section">
            <h2>Profil recherché</h2>
            <ul class="page-offre__list">
              <li
                v-for="profil in offre.profilRecherche"
                :key="profil"
              >
                {{ profil }}
              </li>
            </ul>
          </section>

          <section class="page-offre__section">
            <h2>Informations pratiques</h2>
            <dl class="page-offre__infos">
              <div
                v-for="info in offre.informationsPratiques"
                :key="info.label"
                class="page-offre__info"
              >
                <dt>{{ info.label }}</dt>
                <dd>{{ info.valeur }}</dd>
              </div>
            </dl>
          </section>

          <section class="page-offre__section">
            <h2>Étapes du recrutement</h2>
            <ol class="page-offre__etapes">
              <li
                v-for="(etape, index) in offre.etapesProcessus"
                :key="etape"
              >
                <span class="page-offre__etape-numero">{{ index + 1 }}</span>
                {{ etape }}
              </li>
            </ol>
          </section>
        </div>

        <aside class="page-offre__sidebar">
          <CspCard class="page-offre__cta-card">
            <template #title>
              Postuler à cette offre
            </template>

            <p class="page-offre__cta-hint">
              <CspIcon
                name="ri:information-line"
                :size="16"
              />
              « Postuler » vous mène directement à la candidature, dans cet outil.
              Vous ne quittez pas ce site.
            </p>

            <CspButton
              variant="primary"
              size="lg"
              label="Postuler"
              class="page-offre__cta-button"
              @click="$emit('postuler')"
            />

            <p class="page-offre__no-account">
              Pas besoin de créer un compte pour candidater.
            </p>

            <CspSeparator class="page-offre__cta-separator" />

            <dl class="page-offre__cta-infos">
              <div>
                <dt>Référence</dt>
                <dd>{{ offre.reference }}</dd>
              </div>
              <div>
                <dt>Candidatures jusqu'au</dt>
                <dd>{{ offre.dateLimiteCandidature }}</dd>
              </div>
            </dl>
          </CspCard>
        </aside>
      </div>
    </main>
  </div>
</template>

<style scoped lang="scss">
.page-offre {
  min-height: 100vh;
  background-color: var(--background-alt-grey);
}

.page-offre__main {
  padding: var(--csp-space-8) var(--csp-space-6);
  display: flex;
  justify-content: center;
}

.page-offre__layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 20rem;
  gap: var(--csp-space-8);
  max-width: 64rem;
  width: 100%;
  align-items: start;
}

.page-offre__content {
  background-color: var(--background-default-grey);
  border-radius: 0.5rem;
  padding: var(--csp-space-8);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
}

.page-offre__breadcrumb {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0 0 var(--csp-space-6);
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.page-offre__header {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  padding-bottom: var(--csp-space-6);
  margin-bottom: var(--csp-space-6);
  border-bottom: 1px solid var(--border-default-grey);
}

.page-offre__title {
  margin: var(--csp-space-2) 0 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-title-grey);
  line-height: 1.2;
}

.page-offre__organisme {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: 1rem;
  color: var(--text-default-grey);
  font-weight: 500;
}

.page-offre__service {
  color: var(--text-mention-grey);
  font-weight: 400;
}

.page-offre__meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-4);
  list-style: none;
  margin: var(--csp-space-2) 0 0;
  padding: 0;

  li {
    display: flex;
    align-items: center;
    gap: var(--csp-space-1);
    font-size: 0.875rem;
    color: var(--text-mention-grey);
  }
}

.page-offre__section {
  margin-bottom: var(--csp-space-6);

  &:last-child {
    margin-bottom: 0;
  }

  h2 {
    margin: 0 0 var(--csp-space-3);
    font-size: 1.125rem;
    font-weight: 700;
    color: var(--text-title-grey);
  }

  p {
    margin: 0;
    font-size: 0.9375rem;
    line-height: 1.6;
    color: var(--text-default-grey);
  }
}

.page-offre__list {
  margin: 0;
  padding-left: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  font-size: 0.9375rem;
  line-height: 1.5;
  color: var(--text-default-grey);
}

.page-offre__infos {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--csp-space-4);
  margin: 0;
}

.page-offre__info {
  dt {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    color: var(--text-mention-grey);
    margin: 0 0 0.125rem;
  }

  dd {
    margin: 0;
    font-size: 0.9375rem;
    font-weight: 500;
    color: var(--text-default-grey);
  }
}

.page-offre__etapes {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);

  li {
    display: flex;
    align-items: center;
    gap: var(--csp-space-3);
    font-size: 0.9375rem;
    color: var(--text-default-grey);
  }
}

.page-offre__etape-numero {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background-color: var(--background-contrast-blue-france);
  color: var(--text-action-high-blue-france);
  font-size: 0.75rem;
  font-weight: 700;
}

.page-offre__sidebar {
  position: sticky;
  top: var(--csp-space-6);
}

.page-offre__cta-card {
  display: flex;
  flex-direction: column;
}

.page-offre__cta-hint {
  display: flex;
  gap: var(--csp-space-2);
  margin: 0 0 var(--csp-space-4);
  padding: var(--csp-space-3);
  border-radius: 0.25rem;
  background-color: var(--background-alt-blue-france);
  color: var(--text-mention-grey);
  font-size: 0.8125rem;
  line-height: 1.4;
}

.page-offre__cta-button {
  width: 100%;
  justify-content: center;
}

.page-offre__no-account {
  margin: var(--csp-space-2) 0 0;
  text-align: center;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.page-offre__cta-separator {
  margin: var(--csp-space-4) 0;
}

.page-offre__cta-infos {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;

  dt {
    font-size: 0.75rem;
    color: var(--text-mention-grey);
    margin: 0;
  }

  dd {
    margin: 0.125rem 0 0;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-default-grey);
  }
}

@media (max-width: 56rem) {
  .page-offre__layout {
    grid-template-columns: 1fr;
  }

  .page-offre__sidebar {
    position: static;
    order: -1;
  }
}
</style>
