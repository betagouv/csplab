<script setup lang="ts">
import type { Fiche, Offre, Proposition } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import BlocValidation from './BlocValidation.vue'
import { useNav } from './nav'
import ResumeValidation from './ResumeValidation.vue'
import { le, repondre, sauvegarder, UTILISATEUR } from './store'

// Bloc du valideur, en haut de la page : le résumé pour décider, puis la décision
// (valider tel quel, valider avec un commentaire, refuser avec un commentaire).
// Les propositions de modification préparées dans les sections partent avec la réponse.
const props = defineProps<{ offre: Offre, fiche?: Fiche, propositions: Proposition[] }>()
const emit = defineEmits<{ retirer: [section: Proposition['section']], envoye: [] }>()
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
const SECTIONS: Record<Proposition['section'], string> = { annonce: 'Annonce', candidature: 'Formulaire de candidature', publication: 'Publication' }

function envoyer() {
  if (!pret.value || indice.value < 0) {
    return
  }
  repondre(o.value, indice.value, choix.value === 'refus' ? 'refus' : 'accord', UTILISATEUR, commentaireRequis.value ? commentaire.value.trim() : undefined, props.propositions)
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
      <CspTextarea
        v-if="commentaireRequis"
        v-model="commentaire"
        :label="choix === 'refus' ? 'Commentaire (obligatoire) : ce qui manque ou le motif du refus' : 'Commentaire (obligatoire)'"
        hint="Visible de la personne qui rédige l'offre et des autres valideurs ; jamais publié."
        :rows="3"
      />

      <div class="decision__props">
        <p
          v-if="!propositions.length"
          class="mention"
        >
          Pour proposer des modifications, cliquez sur « Proposer des modifications » dans la section concernée, plus bas : elles partiront avec votre réponse.
        </p>
        <template v-else>
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
