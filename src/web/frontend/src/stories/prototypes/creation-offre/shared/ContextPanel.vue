<script setup lang="ts">
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { libelleMetier, ORGANISMES, personne } from '../data/referentiels'
import { useOffre } from '../data/useOffre'

// Panneau latéral « contexte du recrutement » : toujours visible, il répond à
// « où en est-on, qui attend quoi, d'où viennent les données ? ».
const { state, manques, etapeEnCours, aller, validationRestante, peutPublier } = useOffre()

const prochaineAction = computed(() => {
  switch (state.statut) {
    case 'publiee':
      return { qui: 'Équipe de recrutement', quoi: 'Suivre les candidatures reçues', icon: 'ri:team-line' }
    case 'validee':
      return peutPublier.value
        ? { qui: 'Vous', quoi: 'Publier l\'offre', icon: 'ri:send-plane-line' }
        : { qui: 'Vous', quoi: 'Compléter la diffusion avant publication', icon: 'ri:edit-line' }
    case 'a_corriger':
      return { qui: 'Vous', quoi: 'Traiter les corrections demandées puis renvoyer', icon: 'ri:edit-line' }
    case 'a_valider':
      return etapeEnCours.value
        ? { qui: personne(etapeEnCours.value.personneId).nom, quoi: etapeEnCours.value.libelle, icon: 'ri:time-line' }
        : { qui: '—', quoi: 'Validation en cours', icon: 'ri:time-line' }
    default:
      if (manques.value.some(m => m.stepId !== 'diffusion')) {
        return { qui: 'Vous', quoi: `Compléter ${manques.value.filter(m => m.stepId !== 'diffusion').length} information(s) requise(s)`, icon: 'ri:edit-line' }
      }
      return validationRestante.value.length
        ? { qui: 'Vous', quoi: 'Soumettre l\'offre à validation', icon: 'ri:send-plane-line' }
        : { qui: 'Vous', quoi: 'Vérifier puis publier', icon: 'ri:send-plane-line' }
  }
})

const intervenants = computed(() => {
  const ids = new Set<string>(['camille'])
  state.contributions.forEach(c => ids.add(c.personneId))
  state.circuit.forEach(e => ids.add(e.personneId))
  if (state.besoin.darApplicable === 'oui') {
    ids.add('helene')
  }
  return [...ids].map(personne)
})

const contributionsEnAttente = computed(() => state.contributions.filter(c => c.statut === 'en_attente'))
const organisme = computed(() => ORGANISMES.find(o => o.value === state.besoin.organisme))
</script>

