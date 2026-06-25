<script setup lang="ts">
import type { EtapePrototype, StatutCandidat } from '../../data/pipelineMock'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSortableList from '@/components/base/CspSortableList/CspSortableList.vue'
import { createPipeline, isObligatoire, statutCandidatLabels, statutCandidatVisuel } from '../../data/pipelineMock'

interface Props {
  // 'mirror' = colonne candidat à droite ; 'inline' = pastille + légende.
  variant: 'mirror' | 'inline'
}

defineProps<Props>()

const etapes = ref<EtapePrototype[]>(createPipeline())

function onReorder(items: EtapePrototype[]) {
  etapes.value = items
}

function variantOf(etape: EtapePrototype): 'default' | 'alt' {
  return isObligatoire(etape) ? 'alt' : 'default'
}

// Statuts effectivement présents, pour la légende de la variante inline.
const statutsUtilises = computed(() => {
  const seen = new Set<StatutCandidat>()
  const ordered: StatutCandidat[] = []
  for (const e of etapes.value) {
    if (!seen.has(e.statutCandidat)) {
      seen.add(e.statutCandidat)
      ordered.push(e.statutCandidat)
    }
  }
  return ordered
})
</script>

<template>
  <section
    class="visi"
    :class="`visi--${variant}`"
  >
    <div class="visi__cols">
      <div class="visi__recruteur">
        <p class="visi__col-title">
          Vos étapes
        </p>

        <CspSortableList
          :items="etapes"
          :get-item-key="(e: EtapePrototype) => e.identifiant"
          :get-item-label="(e: EtapePrototype) => e.nom"
          :is-item-draggable="(e: EtapePrototype) => !isObligatoire(e)"
          :get-item-variant="variantOf"
          @reorder="onReorder"
        >
          <template #item="{ item, isDraggable }">
            <span class="visi__name">{{ item.nom }}</span>
            <span
              v-if="!isDraggable"
              class="visi__flag"
            >Obligatoire</span>

            <!-- Variante inline : pastille d'état candidat (ton doctrine, atténué) -->
            <span
              v-if="variant === 'inline'"
              class="visi__dot"
              :class="`visi__dot--${statutCandidatVisuel[item.statutCandidat].ton}`"
              :title="`Vu par le candidat : ${statutCandidatLabels[item.statutCandidat]}`"
              aria-hidden="true"
            />
            <span
              v-if="variant === 'inline'"
              class="visi__sr-only"
            >Vu par le candidat : {{ statutCandidatLabels[item.statutCandidat] }}</span>
          </template>
        </CspSortableList>
      </div>

      <!-- Variante mirror : colonne candidat alignée ligne à ligne -->
      <ol
        v-if="variant === 'mirror'"
        class="visi__candidat"
        aria-label="Aperçu de ce que voit le candidat"
      >
        <li class="visi__candidat-title">
          <span class="visi__col-title">Ce que voit le candidat</span>
        </li>
        <li
          v-for="(etape, index) in etapes"
          :key="etape.identifiant"
          class="visi__tl-item"
          :class="[
            `visi__tl-item--${statutCandidatVisuel[etape.statutCandidat].ton}`,
            { 'visi__tl-item--first': index === 0, 'visi__tl-item--last': index === etapes.length - 1 },
          ]"
        >
          <span class="visi__tl-marker">
            <CspIcon
              :name="statutCandidatVisuel[etape.statutCandidat].icon"
              :size="16"
            />
          </span>
          <span class="visi__tl-label">{{ statutCandidatLabels[etape.statutCandidat] }}</span>
        </li>
      </ol>
    </div>

    <!-- Variante inline : légende globale, couleurs atténuées -->
    <div
      v-if="variant === 'inline'"
      class="visi__legend"
    >
      <span class="visi__legend-title">Vu par le candidat :</span>
      <span
        v-for="statut in statutsUtilises"
        :key="statut"
        class="visi__legend-item"
      >
        <span
          class="visi__dot"
          :class="`visi__dot--${statutCandidatVisuel[statut].ton}`"
          aria-hidden="true"
        />
        {{ statutCandidatLabels[statut] }}
      </span>
    </div>

    <CspButton
      class="visi__add"
      label="Ajouter une étape"
      icon="ri:add-line"
      variant="tertiary"
      is-icon-left
      size="sm"
    />
  </section>
</template>

