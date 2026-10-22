<script setup lang="ts">
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import Panel from '../../shared/Panel.vue'
import ApercuCandidat from './ApercuCandidat.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { db, publier as publierOffre, SITES_PARTENAIRES, SUPPORT_MAITRE } from './store'

// L'offre telle que la voient les candidats. Depuis l'encart « Prête à être publiée », la même page
// propose la diffusion : simple (support maître seul) ou multi-diffusion (sites partenaires au choix).
const props = defineProps<{ id: string, publier?: boolean }>()
const { aller, notifier } = useNav()

const o = computed(() => db.offres.find(x => x.id === props.id)!)
const avecPublication = computed(() => props.publier && o.value.etat === 'a_publier')

const diffusion = ref<'simple' | 'multi'>('simple')
const DIFFUSIONS = [
  { value: 'simple', label: `Simple diffusion — ${SUPPORT_MAITRE.nom} uniquement` },
  { value: 'multi', label: 'Multi-diffusion — Choisir le Service Public et des sites partenaires' },
]
const partenaires = ref<string[]>([])
const OPTIONS_PARTENAIRES = SITES_PARTENAIRES.map(s => ({ value: s.id, label: `${s.nom} — ${s.detail}` }))

const tentative = ref(false)
const erreurDate = computed(() => tentative.value && !o.value.dateLimite)
const erreurSites = computed(() => tentative.value && diffusion.value === 'multi' && !partenaires.value.length)

function publier() {
  tentative.value = true
  if (erreurDate.value || erreurSites.value) {
    return
  }
  publierOffre(o.value, diffusion.value, partenaires.value)
  notifier('Offre publiée (simulation : rien n\'est envoyé).')
  aller({ nom: 'offre', id: o.value.id })
}
</script>

<template>
  <PageAts
    actif="offres"
    largeur="full"
    :titre="avecPublication ? 'Publier l\'offre' : 'Affichage candidat'"
    :sous-titre="avecPublication ? 'Relisez l\'offre telle que les candidats la verront, puis choisissez sa diffusion.' : 'L\'offre telle que les candidats la verront.'"
    :fil="[{ label: 'Offres d\'emploi', to: '/offres' }, { label: o.titre || o.id, to: `/offre/${o.id}` }, { label: avecPublication ? 'Publier' : 'Affichage candidat' }]"
    :retour="{ to: `/offre/${o.id}`, label: 'Retour à l\'offre' }"
  >
    <div
      class="page"
      :class="{ 'page--publier': avecPublication }"
    >
      <div class="apercu">
        <ApercuCandidat
          :offre="o"
          :organisme="db.organisme.nom"
        />
      </div>

      <aside
        v-if="avecPublication"
        class="diffusion"
      >
        <Panel
          titre="Diffusion"
          description="Choisir le Service Public est le support de publication maître : l'offre y est toujours publiée."
        >
          <CspRadioGroup
            v-model="diffusion"
            label="Type de diffusion"
            :options="DIFFUSIONS"
          />
          <CspCheckboxGroup
            v-if="diffusion === 'multi'"
            v-model="partenaires"
            label="Sites partenaires"
            :options="OPTIONS_PARTENAIRES"
            :error="erreurSites"
            :error-message="erreurSites ? 'Choisissez au moins un site partenaire.' : undefined"
          />
          <CspInput
            v-model="o.dateLimite"
            label="Date limite de candidature"
            placeholder="AAAA-MM-JJ"
            :error="erreurDate"
            :error-message="erreurDate ? 'Indiquez la date limite de candidature.' : undefined"
          />
        </Panel>
        <div class="actions">
          <CspButton
            label="Annuler"
            variant="secondary"
            @click="aller({ nom: 'offre', id: o.id })"
          />
          <CspButton
            label="Publier l'offre"
            icon="ri:send-plane-line"
            is-icon-left
            @click="publier"
          />
        </div>
      </aside>
    </div>
  </PageAts>
</template>

<style scoped lang="scss">
.page {
  display: grid;
  grid-template-columns: minmax(0, 48rem);
  justify-content: center;
  gap: var(--csp-space-6);
  align-items: start;

  &--publier {
    grid-template-columns: minmax(0, 48rem) 24rem;
  }

  @media (max-width: 75rem) {
    &--publier {
      grid-template-columns: minmax(0, 48rem);
    }
  }
}

.diffusion {
  position: sticky;
  align-self: start;
  top: var(--csp-space-4);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-2);
}
</style>
