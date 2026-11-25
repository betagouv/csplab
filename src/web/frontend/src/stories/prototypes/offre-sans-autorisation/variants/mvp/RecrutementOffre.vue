<script setup lang="ts">
import { computed } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import Panel from '../../shared/Panel.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { candidatures } from './recrutement'
import { dateLongue, db } from './store'
import { referenceCsp } from './suivi'

// Le recrutement créé par la publication d'une offre. Écran simplifié pour le proto : dans l'outil, c'est l'écran
// existant du recrutement (candidatures, étapes, équipe) qui s'ouvre.
const props = defineProps<{ id: string }>()
const { aller } = useNav()
const o = computed(() => db.offres.find(x => x.id === props.id)!)
const n = computed(() => candidatures(o.value).total)
const meta = computed(() => [
  { icon: 'ri:price-tag-3-line', srLabel: 'Référence CSP', label: `Réf. CSP ${referenceCsp(o.value)}` },
  { icon: 'ri:calendar-line', srLabel: 'Publication', label: o.value.etat === 'publiee' ? `Offre en ligne jusqu'au ${dateLongue(o.value.dateFin)}` : 'Offre retirée' },
  { icon: 'ri:map-pin-2-line', srLabel: 'Lieu', label: o.value.lieu || 'Lieu à préciser' },
])
</script>

<template>
  <PageAts
    actif="recrutements"
    largeur="full"
    :titre="o.titre"
    :fil="[{ label: 'Mes recrutements', to: '/recrutements' }, { label: o.titre }]"
    :retour="{ to: '/recrutements', label: 'Retour à mes recrutements' }"
  >
    <template #meta>
      <div class="meta">
        <CspBadge
          label="En cours"
          type="success"
          size="sm"
        />
        <CspMetaList :items="meta" />
      </div>
    </template>
    <template #actions>
      <CspButton
        label="Voir l'offre"
        size="sm"
        variant="secondary"
        icon="ri:file-list-3-line"
        is-icon-left
        @click="aller({ nom: 'offre', id: o.id })"
      />
    </template>

    <p class="proto">
      <CspIcon
        name="ri:information-line"
        :size="16"
      />
      Écran simplifié pour le prototype : dans l'outil, c'est l'écran existant du recrutement qui s'ouvre.
    </p>

    <Panel :titre="`Candidatures (${n})`">
      <div
        v-if="!n"
        class="vide"
      >
        <CspIcon
          name="ri:inbox-2-line"
          :size="32"
        />
        <p>Aucune candidature pour l'instant. Elles arriveront ici dès que des candidats postuleront.</p>
      </div>
      <p
        v-else
        class="texte"
      >
        {{ n }} candidature{{ n > 1 ? 's' : '' }} reçue{{ n > 1 ? 's' : '' }} (données fictives).
      </p>
    </Panel>
  </PageAts>
</template>

<style scoped lang="scss">
.meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-3);
}

.proto {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.vide {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--csp-space-2);
  padding: var(--csp-space-8) 0;
  color: var(--text-mention-grey);
  text-align: center;

  p {
    margin: 0;
  }
}

.texte {
  margin: 0;
}
</style>
