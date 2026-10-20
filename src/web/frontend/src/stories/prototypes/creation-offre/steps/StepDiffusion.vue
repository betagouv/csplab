<script setup lang="ts">
import { computed } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import { useOffre } from '../data/useOffre'
import FormSection from '../shared/FormSection.vue'
import StepFooter from '../shared/StepFooter.vue'
import StepHeader from '../shared/StepHeader.vue'

// Écran 8 — configurer la diffusion. La rédaction est faite ; ici on choisit où et quand
// l'offre sera visible, et on voit ce qui restera à faire à la main.
const { state, canaux, manques, validationRestante, afficherErreurs, aller } = useOffre()

const lignes = computed(() => canaux.map(c => ({ ...c, etat: state.canaux.find(x => x.id === c.id)! })))
const selection = computed(() => lignes.value.filter(l => l.etat.selectionne))

const manquesContenu = computed(() => manques.value.filter(m => m.stepId !== 'diffusion'))
const actionsManuelles = computed(() => selection.value.flatMap(l => l.actionsManuelles.map(a => ({ canal: l.nom, action: a }))))
const attendusManquants = computed(() => selection.value.flatMap(l => l.attendus.filter(a => !a.ok(state)).map(a => ({ canal: l.nom, ...a }))))

const ISO = /^\d{4}-\d{2}-\d{2}$/
const erreurDebut = computed(() => (state.dateDebutDiffusion && !ISO.test(state.dateDebutDiffusion) ? 'Format attendu : AAAA-MM-JJ' : undefined))
const erreurLimite = computed(() => {
  if (!state.dateLimite) {
    return afficherErreurs.value ? 'Indiquez une date limite de candidature.' : undefined
  }
  if (!ISO.test(state.dateLimite)) {
    return 'Format attendu : AAAA-MM-JJ'
  }
  if (state.dateDebutDiffusion && state.dateLimite <= state.dateDebutDiffusion) {
    return 'La date limite doit être postérieure au début de la diffusion.'
  }
  return undefined
})
const dureeJours = computed(() => {
  if (!state.dateDebutDiffusion || !state.dateLimite || erreurLimite.value || erreurDebut.value) {
    return null
  }
  return Math.round((+new Date(state.dateLimite) - +new Date(state.dateDebutDiffusion)) / 86400000)
})
</script>

<template>
  <StepHeader
    id="diffusion"
    description="Où et quand l'offre sera visible. Les canaux sont indicatifs : aucune connexion réelle n'est simulée, mais vous voyez ce que chaque canal attend et les actions qui resteront à faire."
  />

  <section
    class="ready"
    aria-label="Préparation de la publication"
  >
    <div
      class="ready__col"
      :class="manquesContenu.length ? 'ready__col--ko' : 'ready__col--ok'"
    >
      <p class="ready__label">
        Contenu de l'offre
      </p>
      <p class="ready__value">
        <CspIcon
          :name="manquesContenu.length ? 'ri:error-warning-line' : 'ri:checkbox-circle-fill'"
          :size="16"
        />
        {{ manquesContenu.length ? `${manquesContenu.length} information(s) manquante(s)` : 'Prêt à être publié' }}
      </p>
      <CspButton
        v-if="manquesContenu.length"
        label="Voir le récapitulatif"
        variant="tertiary-no-outline"
        size="sm"
        @click="aller('recap')"
      />
    </div>
    <div
      class="ready__col"
      :class="validationRestante.length ? 'ready__col--wait' : 'ready__col--ok'"
    >
      <p class="ready__label">
        Validations
      </p>
      <p class="ready__value">
        <CspIcon
          :name="validationRestante.length ? 'ri:time-line' : 'ri:checkbox-circle-fill'"
          :size="16"
        />
        {{ validationRestante.length ? `${validationRestante.length} validation(s) obligatoire(s) restante(s)` : 'Toutes obtenues' }}
      </p>
      <CspButton
        v-if="validationRestante.length"
        label="Voir le circuit"
        variant="tertiary-no-outline"
        size="sm"
        @click="aller('validation')"
      />
    </div>
    <div class="ready__col ready__col--info">
      <p class="ready__label">
        Actions de diffusion
      </p>
      <p class="ready__value">
        <CspIcon
          name="ri:task-line"
          :size="16"
        />
        {{ actionsManuelles.length ? `${actionsManuelles.length} action(s) manuelle(s) après publication` : 'Aucune action manuelle' }}
      </p>
    </div>
  </section>

  <FormSection
    titre="Période de diffusion"
    nature="recrutement"
  >
    <div class="dates">
      <CspInput
        v-model="state.dateDebutDiffusion"
        label="Début de diffusion"
        hint="Vide = dès la publication"
        placeholder="AAAA-MM-JJ"
        :error="Boolean(erreurDebut)"
        :error-message="erreurDebut"
      />
      <CspInput
        v-model="state.dateLimite"
        label="Date limite de candidature *"
        placeholder="AAAA-MM-JJ"
        :error="Boolean(erreurLimite)"
        :error-message="erreurLimite"
      />
      <p
        v-if="dureeJours !== null"
        class="dates__duree"
      >
        {{ dureeJours }} jours de diffusion
      </p>
    </div>
  </FormSection>

  <FormSection
    titre="Canaux de diffusion"
    description="Cochez les canaux envisagés. Le texte de l'offre est le même partout ; seule la mise en forme varie."
    nature="recrutement"
  >
    <p
      v-if="afficherErreurs && !selection.length"
      class="err"
      role="alert"
    >
      Sélectionnez au moins un canal.
    </p>
    <ul class="channels">
      <li
        v-for="l in lignes"
        :key="l.id"
        class="channel"
        :class="{ 'channel--on': l.etat.selectionne }"
      >
        <label class="channel__main">
          <input
            v-model="l.etat.selectionne"
            type="checkbox"
            class="channel__check"
          >
          <span class="channel__text">
            <strong>{{ l.nom }}</strong>
            <small>{{ l.description }}</small>
          </span>
          <CspBadge
            :label="l.mode === 'connecteur' ? 'Transmission automatique (hypothèse)' : 'Action manuelle'"
            :type="l.mode === 'connecteur' ? 'info' : 'warning'"
            variant="outline"
            size="sm"
          />
        </label>
        <div
          v-if="l.etat.selectionne && (l.attendus.length || l.actionsManuelles.length)"
          class="channel__details"
        >
          <ul
            v-if="l.attendus.length"
            class="channel__checks"
          >
            <li
              v-for="a in l.attendus"
              :key="a.libelle"
              :class="a.ok(state) ? 'ok' : 'ko'"
            >
              <CspIcon
                :name="a.ok(state) ? 'ri:check-line' : 'ri:error-warning-line'"
                :size="14"
              />
              {{ a.libelle }}
              <button
                v-if="!a.ok(state)"
                type="button"
                class="link"
                @click="aller(a.stepId)"
              >
                Compléter
              </button>
            </li>
          </ul>
          <ul
            v-if="l.actionsManuelles.length"
            class="channel__todo"
          >
            <li
              v-for="a in l.actionsManuelles"
              :key="a"
            >
              <CspIcon
                name="ri:time-line"
                :size="14"
              />
              Après publication : {{ a }}
            </li>
          </ul>
        </div>
      </li>
    </ul>
  </FormSection>

  <section
    class="summary"
    aria-labelledby="summary-title"
  >
    <h3
      id="summary-title"
      class="summary__title"
    >
      Publication envisagée
    </h3>
    <p v-if="selection.length">
      Diffusion sur <strong>{{ selection.map(s => s.nom).join(', ') }}</strong>,
      <template v-if="state.dateDebutDiffusion">
        à partir du {{ state.dateDebutDiffusion }}
      </template>
      <template v-else>
        dès la publication
      </template>
      <template v-if="state.dateLimite">
        , jusqu'au {{ state.dateLimite }}.
      </template>
      <template v-else>
        — date limite à définir.
      </template>
    </p>
    <p
      v-else
      class="muted"
    >
      Aucun canal sélectionné.
    </p>
    <p
      v-if="attendusManquants.length"
      class="muted"
    >
      {{ attendusManquants.length }} information(s) attendue(s) par les canaux restent à compléter.
    </p>
  </section>

  <StepFooter id="diffusion" />
