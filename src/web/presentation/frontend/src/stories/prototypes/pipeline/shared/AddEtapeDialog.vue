<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'

interface PositionOption {
  // Index d'insertion dans la liste complète.
  index: number
  label: string
}

interface Props {
  open: boolean
  // Noms déjà pris (doublon interdit).
  noms: string[]
  // Positions d'insertion proposées (déjà bornées au segment réordonnable).
  positions: PositionOption[]
  // Index par défaut (fin de segment).
  defaultIndex: number
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'confirm': [payload: { nom: string, index: number }]
}>()

const nom = ref('')
// CspRadioGroup pilote des valeurs string : on stocke l'index sous forme de chaîne.
const indexValue = ref(String(props.defaultIndex))
const error = ref<string | null>(null)

watch(() => props.open, (isOpen) => {
  if (isOpen) {
    nom.value = ''
    indexValue.value = String(props.defaultIndex)
    error.value = null
  }
})

const positionOptions = computed(() =>
  props.positions.map(p => ({ value: String(p.index), label: p.label })),
)

function validate(value: string): string | null {
  const trimmed = value.trim()
  if (!trimmed)
    return 'Le nom de l\'étape ne peut pas être vide.'
  if (props.noms.includes(trimmed))
    return 'Une étape porte déjà ce nom.'
  return null
}

function confirm() {
  const message = validate(nom.value)
  if (message) {
    error.value = message
    return
  }
  emit('confirm', { nom: nom.value.trim(), index: Number(indexValue.value) })
  emit('update:open', false)
}
</script>

<template>
  <CspDialog
    :open="open"
    size="sm"
    title="Ajouter une étape"
    close-label="Fermer"
    @update:open="value => emit('update:open', value)"
  >
    <div class="add-etape">
      <CspInput
        v-model="nom"
        label="Nom de l'étape"
        :error="Boolean(error)"
        :error-message="error ?? undefined"
        @keydown.enter="confirm"
      />

      <CspRadioGroup
        v-model="indexValue"
        label="Position dans le pipeline"
        :options="positionOptions"
      />
    </div>

    <template #footer>
      <CspButton
        label="Annuler"
        variant="secondary"
        size="sm"
        @click="emit('update:open', false)"
      />
      <CspButton
        label="Ajouter"
        variant="primary"
        size="sm"
        @click="confirm"
      />
    </template>
  </CspDialog>
</template>

<style scoped lang="scss">
.add-etape {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}
</style>
