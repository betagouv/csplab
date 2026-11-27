<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { dateLongue, SITES_PARTENAIRES, SUPPORT_MAITRE } from './store'

// Partie 3 « Multidiffusion » (Alice, 27/11/2026) : l'offre est publiée par défaut sur Choisir le Service Public ; on coche
// directement les sites partenaires en plus, sans question oui / non. Les candidatures sont toujours gérées dans l'ATS
// (retour PO, 27/11/2026) ; seules les offres téléversées sont gérées hors ATS : on le rappelle, en lecture seule.
// En lecture (page de l'offre, revue Alice du 27/11/2026) : les mêmes cartes, sans case, avec l'état de publication de chaque site.
const props = defineProps<{ offre: Offre, lecture?: boolean }>()
const o = computed(() => props.offre)
const horsAts = computed(() => o.value.modeCandidature !== 'ats')

function coche(id: string) {
  return o.value.canaux.includes(id)
}
function publication(id: string) {
  return o.value.publications[id]
}
function basculer(id: string, v: boolean) {
  if (props.lecture) {
    return
  }
  const autres = o.value.canaux.filter(c => c !== id && c !== SUPPORT_MAITRE.id)
  const partenaires = [...autres, ...(v ? [id] : [])]
  o.value.canaux = [SUPPORT_MAITRE.id, ...partenaires]
  o.value.diffusion = partenaires.length ? 'multi' : 'simple'
}
const NOM_MAITRE = SUPPORT_MAITRE.nom
// Pas de vrais logos dans le proto : une pastille avec les initiales du site.
function initiales(nom: string) {
  return nom.split(/\s+/).map(m => m[0]).join('').slice(0, 2).toUpperCase()
}
</script>

<template>
  <div
    v-if="horsAts"
    class="groupe"
  >
    <h3 class="groupe__titre">
      Gestion des candidatures
    </h3>
    <p class="valeur">
      Candidatures gérées hors de l'ATS
      <span class="valeur__note">
        Les candidats postulent {{ o.modeCandidature === 'courriel' ? `par courriel (${o.courrielCandidature})` : `sur ${o.urlCandidature}` }}.
      </span>
    </p>
  </div>

  <div class="groupe">
    <p
      v-if="!lecture"
      class="intro"
    >
      L'offre est par défaut publiée sur <strong>{{ NOM_MAITRE }}</strong>. Vous pouvez aussi la diffuser sur d'autres sites.
    </p>
    <div
      v-else
      class="maitre"
    >
      <span class="maitre__nom">{{ NOM_MAITRE }}</span>
      <span class="maitre__note">Par défaut</span>
      <template v-if="publication('csp')">
        <CspBadge
          :label="publication('csp')!.etat === 'publiee' ? 'En ligne' : 'Arrêtée'"
          :type="publication('csp')!.etat === 'publiee' ? 'success' : 'info'"
          size="sm"
        />
        <span class="maitre__note">Depuis le {{ publication('csp')!.debut }} · jusqu'au {{ dateLongue(publication('csp')!.fin) }}</span>
      </template>
      <span
        v-else
        class="maitre__note"
      >Publiée à la mise en ligne de l'offre</span>
    </div>
    <fieldset class="sites">
      <legend class="sites__legende">
        Sites partenaires (liste indicative)
      </legend>
      <!-- Toute la carte est cliquable ; la case reste le contrôle pour le clavier et les lecteurs d'écran. -->
      <div
        class="sites__grille"
        :class="{ 'sites__grille--lecture': lecture }"
      >
        <div
          v-for="s in SITES_PARTENAIRES"
          :key="s.id"
          class="site"
          :class="{ 'site--coche': coche(s.id) && !lecture, 'site--off': lecture && !coche(s.id) }"
          @click="basculer(s.id, !coche(s.id))"
        >
          <div class="site__tete">
            <span
              class="site__logo"
              aria-hidden="true"
            >{{ initiales(s.nom) }}</span>
            <span
              v-if="!lecture"
              @click.stop
            >
              <CspCheckbox
                variant="checkbox-only"
                :model-value="coche(s.id)"
                :label="`${s.nom} : ${s.detail}, ${s.modalite}`"
                @update:model-value="(v?: boolean) => basculer(s.id, Boolean(v))"
              />
            </span>
          </div>
          <span class="site__nom">{{ s.nom }}</span>
          <span class="site__public">
            <CspIcon
              name="ri:group-line"
              :size="14"
            />
            {{ s.detail }}
          </span>
          <span class="site__modalite">
            <CspIcon
              name="ri:information-line"
              :size="14"
            />
            {{ s.modalite }}
          </span>
          <span
            v-if="lecture"
            class="site__etat"
          >
            <template v-if="publication(s.id)">
              <CspBadge
                :label="publication(s.id)!.etat === 'publiee' ? 'En ligne' : 'Arrêtée'"
                :type="publication(s.id)!.etat === 'publiee' ? 'success' : 'info'"
                size="sm"
              />
              <span class="site__date">Depuis le {{ publication(s.id)!.debut }}</span>
            </template>
            <span
              v-else-if="coche(s.id)"
              class="site__date"
            >Publiée à la mise en ligne de l'offre</span>
            <span
              v-else
              class="site__date"
            >Non diffusée</span>
          </span>
        </div>
      </div>
    </fieldset>
  </div>
