<script setup lang="ts">
import type { Critere } from '../data/types'
import { ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import { TYPES_CRITERE } from '../data/referentiels'
import { nouvelId } from '../data/useOffre'

// Liste de critères typés : ajout, modification, suppression. Réutilisée pour
// les critères indispensables et souhaités.
const props = defineProps<{
  titre: string
  aide: string
  vide: string
  disabled?: boolean
}>()

const emit = defineEmits<{ supprime: [id: string] }>()

const criteres = defineModel<Critere[]>({ required: true })
const libelle = ref('')
const type = ref<Critere['type']>('competence')
const erreur = ref('')

function ajouter() {
  if (!libelle.value.trim()) {
    erreur.value = 'Décrivez le critère avant de l\'ajouter.'
    return
  }
  erreur.value = ''
  criteres.value = [...criteres.value, { id: nouvelId('c'), libelle: libelle.value.trim(), type: type.value }]
  libelle.value = ''
}

function maj(id: string, patch: Partial<Critere>) {
  criteres.value = criteres.value.map(c => (c.id === id ? { ...c, ...patch } : c))
}

function supprimer(id: string) {
  criteres.value = criteres.value.filter(c => c.id !== id)
  emit('supprime', id)
}
</script>

<template>
  <div class="criteres">
    <div class="criteres__head">
      <h4 class="criteres__title">
        {{ titre }} <span class="criteres__count">({{ criteres.length }})</span>
      </h4>
      <p class="criteres__aide">
        {{ aide }}
      </p>
    </div>
    <table
      v-if="criteres.length"
      class="criteres__table"
    >
      <thead>
        <tr>
          <th scope="col">
            Critère
          </th>
          <th
            scope="col"
            class="criteres__col-type"
          >
            Nature
          </th>
          <th scope="col">
            <span class="sr-only">Actions</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="c in criteres"
          :key="c.id"
        >
          <td>
            <input
              class="criteres__input"
              :value="c.libelle"
              :aria-label="`Libellé du critère ${c.libelle}`"
              :disabled="props.disabled"
              @change="maj(c.id, { libelle: ($event.target as HTMLInputElement).value })"
            >
          </td>
          <td>
            <select
              class="criteres__select"
              :value="c.type"
              :aria-label="`Nature du critère ${c.libelle}`"
              :disabled="props.disabled"
              @change="maj(c.id, { type: ($event.target as HTMLSelectElement).value as Critere['type'] })"
            >
              <option
                v-for="t in TYPES_CRITERE"
                :key="t.value"
                :value="t.value"
              >
                {{ t.label }}
              </option>
            </select>
          </td>
          <td class="criteres__actions">
            <CspButton
              v-if="!props.disabled"
              icon="ri:delete-bin-line"
              variant="tertiary-no-outline"
              size="sm"
              :aria-label="`Supprimer le critère ${c.libelle}`"
              @click="supprimer(c.id)"
            />
          </td>
        </tr>
      </tbody>
    </table>
    <p
      v-else
      class="criteres__vide"
    >
      {{ vide }}
    </p>
    <form
      v-if="!props.disabled"
      class="criteres__add"
      @submit.prevent="ajouter"
    >
      <CspInput
        v-model="libelle"
        size="sm"
        placeholder="Ex. : expérience de 2 ans en gestion de projet"
        :aria-label="`Nouveau critère — ${titre}`"
        :error="Boolean(erreur)"
        :error-message="erreur"
      />
      <CspSelect
        v-model="type"
        class="criteres__type"
        size="sm"
        label="Nature"
        :options="TYPES_CRITERE"
      />
      <CspButton
        type="submit"
        label="Ajouter"
        icon="ri:add-line"
        is-icon-left
        variant="secondary"
        size="sm"
      />
    </form>
  </div>
</template>

<style scoped lang="scss">
.criteres {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.criteres__title {
  margin: 0;
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-bold);
}

.criteres__count {
  font-weight: var(--csp-font-weight-regular);
  color: var(--text-mention-grey);
}

.criteres__aide {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.criteres__table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--csp-font-size-sm);

  th {
    text-align: left;
    font-weight: var(--csp-font-weight-medium);
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
    padding: var(--csp-space-1) var(--csp-space-2);
    border-bottom: 1px solid var(--border-default-grey);
  }

  td {
    padding: var(--csp-space-1) var(--csp-space-1);
    border-bottom: 1px solid var(--border-default-grey);
  }
}

.criteres__col-type {
  width: 12rem;
}

.criteres__actions {
  width: 2.5rem;
  text-align: right;
}

.criteres__input,
.criteres__select {
  width: 100%;
  padding: var(--csp-space-1) var(--csp-space-2);
  border: 1px solid transparent;
  background: transparent;
  font: inherit;
  color: var(--text-default-grey);

  &:hover:not(:disabled) {
    border-color: var(--border-default-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
  }
}

.criteres__vide {
  margin: 0;
  padding: var(--csp-space-3);
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
  background: var(--background-alt-grey);
}

.criteres__add {
  display: flex;
  gap: var(--csp-space-2);
  align-items: flex-end;

  > :first-child {
    flex: 1;
  }
}

.criteres__type {
  width: 11rem;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