<template>
  <aside
    class="ctx"
    aria-label="Contexte du recrutement"
  >
    <section class="ctx__block ctx__block--next">
      <h3 class="ctx__title">
        Prochaine action
      </h3>
      <p class="ctx__next">
        <CspIcon
          :name="prochaineAction.icon"
          :size="16"
        />
        <span>
          <strong>{{ prochaineAction.quoi }}</strong>
          <small>Par : {{ prochaineAction.qui }}</small>
        </span>
      </p>
      <CspButton
        v-if="state.statut === 'brouillon' || state.statut === 'a_corriger'"
        label="Voir le récapitulatif"
        size="sm"
        variant="secondary"
        @click="aller('recap')"
      />
    </section>

    <section class="ctx__block">
      <h3 class="ctx__title">
        Recrutement
      </h3>
      <dl class="ctx__dl">
        <dt>Poste</dt>
        <dd>{{ state.besoin.intitule || '—' }}</dd>
        <dt>Organisme</dt>
        <dd>
          {{ organisme?.label ?? '—' }}
          <small v-if="organisme">{{ organisme.versant }}</small>
        </dd>
        <dt>Métier</dt>
        <dd>{{ libelleMetier(state.besoin.metier) || state.besoin.metierHorsReferentiel || '—' }}</dd>
        <dt>Catégorie</dt>
        <dd>{{ state.besoin.categories.join(', ') || '—' }}</dd>
      </dl>
    </section>

    <section
      v-if="state.sourceLibelle || state.besoin.darRef || state.besoin.ficheRef"
      class="ctx__block"
    >
      <h3 class="ctx__title">
        Documents liés
      </h3>
      <ul class="ctx__list">
        <li v-if="state.besoin.darRef">
          <CspIcon
            name="ri:shield-check-line"
            :size="14"
          />
          {{ state.besoin.darRef }}
          <small>{{ { "validee": 'validée', "en_cours": 'en cours', "a_demander": 'à demander', '': '' }[state.besoin.darStatut] }}</small>
        </li>
        <li v-if="state.besoin.ficheRef">
          <CspIcon
            name="ri:file-text-line"
            :size="14"
          />
          {{ state.besoin.ficheRef }}
        </li>
        <li v-if="state.startMode === 'duplication'">
          <CspIcon
            name="ri:file-copy-2-line"
            :size="14"
          />
          {{ state.sourceLibelle.split(' — ')[0] }} <small>offre dupliquée</small>
        </li>
      </ul>
    </section>

    <section class="ctx__block">
      <h3 class="ctx__title">
        Intervenants
      </h3>
      <ul class="ctx__people">
        <li
          v-for="p in intervenants"
          :key="p.id"
        >
          <span
            class="ctx__avatar"
            aria-hidden="true"
          >{{ p.nom.split(' ').map(n => n[0]).join('') }}</span>
          <span>
            {{ p.nom }}<template v-if="p.id === 'camille'"> (vous)</template>
            <small>{{ p.role }}</small>
          </span>
        </li>
      </ul>
      <p
        v-if="contributionsEnAttente.length"
        class="ctx__pending"
      >
        {{ contributionsEnAttente.length }} contribution(s) attendue(s) —
        <button
          type="button"
          class="ctx__link"
          @click="aller('validation')"
        >
          voir
        </button>
      </p>
    </section>

    <section class="ctx__block">
      <h3 class="ctx__title">
        Historique
      </h3>
      <ol class="ctx__journal">
        <li
          v-for="(j, i) in [...state.journal].reverse().slice(0, 5)"
          :key="i"
        >
          <small>{{ j.date }}</small>
          {{ j.texte }}
        </li>
      </ol>
    </section>
  </aside>
</template>

<style scoped lang="scss">
.ctx {
  display: flex;
  flex-direction: column;
  font-size: var(--csp-font-size-sm);
}

.ctx__block {
  padding: var(--csp-space-4);
  border-bottom: 1px solid var(--border-default-grey);

  &--next {
    background: var(--background-alt-blue-france);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: var(--csp-space-2);
  }
}

.ctx__title {
  margin: 0 0 var(--csp-space-2);
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--text-mention-grey);

  .ctx__block--next & {
    margin: 0;
  }
}

.ctx__next {
  display: flex;
  gap: var(--csp-space-2);
  margin: 0;

  :deep(.csp-icon) {
    flex-shrink: 0;
    margin-top: 2px;
    color: var(--text-action-high-blue-france);
  }
}

small {
  display: block;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.ctx__dl {
  display: grid;
  grid-template-columns: 5.5rem 1fr;
  gap: var(--csp-space-1) var(--csp-space-2);
  margin: 0;

  dt {
    color: var(--text-mention-grey);
  }

  dd {
    margin: 0;
    min-width: 0;
    overflow-wrap: anywhere;
  }
}

.ctx__list,
.ctx__people,
.ctx__journal {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

.ctx__list li {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-1);

  small {
    display: inline;
  }
}

.ctx__people li {
  display: flex;
  gap: var(--csp-space-2);
  align-items: flex-start;
}

.ctx__avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 1.75rem;
  height: 1.75rem;
  border-radius: 50%;
  background: var(--background-contrast-grey);
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
}

.ctx__pending {
  margin: var(--csp-space-3) 0 0;
  color: var(--text-default-warning);
}

.ctx__link {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}

.ctx__journal li {
  padding-left: var(--csp-space-3);
  border-left: 2px solid var(--border-default-grey);
}
</style>
