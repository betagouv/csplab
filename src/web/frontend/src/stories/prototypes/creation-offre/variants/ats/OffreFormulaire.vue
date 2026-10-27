<script setup lang="ts">
import type { EtapeFormulaire } from './aide'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import Panel from '../../shared/Panel.vue'
import { manquesPublication } from './aide'
import ChampsPublication from './ChampsPublication.vue'
import DemandeValidation from './DemandeValidation.vue'
import FormAnnonce from './FormAnnonce.vue'
import FormCandidature from './FormCandidature.vue'
import FormEquipe from './FormEquipe.vue'
import FormInternes from './FormInternes.vue'
import FormProcessus from './FormProcessus.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { db, heure, LIBELLES_VALIDATION, maintenant, sauvegarder, signalerModification, UTILISATEUR, validationManquante } from './store'

// Formulaire de l'offre, page entière sur laquelle on arrive en créant une offre. Six étapes, navigation libre,
// enregistrement automatique. « Demander la validation » est disponible à toutes les étapes, sans champ minimum ;
// les champs obligatoires ne sont contrôlés qu'au moment de publier.
const props = defineProps<{ id: string, etape?: EtapeFormulaire }>()
const { aller, notifier } = useNav()
const o = computed(() => db.offres.find(x => x.id === props.id)!)
const fiche = computed(() => db.fiches.find(x => x.id === o.value.ficheId)!)
const nouvelle = computed(() => o.value.etat === 'brouillon' && o.value.historique.length <= 1)

const ETAPES: { id: EtapeFormulaire, label: string, aide: string }[] = [
  { id: 'internes', label: 'Informations internes', aide: 'Jamais publiées' },
  { id: 'annonce', label: 'Annonce', aide: 'Ce que lit le candidat' },
  { id: 'candidature', label: 'Formulaire de candidature', aide: 'Mode, pièces, questions' },
  { id: 'processus', label: 'Processus', aide: 'Facultatif' },
  { id: 'equipe', label: 'Équipe', aide: 'Facultatif' },
  { id: 'publication', label: 'Publication', aide: 'Dates et diffusion' },
]
const etape = ref<EtapeFormulaire>(props.etape ?? 'internes')
const index = computed(() => ETAPES.findIndex(e => e.id === etape.value))
const manques = computed(() => manquesPublication(o.value))
const aCompleter = (id: EtapeFormulaire) => manques.value.filter(m => m.etape === id).length
function aller_etape(id: EtapeFormulaire) {
  etape.value = id
  document.querySelector('.ats__main')?.scrollTo({ top: 0 })
}

// --- Enregistrement automatique ; une modification après validation est signalée, sans relancer le circuit ---
const sauvegarde = ref<'' | 'modif' | 'ok'>('')
const heureOk = ref('')
let timer: ReturnType<typeof setTimeout> | undefined
let aEnregistrer = false
const contenu = computed(() => {
  const { historique: _h, modifieLe: _m, validations: _v, validationEtat: _e, modifieeDepuisValidation: _d, ...reste } = o.value
  return JSON.stringify(reste)
})
watch(contenu, () => {
  aEnregistrer = true
  sauvegarde.value = 'modif'
  clearTimeout(timer)
  timer = setTimeout(enregistrerAuto, 1200)
})
function enregistrerAuto() {
  clearTimeout(timer)
  if (aEnregistrer) {
    o.value.modifieLe = maintenant()
    signalerModification(o.value)
    const dernier = o.value.historique.at(-1)
    if (dernier?.texte === 'Contenu de l\'offre modifié' && dernier.date.startsWith('Aujourd')) {
      dernier.date = maintenant()
    }
    else {
      o.value.historique.push({ date: maintenant(), texte: 'Contenu de l\'offre modifié' })
    }
    aEnregistrer = false
  }
  sauvegarder()
  sauvegarde.value = 'ok'
  heureOk.value = heure()
}

