<script setup lang="ts">
import type { ProtoCandidature, ProtoEtape } from '../data/mock'
import type { CspMetaItem } from '@/components/base/CspMeta/types'
import { computed } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import { CATEGORIE_CONFIG } from '@/features/etapes-recrutement/constants/etape-recrutement'
import { formatElapsedDays } from '@/utils/date'
import { INTITULE_OFFRE } from '../data/mock'
import { formatCandidatNom } from '../shared/format'

const props = defineProps<{
  candidature: ProtoCandidature
  etapeCourante: ProtoEtape | null
  etapes: ProtoEtape[]
}>()

const emit = defineEmits<{
  close: []
  changerEtape: [etapeUuid: string]
  copierLien: []
}>()

const nom = computed(() => formatCandidatNom(props.candidature.candidat))

const meta = computed<CspMetaItem[]>(() => {
  const { candidat, dateSoumission } = props.candidature
  return [
    { icon: 'ri:calendar-line', srLabel: 'Date de candidature', label: `Candidature ${formatElapsedDays(dateSoumission)}` },
    { icon: 'ri:map-pin-2-line', srLabel: 'Localisation', label: candidat.localisation ?? '' },
    { icon: 'ri:mail-line', srLabel: 'Courriel', label: candidat.email },
    { icon: 'ri:phone-line', srLabel: 'Téléphone', label: candidat.telephone ?? '' },
  ]
})

const etapeSections = computed(() => [{
  items: props.etapes.map(etape => ({
    label: etape.uuid === props.etapeCourante?.uuid ? `${etape.nom} (étape actuelle)` : etape.nom,
    icon: etape.categorie === 'REFUS' || etape.categorie === 'ACCEPTE' ? CATEGORIE_CONFIG[etape.categorie].icon : undefined,
    disabled: etape.uuid === props.etapeCourante?.uuid,
    onSelect: () => emit('changerEtape', etape.uuid),
  })),
}])

const moreSections = [{
  items: [
    { label: 'Copier le lien de la candidature', icon: 'ri:link', onSelect: () => emit('copierLien') },
    { label: 'Envoyer un message', icon: 'ri:chat-3-line', disabled: true },
  ],
}]
</script>

<template>
  <div class="panel-header">
    <CspButton
      variant="tertiary-no-outline"
      size="sm"
      icon="ri:arrow-left-line"
      aria-label="Fermer le panneau et revenir au kanban"
      class="panel-header__back"
      @click="emit('close')"
    />
    <div class="panel-header__identity">
      <div class="panel-header__name-row">
        <h2 class="panel-header__name">
          {{ nom }}
        </h2>
        <CspBadge
          v-if="etapeCourante"
          size="sm"
          :label="etapeCourante.nom"
          :type="CATEGORIE_CONFIG[etapeCourante.categorie].type"
          :icon="CATEGORIE_CONFIG[etapeCourante.categorie].icon"
        />
      </div>
      <p class="panel-header__offre">
        {{ INTITULE_OFFRE }}
      </p>
      <CspMetaList
        :items="meta"
        class="panel-header__meta"
      />
    </div>
    <div class="panel-header__actions">
      <CspDropdownMenu
        :sections="etapeSections"
        side="bottom"
        align="end"
      >
        <template #trigger>
          <CspButton
            label="Changer d'étape"
            icon="ri:arrow-left-right-line"
            is-icon-left
            size="sm"
          />
        </template>
      </CspDropdownMenu>
      <CspButton
        variant="tertiary"
        size="sm"
        icon="ri:link"
        aria-label="Copier le lien de la candidature"
        @click="emit('copierLien')"
      />
      <CspDropdownMenu
        :sections="moreSections"
        side="bottom"
        align="end"
      >
        <template #trigger>
          <CspButton
            variant="tertiary"
            size="sm"
            icon="ri:more-fill"
            aria-label="Autres actions"
          />
        </template>
      </CspDropdownMenu>
    </div>
  </div>
</template>

<style scoped lang="scss">
.panel-header {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-3);
  width: 100%;
  font-weight: var(--csp-font-weight-regular);
}

.panel-header__back {
  flex-shrink: 0;
  margin-top: var(--csp-space-1);
  margin-left: calc(-1 * var(--csp-space-2));
}

.panel-header__identity {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: var(--csp-space-1);
  min-width: 0;
}

.panel-header__name-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--csp-space-3);
  min-height: 2.5rem;
}

.panel-header__name {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  line-height: 1.25;
  color: var(--text-title-grey);
}

.panel-header__offre {
  margin: 0;
  font-size: 1rem;
  line-height: 1.5;
  color: var(--text-default-grey);
}

.panel-header__meta {
  margin-top: var(--csp-space-1);
}

.panel-header__actions {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  gap: var(--csp-space-2);
  margin-top: var(--csp-space-1);
}
</style>