</template>

<style scoped lang="scss">
.groupe {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  max-width: 60rem;

  & + & {
    margin-top: var(--csp-space-3);
    padding-top: var(--csp-space-6);
    border-top: 1px solid var(--border-default-grey);
  }
}

.groupe__titre {
  margin: 0;
  font-size: 1.125rem;
  font-weight: var(--csp-font-weight-bold);
  line-height: 1.4;
  color: var(--text-title-grey);
}

.groupe__desc {
  margin: calc(-1 * var(--csp-space-2)) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.valeur {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-sm);
}

.valeur__note {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.sites {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  border: 0;
}

.sites__legende {
  margin-bottom: var(--csp-space-2);
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
}

.sites__grille {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr));
  gap: var(--csp-space-3);
}

// Même structure d'une carte à l'autre : les lignes (en-tête, nom, public, modalité) s'alignent entre les cartes.
.site {
  display: grid;
  grid-row: span 4;
  grid-template-rows: subgrid;
  row-gap: var(--csp-space-2);
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  cursor: pointer;

  &:hover {
    background: var(--background-default-grey-hover);
  }

  .sites__grille--lecture & {
    grid-row: span 5;
    cursor: default;

    &:hover {
      background: var(--background-default-grey);
    }
  }

  &--off {
    border-style: dashed;

    .site__nom,
    .site__public {
      color: var(--text-mention-grey);
    }
  }

  &--coche {
    border-color: var(--border-active-blue-france);
    background: var(--background-alt-blue-france);

    &:hover {
      background: var(--background-alt-blue-france-hover);
    }
  }
}

.site__tete {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.site__logo {
  display: inline-grid;
  place-items: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.25rem;
  background: var(--background-contrast-grey);
  font-size: var(--csp-font-size-xs);
  font-weight: 700;
  color: var(--text-mention-grey);
}

.site__nom {
  font-weight: 700;
  color: var(--text-title-grey);
}

.site__public,
.site__modalite {
  display: flex;
  align-items: flex-start;
  gap: 4px;

  :deep(svg),
  .csp-icon {
    flex-shrink: 0;
    margin-top: 2px;
  }
}

.site__public {
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
}

.site__modalite {
  align-self: start;
  padding: 2px var(--csp-space-2);
  border-radius: 0.25rem;
  background: var(--background-contrast-grey);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.site__etat {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  padding-top: var(--csp-space-2);
  border-top: 1px solid var(--border-default-grey);
}

.site__date,
.maitre__note {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.maitre {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-2) var(--csp-space-3);
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
}

.maitre__nom {
  font-weight: 700;
}

.intro {
  margin: 0;
  font-size: var(--csp-font-size-sm);
}
</style>
