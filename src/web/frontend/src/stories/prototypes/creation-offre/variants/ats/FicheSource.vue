<script setup lang="ts">
import type { Fiche } from './store'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import OrigineBadge from './OrigineBadge.vue'

// La fiche de poste source, en consultation seule, à côté de l'annonce qu'on rédige.
defineProps<{ fiche: Fiche }>()
</script>

<template>
  <div
    class="source"
  >
    <p class="source__tete">
      <CspIcon
        name="ri:lock-line"
        :size="14"
      />
      {{ fiche.id }} · <OrigineBadge
        :origine="fiche.origine"
        court
      /> · consultation seule
    </p>
    <h3 class="source__titre">
      {{ fiche.intitule }}
    </h3>
    <p class="source__meta">
      {{ fiche.service }} · {{ fiche.localisation }}
    </p>
    <p class="source__label">
      Missions
    </p>
    <p class="source__texte">
      {{ fiche.missions || '-' }}
    </p>
    <ul
      v-if="fiche.activites.length"
      class="source__liste"
    >
      <li
        v-for="a in fiche.activites"
        :key="a"
      >
        {{ a }}
      </li>
    </ul>
    <p class="source__label">
      Profil
    </p>
    <p class="source__texte">
      {{ fiche.profil || '-' }}
    </p>
  </div>
</template>

<style scoped lang="scss">
.source {
  font-size: var(--csp-font-size-sm);

  p {
    margin: 0;
  }
}

.source__tete {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.source__titre {
  margin: var(--csp-space-2) 0 0;
  font-size: var(--csp-font-size-lg);
}

.source__meta {
  color: var(--text-mention-grey);
}

.source__label {
  margin-top: var(--csp-space-3) !important;
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.source__liste {
  margin: 0;
  padding-left: var(--csp-space-5);
  list-style: disc;
}
</style>
