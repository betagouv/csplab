<script setup lang="ts">
import type { PieceJointe } from '../../data/espaceMock'
import { computed, nextTick, onMounted, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { formaterDateHeure } from '../../data/format'
import { useEspace } from '../../data/useEspace'
import MobileBottomSheet from '../../shared/mobile/MobileBottomSheet.vue'
import RetourLien from '../../shared/mobile/RetourLien.vue'

const props = defineProps<{
  candidatureId: string
  conversationId: string
}>()

defineEmits<{
  retour: []
}>()

const FORMATS_ACCEPTES = ['pdf', 'doc', 'docx', 'odt', 'jpg', 'jpeg', 'png']
const FORMATS_IMAGE = ['jpg', 'jpeg', 'png']

const espace = useEspace()
const candidature = computed(() => espace.candidature(props.candidatureId))
const conversation = computed(() =>
  candidature.value?.conversations.find(c => c.id === props.conversationId),
)

const texte = ref('')
const pieces = ref<PieceJointe[]>([])
const erreurFormat = ref('')
const envoi = ref<'repos' | 'envoi' | 'echec'>('repos')
const sourcesOuvertes = ref(false)
let echecDejaSimule = false
let compteurPieces = 0

const inputPhoto = ref<HTMLInputElement>()
const inputPhototheque = ref<HTMLInputElement>()
const inputFichiers = ref<HTMLInputElement>()

const peutEnvoyer = computed(() =>
  (texte.value.trim().length > 0 || pieces.value.length > 0) && envoi.value !== 'envoi',
)

function defilerVersLeBas(comportement: ScrollBehavior = 'auto') {
  window.scrollTo({ top: document.documentElement.scrollHeight, behavior: comportement })
}

onMounted(async () => {
  espace.marquerConversationLue(props.candidatureId, props.conversationId)
  await nextTick()
  defilerVersLeBas()
})

function choisirSource(input: HTMLInputElement | undefined) {
  input?.click()
  sourcesOuvertes.value = false
}

function surFichiersChoisis(event: Event) {
  const input = event.target as HTMLInputElement
  erreurFormat.value = ''
  for (const fichier of Array.from(input.files ?? [])) {
    const extension = fichier.name.split('.').pop()?.toLowerCase() ?? ''
    if (!FORMATS_ACCEPTES.includes(extension)) {
      erreurFormat.value = `Format non accepté : ${fichier.name}. Formats acceptés : PDF, DOC, DOCX, ODT, JPG, PNG.`
      continue
    }
    const estImage = FORMATS_IMAGE.includes(extension)
    pieces.value.push({
      id: `pj-${++compteurPieces}`,
      nom: fichier.name,
      type: estImage ? 'image' : 'document',
      url: estImage ? URL.createObjectURL(fichier) : undefined,
    })
  }
  input.value = ''
}

function retirerPiece(id: string) {
  pieces.value = pieces.value.filter(p => p.id !== id)
}

async function envoyer() {
  if (!peutEnvoyer.value) {
    return
  }
  erreurFormat.value = ''
  envoi.value = 'envoi'
  await new Promise(resolve => setTimeout(resolve, 700))

  if (espace.options.simulerEchecEnvoi && !echecDejaSimule) {
    echecDejaSimule = true
    envoi.value = 'echec'
    return
  }

  espace.envoyerMessage(props.candidatureId, props.conversationId, texte.value.trim(), pieces.value)
  texte.value = ''
  pieces.value = []
  envoi.value = 'repos'
  await nextTick()
  defilerVersLeBas('smooth')
}
</script>

<template>
  <div
    v-if="conversation && candidature"
    class="conversation"
  >
    <div class="conversation__entete">
      <RetourLien
        :label="candidature.intitule"
        @retour="$emit('retour')"
      />
      <h1 class="conversation__sujet">
        {{ conversation.sujet }}
      </h1>
      <p class="conversation__organisme">
        {{ candidature.organisme }}
      </p>
    </div>

    <ol class="fil">
      <li
        v-for="message in conversation.messages"
        :key="message.id"
        class="message"
        :class="`message--${message.auteur}`"
      >
        <p class="message__auteur">
          {{ message.auteur === 'candidat' ? 'Vous' : message.auteurNom }}
        </p>
        <div class="message__bulle">
          <p
            v-if="message.texte"
            class="message__texte"
          >
            {{ message.texte }}
          </p>
          <ul
            v-if="message.pieces.length > 0"
            class="message__pieces"
          >
            <li
              v-for="piece in message.pieces"
              :key="piece.id"
            >
              <img
                v-if="piece.url"
                :src="piece.url"
                :alt="piece.nom"
                class="message__vignette"
              >
              <span
                v-else
                class="message__fichier"
              >
                <CspIcon
                  name="ri:file-text-line"
                  :size="18"
                />
                {{ piece.nom }}
              </span>
            </li>
          </ul>
        </div>
        <p class="message__date">
          {{ formaterDateHeure(message.date) }}
        </p>
      </li>
    </ol>

    <form
      class="reponse"
      @submit.prevent="envoyer"
    >
      <CspCallout
        v-if="erreurFormat"
        variant="warning"
        :description="erreurFormat"
      />
      <CspCallout
        v-if="envoi === 'echec'"
        variant="error"
        title="Votre message n'a pas pu être envoyé"
        description="Votre texte et vos pièces jointes sont conservés."
      />

      <ul
        v-if="pieces.length > 0"
        class="apercus"
      >
        <li
          v-for="piece in pieces"
          :key="piece.id"
          class="apercu"
        >
          <img
            v-if="piece.url"
            :src="piece.url"
            :alt="piece.nom"
            class="apercu__image"
          >
          <span
            v-else
            class="apercu__fichier"
          >
            <CspIcon
              name="ri:file-text-line"
              :size="20"
            />
          </span>
          <span class="apercu__nom">{{ piece.nom }}</span>
          <button
            type="button"
            class="apercu__retirer"
            :aria-label="`Retirer ${piece.nom}`"
            @click="retirerPiece(piece.id)"
          >
            <CspIcon
              name="ri:close-line"
              :size="18"
            />
          </button>
        </li>
      </ul>

      <CspTextarea
        v-model="texte"
        label="Votre réponse"
        :rows="2"
        placeholder="Écrivez votre message…"
      />

      <div class="reponse__actions">
        <CspButton
          variant="secondary"
          size="lg"
          icon="ri:attachment-2"
          is-icon-left
          label="Joindre"
          class="reponse__joindre"
          @click="sourcesOuvertes = true"
        />
        <CspButton
          type="submit"
          variant="primary"
          size="lg"
          :icon="envoi === 'echec' ? 'ri:refresh-line' : 'ri:send-plane-2-line'"
          is-icon-left
          :label="envoi === 'envoi' ? 'Envoi…' : envoi === 'echec' ? 'Réessayer' : 'Envoyer'"
          :disabled="!peutEnvoyer"
          class="reponse__envoyer"
        />
      </div>
    </form>

    <MobileBottomSheet
      v-model:open="sourcesOuvertes"
      title="Joindre un fichier"
      description="PDF, DOC, DOCX, ODT, JPG ou PNG."
    >
      <button
        type="button"
        class="source"
        @click="choisirSource(inputPhoto)"
      >
        <CspIcon
          name="ri:camera-line"
          :size="22"
        />
        Prendre une photo
      </button>
      <button
        type="button"
        class="source"
        @click="choisirSource(inputPhototheque)"
      >
        <CspIcon
          name="ri:image-line"
          :size="22"
        />
        Photothèque
      </button>
      <button
        type="button"
        class="source"
        @click="choisirSource(inputFichiers)"
      >
        <CspIcon
          name="ri:folder-open-line"
          :size="22"
        />
        Fichiers
      </button>
    </MobileBottomSheet>

    <input
      ref="inputPhoto"
      type="file"
      accept="image/*"
      capture="environment"
      class="champ-fichier"
      tabindex="-1"
      @change="surFichiersChoisis"
    >
    <input
      ref="inputPhototheque"
      type="file"
      accept=".jpg,.jpeg,.png,image/jpeg,image/png"
      multiple
      class="champ-fichier"
      tabindex="-1"
      @change="surFichiersChoisis"
    >
    <input
      ref="inputFichiers"
      type="file"
      accept=".pdf,.doc,.docx,.odt,.jpg,.jpeg,.png"
      multiple
      class="champ-fichier"
      tabindex="-1"
      @change="surFichiersChoisis"
    >
  </div>
</template>

<style scoped lang="scss">
.conversation {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.conversation__entete {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  padding: var(--csp-space-2) var(--csp-space-4) var(--csp-space-3);
  box-shadow: inset 0 -1px 0 var(--border-default-grey);
}

.conversation__sujet {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.conversation__organisme {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.fil {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  margin: 0;
  padding: var(--csp-space-4);
  list-style: none;
}

.message {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  max-width: 88%;

  &--candidat {
    align-self: flex-end;
    align-items: flex-end;
  }
}

.message__auteur {
  margin: 0;
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.message__bulle {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  padding: var(--csp-space-3) var(--csp-space-4);
  border-radius: 0.75rem;
  background-color: var(--background-alt-grey);
}

.message--candidat .message__bulle {
  background-color: var(--background-alt-blue-france);
}

.message__texte {
  margin: 0;
  font-size: 0.9375rem;
  line-height: 1.5;
  color: var(--text-default-grey);
  white-space: pre-line;
}

.message__pieces {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

.message__vignette {
  width: 6rem;
  height: 6rem;
  border-radius: 0.5rem;
  object-fit: cover;
}

.message__fichier {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-2);
  padding: var(--csp-space-2) var(--csp-space-3);
  border-radius: 0.5rem;
  background-color: var(--background-default-grey);
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--text-action-high-blue-france);
}

.message__date {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.reponse {
  position: sticky;
  bottom: 0;
  z-index: 5;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4) max(var(--csp-space-3), env(safe-area-inset-bottom));
  background-color: var(--background-default-grey);
  box-shadow:
    inset 0 1px 0 var(--border-default-grey),
    0 -2px 8px rgb(0 0 0 / 6%);
}

.apercus {
  display: flex;
  gap: var(--csp-space-2);
  margin: 0;
  padding: var(--csp-space-2) var(--csp-space-1) var(--csp-space-1) 0;
  list-style: none;
  overflow-x: auto;
}

.apercu {
  position: relative;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--csp-space-1);
  width: 5rem;
}

.apercu__image,
.apercu__fichier {
  width: 4.5rem;
  height: 4.5rem;
  border-radius: 0.5rem;
  object-fit: cover;
  background-color: var(--background-alt-grey);
}

.apercu__fichier {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-action-high-blue-france);
}

.apercu__nom {
  max-width: 100%;
  font-size: 0.6875rem;
  color: var(--text-mention-grey);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.apercu__retirer {
  position: absolute;
  top: -0.375rem;
  right: -0.125rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.75rem;
  height: 1.75rem;
  border: none;
  border-radius: 50%;
  background-color: var(--background-flat-grey);
  color: var(--text-inverted-grey);
  cursor: pointer;
}

.reponse__actions {
  display: flex;
  gap: var(--csp-space-3);
}

.reponse__joindre {
  flex-shrink: 0;
  min-height: 3rem;
}

.reponse__envoyer {
  flex: 1;
  justify-content: center;
  min-height: 3rem;
}

.source {
  display: flex;
  align-items: center;
  gap: var(--csp-space-4);
  width: 100%;
  min-height: 3.5rem;
  padding: 0 var(--csp-space-4);
  border: none;
  border-radius: 0.5rem;
  background-color: var(--background-alt-grey);
  cursor: pointer;
  font: inherit;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-title-grey);
}

.champ-fichier {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  opacity: 0;
  pointer-events: none;
}
</style>
