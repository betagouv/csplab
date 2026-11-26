<script setup lang="ts">
import { computed, ref } from 'vue'
import CspCombobox from '@/components/base/CspCombobox/CspCombobox.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'

// Plusieurs choix parmi une liste fixe (corps, grades, compétences RMFP… retour PO, 26/11/2026) :
// on cherche et on choisit dans la liste, chaque choix devient une étiquette qu'on peut retirer.
const props = defineProps<{ options: string[], label: string, placeholder?: string, hint?: string }>()
const choisis = defineModel<string[]>({ default: () => [] })

const recherche = ref('')
const valeur = ref<string | null>(null)
const proposees = computed(() => props.options
  .filter(o => !choisis.value.includes(o) && o.toLowerCase().includes(recherche.value.trim().toLowerCase()))
  .map(o => ({ value: o, label: o })))
function choisir(v: string | null) {
  if (v && !choisis.value.includes(v)) {
    choisis.value = [...choisis.value, v]
  }
  valeur.value = null
  recherche.value = ''
}
function retirer(v: string) {
  choisis.value = choisis.value.filter(x => x !== v)
}
</script>

<template>
  <div class="choix">
    <CspCombobox
      v-model:search-term="recherche"
      :model-value="valeur"
      :options="proposees"
      :label="label"
      :hint="hint"
      :placeholder="placeholder ?? 'Rechercher dans la liste'"
      empty-label="Aucun résultat dans la liste"
      @update:model-value="choisir"
    />
    <ul
      v-if="choisis.length"
      class="choix__liste"
    >
      <li
        v-for="c in choisis"
        :key="c"
      >
        <CspTag
          variant="dismissible"
          size="sm"
          :label="c"
          :dismiss-label="`Retirer ${c}`"
          @dismiss="retirer(c)"
        />
      </li>
    </ul>
  </div>
</template>

<style scoped lang="scss">
.choix {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.choix__liste {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}
</style>
