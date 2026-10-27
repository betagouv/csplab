<script setup lang="ts">
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import Panel from '../../shared/Panel.vue'
import { manquesPublication } from './aide'
import ApercuCandidat from './ApercuCandidat.vue'
import ChampsPublication from './ChampsPublication.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { db, publier as publierOffre, SUPPORT_MAITRE, validationManquante } from './store'

// L'offre telle que la voient les candidats. Depuis « Publier », la même page propose les dates
// et la diffusion : simple (support maître seul) ou multi-diffusion (sites partenaires au choix).
const props = defineProps<{ id: string, publier?: boolean }>()
const { aller, notifier } = useNav()

const o = computed(() => db.offres.find(x => x.id === props.id)!)
const avecPublication = computed(() => props.publier && o.value.etat === 'brouillon' && !validationManquante(o.value))
const tentative = ref(false)
const manques = computed(() => manquesPublication(o.value))

function publier() {
  tentative.value = true
  if (manques.value.length || (o.value.diffusion === 'multi' && o.value.canaux.length < 2)) {
    return
  }
  publierOffre(o.value, o.value.diffusion ?? 'simple', o.value.canaux.filter(c => c !== SUPPORT_MAITRE.id))
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
          titre="Dates et diffusion"
          description="Choisir le Service Public est le support de publication maître : l'offre y est toujours publiée."
        >
          <ChampsPublication
            :offre="o"
            :tentative="tentative"
          />
        </Panel>
        <p
          v-if="tentative && manques.filter(m => m.etape !== 'publication').length"
          class="manque"
          role="alert"
        >
          Pour publier, complétez : {{ manques.filter(m => m.etape !== 'publication').map(m => m.label).join(', ') }}.
          <button
            type="button"
            class="lien"
            @click="aller({ nom: 'formulaire', id: o.id, etape: manques[0]!.etape })"
          >
            Ouvrir le formulaire
          </button>
        </p>
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

.manque {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-error);
}

.lien {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-2);
}
</style>
