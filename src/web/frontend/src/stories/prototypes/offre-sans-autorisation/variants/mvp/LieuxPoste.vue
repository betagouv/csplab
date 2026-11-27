<script setup lang="ts">
import type { LieuPoste, Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspCombobox from '@/components/base/CspCombobox/CspCombobox.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import ChampSimple from './ChampSimple.vue'

// Lieux du poste (retour PO, F9) : « Ajouter un lieu » ; chaque lieu a son adresse, saisie avec des suggestions
// (simulées ici, la Base adresse nationale en vrai) et géolocalisée dès qu'on choisit une suggestion.
// « Pas de lieu fixe » est gardé en attendant la réponse de la DGAFP. Le champ « lieu » (villes) suit pour la liste.
const props = defineProps<{ offre: Offre }>()
const o = computed(() => props.offre)

const ADRESSES: Required<Omit<LieuPoste, 'affectation'>>[] = [
  { adresse: '520 allée Henri II de Montmorency, 34000 Montpellier', ville: 'Montpellier (34)', geo: '43,6119 · 3,8999' },
  { adresse: '1 rue de la Cité administrative, 31000 Toulouse', ville: 'Toulouse (31)', geo: '43,6106 · 1,4436' },
  { adresse: '5 rue Saint-Rémy, 30000 Nîmes', ville: 'Nîmes (30)', geo: '43,8336 · 4,3591' },
  { adresse: '12 rue de la Préfecture, 66000 Perpignan', ville: 'Perpignan (66)', geo: '42,6987 · 2,8956' },
  { adresse: '3 boulevard Gambetta, 46000 Cahors', ville: 'Cahors (46)', geo: '44,4475 · 1,4410' },
  { adresse: '10 place du Foirail, 12000 Rodez', ville: 'Rodez (12)', geo: '44,3506 · 2,5750' },
  { adresse: '2 rue Marcellin Albert, 11000 Carcassonne', ville: 'Carcassonne (11)', geo: '43,2122 · 2,3537' },
]

const lieux = computed(() => o.value.lieux ?? [])
// Un premier lieu est affiché d'emblée (revue UI, 27/11/2026) : « Ajouter un autre lieu » sert à en mettre plusieurs.
if (!lieux.value.length) {
  o.value.lieux = [{ adresse: '', ville: '' }]
}
function synchro() {
  o.value.lieu = o.value.sansLieuFixe ? 'Pas de lieu fixe' : lieux.value.map(l => l.ville).filter(Boolean).join(', ')
  o.value.adresse = lieux.value[0]?.adresse ?? ''
}
function ajouter() {
  o.value.lieux = [...lieux.value, { adresse: '', ville: '' }]
}
function retirer(i: number) {
  o.value.lieux = lieux.value.filter((_, j) => j !== i)
  synchro()
}

const recherches = ref<string[]>([])
function options(i: number) {
  const t = (recherches.value[i] ?? '').toLowerCase().trim()
  return ADRESSES.filter(a => !t || a.adresse.toLowerCase().includes(t)).map(a => ({ value: a.adresse, label: a.adresse }))
}
function choisir(l: LieuPoste, valeur: string | null) {
  const a = ADRESSES.find(x => x.adresse === valeur)
  l.adresse = a?.adresse ?? ''
  l.ville = a?.ville ?? ''
  l.geo = a?.geo
  synchro()
}
const sansLieuFixe = computed({
  get: () => Boolean(o.value.sansLieuFixe),
  set: (v: boolean) => {
    o.value.sansLieuFixe = v
    synchro()
  },
})
</script>

<template>
  <div class="lieux">
    <template v-if="!sansLieuFixe">
      <div
        v-for="(l, i) in lieux"
        :key="i"
        class="lieu"
      >
        <div class="lieu__tete">
          <h4 class="lieu__titre">
            {{ lieux.length > 1 ? `Lieu ${i + 1}` : 'Lieu' }}
          </h4>
          <CspButton
            v-if="lieux.length > 1"
            label="Retirer"
            variant="tertiary-no-outline"
            size="sm"
            icon="ri:delete-bin-line"
            is-icon-left
            @click="retirer(i)"
          />
        </div>
        <ChampSimple
          label="Adresse"
          obligatoire
          hint="Commencez à taper, puis choisissez une adresse dans la liste"
        >
          <CspCombobox
            :model-value="l.adresse || null"
            :search-term="recherches[i] ?? ''"
            label="Adresse"
            placeholder="Numéro, rue, ville"
            empty-label="Aucune adresse trouvée"
            :options="options(i)"
            @update:search-term="(t: string) => (recherches[i] = t)"
            @update:model-value="(v: string | null) => choisir(l, v)"
          />
        </ChampSimple>
        <p
          v-if="l.geo"
          class="lieu__geo"
        >
          <CspIcon
            name="ri:map-pin-2-line"
            :size="16"
          />
          Géolocalisé : {{ l.ville }} · {{ l.geo }}
        </p>
        <CspInput
          v-model="l.affectation"
          label="Lieu d'affectation"
          placeholder="Ex. : site de la Pompignane, bâtiment B"
        />
      </div>
      <div>
        <CspButton
          label="Ajouter un autre lieu"
          variant="secondary"
          size="sm"
          icon="ri:add-line"
          is-icon-left
          @click="ajouter"
        />
      </div>
    </template>
    <CspCheckbox
      v-model="sansLieuFixe"
      label="Pas de lieu fixe (poste itinérant)"
    />
  </div>
</template>

<style scoped lang="scss">
.lieux {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.lieu {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
}

.lieu__tete {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.lieu__titre {
  margin: 0;
  font-size: 1rem;
}

.lieu__geo {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-default-success);
}
</style>
