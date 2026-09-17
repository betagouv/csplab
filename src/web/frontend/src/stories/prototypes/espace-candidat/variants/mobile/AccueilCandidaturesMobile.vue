<script setup lang="ts">
import type { ActionRequise } from '../../data/candidatMock'
import { actionsRequises, candidatures } from '../../data/candidatMock'
import ActionRequiseCard from '../../shared/ActionRequiseCard.vue'
import CandidatureCard from '../../shared/CandidatureCard.vue'
import MobileTopBar from '../../shared/mobile/MobileTopBar.vue'
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'

defineEmits<{
  ouvrirCandidature: [id: string]
  ouvrirProfil: []
  agir: [action: ActionRequise]
}>()
</script>

<template>
  <div class="accueil">
    <MobileTopBar title="Mes candidatures">
      <template #end>
        <button
          type="button"
          class="accueil__profil"
          aria-label="Mon profil"
          @click="$emit('ouvrirProfil')"
        >
          <CspAvatar
            name="Camille Rousseau"
            size="sm"
          />
        </button>
      </template>
    </MobileTopBar>

    <div class="accueil__content">
      <section
        v-if="actionsRequises.length > 0"
        class="accueil__section"
      >
        <h2 class="accueil__titre">
          {{ actionsRequises.length }} action{{ actionsRequises.length > 1 ? 's' : '' }} à effectuer
        </h2>
        <div class="accueil__actions">
          <ActionRequiseCard
            v-for="action in actionsRequises"
            :key="action.id"
            :action="action"
            @agir="$emit('agir', action)"
          />
        </div>
      </section>

      <section class="accueil__section">
        <h2 class="accueil__titre">
          Où en sont mes candidatures ?
        </h2>
        <div class="accueil__candidatures">
          <CandidatureCard
            v-for="candidature in candidatures"
            :key="candidature.id"
            :candidature="candidature"
            @ouvrir="$emit('ouvrirCandidature', $event)"
          />
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped lang="scss">
.accueil {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.accueil__content {
  padding: var(--csp-space-4);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
}

.accueil__titre {
  margin: 0 0 var(--csp-space-3);
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.accueil__actions {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.accueil__candidatures {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.accueil__profil {
  display: flex;
  border: none;
  background: none;
  cursor: pointer;
  padding: 0;
  border-radius: 50%;
}
</style>