function quitter() {
  enregistrerAuto()
  notifier('Offre enregistrée.')
  aller({ nom: 'offre', id: o.value.id })
}
const peutPublier = computed(() => db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier)
</script>

<template>
  <PageAts
    actif="offres"
    largeur="full"
    :titre="nouvelle ? 'Créer une offre' : 'Modifier l\'offre'"
    :sous-titre="`${o.titre || 'Offre sans titre'} · ${o.id}`"
    :fil="nouvelle ? [{ label: 'Offres d\'emploi', to: '/offres' }, { label: 'Créer une offre' }] : [{ label: 'Offres d\'emploi', to: '/offres' }, { label: o.titre || o.id, to: `/offre/${o.id}` }, { label: 'Modifier' }]"
    :retour="{ to: `/offre/${o.id}`, label: 'Retour à l\'offre' }"
  >
    <template #actions>
      <span
        class="save"
        aria-live="polite"
      >
        <template v-if="sauvegarde === 'modif'">Modifications en cours…</template>
        <template v-else-if="sauvegarde === 'ok'"><CspIcon
          name="ri:check-line"
          :size="14"
        /> Enregistré à {{ heureOk }}</template>
        <template v-else>Brouillon enregistré automatiquement</template>
      </span>
    </template>

    <p
      v-if="o.validationEtat === 'en_attente'"
      class="bandeau"
    >
      <CspIcon
        name="ri:time-line"
        :size="16"
      />
      Validation en cours : vous pouvez continuer à modifier l'offre.
    </p>
    <p
      v-else-if="o.validationEtat === 'refusee'"
      class="bandeau bandeau--attention"
    >
      <CspIcon
        name="ri:chat-1-line"
        :size="16"
      />
      <span>
        Refusée :
        <template
          v-for="v in (o.validations ?? []).filter(x => x.decision === 'refus')"
          :key="v.nom"
        >« {{ v.commentaire }} » ({{ v.nom }}). </template>
        Complétez l'offre puis redemandez la validation ; les accords déjà donnés restent acquis.
      </span>
    </p>
    <p
      v-else-if="o.modifieeDepuisValidation"
      class="bandeau"
    >
      <CspIcon
        name="ri:information-line"
        :size="16"
      />
      Modifiée depuis la validation. Le circuit n'est pas relancé ; le détail figure dans le journal de l'offre.
    </p>

    <div class="formulaire">
      <nav
        class="etapes"
        aria-label="Étapes du formulaire"
      >
        <ol>
          <li
            v-for="(e, i) in ETAPES"
            :key="e.id"
          >
            <button
              type="button"
              class="etape"
              :aria-current="etape === e.id ? 'step' : undefined"
              @click="aller_etape(e.id)"
            >
              <span class="etape__num">{{ i + 1 }}</span>
              <span>
                <span class="etape__label">{{ e.label }}</span>
                <small>{{ aCompleter(e.id) ? `${aCompleter(e.id)} à compléter pour publier` : e.aide }}</small>
              </span>
            </button>
          </li>
        </ol>
      </nav>

      <div class="contenu">
        <h2 class="contenu__titre">
          {{ index + 1 }}. {{ ETAPES[index]!.label }}
        </h2>

        <FormInternes
          v-if="etape === 'internes'"
          :offre="o"
          :fiche="fiche"
        />
        <FormAnnonce
          v-else-if="etape === 'annonce'"
          :offre="o"
          :fiche="fiche"
        />
        <FormCandidature
          v-else-if="etape === 'candidature'"
          :offre="o"
        />
        <FormProcessus
          v-else-if="etape === 'processus'"
          :offre="o"
        />
        <FormEquipe
          v-else-if="etape === 'equipe'"
          :offre="o"
        />
        <template v-else>
          <Panel
            titre="Dates et diffusion"
            description="C'est à la publication que les champs obligatoires sont contrôlés."
          >
            <ChampsPublication
              :offre="o"
              :disabled="o.etat !== 'brouillon'"
            />
          </Panel>
          <Panel
            v-if="o.etat === 'brouillon'"
            titre="Avant de publier"
          >
            <p
              v-if="validationManquante(o)"
              class="texte"
            >
              <CspIcon
                name="ri:shield-check-line"
                :size="14"
              />
              Validation : {{ LIBELLES_VALIDATION[o.validationEtat].toLowerCase() }}. Elle doit être obtenue avant la publication.
            </p>
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
                  @click="aller_etape(m.etape)"
                >
                  Compléter
                </button>
              </li>
            </ul>
            <p
              v-if="!manques.length && !validationManquante(o)"
              class="texte"
            >
              L'offre est complète{{ db.organisme.validationActive ? ' et validée' : '' }} : vous pouvez la publier.
            </p>
            <div v-if="!manques.length && !validationManquante(o) && peutPublier">
              <CspButton
                label="Publier"
                icon="ri:send-plane-line"
                is-icon-left
                @click="enregistrerAuto(); aller({ nom: 'apercu', id: o.id, publier: true })"
              />
            </div>
          </Panel>
        </template>

        <div class="pied">
          <CspButton
            v-if="index > 0"
            label="Étape précédente"
            variant="tertiary-no-outline"
            icon="ri:arrow-left-line"
            is-icon-left
            @click="aller_etape(ETAPES[index - 1]!.id)"
          />
          <span class="pied__espace" />
          <CspButton
            label="Enregistrer et voir l'offre"
            variant="secondary"
            @click="quitter"
          />
          <DemandeValidation
            :offre="o"
            @demandee="enregistrerAuto"
          />
          <CspButton
            v-if="index < ETAPES.length - 1"
            label="Étape suivante"
            icon="ri:arrow-right-line"
            @click="aller_etape(ETAPES[index + 1]!.id)"
          />
        </div>
      </div>
    </div>
  </PageAts>
