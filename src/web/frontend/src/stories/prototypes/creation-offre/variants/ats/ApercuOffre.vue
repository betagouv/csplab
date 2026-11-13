<script setup lang="ts">
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import Panel from '../../shared/Panel.vue'
import { manquesPublication } from './aide'
import ApercuCandidat from './ApercuCandidat.vue'
import ChampsPublication from './ChampsPublication.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import ParametresRecrutement from './ParametresRecrutement.vue'
import { dateLongue, db, publier as publierOffre, sauvegarder, SUPPORT_MAITRE, validationManquante } from './store'

// L'offre telle que la voient les candidats. Depuis « Publier », un parcours en 3 étapes à côté de l'aperçu :
// 1. dates et diffusion (simple ou multi-diffusion), 2. paramétrer le recrutement (responsable, équipe,
// notifications : éléments du recrutement, plus demandés pendant la rédaction), 3. confirmation.
const props = defineProps<{ id: string, publier?: boolean }>()
const { aller, notifier } = useNav()

const o = computed(() => db.offres.find(x => x.id === props.id)!)
const etape = ref<1 | 2 | 3>(1)
const avecPublication = computed(() => props.publier && (etape.value === 3 || (o.value.etat === 'brouillon' && !validationManquante(o.value))))
const tentative = ref(false)
const ETAPES = ['Dates et diffusion', 'Paramétrer le recrutement', 'Recrutement ouvert']
const manques = computed(() => manquesPublication(o.value))

function suivant() {
  tentative.value = true
  if (manques.value.length || (o.value.diffusion === 'multi' && o.value.canaux.length < 2)) {
    return
  }
  etape.value = 2
}
function publier() {
  publierOffre(o.value, o.value.diffusion ?? 'simple', o.value.canaux.filter(c => c !== SUPPORT_MAITRE.id))
  o.value.responsables = o.value.equipe.filter(m => m.role === 'Responsable').map(m => m.nom)
  sauvegarder()
  notifier('Offre publiée : le recrutement est ouvert (simulation).')
  etape.value = 3
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
        <ol class="etapes">
          <li
            v-for="(e, i) in ETAPES"
            :key="e"
            :class="{ 'etapes--active': etape === i + 1, 'etapes--faite': etape > i + 1 }"
            :aria-current="etape === i + 1 ? 'step' : undefined"
          >
            <span class="etapes__num">{{ i + 1 }}</span>{{ e }}
          </li>
        </ol>

        <template v-if="etape === 1">
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
              label="Suivant"
              icon="ri:arrow-right-line"
              @click="suivant"
            />
          </div>
        </template>

        <template v-else-if="etape === 2">
          <Panel
            titre="Paramétrer le recrutement"
            description="La publication ouvre un recrutement. Indiquez qui le suit ; vous pourrez changer ces réglages dans Mes recrutements."
          >
            <ParametresRecrutement :offre="o" />
          </Panel>
          <div class="actions">
            <CspButton
              label="Précédent"
              variant="secondary"
              icon="ri:arrow-left-line"
              is-icon-left
              @click="etape = 1"
            />
            <CspButton
              label="Publier et ouvrir le recrutement"
              icon="ri:send-plane-line"
              is-icon-left
              @click="publier"
            />
          </div>
        </template>

        <Panel
          v-else
          titre="Le recrutement est ouvert"
          :description="`L'offre est en ligne jusqu'au ${dateLongue(o.dateFin)}. Les candidatures arriveront dans Mes recrutements.`"
        >
          <div class="actions actions--colonne">
            <CspButton
              label="Voir mes recrutements"
              icon="ri:arrow-right-line"
              @click="aller({ nom: 'recrutements' })"
            />
            <CspButton
              label="Revenir à mes offres"
              variant="secondary"
              @click="aller({ nom: 'offres' })"
            />
          </div>
        </Panel>
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

.etapes {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);

  li {
    display: flex;
    align-items: center;
    gap: var(--csp-space-2);
  }

  &--active {
    font-weight: var(--csp-font-weight-bold);
    color: var(--text-title-grey);
  }
}

.etapes__num {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 1.5rem;
  height: 1.5rem;
  border: 1px solid currentColor;
  border-radius: 50%;
  font-size: var(--csp-font-size-xs);

  .etapes--active & {
    border-color: var(--background-action-high-blue-france);
    background: var(--background-action-high-blue-france);
    color: var(--text-inverted-blue-france);
  }

  .etapes--faite & {
    border-color: var(--border-plain-success);
    color: var(--text-default-success);
  }
}

.actions.actions--colonne {
  flex-direction: column;
  align-items: stretch;
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
