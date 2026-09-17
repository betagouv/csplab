<script setup lang="ts">
import MobileTopBar from '../../shared/mobile/MobileTopBar.vue'
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'

defineEmits<{
  retour: []
}>()
</script>

<template>
  <div class="profil">
    <MobileTopBar
      title="Profil"
      show-back
      @back="$emit('retour')"
    />

    <div class="profil__content">
      <CspAvatar
        name="Camille Rousseau"
        size="lg"
      />
      <p class="profil__nom">
        Camille Rousseau
      </p>
      <p class="profil__email">
        camille.rousseau@example.com
      </p>
      <CspButton
        variant="secondary"
        label="Se déconnecter"
        icon="ri:logout-box-line"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.profil {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.profil__content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--csp-space-2);
  padding: var(--csp-space-8) var(--csp-space-4);
  text-align: center;
}

.profil__nom {
  margin: var(--csp-space-2) 0 0;
  font-size: 1.0625rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.profil__email {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}
</style>
