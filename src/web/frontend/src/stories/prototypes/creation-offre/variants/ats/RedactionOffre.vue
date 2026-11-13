<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import Panel from '../../shared/Panel.vue'
import { manquesAnnonce } from './aide'
import ApercuCandidat from './ApercuCandidat.vue'
import DemandeValidation from './DemandeValidation.vue'
import FormAnnonce from './FormAnnonce.vue'
import FormCandidature from './FormCandidature.vue'
import FormInterne from './FormInterne.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import ResumeValidation from './ResumeValidation.vue'
import { db, fiche, heure, sauvegarder, validationManquante } from './store'

// Création d'une offre (retour PO) : un parcours en étapes, distinct de la page de l'offre, qui va droit au but.
// On ne demande que ce qui sert à valider et publier l'offre : annonce, informations internes, formulaire de
// candidature. Paramètres et équipe du recrutement viennent au moment de publier ; la page de l'offre sert ensuite
// à consulter et modifier.
const props = defineProps<{ id: string, etape?: number }>()
const { aller } = useNav()
const o = computed(() => db.offres.find(x => x.id === props.id)!)
const f = computed(() => fiche(o.value.ficheId))

const ETAPES = [
  { titre: 'Annonce', aide: 'Ce que liront les candidats sur Choisir le Service Public.' },
  { titre: 'Informations internes', aide: 'Jamais publiées. Elles servent au suivi et au résumé pour les valideurs.' },
  { titre: 'Formulaire de candidature', aide: 'Comment les candidats postulent et quelles pièces ils fournissent.' },
  { titre: 'Récapitulatif', aide: 'Relisez l\'annonce telle que les candidats la verront. À droite, ce qui manque et ce que verront les valideurs.' },
]
const etape = ref(Math.min(Math.max(props.etape ?? 1, 1), ETAPES.length))
const courante = computed(() => ETAPES[etape.value - 1]!)

// Enregistrement automatique, comme sur la page de l'offre.
const enregistre = ref(heure())
watch(o, () => {
  sauvegarder()
  enregistre.value = heure()
}, { deep: true })

function allerEtape(n: number) {
  etape.value = n
  document.querySelector('.ats__main')?.scrollTo({ top: 0 })
}

const manques = computed(() => manquesAnnonce(o.value))
const avecValidation = computed(() => db.organisme.validationActive)
const pretePublier = computed(() => !validationManquante(o.value) && !manques.value.length)
const ETAPE_DU_MANQUE: Record<string, number> = { annonce: 1, candidature: 3 }
</script>

