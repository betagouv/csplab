<script setup lang="ts">
import type { Offre } from '../../data/candidatMock'
import ConfettiBurst from '../../shared/mobile/ConfettiBurst.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

defineProps<{
  open: boolean
  offre: Offre
}>()

defineEmits<{
  close: []
  creerCompte: []
}>()
</script>

<template>
  <CspDialog
    :open="open"
    size="sm"
    close-label="Fermer"
    @update:open="(value) => !value && $emit('close')"
  >
    <ConfettiBurst v-if="open" />

    <div class="succes">
      <span class="succes__icon">
        <CspIcon
          name="ri:checkbox-circle-fill"
          :size="30"
        />
      </span>

      <h1 class="succes__titre">
        Candidature envoyée !
      </h1>

      <p class="succes__texte">
        Votre candidature a bien été transmise à <strong>{{ offre.organisme }}</strong>.
      </p>
      <p class="succes__texte succes__texte--accent">
        Vous recevrez un email dès qu'il y aura une suite à votre candidature.
      </p>

      <div class="succes__upsell">
        <p class="succes__upsell-titre">
          Envie de retrouver toutes vos candidatures au même endroit ?
        </p>
        <p class="succes__upsell-texte">
          Vous pouvez créer gratuitement votre espace candidat pour suivre vos candidatures et
          retrouver vos échanges. Ce n'est pas obligatoire : vous recevrez dans tous les cas un
          email si votre candidature évolue.
        </p>
        <CspButton
          variant="secondary"
          size="sm"
          label="Créer mon espace candidat"
          class="succes__upsell-cta"
          @click="$emit('creerCompte')"
        />
      </div>

      <button
        type="button"
        class="succes__continuer"
        @click="$emit('close')"
      >
        Terminer et retourner sur l'offre
      </button>
    </div>
  </CspDialog>
</template>

<style scoped lang="scss">
.succes {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--csp-space-2);
}

.succes__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 50%;
  background-color: var(--background-contrast-success);
  color: var(--text-default-success);
  margin-bottom: var(--csp-space-1);
}

.succes__titre {
  margin: 0;
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.succes__texte {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-default-grey);
  line-height: 1.5;
}

.succes__texte--accent {
  font-weight: 600;
}

.succes__upsell {
  width: 100%;
  margin-top: var(--csp-space-4);
  padding: var(--csp-space-4);
  border-radius: 0.5rem;
  background-color: var(--background-alt-grey);
  text-align: left;
}

.succes__upsell-titre {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.succes__upsell-texte {
  margin: var(--csp-space-1) 0 var(--csp-space-3);
  font-size: 0.8125rem;
  line-height: 1.5;
  color: var(--text-mention-grey);
}

.succes__upsell-cta {
  width: 100%;
  justify-content: center;
}

.succes__continuer {
  margin-top: var(--csp-space-3);
  border: none;
  background: none;
  cursor: pointer;
  padding: var(--csp-space-2);
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--text-mention-grey);
  text-decoration: underline;
}
</style>
