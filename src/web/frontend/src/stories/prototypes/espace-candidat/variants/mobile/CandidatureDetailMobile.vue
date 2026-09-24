<script setup lang="ts">
import { computed, ref } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { statutMeta } from '../../data/espaceMock'
import { formaterDateHeure, formaterDateLongue } from '../../data/format'
import { useEspace } from '../../data/useEspace'
import RetourLien from '../../shared/mobile/RetourLien.vue'
import StatutCandidatBadge from '../../shared/mobile/StatutCandidatBadge.vue'
import RetraitSheet from './RetraitSheet.vue'

const props = defineProps<{
  candidatureId: string
}>()

const emit = defineEmits<{
  retour: []
  ouvrirConversation: [conversationId: string]
  retiree: []
}>()

const espace = useEspace()
const candidature = computed(() => espace.candidature(props.candidatureId))
const conversations = computed(() => espace.conversationsTriees(props.candidatureId))
const retraitOuvert = ref(false)

function apercu(conversationId: string): string {
  const message = conversations.value.find(c => c.id === conversationId)?.messages.at(-1)
  if (!message) {
    return ''
  }
  return `${message.auteur === 'candidat' ? 'Vous : ' : ''}${message.texte}`
}

function confirmerRetrait(motif: string | undefined) {
  espace.retirer(props.candidatureId, motif)
  retraitOuvert.value = false
  emit('retiree')
}
</script>

<template>
  <div
    v-if="candidature"
    class="detail"
  >
    <RetourLien
      label="Mes candidatures"
      @retour="emit('retour')"
    />

    <header class="detail__entete">
      <h1 class="detail__intitule">
        {{ candidature.intitule }}
      </h1>
      <p class="detail__organisme">
        {{ candidature.organisme }}
      </p>
      <div class="detail__statut">
        <StatutCandidatBadge :statut="candidature.statut" />
        <p class="detail__phrase">
          {{ statutMeta[candidature.statut].phrase }}
        </p>
      </div>
      <p class="detail__depot">
        Candidature déposée le {{ formaterDateLongue(candidature.dateDepot) }}
      </p>
    </header>

    <section class="detail__section">
      <h2>Conversations</h2>
      <p
        v-if="conversations.length === 0"
        class="detail__vide"
      >
        Aucune conversation pour le moment.
      </p>
      <ul
        v-else
        class="detail__conversations"
      >
        <li
          v-for="conversation in conversations"
          :key="conversation.id"
        >
          <button
            type="button"
            class="conv"
            :class="{ 'conv--non-lue': espace.nonLusConversation(conversation) > 0 }"
            @click="emit('ouvrirConversation', conversation.id)"
          >
            <span
              v-if="espace.nonLusConversation(conversation) > 0"
              class="conv__point"
              aria-hidden="true"
            />
            <span class="conv__corps">
              <span class="conv__sujet">
                {{ conversation.sujet }}
                <span
                  v-if="espace.nonLusConversation(conversation) > 0"
                  class="conv__non-lu"
                >Non lu</span>
              </span>
              <span class="conv__apercu">{{ apercu(conversation.id) }}</span>
              <span class="conv__date">
                {{ formaterDateHeure(conversation.messages.at(-1)!.date) }}
              </span>
            </span>
            <CspIcon
              name="ri:arrow-right-s-line"
              :size="22"
              class="conv__chevron"
            />
          </button>
        </li>
      </ul>
    </section>

    <details class="detail__pli">
      <summary>
        <span>L'offre</span>
        <CspIcon
          name="ri:arrow-down-s-line"
          :size="20"
          class="detail__pli-icone"
        />
      </summary>
      <dl class="detail__faits">
        <div>
          <dt>Lieu</dt>
          <dd>{{ candidature.offre.lieu }}</dd>
        </div>
        <div>
          <dt>Type de contrat</dt>
          <dd>{{ candidature.offre.typeContrat }}</dd>
        </div>
        <div>
          <dt>Catégorie</dt>
          <dd>{{ candidature.offre.categorie }}</dd>
        </div>
      </dl>
      <p class="detail__description">
        {{ candidature.offre.description }}
      </p>
    </details>

    <details class="detail__pli">
      <summary>
        <span>Pièces déposées à la candidature</span>
        <CspIcon
          name="ri:arrow-down-s-line"
          :size="20"
          class="detail__pli-icone"
        />
      </summary>
      <ul class="detail__pieces">
        <li
          v-for="piece in candidature.piecesDeposees"
          :key="piece.id"
        >
          <CspIcon
            name="ri:file-text-line"
            :size="20"
          />
          <span class="detail__piece-corps">
            <span class="detail__piece-libelle">{{ piece.libelle }}</span>
            <span class="detail__piece-nom">{{ piece.nom }}</span>
          </span>
        </li>
      </ul>
    </details>

    <button
      v-if="statutMeta[candidature.statut].enCours"
      type="button"
      class="detail__retrait"
      @click="retraitOuvert = true"
    >
      Retirer ma candidature
    </button>

    <RetraitSheet
      v-model:open="retraitOuvert"
      @confirmer="confirmerRetrait"
    />
  </div>
