<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import ChampSimple from './ChampSimple.vue'
import { SITES_PARTENAIRES, SUPPORT_MAITRE } from './store'

// Partie 3 « Diffusion » (revue UI équipe, 27/11/2026) : d'abord, diffuser seulement ou diffuser et gérer les
// candidatures dans l'ATS ; ensuite, multidiffuser ou non. Proposition : « Diffuser uniquement » demande où
// postuler (lien ou adresse électronique), et la partie 2 n'a alors plus rien à paramétrer.
// Une fois l'offre publiée, la gestion des candidatures ne change plus (des candidats ont pu postuler).
const props = defineProps<{ offre: Offre, verrouille?: boolean }>()
const o = computed(() => props.offre)
// Les sites restent modifiables après publication ; la gestion des candidatures, non.
const gestionFigee = computed(() => props.verrouille || o.value.etat !== 'brouillon')

const GESTIONS = [
  { value: 'ats', label: 'Diffuser l\'offre et gérer les candidatures dans l\'ATS' },
  { value: 'hors', label: 'Diffuser l\'offre uniquement : les candidatures sont gérées ailleurs' },
]
const gestion = computed({
  get: () => (o.value.modeCandidature === 'ats' ? 'ats' : 'hors'),
  set: (v: string) => {
    o.value.modeCandidature = v === 'ats' ? 'ats' : o.value.modeCandidature === 'courriel' ? 'courriel' : 'externe'
  },
})
const POSTULER = [
  { value: 'externe' as const, label: 'Sur un site (lien)' },
  { value: 'courriel' as const, label: 'Par courriel' },
]
const postuler = computed({
  get: () => (o.value.modeCandidature === 'courriel' ? 'courriel' as const : 'externe' as const),
  set: (v: 'externe' | 'courriel') => (o.value.modeCandidature = v),
})

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
const libelleGestion = computed(() => GESTIONS.find(g => g.value === gestion.value)!.label)
</script>

<template>
  <div class="groupe">
    <h3 class="groupe__titre">
      Gestion des candidatures
    </h3>
    <p
      v-if="gestionFigee"
      class="valeur"
    >
      {{ libelleGestion }}
      <span class="valeur__note">Ne peut plus changer : l'offre a été publiée.</span>
    </p>
    <ChampSimple
      v-else
      label="Que souhaitez-vous faire ?"
      obligatoire
    >
      <CspRadioGroup
        v-model="gestion"
        label="Que souhaitez-vous faire ?"
        name="gestion-candidatures"
        :options="GESTIONS"
      />
    </ChampSimple>
    <template v-if="gestion === 'hors' && !gestionFigee">
      <ChampSimple
        label="Où les candidats postulent-ils ?"
        obligatoire
      >
        <CspSegmentedControl
          v-model="postuler"
          legend="Où les candidats postulent-ils ?"
          hide-legend
          size="sm"
          :options="POSTULER"
        />
      </ChampSimple>
      <CspInput
        v-if="postuler === 'externe'"
        v-model="o.urlCandidature"
        label="Lien pour postuler *"
        placeholder="https://"
      />
      <CspInput
        v-else
        v-model="o.courrielCandidature"
        label="Adresse électronique pour postuler *"
        placeholder="recrutement@exemple.gouv.fr"
      />
      <p class="note">
        Les candidatures n'arriveront pas dans l'ATS : la partie « Paramétrage des candidatures » ne s'applique pas.
      </p>
    </template>
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

.note {
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-info);
  background: var(--background-contrast-info);
  font-size: var(--csp-font-size-sm);
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
