<script setup lang="ts">
import type { Champ } from './aide'
import type { Offre } from './store'
import { computed, ref } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { alerte, CONSEILS } from './aide'

// Un champ de l'annonce avec son aide légère : un conseil (et un exemple à la demande),
// une alerte discrète au besoin, et l'indication « repris de la fiche » tant que le texte n'a pas été adapté.
const props = defineProps<{
  offre: Offre
  champ: Champ
  label?: string
  forId?: string
  repris?: boolean
  modifie?: boolean
}>()
const emit = defineEmits<{ restaurer: [] }>()

const aide = computed(() => CONSEILS[props.champ])
const a = computed(() => alerte(props.offre, props.champ))
const exemple = ref(false)
</script>

<template>
  <div class="champ">
    <div
      v-if="label"
      class="champ__tete"
    >
      <label
        :for="forId"
        class="champ__label"
      >{{ label }}</label>
      <span
        v-if="repris"
        class="champ__tag"
      >Repris de la fiche</span>
      <button
        v-else-if="modifie"
        type="button"
        class="champ__lien"
        @click="emit('restaurer')"
      >
        Reprendre le texte de la fiche
      </button>
    </div>
    <p class="champ__conseil">
      {{ aide.conseil }}
      <button
        v-if="aide.exemple"
        type="button"
        class="champ__lien"
        :aria-expanded="exemple"
        @click="exemple = !exemple"
      >
        {{ exemple ? 'Masquer l\'exemple' : 'Exemple' }}
      </button>
    </p>
    <p
      v-if="exemple"
      class="champ__exemple"
    >
      {{ aide.exemple }}
    </p>
    <slot />
    <p
      v-if="a"
      class="champ__alerte"
      :class="`champ__alerte--${a.niveau}`"
    >
      <CspIcon
        :name="a.niveau === 'attention' ? 'ri:error-warning-line' : 'ri:lightbulb-line'"
        :size="14"
      />
      {{ a.texte }}
    </p>
  </div>
</template>

<style scoped lang="scss">
.champ {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
}

.champ__tete {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: var(--csp-space-3);
}

.champ__label {
  font-weight: var(--csp-font-weight-bold);
}

.champ__tag {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.champ__conseil,
.champ__exemple,
.champ__alerte {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.champ__exemple {
  padding: var(--csp-space-2) var(--csp-space-3);
  background: var(--background-alt-blue-france);
  color: var(--text-default-grey);
}

.champ__alerte {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);

  &--attention {
    color: var(--text-default-warning);
  }
}

.champ__lien {
  margin-left: var(--csp-space-1);
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  font-size: var(--csp-font-size-xs);
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}
</style>
