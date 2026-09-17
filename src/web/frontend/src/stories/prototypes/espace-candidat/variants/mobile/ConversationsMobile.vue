<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { actionsRequises, conversations, nombreMessagesNonLus } from '../../data/candidatMock'
import MobileTopBar from '../../shared/mobile/MobileTopBar.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'

const props = defineProps<{
  initialConversationId?: string | null
}>()

const selectedId = ref<string | null>(props.initialConversationId ?? null)

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
</script>

<template>
  <div
    v-if="selected"
    class="thread"
  >
    <MobileTopBar
      :title="selected.poste"
      show-back
      @back="selectedId = null"
    />

    <div class="thread__messages">
      <p class="thread__recruteur">
        Recruteur : {{ selected.recruteurNom }}
      </p>
      <div
        v-for="message in selected.messages"
        :key="message.id"
        class="thread__message"
        :class="`thread__message--${message.auteur}`"
      >
        <p class="thread__message-texte">
          {{ message.texte }}
        </p>
        <p class="thread__message-date">
          {{ message.date }}
        </p>
      </div>
    </div>

    <div class="thread__reply">
      <CspTextarea
        v-model="brouillon"
        label="Votre réponse"
        :rows="2"
        placeholder="Écrivez votre message..."
      />
      <CspButton
        variant="primary"
        label="Envoyer"
        icon="ri:send-plane-2-line"
        class="thread__reply-send"
        @click="envoyerReponse"
      />
    </div>
  </div>

  <div
    v-else
    class="liste"
  >
    <MobileTopBar title="Messages" />

    <ul class="liste__items">
      <li
        v-for="conversation in conversations"
        :key="conversation.id"
      >
        <button
          type="button"
          class="liste__item"
          @click="selectedId = conversation.id"
        >
          <span
            v-if="nombreMessagesNonLus(conversation) > 0"
            class="liste__unread-dot"
            aria-label="Message non lu"
          />
          <span class="liste__item-body">
            <span
              class="liste__item-poste"
              :class="{ 'liste__item-poste--unread': nombreMessagesNonLus(conversation) > 0 }"
            >
              {{ conversation.poste }}
            </span>
            <span class="liste__item-organisme">{{ conversation.organisme }}</span>
            <span class="liste__item-preview">{{ conversation.messages.at(-1)?.texte }}</span>
          </span>
          <CspIcon
            name="ri:arrow-right-s-line"
            :size="20"
            class="liste__item-chevron"
          />
        </button>
      </li>
    </ul>
  </div>
</template>

<style scoped lang="scss">
.liste,
.thread {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.liste__items {
  list-style: none;
  margin: 0;
  padding: var(--csp-space-2);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
}

.liste__item {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-2);
  width: 100%;
  text-align: left;
  border: none;
  background: none;
  cursor: pointer;
  padding: var(--csp-space-3);
  border-radius: 0.5rem;
  font: inherit;
  min-height: 3.5rem;

  &:active {
    background-color: var(--background-alt-grey);
  }
}

.liste__unread-dot {
  flex-shrink: 0;
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background-color: var(--background-action-high-blue-france);
  margin-top: 0.375rem;
}

.liste__item-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  padding-right: var(--csp-space-6);
}

.liste__item-poste {
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--text-default-grey);

  &--unread {
    font-weight: 700;
    color: var(--text-title-grey);
  }
}

.liste__item-organisme {
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.liste__item-preview {
  margin-top: 0.125rem;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.liste__item-chevron {
  position: absolute;
  right: var(--csp-space-3);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-mention-grey);
}

.thread__messages {
  flex: 1;
  padding: var(--csp-space-4);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.thread__recruteur {
  margin: 0 0 var(--csp-space-2);
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.thread__message {
  max-width: 85%;
  padding: var(--csp-space-3);
  border-radius: 0.75rem;
  background-color: var(--background-alt-grey);

  &--candidat {
    align-self: flex-end;
    background-color: var(--background-alt-blue-france);
  }
}

.thread__message-texte {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--text-default-grey);
}

.thread__message-date {
  margin: 0.25rem 0 0;
  font-size: 0.6875rem;
  color: var(--text-mention-grey);
}

.thread__reply {
  position: sticky;
  bottom: 0;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  padding: var(--csp-space-3) var(--csp-space-4) max(var(--csp-space-3), env(safe-area-inset-bottom));
  background-color: var(--background-default-grey);
  box-shadow: inset 0 1px 0 var(--border-default-grey);
}

.thread__reply-send {
  width: 100%;
  justify-content: center;
}
</style>
