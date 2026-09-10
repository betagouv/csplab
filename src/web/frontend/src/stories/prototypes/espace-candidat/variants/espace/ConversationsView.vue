<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { actionsRequises, conversations, nombreMessagesNonLus } from '../../data/candidatMock'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'

const props = defineProps<{
  initialConversationId?: string | null
}>()

const selectedId = ref(props.initialConversationId ?? conversations[0]?.id ?? null)

watch(() => props.initialConversationId, (id) => {
  if (id) {
    selectedId.value = id
  }
})

watch(selectedId, (id) => {
  const conv = conversations.find(c => c.id === id)
  conv?.messages.forEach((m) => { m.lu = true })
}, { immediate: true })

const selected = computed(() => conversations.find(c => c.id === selectedId.value) ?? null)

const brouillon = ref('')

function envoyerReponse() {
  if (!selected.value || !brouillon.value.trim()) {
    return
  }
  selected.value.messages.push({
    id: `m-${Date.now()}`,
    auteur: 'candidat',
    texte: brouillon.value.trim(),
    date: 'À l\'instant',
    lu: true,
  })
  brouillon.value = ''

  const candidatureId = selected.value.candidatureId
  const index = actionsRequises.findIndex(a => a.candidatureId === candidatureId && a.type === 'message')
  if (index !== -1) {
    actionsRequises.splice(index, 1)
  }
}

function ouvrirConversation(id: string) {
  selectedId.value = id
}
</script>

<template>
  <div class="conversations">
    <h1 class="conversations__title">
      Messages
    </h1>

    <div class="conversations__layout">
      <ul class="conversations__list">
        <li
          v-for="conversation in conversations"
          :key="conversation.id"
        >
          <button
            type="button"
            class="conversations__item"
            :class="{ 'conversations__item--active': conversation.id === selectedId }"
            @click="ouvrirConversation(conversation.id)"
          >
            <span
              v-if="nombreMessagesNonLus(conversation) > 0"
              class="conversations__unread-dot"
              aria-label="Message non lu"
            />
            <span class="conversations__item-body">
              <span
                class="conversations__item-poste"
                :class="{ 'conversations__item-poste--unread': nombreMessagesNonLus(conversation) > 0 }"
              >
                {{ conversation.poste }}
              </span>
              <span class="conversations__item-organisme">{{ conversation.organisme }}</span>
              <span class="conversations__item-preview">
                {{ conversation.messages.at(-1)?.texte }}
              </span>
            </span>
          </button>
        </li>
      </ul>

      <div
        v-if="selected"
        class="conversations__thread"
      >
        <header class="conversations__thread-header">
          <p class="conversations__thread-poste">
            {{ selected.poste }} — {{ selected.organisme }}
          </p>
          <p class="conversations__thread-recruteur">
            Recruteur : {{ selected.recruteurNom }}
          </p>
        </header>

        <div class="conversations__messages">
          <div
            v-for="message in selected.messages"
            :key="message.id"
            class="conversations__message"
            :class="`conversations__message--${message.auteur}`"
          >
            <p class="conversations__message-text">
              {{ message.texte }}
            </p>
            <p class="conversations__message-date">
              {{ message.date }}
            </p>
          </div>
        </div>

        <div class="conversations__reply">
          <CspTextarea
            v-model="brouillon"
            label="Votre réponse"
            :rows="3"
            placeholder="Écrivez votre message..."
          />
          <CspButton
            variant="primary"
            label="Envoyer"
            icon="ri:send-plane-2-line"
            class="conversations__reply-send"
            @click="envoyerReponse"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.conversations {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  height: 100%;
}

.conversations__title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.conversations__layout {
  display: grid;
  grid-template-columns: 18rem minmax(0, 1fr);
  gap: var(--csp-space-4);
  min-height: 28rem;
}

.conversations__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  border-radius: 0.375rem;
  background-color: var(--background-default-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  padding: var(--csp-space-2);
  height: fit-content;
}

.conversations__item {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-2);
  width: 100%;
  text-align: left;
  border: none;
  background: none;
  cursor: pointer;
  padding: var(--csp-space-3);
  border-radius: 0.25rem;
  font: inherit;

  &:hover {
    background-color: var(--background-alt-grey);
  }

  &--active {
    background-color: var(--background-alt-blue-france);
  }
}

.conversations__unread-dot {
  flex-shrink: 0;
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background-color: var(--background-action-high-blue-france);
  margin-top: 0.375rem;
}

.conversations__item-body {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.conversations__item-poste {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-default-grey);

  &--unread {
    font-weight: 700;
    color: var(--text-title-grey);
  }
}

.conversations__item-organisme {
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.conversations__item-preview {
  margin-top: 0.125rem;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conversations__thread {
  display: flex;
  flex-direction: column;
  border-radius: 0.375rem;
  background-color: var(--background-default-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  padding: var(--csp-space-5);
  gap: var(--csp-space-4);
}

.conversations__thread-header {
  padding-bottom: var(--csp-space-3);
  border-bottom: 1px solid var(--border-default-grey);
}

.conversations__thread-poste {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.conversations__thread-recruteur {
  margin: 0.125rem 0 0;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.conversations__messages {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  flex: 1;
}

.conversations__message {
  max-width: 26rem;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-radius: 0.5rem;
  background-color: var(--background-alt-grey);

  &--candidat {
    align-self: flex-end;
    background-color: var(--background-alt-blue-france);
  }
}

.conversations__message-text {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--text-default-grey);
}

.conversations__message-date {
  margin: 0.25rem 0 0;
  font-size: 0.6875rem;
  color: var(--text-mention-grey);
}

.conversations__reply {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  padding-top: var(--csp-space-3);
  border-top: 1px solid var(--border-default-grey);
}

.conversations__reply-send {
  align-self: flex-end;
}
</style>
