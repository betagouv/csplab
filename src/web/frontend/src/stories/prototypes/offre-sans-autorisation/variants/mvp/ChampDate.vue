<script setup lang="ts">
import { ref, watch } from 'vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'

// Date saisie au format JJ-MM-AAAA (retour PO, 26/11/2026), gardée en AAAA-MM-JJ dans les données.
// Les autres attributs (label, hint, error…) passent au champ.
defineOptions({ inheritAttrs: false })
const model = defineModel<string>({ default: '' })

const versTexte = (iso: string) => (/^\d{4}-\d{2}-\d{2}$/.test(iso) ? iso.split('-').reverse().join('-') : iso)
function versIso(t: string): string {
  const m = /^(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})$/.exec(t.trim())
  return m ? `${m[3]}-${m[2]!.padStart(2, '0')}-${m[1]!.padStart(2, '0')}` : ''
}
const texte = ref(versTexte(model.value))
watch(model, (v) => {
  if (versIso(texte.value) !== v) {
    texte.value = versTexte(v)
  }
})
function saisir(t: string | number | undefined) {
  texte.value = String(t ?? '')
  model.value = versIso(texte.value)
}
</script>

<template>
  <CspInput
    v-bind="$attrs"
    :model-value="texte"
    placeholder="JJ-MM-AAAA"
    @update:model-value="saisir"
  />
</template>