<template>
  <PageAts
    actif="offres"
    :titre="o.titre || 'Nouvelle offre'"
    sous-titre="Nouvelle offre d'emploi"
    :fil="[{ label: 'Mes offres d\'emploi', to: '/offres' }, { label: 'Nouvelle offre' }]"
  >
    <template #actions>
      <span class="enregistre">Enregistré automatiquement à {{ enregistre }}</span>
      <CspButton
        label="Enregistrer et quitter"
        size="sm"
        variant="secondary"
        @click="aller({ nom: 'offres' })"
      />
    </template>

    <div
      class="redaction"
      :class="{ 'redaction--recap': etape === ETAPES.length }"
    >
      <!-- Indicateur d'étapes (modèle DSFR) -->
      <div class="stepper">
        <h2 class="stepper__titre">
          {{ courante.titre }}
          <span class="stepper__etat">Étape {{ etape }} sur {{ ETAPES.length }}</span>
        </h2>
        <div
          class="stepper__barre"
          aria-hidden="true"
        >
          <span
            v-for="n in ETAPES.length"
            :key="n"
            :class="{ faite: n <= etape }"
          />
        </div>
        <p
          v-if="etape < ETAPES.length"
          class="stepper__suivante"
        >
          <strong>Étape suivante :</strong> {{ ETAPES[etape]!.titre }}
        </p>
      </div>

      <p class="aide">
        {{ courante.aide }}
      </p>

      <div
        v-if="etape < ETAPES.length"
        class="corps"
      >
        <FormAnnonce
          v-if="etape === 1"
          :offre="o"
          :fiche="f"
        />
        <FormInterne
          v-else-if="etape === 2"
          :offre="o"
        />
        <FormCandidature
          v-else
          :offre="o"
        />
      </div>

      <!-- Récapitulatif : l'annonce vue par les candidats à gauche, ce qui sert à décider à droite. -->
      <div
        v-else
        class="recap"
      >
        <div class="recap__apercu">
          <ApercuCandidat
            :offre="o"
            :organisme="db.organisme.nom"
          />
        </div>

        <aside class="recap__panneau">
          <Panel
            :titre="manques.length ? 'À compléter avant de publier' : 'L\'annonce est complète'"
            :description="manques.length ? (avecValidation ? 'Vous pouvez demander la validation dès maintenant et compléter pendant la validation.' : undefined) : 'Les dates et la diffusion se choisiront au moment de publier.'"
          >
            <ul
              v-if="manques.length"
              class="manques"
            >
              <li
                v-for="m in manques"
                :key="m.label"
              >
                {{ m.label }}
                <button
                  type="button"
                  class="lien"
                  @click="allerEtape(ETAPE_DU_MANQUE[m.etape] ?? 1)"
                >
                  Compléter
                </button>
              </li>
            </ul>
          </Panel>

          <Panel
            v-if="avecValidation"
            titre="Résumé pour la validation"
            description="Ce que verront les valideurs. Jamais publié."
          >
            <ResumeValidation
              :offre="o"
              :fiche="f"
              integre
              compact
            />
            <button
              type="button"
              class="lien lien--seul"
              @click="allerEtape(2)"
            >
              {{ o.commentaireValideurs ? 'Modifier le commentaire pour les valideurs' : 'Ajouter un commentaire pour les valideurs' }}
            </button>
          </Panel>
        </aside>
      </div>

      <div class="nav">
        <CspButton
          v-if="etape > 1"
          label="Précédent"
          variant="secondary"
          icon="ri:arrow-left-line"
          is-icon-left
          @click="allerEtape(etape - 1)"
        />
        <span class="nav__espace" />
        <CspButton
          v-if="etape < ETAPES.length"
          label="Suivant"
          icon="ri:arrow-right-line"
          @click="allerEtape(etape + 1)"
        />
        <template v-else>
          <CspButton
            label="Enregistrer le brouillon"
            variant="secondary"
            @click="aller({ nom: 'offre', id: o.id })"
          />
          <DemandeValidation
            v-if="avecValidation"
            :offre="o"
            variant="primary"
            @demandee="aller({ nom: 'offre', id: o.id })"
          />
          <CspButton
            v-else-if="pretePublier"
            label="Publier"
            icon="ri:arrow-right-line"
            @click="aller({ nom: 'apercu', id: o.id, publier: true })"
          />
        </template>
      </div>
    </div>
  </PageAts>
</template>

<style scoped lang="scss">
.redaction {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
  max-width: 52rem;

  &--recap {
    max-width: 80rem;
  }
}

.recap {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 24rem;
  gap: var(--csp-space-6);
  align-items: start;

  @media (max-width: 75rem) {
    grid-template-columns: minmax(0, 1fr);
  }
}

.recap__apercu {
  min-width: 0;
}

// Le panneau suit le défilement de l'annonce ; s'il est plus haut que l'écran, il défile de son côté.
// Les boutons d'envoi sont sur la ligne de « Précédent », ferrés à droite.
.recap__panneau {
  position: sticky;
  top: var(--csp-space-4);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  max-height: calc(100vh - 10rem);
  overflow-y: auto;
}

.lien--seul {
  margin: var(--csp-space-3) 0 0;
  font-size: var(--csp-font-size-sm);
}

.enregistre {
  align-self: center;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.stepper__titre {
  display: flex;
  flex-direction: column-reverse;
  gap: var(--csp-space-1);
  margin: 0 0 var(--csp-space-3);
  font-size: 1.375rem;
  line-height: 1.3;
}

.stepper__etat {
  font-size: var(--csp-font-size-sm);
  font-weight: 400;
  color: var(--text-mention-grey);
}

.stepper__barre {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: 1fr;
  gap: var(--csp-space-2);

  span {
    height: 6px;
    background: var(--background-contrast-grey);

    &.faite {
      background: var(--background-action-high-blue-france);
    }
  }
}

.stepper__suivante {
  margin: var(--csp-space-3) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.aide {
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-contrast-info);
  font-size: var(--csp-font-size-sm);
}

.corps {
  padding: var(--csp-space-6) var(--csp-space-8);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.manques {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding-left: var(--csp-space-5);
  font-size: var(--csp-font-size-sm);
}

.lien {
  margin-left: var(--csp-space-2);
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}

.nav {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
}

.nav__espace {
  flex: 1;
}
</style>
