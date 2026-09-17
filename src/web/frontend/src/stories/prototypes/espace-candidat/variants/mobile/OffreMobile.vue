<script setup lang="ts">
import type { Offre } from '../../data/candidatMock'
import { offrePrincipale } from '../../data/candidatMock'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

const props = withDefaults(defineProps<{
  offre?: Offre
}>(), {
  offre: () => offrePrincipale,
})

defineEmits<{
  postuler: []
}>()

const estExterne = props.offre.modeCandidature === 'externe'
</script>

<template>
  <div class="offre">
    <div class="offre__scroll">
      <p class="offre__breadcrumb">
        <CspIcon
          name="ri:arrow-left-line"
          :size="16"
        />
        Toutes les offres
      </p>

      <CspBadge
        label="Offre ouverte"
        type="success"
        variant="soft"
      />

      <h1 class="offre__titre">
        {{ offre.intitule }}
      </h1>

      <p class="offre__organisme">
        {{ offre.organisme }}
      </p>

      <ul class="offre__meta">
        <li>
          <CspIcon
            name="ri:map-pin-line"
            :size="18"
          />
          {{ offre.localisation }}
        </li>
        <li>
          <CspIcon
            name="ri:briefcase-line"
            :size="18"
          />
          {{ offre.typeContrat }}
        </li>
        <li>
          <CspIcon
            name="ri:money-euro-circle-line"
            :size="18"
          />
          {{ offre.remunerationDetail }}
        </li>
      </ul>

      <section class="offre__section">
        <h2>Description du poste</h2>
        <p>{{ offre.description }}</p>
      </section>

      <section class="offre__section">
        <h2>Vos missions</h2>
        <ul class="offre__liste">
          <li
            v-for="mission in offre.missions"
            :key="mission"
          >
            {{ mission }}
          </li>
        </ul>
      </section>

      <section class="offre__section">
        <h2>Profil recherché</h2>
        <ul class="offre__liste">
          <li
            v-for="profil in offre.profilRecherche"
            :key="profil"
          >
            {{ profil }}
          </li>
        </ul>
      </section>

      <details class="offre__accordeon">
        <summary>
          Informations pratiques
          <CspIcon
            name="ri:arrow-down-s-line"
            :size="18"
            class="offre__accordeon-icon"
          />
        </summary>
        <dl class="offre__infos">
          <div
            v-for="info in offre.informationsPratiques"
            :key="info.label"
          >
            <dt>{{ info.label }}</dt>
            <dd>{{ info.valeur }}</dd>
          </div>
        </dl>
      </details>

      <details class="offre__accordeon">
        <summary>
          Étapes du recrutement
          <CspIcon
            name="ri:arrow-down-s-line"
            :size="18"
            class="offre__accordeon-icon"
          />
        </summary>
        <ol class="offre__etapes">
          <li
            v-for="(etape, index) in offre.etapesProcessus"
            :key="etape"
          >
            <span class="offre__etape-numero">{{ index + 1 }}</span>
            {{ etape }}
          </li>
        </ol>
      </details>
    </div>

    <div class="offre__cta">
      <p
        v-if="estExterne"
        class="offre__cta-hint offre__cta-hint--externe"
      >
        <CspIcon
          name="ri:external-link-line"
          :size="16"
        />
        Vous allez être redirigé·e vers le site {{ offre.partenaireNom }}.
      </p>
      <p
        v-else
        class="offre__cta-hint"
      >
        Vous restez sur ce site, pas besoin de compte pour candidater.
      </p>

      <CspButton
        variant="primary"
        size="lg"
        :icon="estExterne ? 'ri:external-link-line' : undefined"
        :label="estExterne ? `Postuler sur ${offre.partenaireNom}` : 'Postuler'"
        class="offre__cta-button"
        @click="$emit('postuler')"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.offre {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--background-default-grey);
}

.offre__scroll {
  flex: 1;
  padding: var(--csp-space-4) var(--csp-space-4) calc(var(--csp-space-8) * 2);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.offre__breadcrumb {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  align-self: flex-start;
  margin: 0;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.offre__titre {
  margin: 0;
  font-size: 1.375rem;
  font-weight: 700;
  line-height: 1.25;
  color: var(--text-title-grey);
}

.offre__organisme {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--text-default-grey);
}

.offre__meta {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  list-style: none;
  margin: var(--csp-space-2) 0;
  padding: var(--csp-space-3);
  border-radius: 0.5rem;
  background-color: var(--background-alt-grey);

  li {
    display: flex;
    align-items: center;
    gap: var(--csp-space-2);
    font-size: 0.875rem;
    color: var(--text-default-grey);
  }
}

.offre__section {
  margin-top: var(--csp-space-2);

  h2 {
    margin: 0 0 var(--csp-space-2);
    font-size: 1.0625rem;
    font-weight: 700;
    color: var(--text-title-grey);
  }

  p {
    margin: 0;
    font-size: 0.9375rem;
    line-height: 1.55;
    color: var(--text-default-grey);
  }
}

.offre__liste {
  margin: 0;
  padding-left: 1.125rem;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  font-size: 0.9375rem;
  line-height: 1.5;
  color: var(--text-default-grey);
}

.offre__accordeon {
  margin-top: var(--csp-space-2);
  padding: var(--csp-space-3);
  border-radius: 0.5rem;
  background-color: var(--background-alt-grey);

  summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-title-grey);
    list-style: none;
    min-height: 2rem;

    &::-webkit-details-marker {
      display: none;
    }
  }

  &[open] summary .offre__accordeon-icon {
    transform: rotate(180deg);
  }
}

.offre__accordeon-icon {
  transition: transform 0.15s ease;
  color: var(--text-mention-grey);
}

.offre__infos {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: var(--csp-space-3) 0 0;

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

.offre__etapes {
  margin: var(--csp-space-3) 0 0;
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

.offre__etape-numero {
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

.offre__cta {
  position: sticky;
  bottom: 0;
  padding: var(--csp-space-3) var(--csp-space-4) max(var(--csp-space-3), env(safe-area-inset-bottom));
  background-color: var(--background-default-grey);
  box-shadow: inset 0 1px 0 var(--border-default-grey), 0 -2px 8px rgb(0 0 0 / 6%);
}

.offre__cta-hint {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0 0 var(--csp-space-2);
  font-size: 0.75rem;
  color: var(--text-mention-grey);
  text-align: center;
  justify-content: center;

  &--externe {
    color: var(--text-default-info);
  }
}

.offre__cta-button {
  width: 100%;
  justify-content: center;
  min-height: 3rem;
}

@media (min-width: 40rem) {
  .offre__scroll {
    max-width: 34rem;
    margin: 0 auto;
    width: 100%;
  }

  .offre__cta {
    display: flex;
    flex-direction: column;
    align-items: center;

    > * {
      max-width: 34rem;
      width: 100%;
    }
  }
}
</style>
