<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspSwitch from '@/components/base/CspSwitch/CspSwitch.vue'
import Panel from '../../shared/Panel.vue'
import SimulationNote from '../../shared/SimulationNote.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { appliquerParametreDar, db, ENTITES, sauvegarder, TYPES_DAR } from './store'

// Paramètres de l'organisme (simulés) : administrés par le superviseur. La nécessité d'une DAR est définie
// ici pour tout l'organisme ; le parcours de chaque offre s'adapte. Le responsable du recrutement consulte seulement.
const { notifier } = useNav()

function changerRole() {
  db.role = db.role === 'superviseur' ? 'recruteur' : 'superviseur'
  sauvegarder()
  notifier(db.role === 'superviseur' ? `Vous agissez en tant que superviseur (${db.organisme.superviseur}).` : 'Retour au profil responsable du recrutement.')
}

function basculerDar(v: boolean) {
  db.organisme.darObligatoire = v
  appliquerParametreDar()
  notifier(v ? 'Les recrutements passent désormais par une DAR.' : 'Les recrutements ne passent plus par une DAR.')
}
</script>

<template>
  <PageAts
    actif="parametres"
    titre="Paramètres de l'organisme"
    :sous-titre="`${db.organisme.nom} · administrés par le superviseur, ${db.organisme.superviseur}`"
  >
    <template #actions>
      <SimulationNote titre="Profil">
        <span class="profil">{{ db.role === 'superviseur' ? `Superviseur (${db.organisme.superviseur})` : 'Responsable du recrutement (Camille Moreau)' }}</span>
        <CspButton
          :label="db.role === 'superviseur' ? 'Revenir en responsable du recrutement' : 'Agir en tant que superviseur'"
          size="sm"
          variant="tertiary"
          @click="changerRole"
        />
      </SimulationNote>
    </template>
    <p
      v-if="db.role !== 'superviseur'"
      class="lecture"
    >
      <CspIcon
        name="ri:lock-line"
        :size="16"
      />
      Ces paramètres sont définis par le superviseur de l'organisme. Vous pouvez les consulter.
    </p>
    <Panel
      titre="Demande d'autorisation de recrutement (DAR)"
      description="Défini par l'organisme pour tous ses recrutements. Le parcours de création des offres s'adapte automatiquement."
    >
      <CspSwitch
        :model-value="db.organisme.darObligatoire"
        label="Les recrutements de l'organisme passent par une DAR"
        :disabled="db.role !== 'superviseur'"
        @update:model-value="basculerDar"
      />
      <div class="parcours">
        <p class="parcours__titre">
          Parcours appliqué aux offres
        </p>
        <ol class="parcours__etapes">
          <li>Rédaction</li>
          <li :class="{ barre: !db.organisme.darObligatoire }">
            DAR : saisie, enregistrement, validation
          </li>
          <li>Préparation (postes, modalités)</li>
          <li>Publication</li>
        </ol>
      </div>
      <template v-if="db.organisme.darObligatoire">
        <CspSelect
          v-model="db.organisme.entite"
          label="Entité préremplie dans les DAR"
          :options="ENTITES.map(e => ({ value: e, label: e }))"
          :disabled="db.role !== 'superviseur'"
          @update:model-value="sauvegarder"
        />
        <CspSelect
          v-model="db.organisme.typeDar"
          label="Type de DAR"
          :options="TYPES_DAR.map(t => ({ value: t, label: t }))"
          :disabled="db.role !== 'superviseur'"
          @update:model-value="sauvegarder"
        />
        <p class="mention">
          <CspIcon
            name="ri:user-line"
            :size="14"
          />
          Validation des DAR : {{ db.organisme.valideur }} (simulation).
        </p>
      </template>
      <p class="mention">
        Paramètre commun à tout l'organisme dans un premier temps. Hypothèse : un changement s'applique aux nouvelles offres et à celles en rédaction dont la DAR n'est pas encore soumise.
      </p>
    </Panel>
  </PageAts>
</template>

<style scoped lang="scss">
.lecture {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-blue-france);
  background: var(--background-default-grey);
  font-size: var(--csp-font-size-sm);
}

.profil {
  font-size: var(--csp-font-size-sm);
}

.parcours {
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-alt-grey);
}

.parcours__titre {
  margin: 0 0 var(--csp-space-2);
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.parcours__etapes {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: var(--csp-font-size-sm);

  li {
    padding: var(--csp-space-1) var(--csp-space-3);
    border: 1px solid var(--border-default-grey);
    background: var(--background-default-grey);
  }

  li + li::before {
    content: '→ ';
    color: var(--text-mention-grey);
  }
}

.barre {
  text-decoration: line-through;
  color: var(--text-mention-grey);
}

.mention {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}
</style>
