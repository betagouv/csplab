<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'

function keepOpen() {}

function preventAutoFocus(event: Event) {
  event.preventDefault()
}
</script>

<template>
  <div class="ecarts-modales">
    <CspDialog
      class="ecarts-modales__dialog"
      :open="true"
      :modal="false"
      size="sm"
      title="Supprimer le fichier ?"
      description="Le fichier sera supprimé définitivement."
      @update:open="keepOpen"
      @open-auto-focus="preventAutoFocus"
    >
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
        />
        <CspButton label="Supprimer" />
      </template>
    </CspDialog>

    <CspDrawer
      :open="true"
      :modal="false"
      :overlay="false"
      side="right"
      size="xs"
      title="Filtres"
      @update:open="keepOpen"
      @open-auto-focus="preventAutoFocus"
    >
      <p class="ecarts-modales__text">
        Aucun filtre actif.
      </p>
    </CspDrawer>
  </div>
</template>

<style scoped lang="scss">
.ecarts-modales {
  min-height: 100vh;
}

.ecarts-modales__text {
  margin: 0;
  color: var(--text-default-grey);
  font-size: var(--csp-font-size-sm);
}
</style>
