<script setup lang="ts">
import type { Choix, Reponse, Valeur } from './moteur'
import { computed, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspSwitch from '@/components/base/CspSwitch/CspSwitch.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import ListEditor from '../offre-sans-autorisation/shared/ListEditor.vue'
import ChampDate from '../offre-sans-autorisation/variants/mvp/ChampDate.vue'
import ChampSimple from '../offre-sans-autorisation/variants/mvp/ChampSimple.vue'
import ChoixMultiple from '../offre-sans-autorisation/variants/mvp/ChoixMultiple.vue'
import { choixDe } from './moteur'

// Une question de la description, affichée avec le composant Csp* qui correspond à son type.
// `choix` vaut null quand la question dépend d'une autre encore vide (champ désactivé).
const props = defineProps<{ id: string, reponse: Reponse, valeur: Valeur | undefined, choix: Choix[] | null }>()
const emit = defineEmits<{ repondre: [valeur: Valeur] }>()
const nom = useId()

const r = computed(() => props.reponse)
const texte = computed(() => (typeof props.valeur === 'string' ? props.valeur : ''))
const liste = computed(() => (Array.isArray(props.valeur) ? props.valeur as string[] : []))
const elements = computed(() => (Array.isArray(props.valeur) ? props.valeur as Record<string, string>[] : []))
const desactive = computed(() => props.choix === null)

const VIDE = '__vide'
const optionsListe = computed(() => [
  { value: VIDE, label: desactive.value ? (r.value.texteParentVide ?? 'Répondez d\'abord à la question précédente') : (r.value.placeholder ?? (r.value.obligatoire ? 'Choisir' : 'Non renseigné')) },
  ...(props.choix ?? []).map(c => ({ value: c.valeur, label: c.libelle })),
])
const optionsRadio = computed(() => (props.choix ?? []).map(c => ({ value: c.valeur, label: c.libelle })))
const OUI_NON = [{ value: 'oui', label: 'Oui' }, { value: 'non', label: 'Non' }]

function choisir(v: string | undefined) {
  emit('repondre', !v || v === VIDE ? '' : v)
}

// Répétable : une ligne par élément, chaque sous-champ (texte ou liste) sur la même ligne.
function optionsSous(s: Reponse) {
  return [{ value: VIDE, label: 'Choisir' }, ...choixDe(s).map(c => ({ value: c.valeur, label: c.libelle }))]
}
function modifierElement(i: number, cle: string, v: string) {
  emit('repondre', elements.value.map((e, j) => (j === i ? { ...e, [cle]: v === VIDE ? '' : v } : e)))
}
function ajouterElement() {
  emit('repondre', [...elements.value, Object.fromEntries(Object.keys(r.value.champs ?? {}).map(k => [k, '']))])
}
function retirerElement(i: number) {
  emit('repondre', elements.value.filter((_, j) => j !== i))
}
</script>

<template>
  <!-- Interrupteur : le libellé est celui du switch -->
  <div
    v-if="r.type === 'interrupteur'"
    class="interrupteur"
  >
    <CspSwitch
      :model-value="valeur === true"
      :label="r.libelle"
      size="sm"
      @update:model-value="(v: boolean) => emit('repondre', v)"
    />
    <span
      v-if="r.aide"
      class="interrupteur__aide"
    >{{ r.aide }}</span>
  </div>

  <!-- Liste de textes : le composant de liste a déjà son libellé et son aide (astérisque ajouté au libellé) -->
  <ListEditor
    v-else-if="r.type === 'liste-texte'"
    :model-value="liste"
    :label="r.obligatoire ? `${r.libelle} *` : r.libelle"
    :hint="r.aide"
    :placeholder="r.placeholder"
    :add-label="r.ajouter"
    @update:model-value="(v: string[]) => emit('repondre', v)"
  />

  <ChampSimple
    v-else
    :label="r.libelle"
    :hint="r.aide"
    :obligatoire="r.obligatoire"
  >
    <CspInput
      v-if="r.type === 'texte' || r.type === 'url' || r.type === 'nombre'"
      :model-value="texte"
      :type="r.type === 'nombre' ? 'number' : r.type === 'url' ? 'url' : 'text'"
      :label="r.libelle"
      :placeholder="r.placeholder"
      @update:model-value="(v: string | number | undefined) => emit('repondre', String(v ?? ''))"
    />

    <CspTextarea
      v-else-if="r.type === 'texte-long'"
      :model-value="texte"
      :label="r.libelle"
      :placeholder="r.placeholder"
      :rows="5"
      @update:model-value="(v: string) => emit('repondre', v)"
    />

    <ChampDate
      v-else-if="r.type === 'date'"
      :model-value="texte"
      :label="r.libelle"
      @update:model-value="(v: string) => emit('repondre', v)"
    />

    <CspRadioGroup
      v-else-if="r.type === 'choix' && r.affichage === 'radio'"
      :model-value="texte"
      :label="r.libelle"
      :name="nom"
      :options="optionsRadio"
      @update:model-value="choisir"
    />

    <CspSegmentedControl
      v-else-if="r.type === 'choix' && r.affichage === 'segments'"
      :model-value="texte"
      :legend="r.libelle"
      hide-legend
      size="sm"
      :options="optionsRadio"
      @update:model-value="(v: string) => choisir(v)"
    />

    <!-- La clé recrée la liste quand elle s'active : sinon le texte affiché pour « vide » ne suit pas. -->
    <CspSelect
      v-else-if="r.type === 'choix'"
      :key="desactive ? 'desactive' : 'actif'"
      :model-value="texte || VIDE"
      :label="r.libelle"
      :options="optionsListe"
      :disabled="desactive"
      @update:model-value="choisir"
    />

    <CspRadioGroup
      v-else-if="r.type === 'oui-non'"
      :model-value="texte"
      :label="r.libelle"
      :name="nom"
      :options="OUI_NON"
      @update:model-value="choisir"
    />

    <template v-else-if="r.type === 'choix-multiple'">
      <CspSelect
        v-if="desactive"
        :model-value="VIDE"
        :label="r.libelle"
        :options="optionsListe.slice(0, 1)"
        disabled
      />
      <ChoixMultiple
        v-else
        :model-value="liste"
        :label="r.libelle"
        :options="(choix ?? []).map(c => c.valeur)"
        :placeholder="r.placeholder"
        @update:model-value="(v: string[]) => emit('repondre', v)"
      />
    </template>

    <div
      v-else-if="r.type === 'repetable'"
      class="repetable"
    >
      <div
        v-for="(e, i) in elements"
        :key="i"
        class="repetable__ligne"
        :style="{ gridTemplateColumns: `repeat(${Object.keys(r.champs ?? {}).length}, minmax(0, 1fr)) auto` }"
      >
        <template
          v-for="(s, cle) in r.champs"
          :key="cle"
        >
          <CspSelect
            v-if="s.type === 'choix'"
            :model-value="e[cle] || VIDE"
            :label="`${s.libelle} ${i + 1}${s.obligatoire ? ' *' : ''}`"
            :options="optionsSous(s)"
            @update:model-value="(v: string | undefined) => modifierElement(i, String(cle), v ?? '')"
          />
          <CspInput
            v-else
            :model-value="e[cle] ?? ''"
            :label="`${s.libelle} ${i + 1}${s.obligatoire ? ' *' : ''}`"
            @update:model-value="(v: string | number | undefined) => modifierElement(i, String(cle), String(v ?? ''))"
          />
        </template>
        <CspButton
          label="Retirer"
          variant="tertiary"
          size="sm"
          icon="ri:delete-bin-line"
          is-icon-left
          @click="retirerElement(i)"
        />
      </div>
      <div>
        <CspButton
          :label="r.ajouter ?? 'Ajouter'"
          variant="secondary"
          size="sm"
          icon="ri:add-line"
          is-icon-left
          @click="ajouterElement"
        />
      </div>
    </div>
  </ChampSimple>
</template>

<style scoped lang="scss">
.interrupteur {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
}

.interrupteur__aide {
  padding-left: 3rem;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.repetable {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.repetable__ligne {
  display: grid;
  gap: var(--csp-space-3);
  align-items: end;
}

// Dans un répétable, le libellé de chaque sous-champ reste visible (le cadre ne masque que le premier niveau).
.repetable :deep(.csp-select-group__label),
.repetable :deep(.csp-input-group__label) {
  position: static;
  width: auto;
  height: auto;
  overflow: visible;
  clip: auto;
}
</style>
