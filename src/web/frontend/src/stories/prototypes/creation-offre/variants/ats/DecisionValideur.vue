<script setup lang="ts">
import type { Fiche, Offre, Proposition } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import BlocValidation from './BlocValidation.vue'
import ChampSimple from './ChampSimple.vue'
import { useNav } from './nav'
import ResumeValidation from './ResumeValidation.vue'
import { le, repondre, sauvegarder, UTILISATEUR } from './store'

// Bloc du valideur, en haut de la page : le résumé pour décider, puis la décision
// (valider tel quel, valider avec un commentaire, refuser avec un commentaire).
// Les propositions de modification préparées dans les sections partent avec la réponse.
const props = defineProps<{ offre: Offre, fiche?: Fiche, propositions: Proposition[] }>()
const emit = defineEmits<{ retirer: [section: Proposition['section']], proposer: [section: Proposition['section']], envoye: [] }>()
const { notifier } = useNav()
const o = computed(() => props.offre)

const indice = computed(() => (o.value.validations ?? []).findIndex(v => v.decision === 'attente' && v.valideurs.includes(UTILISATEUR)))
const groupe = computed(() => o.value.validations?.[indice.value]?.nom ?? '')

type Choix = 'tel_quel' | 'commentaire' | 'refus'
const CHOIX = [
  { value: 'tel_quel', label: 'Valider tel quel' },
  { value: 'commentaire', label: 'Valider avec un commentaire' },
  { value: 'refus', label: 'Refuser avec un commentaire' },
]
const choix = ref<Choix>('tel_quel')
const commentaire = ref('')
const nbChamps = computed(() => props.propositions.reduce((n, p) => n + p.champs.length, 0))
const commentaireRequis = computed(() => choix.value !== 'tel_quel')
const pret = computed(() => !commentaireRequis.value || Boolean(commentaire.value.trim()))
// Dates et diffusion se choisissent au moment de publier : pas de proposition sur la publication.
const SECTIONS: Record<Proposition['section'], string> = { annonce: 'Annonce', candidature: 'Formulaire de candidature', publication: 'Publication' }
const PROPOSABLES: Proposition['section'][] = ['annonce', 'candidature']
// « Proposer des modifications » : on choisit la partie à modifier, l'écran défile jusqu'à elle en mode modification.
const MENU = computed(() => [{
  items: PROPOSABLES.map(id => ({
    label: props.propositions.some(p => p.section === id) ? `${SECTIONS[id]} (déjà modifiée)` : SECTIONS[id],
    onSelect: () => emit('proposer', id),
  })),
}])

function envoyer() {
  if (!pret.value || indice.value < 0) {
    return
  }
  // « Valider tel quel » : ni commentaire ni proposition.
  repondre(o.value, indice.value, choix.value === 'refus' ? 'refus' : 'accord', UTILISATEUR, commentaireRequis.value ? commentaire.value.trim() : undefined, commentaireRequis.value ? props.propositions : [])
  sauvegarder()
  notifier(choix.value === 'refus' ? 'Refus envoyé à la personne qui rédige l\'offre.' : 'Validation envoyée.')
  emit('envoye')
}
</script>

<template>
  <section
    id="validation"
    class="decision"
  >
    <header>
      <h3 class="decision__titre">
        Votre décision · {{ groupe }}
      </h3>
      <p class="decision__desc">
        Demandée {{ le(o.validationDemandeeLe) }} par {{ o.creePar }}. Consultez le résumé et l'offre, puis répondez.
      </p>
    </header>

    <BlocValidation :offre="o" />

    <div class="decision__resume">
      <h4 class="decision__sous">
        Résumé pour la validation
      </h4>
      <ResumeValidation
        :offre="o"
        :fiche="fiche"
        integre
      />
    </div>

    <div class="decision__reponse">
      <h4 class="decision__sous">
        Votre réponse
      </h4>
      <CspRadioGroup
        v-model="choix"
        label="Décision"
        :options="CHOIX"
      />
      <ChampSimple
        v-if="commentaireRequis"
        :label="choix === 'refus' ? 'Commentaire : ce qui manque ou le motif du refus' : 'Commentaire'"
        hint="Champ obligatoire"
        info="Visible de la personne qui rédige l'offre et des autres valideurs ; jamais publié."
      >
        <CspTextarea
          v-model="commentaire"
          label="Commentaire"
          :rows="3"
        />
      </ChampSimple>

      <div v-if="commentaireRequis">
        <CspDropdownMenu
          :sections="MENU"
          side="bottom"
          align="start"
        >
          <template #trigger>
            <CspButton
              label="Proposer des modifications"
              variant="secondary"
              size="sm"
              icon="ri:arrow-down-s-line"
            />
          </template>
        </CspDropdownMenu>
        <p class="aide">
          Choisissez la partie à modifier : vos changements ne modifient pas l'offre et partiront avec votre réponse.
        </p>
      </div>

      <div
        v-if="commentaireRequis && propositions.length"
        class="decision__props"
      >
        <template v-if="propositions.length">
          <p class="mention">
            {{ nbChamps > 1 ? `${nbChamps} modifications proposées partiront` : '1 modification proposée partira' }} avec votre réponse :
          </p>
          <ul class="liste">
            <li
              v-for="p in propositions"
              :key="p.section"
            >
              <span><strong>{{ SECTIONS[p.section] }}</strong> : {{ p.champs.map(c => c.libelle).join(', ') }}</span>
              <CspButton
                label="Retirer"
                size="sm"
                variant="tertiary-no-outline"
                @click="emit('retirer', p.section)"
              />
            </li>
          </ul>
        </template>
      </div>

      <div>
        <CspButton
          label="Envoyer ma réponse"
          icon="ri:send-plane-line"
          is-icon-left
          :disabled="!pret"
          @click="envoyer"
        />
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
.decision {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  scroll-margin-top: 4.5rem;
  padding: var(--csp-space-5) var(--csp-space-6);
  border: 1px solid var(--border-default-grey);
  border-top: 3px solid var(--border-plain-blue-france);
  background: var(--background-default-grey);
}

.decision__titre {
  margin: 0;
  font-size: var(--csp-font-size-lg);
  font-weight: var(--csp-font-weight-bold);
}

.decision__desc {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.decision__sous {
  margin: 0 0 var(--csp-space-3);
  font-size: var(--csp-font-size-md, 1rem);
  font-weight: var(--csp-font-weight-bold);
}

.decision__reponse {
  scroll-margin-top: 4.5rem;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  max-width: 48rem;
  padding-top: var(--csp-space-5);
  border-top: 1px solid var(--border-default-grey);

  .decision__sous {
    margin-bottom: 0;
  }
}

.decision__props {
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-alt-blue-france);
}

.mention {
  margin: 0;
  font-size: var(--csp-font-size-sm);
}

.aide {
  margin: var(--csp-space-2) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.liste {
  margin: var(--csp-space-2) 0 0;
  padding: 0;
  list-style: none;
  font-size: var(--csp-font-size-sm);

  li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: var(--csp-space-3);
  }
}
</style>
