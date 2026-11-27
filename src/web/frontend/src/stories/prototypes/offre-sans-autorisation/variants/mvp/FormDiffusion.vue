<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import ChampSimple from './ChampSimple.vue'
import { SITES_PARTENAIRES, SUPPORT_MAITRE } from './store'

// Partie 3 « Diffusion » : multidiffuser ou non. À la création, plus de choix « dans l'ATS / ailleurs » : les
// candidatures sont toujours gérées dans l'ATS (retour PO, 27/11/2026). Seules les offres téléversées sont gérées hors ATS :
// on le rappelle, en lecture seule.
const props = defineProps<{ offre: Offre }>()
const o = computed(() => props.offre)
const horsAts = computed(() => o.value.modeCandidature !== 'ats')

const MULTI = [
  { value: 'simple', label: `${SUPPORT_MAITRE.nom} uniquement` },
  { value: 'multi', label: `${SUPPORT_MAITRE.nom} et d'autres sites (multidiffusion)` },
]
const multi = computed({
  get: () => o.value.diffusion ?? 'simple',
  set: (v: string) => {
    o.value.diffusion = v as 'simple' | 'multi'
    if (v === 'simple') {
      o.value.canaux = [SUPPORT_MAITRE.id]
    }
  },
})
function coche(id: string) {
  return o.value.canaux.includes(id)
}
function basculer(id: string, v: boolean) {
  const autres = o.value.canaux.filter(c => c !== id && c !== SUPPORT_MAITRE.id)
  o.value.canaux = [SUPPORT_MAITRE.id, ...autres, ...(v ? [id] : [])]
}
const NOM_MAITRE = SUPPORT_MAITRE.nom
</script>

<template>
  <div
    v-if="horsAts"
    class="groupe"
  >
    <h3 class="groupe__titre">
      Gestion des candidatures
    </h3>
    <p class="valeur">
      Candidatures gérées hors de l'ATS
      <span class="valeur__note">
        Les candidats postulent {{ o.modeCandidature === 'courriel' ? `par courriel (${o.courrielCandidature})` : `sur ${o.urlCandidature}` }}.
      </span>
    </p>
  </div>

  <div class="groupe">
    <h3 class="groupe__titre">
      Sites de diffusion
    </h3>
    <p class="groupe__desc">
      L'offre est toujours publiée sur {{ NOM_MAITRE }}.
    </p>
    <ChampSimple label="Multidiffuser l'offre ?">
      <CspRadioGroup
        v-model="multi"
        label="Multidiffuser l'offre ?"
        name="multidiffusion"
        :options="MULTI"
      />
    </ChampSimple>
    <fieldset
      v-if="multi === 'multi'"
      class="sites"
    >
      <legend class="sites__legende">
        Autres sites (liste indicative)
      </legend>
      <div
        v-for="s in SITES_PARTENAIRES"
        :key="s.id"
        class="site"
      >
        <CspCheckbox
          :model-value="coche(s.id)"
          :label="s.nom"
          @update:model-value="(v?: boolean) => basculer(s.id, Boolean(v))"
        />
        <span class="site__detail">{{ s.detail }}</span>
      </div>
    </fieldset>
  </div>
</template>

<style scoped lang="scss">
.groupe {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  max-width: 60rem;

  & + & {
    margin-top: var(--csp-space-3);
    padding-top: var(--csp-space-6);
    border-top: 1px solid var(--border-default-grey);
  }
}

.groupe__titre {
  margin: 0;
  font-size: 1.125rem;
  font-weight: var(--csp-font-weight-bold);
  line-height: 1.4;
  color: var(--text-title-grey);
}

.groupe__desc {
  margin: calc(-1 * var(--csp-space-2)) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.valeur {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-sm);
}

.valeur__note,
.site__detail {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.sites {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  border: 0;
}

.sites__legende {
  margin-bottom: var(--csp-space-2);
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
}

.site {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-1) var(--csp-space-3);
}
</style>