</template>

<style scoped lang="scss">
.detail {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  padding: var(--csp-space-2) var(--csp-space-4) var(--csp-space-8);
}

.detail__entete {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.detail__intitule {
  margin: 0;
  font-size: 1.375rem;
  font-weight: 700;
  line-height: 1.25;
  color: var(--text-title-grey);
}

.detail__organisme {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-default-grey);
}

.detail__statut {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin-top: var(--csp-space-2);
  padding: var(--csp-space-3) var(--csp-space-4);
  border-radius: 0.5rem;
  background-color: var(--background-alt-grey);
}

.detail__phrase {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 600;
  line-height: 1.4;
  color: var(--text-title-grey);
}

.detail__depot {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.detail__section h2 {
  margin: 0 0 var(--csp-space-3);
  font-size: 1.0625rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.detail__vide {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}

.detail__conversations {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

.conv {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  width: 100%;
  min-height: 3.5rem;
  padding: var(--csp-space-3) var(--csp-space-4);
  border: none;
  border-radius: 0.5rem;
  text-align: left;
  cursor: pointer;
  font: inherit;
  background-color: var(--background-default-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);

  &--non-lue {
    background-color: var(--background-alt-blue-france);
    box-shadow:
      inset 0 0 0 1px var(--border-action-low-blue-france),
      inset 4px 0 0 var(--background-action-high-blue-france);
  }
}

.conv__point {
  flex-shrink: 0;
  width: 0.625rem;
  height: 0.625rem;
  border-radius: 50%;
  background-color: var(--background-action-high-blue-france);
}

.conv__corps {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.conv__sujet {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--text-title-grey);
}

.conv--non-lue .conv__sujet {
  font-weight: 700;
}

.conv__non-lu {
  padding: 0.0625rem 0.4375rem;
  border-radius: 999px;
  background-color: var(--background-action-high-blue-france);
  color: var(--text-inverted-blue-france);
  font-size: 0.6875rem;
  font-weight: 700;
}

.conv__apercu {
  font-size: 0.8125rem;
  color: var(--text-default-grey);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conv__date {
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.conv__chevron {
  flex-shrink: 0;
  color: var(--text-mention-grey);
}

.detail__pli {
  border-radius: 0.5rem;
  background-color: var(--background-alt-grey);

  summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 3rem;
    padding: 0 var(--csp-space-4);
    cursor: pointer;
    list-style: none;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-title-grey);

    &::-webkit-details-marker {
      display: none;
    }
  }

  &[open] .detail__pli-icone {
    transform: rotate(180deg);
  }
}

.detail__pli-icone {
  transition: transform 0.15s ease;
  color: var(--text-mention-grey);
}

.detail__faits {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0 var(--csp-space-4) var(--csp-space-3);

  dt {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    color: var(--text-mention-grey);
  }

  dd {
    margin: 0.125rem 0 0;
    font-size: 0.9375rem;
    font-weight: 500;
    color: var(--text-default-grey);
  }
}

.detail__description {
  margin: 0;
  padding: 0 var(--csp-space-4) var(--csp-space-4);
  font-size: 0.9375rem;
  line-height: 1.55;
  color: var(--text-default-grey);
}

.detail__pieces {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0 var(--csp-space-4) var(--csp-space-4);
  list-style: none;

  li {
    display: flex;
    align-items: center;
    gap: var(--csp-space-3);
    color: var(--text-action-high-blue-france);
  }
}

.detail__piece-corps {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.detail__piece-libelle {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-title-grey);
}

.detail__piece-nom {
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.detail__retrait {
  align-self: center;
  min-height: 2.75rem;
  padding: 0 var(--csp-space-3);
  border: none;
  background: none;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-error);
  text-decoration: underline;
}
</style>
