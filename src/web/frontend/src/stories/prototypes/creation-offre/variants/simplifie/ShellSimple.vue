<script setup lang="ts">
import { computed, ref } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSidebarProvider from '@/components/layout/CspSidebar/CspSidebarProvider.vue'
import { personne } from '../../data/referentiels'
import { LIBELLES_STATUT, useOffre } from '../../data/useOffre'
import AppSidebar from './AppSidebar.vue'
import EtapesNav from './EtapesNav.vue'
import SuiviDrawer from './SuiviDrawer.vue'
import { useApp } from './useApp'

// Cadre de la version simplifiée : une barre d'offre (statut, enregistrement, suivi),
// 4 étapes en onglets, un seul bandeau d'état quand il y a vraiment quelque chose à savoir.
const { state, dirty, saving, lastSaved, enregistrer, notifier, flash, etapeEnCours, retirerDeValidation, modifierApresValidation } = useOffre()

const { quitter } = useApp()
const suivi = ref(false)
const statut = computed(() => LIBELLES_STATUT[state.statut])
/** État de la DAR, affiché à côté de celui de l'offre : deux objets, deux statuts. */
const etatDar = computed(() => {
  const b = state.besoin
  if (b.darApplicable !== 'oui' || !b.darRef) {
    return ''
  }
  return { 'validee': 'DAR validée', 'en_cours': 'DAR soumise', 'a_demander': 'DAR en brouillon', '': 'DAR en brouillon' }[b.darStatut]
})
const remarquesOuvertes = computed(() => state.remarques.filter(r => !r.resolue).length)

async function sauver() {
  await enregistrer()
  notifier('Brouillon enregistré. Vous pouvez quitter et le reprendre depuis « Offres ».')
}
</script>

<template>
  <CspSidebarProvider :default-expanded="false">
    <div class="cs-app">
      <AppSidebar />

      <div class="cs-app__content">
        <header class="cs-bar">
          <div class="cs-bar__id">
            <p class="cs-bar__crumb">
              <button
                type="button"
                class="cs-bar__back"
                @click="quitter()"
              >
                Recrutements
              </button>
              <span aria-hidden="true">›</span> {{ state.reference }}
            </p>
            <h1 class="cs-bar__title">
              {{ state.besoin.intitule || 'Nouvelle offre' }}
            </h1>
          </div>
          <div class="cs-bar__right">
            <span
              v-if="etatDar"
              class="cs-bar__dar"
            >{{ state.besoin.darRef }} · {{ etatDar }}</span>
            <CspBadge
              :label="state.statut === 'brouillon' ? 'Offre en brouillon' : statut.label"
              :type="state.statut === 'a_corriger' ? 'warning' : statut.type"
              variant="soft"
              size="sm"
            />
            <span
              class="cs-bar__save"
              aria-live="polite"
            >
              <template v-if="saving">
                <CspIcon
                  name="ri:loader-4-line"
                  class="cs-spin"
                  :size="14"
                />
                Enregistrement en cours…
              </template>
              <template v-else-if="dirty">Modifications en cours…</template>
              <template v-else-if="lastSaved">
                <CspIcon
                  name="ri:check-line"
                  :size="14"
                />
                Enregistré {{ lastSaved }}
              </template>
            </span>
            <CspButton
              label="Suivi"
              variant="tertiary"
              size="sm"
              icon="ri:history-line"
              is-icon-left
              @click="suivi = true"
            />
            <CspButton
              v-if="state.statut === 'brouillon' || state.statut === 'a_corriger'"
              label="Enregistrer le brouillon"
              variant="secondary"
              size="sm"
              :disabled="saving || !dirty"
              @click="sauver"
            />
            <CspButton
              label="Quitter"
              variant="tertiary-no-outline"
              size="sm"
              icon="ri:close-line"
              is-icon-left
              @click="quitter()"
            />
          </div>
        </header>

        <EtapesNav />

        <main class="cs-main">
          <div class="cs-main__inner">
            <div
              v-if="state.statut === 'a_valider'"
              class="cs-banner"
              role="status"
            >
              <CspIcon
                name="ri:time-line"
                :size="16"
              />
              <span>En validation<template v-if="etapeEnCours"> auprès de {{ personne(etapeEnCours.personneId).nom }}</template>. L'offre est en lecture seule.</span>
              <button
                type="button"
                class="cs-banner__link"
                @click="retirerDeValidation"
              >
                Retirer de la validation pour modifier
              </button>
            </div>
            <div
              v-else-if="state.statut === 'a_corriger' && remarquesOuvertes"
              class="cs-banner"
              role="status"
            >
              <CspIcon
                name="ri:chat-1-line"
                :size="16"
              />
              <span>{{ remarquesOuvertes }} correction(s) demandée(s). Elles sont indiquées dans les sections concernées.</span>
              <button
                type="button"
                class="cs-banner__link"
                @click="suivi = true"
              >
                Voir le suivi
              </button>
            </div>
            <div
              v-else-if="state.statut === 'validee'"
              class="cs-banner cs-banner--ok"
              role="status"
            >
              <CspIcon
                name="ri:checkbox-circle-line"
                :size="16"
              />
              <span>Offre validée, prête à publier.</span>
              <button
                type="button"
                class="cs-banner__link"
                @click="modifierApresValidation"
              >
                Modifier (nouvelle validation nécessaire)
              </button>
            </div>
            <slot />
          </div>
        </main>
      </div>

      <SuiviDrawer v-model:open="suivi" />

      <div
        class="cs-flash-region"
        aria-live="polite"
      >
        <div
          v-if="flash"
          class="cs-flash"
        >
          <CspIcon
            :name="flash.variant === 'warning' ? 'ri:information-line' : 'ri:checkbox-circle-line'"
            :size="16"
          />
          {{ flash.texte }}
        </div>
      </div>
    </div>
  </CspSidebarProvider>