</template>

<style scoped lang="scss">
.ready {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.ready__col {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-1);
  padding: var(--csp-space-3) var(--csp-space-4);
  border-top: 3px solid var(--border-default-grey);

  & + & {
    border-left: 1px solid var(--border-default-grey);
  }

  &--ok {
    border-top-color: var(--border-plain-success);
  }

  &--ko {
    border-top-color: var(--border-plain-warning);
  }

  &--wait {
    border-top-color: var(--border-plain-blue-france);
  }

  &--info {
    border-top-color: var(--border-plain-grey);
  }
}

.ready__label {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.ready__value {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
}

.dates {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: var(--csp-space-4);
  align-items: start;
}

.dates__duree {
  margin: var(--csp-space-6) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.err {
  margin: 0;
  color: var(--text-default-error);
  font-size: var(--csp-font-size-sm);
}

.channels {
  margin: 0;
  padding: 0;
  list-style: none;
  border: 1px solid var(--border-default-grey);
}

.channel + .channel {
  border-top: 1px solid var(--border-default-grey);
}

.channel--on {
  background: var(--background-alt-blue-france);
}

.channel__main {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);
  cursor: pointer;
}

.channel__check {
  margin-top: 3px;
  width: 1rem;
  height: 1rem;
  accent-color: var(--background-action-high-blue-france);
}

.channel__text {
  flex: 1;

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.channel__details {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  padding: 0 var(--csp-space-4) var(--csp-space-3) calc(var(--csp-space-4) + 1rem + var(--csp-space-3));
  font-size: var(--csp-font-size-sm);

  ul {
    display: flex;
    flex-direction: column;
    gap: var(--csp-space-1);
    margin: 0;
    padding: 0;
    list-style: none;
  }

  li {
    display: flex;
    align-items: center;
    gap: var(--csp-space-1);
  }
}

.channel__checks .ok {
  color: var(--text-default-success);
}

.channel__checks .ko {
  color: var(--text-default-warning);
}

.channel__todo {
  color: var(--text-mention-grey);
}

.link {
  margin-left: var(--csp-space-1);
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}

.summary {
  padding: var(--csp-space-4) var(--csp-space-5);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);

  p {
    margin: 0 0 var(--csp-space-1);
  }
}

.summary__title {
  margin: 0 0 var(--csp-space-2);
  font-size: var(--csp-font-size-base);
}

.muted {
  color: var(--text-mention-grey);
  font-size: var(--csp-font-size-sm);
}
</style>