<style scoped lang="scss">
.visi {
  max-width: 48rem;

  // Tons alignés sur la doctrine des badges (CspBadge), version atténuée :
  // fond très clair (contrast-*) + couleur de texte de l'état (text-default-*).
  --ton-neutre-bg: var(--background-contrast-grey);
  --ton-neutre-fg: var(--text-mention-grey);
  --ton-info-bg: var(--background-contrast-info);
  --ton-info-fg: var(--text-default-info);
  --ton-error-bg: var(--background-contrast-error);
  --ton-error-fg: var(--text-default-error);
  --ton-success-bg: var(--background-contrast-success);
  --ton-success-fg: var(--text-default-success);

  // Rythme vertical du composant CspSortableList, repris pour aligner la colonne
  // candidat : chaque rangée = padding 12/16 + icône 16px ; gap inter-rangées = space-2.
  --row-pad-y: var(--csp-space-3);
  --row-line: 1.25rem;
  --row-gap: var(--csp-space-2);
}

.visi__cols {
  display: grid;
  gap: var(--csp-space-6);
  grid-template-columns: minmax(0, 1fr);
}

.visi--mirror .visi__cols {
  grid-template-columns: minmax(0, 1fr) 13rem;
  align-items: start;
}

.visi__col-title {
  margin: 0 0 var(--csp-space-3);
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--text-mention-grey);
}

.visi__name {
  flex: 1;
  min-width: 0;
}

.visi__flag {
  flex: 0 0 auto;
  font-size: 0.6875rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--text-mention-grey);
}

/* --- Pastilles inline (atténuées) --- */
.visi__dot {
  flex: 0 0 auto;
  width: 0.625rem;
  height: 0.625rem;
  border-radius: 50%;
  background: var(--dot-fg, var(--text-mention-grey));
}

.visi__dot--neutre {
  --dot-fg: var(--ton-neutre-fg);
}
.visi__dot--info {
  --dot-fg: var(--ton-info-fg);
}
.visi__dot--error {
  --dot-fg: var(--ton-error-fg);
}
.visi__dot--success {
  --dot-fg: var(--ton-success-fg);
}

/* --- Variante mirror : timeline candidat, alignée sur les rangées de gauche --- */
.visi__candidat {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--row-gap);
}

.visi__candidat-title {
  // Occupe la hauteur de l'en-tête « Vos étapes » de gauche.
  display: flex;
  align-items: flex-end;
  margin-bottom: 0;

  .visi__col-title {
    margin: 0;
  }
}

.visi__tl-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  // Même hauteur de boîte que les rangées du composant (padding haut/bas + ligne).
  padding: var(--row-pad-y) 0;
  min-height: calc(var(--row-line) + 2 * var(--row-pad-y));
  box-sizing: border-box;
  color: var(--text-default-grey);

  // Trait de liaison entre marqueurs, centré sur le marqueur (1.75rem / 2).
  &::before {
    content: '';
    position: absolute;
    left: calc(0.875rem - 1px);
    top: 0;
    bottom: 0;
    width: 2px;
    background: var(--border-default-grey);
    z-index: 0;
  }

  &--first::before {
    top: 50%;
  }

  &--last::before {
    bottom: 50%;
  }
}

.visi__tl-marker {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.75rem;
  height: 1.75rem;
  flex: 0 0 auto;
  border-radius: 50%;
  background: var(--marker-bg, var(--background-default-grey));
  box-shadow: inset 0 0 0 1.5px var(--marker-fg, var(--border-default-grey));
  color: var(--marker-fg, var(--text-mention-grey));
}

.visi__tl-item--neutre {
  --marker-fg: var(--ton-neutre-fg);
  --marker-bg: var(--ton-neutre-bg);
}
.visi__tl-item--info {
  --marker-fg: var(--ton-info-fg);
  --marker-bg: var(--ton-info-bg);
}
.visi__tl-item--error {
  --marker-fg: var(--ton-error-fg);
  --marker-bg: var(--ton-error-bg);
}
.visi__tl-item--success {
  --marker-fg: var(--ton-success-fg);
  --marker-bg: var(--ton-success-bg);
}

.visi__tl-label {
  font-size: 0.875rem;
  font-weight: 500;
}

/* --- Variante inline : légende --- */
.visi__legend {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-4);
  margin-top: var(--csp-space-4);
  padding: var(--csp-space-3) var(--csp-space-4);
  border-radius: 0.25rem;
  background: var(--background-alt-grey, var(--background-contrast-grey));
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.visi__legend-title {
  font-weight: 500;
}

.visi__legend-item {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-2);
}

.visi__add {
  margin-top: var(--csp-space-4);
}

.visi__sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>