</template>

<style scoped lang="scss">
.save {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.bandeau {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-blue-france);
  background: var(--background-alt-blue-france);
  font-size: var(--csp-font-size-sm);

  &--attention {
    border-left-color: var(--border-plain-warning);
    background: var(--background-default-grey);
  }
}

.formulaire {
  display: grid;
  grid-template-columns: 15rem minmax(0, 1fr);
  gap: var(--csp-space-6);
  align-items: start;
}

.etapes {
  position: sticky;
  top: var(--csp-space-4);

  ol {
    display: flex;
    flex-direction: column;
    gap: var(--csp-space-1);
    margin: 0;
    padding: 0;
    list-style: none;
  }
}

.etape {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-2);
  width: 100%;
  padding: var(--csp-space-2) var(--csp-space-3);
  border: 0;
  border-left: 3px solid transparent;
  background: none;
  font: inherit;
  text-align: left;
  color: var(--text-default-grey);
  cursor: pointer;

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }

  &:hover {
    background: var(--background-default-grey-hover);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
  }

  &[aria-current='step'] {
    border-left-color: var(--border-active-blue-france);
    background: var(--background-alt-blue-france);

    .etape__label {
      color: var(--text-action-high-blue-france);
      font-weight: var(--csp-font-weight-bold);
    }
  }
}

.etape__num {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
  width: 1.5rem;
  height: 1.5rem;
  border: 1px solid var(--border-default-grey);
  border-radius: 50%;
  font-size: var(--csp-font-size-xs);
}

.etape__label {
  font-size: var(--csp-font-size-sm);
}

.contenu {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  min-width: 0;
}

.contenu__titre {
  margin: 0;
  font-size: var(--csp-font-size-lg);
}

.texte {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-sm);
}

.manques {
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

.pied {
  position: sticky;
  bottom: 0;
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  box-shadow: var(--csp-shadow-md);
}

.pied__espace {
  flex: 1;
}
</style>