</template>

<style scoped lang="scss">
.cs-app {
  display: flex;
  height: 100vh;
  background: var(--background-alt-grey);
  color: var(--text-default-grey);
}

.cs-app__content {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.cs-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-4);
  padding: var(--csp-space-3) var(--csp-space-6);
  background: var(--background-default-grey);
  border-bottom: 1px solid var(--border-default-grey);
}

.cs-bar__id {
  min-width: 0;
}

.cs-bar__crumb {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.cs-bar__title {
  margin: 0;
  font-size: var(--csp-font-size-lg);
  line-height: var(--csp-line-height-tight);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cs-bar__right {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  flex-shrink: 0;
}

.cs-bar__save {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.cs-bar__dar {
  padding: 0 var(--csp-space-2);
  border: 1px solid var(--border-default-grey);
  border-radius: 1rem;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
  white-space: nowrap;
}

.cs-bar__back {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}

.cs-spin {
  animation: cs-spin 1s linear infinite;
}

@keyframes cs-spin {
  to {
    transform: rotate(360deg);
  }
}

.cs-main {
  flex: 1;
  overflow-y: auto;
}

.cs-main__inner {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  max-width: 54rem;
  margin: 0 auto;
  padding: var(--csp-space-6) var(--csp-space-6) var(--csp-space-12);
}

.cs-banner {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
  border-left: 3px solid var(--border-plain-blue-france);
  font-size: var(--csp-font-size-sm);

  span {
    flex: 1;
  }

  &--ok {
    border-left-color: var(--border-plain-success);
  }
}

.cs-banner__link {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}

.cs-flash-region {
  position: fixed;
  bottom: var(--csp-space-6);
  left: 50%;
  transform: translateX(-50%);
  z-index: var(--csp-z-toast, 50);
}

.cs-flash {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
  box-shadow: var(--csp-shadow-md);
  font-size: var(--csp-font-size-sm);
}
</style>
