<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { actionsRequises, conversationParCandidature } from '../../data/candidatMock'
import MobileTopBar from '../../shared/mobile/MobileTopBar.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'

const props = defineProps<{
  candidatureId: string
}>()

defineEmits<{
  retour: []
}>()

const conversation = computed(() => conversationParCandidature(props.candidatureId))

watch(conversation, (conv) => {
  conv?.messages.forEach((m) => { m.lu = true })
}, { immediate: true })

const brouillon = ref('')

function envoyerReponse() {
  if (!conversation.value || !brouillon.value.trim()) {
    return
  }
  conversation.value.messages.push({
    id: `m-${Date.now()}`,
    auteur: 'candidat',
    texte: brouillon.value.trim(),
    date: 'À l\'instant',
    lu: true,
  })
  brouillon.value = ''

  const index = actionsRequises.findIndex(a => a.candidatureId === props.candidatureId && a.type === 'message')
  if (index !== -1) {
    actionsRequises.splice(index, 1)
  }
}
</script>

<template>
  <div
    v-if="conversation"
    class="thread"
  >
    <MobileTopBar
      :title="conversation.poste"
      show-back
      @back="$emit('retour')"
    />

    <div class="thread__messages">
      <p class="thread__recruteur">
        Recruteur : {{ conversation.recruteurNom }}
      </p>
      <div
        v-for="message in conversation.messages"
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
</template>

<style scoped lang="scss">
.thread {
  display: flex;
  flex-direction: column;
  min-height: 100%;
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
