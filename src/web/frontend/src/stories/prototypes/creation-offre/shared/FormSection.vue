<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

// Bloc de formulaire. `nature` distingue visuellement les données internes (administratives,
// fiche de poste) du contenu éditorial destiné aux candidats.
withDefaults(defineProps<{
  titre: string
  description?: string
  nature?: 'interne' | 'candidat' | 'recrutement'
  facultatif?: boolean
}>(), {
  description: undefined,
  nature: 'interne',
  facultatif: false,
})

const NATURES = {
  interne: { icon: 'ri:lock-line', label: 'Usage interne — non publié' },
  candidat: { icon: 'ri:eye-line', label: 'Visible par les candidats' },
  recrutement: { icon: 'ri:settings-3-line', label: 'Paramétrage du recrutement' },
}
</script>

<template>
  <section
    class="form-section"
    :class="`form-section--${nature}`"
  >
    <header class="form-section__header">
      <div>
        <h3 class="form-section__title">
          {{ titre }}
          <span
            v-if="facultatif"
            class="form-section__optional"
          >facultatif</span>
        </h3>
        <p
          v-if="description"
          class="form-section__description"
        >
          {{ description }}
        </p>
      </div>
      <span class="form-section__nature">
        <CspIcon
          :name="NATURES[nature].icon"
          :size="12"
        />
        {{ NATURES[nature].label }}
      </span>
    </header>
    <div class="form-section__body">
      <slot />
    </div>
  </section>
</template>

<style scoped lang="scss">
.form-section {
  border: 1px solid var(--border-default-grey);
  border-left-width: 3px;
  background: var(--background-default-grey);

  &--interne {
    border-left-color: var(--border-plain-grey);
  }

  &--candidat {
    border-left-color: var(--border-plain-blue-france);
  }

  &--recrutement {
    border-left-color: var(--border-plain-purple-glycine, var(--border-plain-grey));
  }
}

.form-section__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--csp-space-4);
  padding: var(--csp-space-4) var(--csp-space-5) 0;
}

.form-section__title {
  margin: 0;
  font-size: var(--csp-font-size-md);
  font-weight: var(--csp-font-weight-bold);
  line-height: var(--csp-line-height-tight);
}

.form-section__optional {
  margin-inline-start: var(--csp-space-2);
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-regular);
  color: var(--text-mention-grey);
}

.form-section__description {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.form-section__nature {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  flex-shrink: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
  white-space: nowrap;

  .form-section--candidat & {
    color: var(--text-action-high-blue-france);
  }
}

.form-section__body {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  padding: var(--csp-space-4) var(--csp-space-5) var(--csp-space-5);
}
</style>
