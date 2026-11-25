<script setup lang="ts">
import type { PartieOffre } from './etapes'
import type { Offre } from './store'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { avancementEtape, champsObligatoires } from './aide'
import { ETAPES_OFFRE } from './etapes'
import FormEtape from './FormEtape.vue'
import { resume } from './resume'
import TexteEtoile from './TexteEtoile.vue'

// Un bloc de la page de l'offre (façon Malt, retour Alice du 25/11/2026) : l'étape en lecture, et un crayon pour
// la modifier sur place. On modifie une copie : « Annuler » ne change rien, « Enregistrer » applique.
const props = defineProps<{ offre: Offre, partie: PartieOffre, modifiable: boolean, verrouille?: string }>()
const emit = defineEmits<{ enregistre: [titre: string] }>()
const edition = defineModel<boolean>('edition', { default: false })
const etape = computed(() => ETAPES_OFFRE.find(e => e.id === props.partie)!)
const lignes = computed(() => resume(props.offre, props.partie))
const champs = computed(() => champsObligatoires(props.offre).filter(c => c.partie === props.partie))
const total = computed(() => champs.value.length)
const reste = computed(() => champs.value.filter(c => !c.ok).length)

const copie = ref<Offre | null>(null)
watch(edition, (v) => {
  copie.value = v ? JSON.parse(JSON.stringify(props.offre)) as Offre : null
}, { immediate: true })

function enregistrer() {
  const cible = props.offre
  Object.assign(cible, JSON.parse(JSON.stringify(copie.value)))
  edition.value = false
  emit('enregistre', etape.value.titre)
}
</script>

<template>
  <section
    :id="`bloc-${partie}`"
    class="bloc"
    :class="{ 'bloc--edition': edition }"
  >
    <header class="bloc__tete">
      <h3 class="bloc__titre">
        {{ etape.titre }}
      </h3>
      <span
        v-if="reste"
        class="bloc__reste"
      >
        <CspIcon
          name="ri:error-warning-line"
          :size="16"
        />
        <TexteEtoile :texte="avancementEtape(total, reste)" />
      </span>
      <span class="bloc__espace" />
      <span
        v-if="verrouille"
        class="bloc__verrou"
      >
        <CspIcon
          name="ri:lock-line"
          :size="16"
        />
        {{ verrouille }}
      </span>
      <CspButton
        v-else-if="modifiable && !edition"
        icon="ri:pencil-line"
        variant="tertiary-no-outline"
        size="sm"
        :aria-label="`Modifier : ${etape.titre}`"
        title="Modifier"
        @click="edition = true"
      />
    </header>

    <template v-if="edition && copie">
      <FormEtape
        :offre="copie"
        :partie="partie"
      />
      <div class="bloc__actions">
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="edition = false"
        />
        <CspButton
          label="Enregistrer"
          @click="enregistrer"
        />
      </div>
    </template>

    <dl
      v-else
      class="lecture"
    >
      <div
        v-for="l in lignes"
        :key="l.label"
        class="lecture__ligne"
        :class="{ 'lecture__ligne--long': l.long || l.liste }"
      >
        <dt>{{ l.label }}</dt>
        <dd v-if="l.liste && l.liste.length">
          <ul class="puces">
            <li
              v-for="x in l.liste"
              :key="x"
            >
              {{ x }}
            </li>
          </ul>
        </dd>
        <dd
          v-else-if="l.valeur"
          class="lecture__valeur"
        >
          {{ l.valeur }}
        </dd>
        <dd
          v-else-if="l.manque"
          class="lecture__manque"
        >
          À renseigner
        </dd>
        <dd
          v-else
          class="lecture__vide"
        >
          Non renseigné
        </dd>
      </div>
    </dl>
  </section>
</template>

<style scoped lang="scss">
.bloc {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  padding: var(--csp-space-6) var(--csp-space-8);
  border: 1px solid var(--border-default-grey);
  border-radius: 0.75rem;
  background: var(--background-default-grey);
  scroll-margin-top: var(--csp-space-16, 4rem);

  &--edition {
    border-color: var(--border-active-blue-france);
    box-shadow: inset 0 0 0 1px var(--border-active-blue-france);
  }
}

.bloc__tete {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-3);
}

.bloc__titre {
  margin: 0;
  font-size: 1.25rem;
  line-height: 1.3;
}

.bloc__reste,
.bloc__verrou {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-sm);
}

.bloc__reste {
  color: var(--text-default-warning);
}

.bloc__verrou {
  color: var(--text-mention-grey);
}

.bloc__espace {
  flex: 1;
}

.bloc__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
  padding-top: var(--csp-space-4);
  border-top: 1px solid var(--border-default-grey);
}

.lecture {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--csp-space-4) var(--csp-space-8);
  margin: 0;
}

.lecture__ligne {
  min-width: 0;

  &--long {
    grid-column: 1 / -1;
  }

  dt {
    font-size: var(--csp-font-size-sm);
    font-weight: 700;
    color: var(--text-title-grey);
  }

  dd {
    margin: 2px 0 0;
    white-space: pre-line;
  }
}

.lecture__vide {
  color: var(--text-mention-grey);
}

.lecture__manque {
  font-weight: 600;
  color: var(--text-default-warning);
}

.puces {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: var(--csp-space-1) 0 0;
  padding: 0;
  list-style: none;

  li {
    padding: 2px var(--csp-space-3);
    border-radius: 0.5rem;
    background: var(--background-alt-blue-france);
    font-size: var(--csp-font-size-sm);
    color: var(--text-action-high-blue-france);
  }
}
</style>
