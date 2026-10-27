<script setup lang="ts">
import type { Fiche, Offre } from './store'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import FieldRow from '../../shared/FieldRow.vue'
import Panel from '../../shared/Panel.vue'
import ChampOffre from './ChampOffre.vue'
import { MOTIFS_DEPART, MOTIFS_RECRUTEMENT } from './store'

// Étape 1 — informations internes : propres à l'organisme et au recrutement, jamais publiées.
// Ce sont des données de contexte : elles ne sont jamais reprises d'une fiche ni d'une offre dupliquée.
const props = defineProps<{ offre: Offre, fiche: Fiche }>()
const o = computed(() => props.offre)

const opts = (l: string[]) => [{ value: 'aucun', label: 'Non renseigné' }, ...l.map(v => ({ value: v, label: v }))]
function modele(cle: 'motifRecrutement' | 'motifDepart' | 'groupeRifseep') {
  return computed({
    get: () => o.value[cle] || 'aucun',
    set: (v: string) => (o.value[cle] = v === 'aucun' ? '' : v),
  })
}
const motif = modele('motifRecrutement')
const depart = modele('motifDepart')
const rifseep = modele('groupeRifseep')
const avecAgent = computed(() => ['Remplacement', 'Renouvellement'].includes(o.value.motifRecrutement))

function joindre(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0]
  if (f) {
    o.value.ficheJointe = f.name
  }
}
</script>

<template>
  <p class="note">
    <CspIcon
      name="ri:lock-line"
      :size="14"
    />
    Ces informations ne sont jamais publiées. Elles ne sont pas reprises si l'offre est dupliquée.
  </p>

  <Panel titre="Le recrutement">
    <FieldRow :cols="3">
      <CspInput
        v-model="o.referenceInterne"
        label="Référence interne (facultatif)"
      />
      <CspInput
        v-model="o.codePoste"
        label="Code poste (facultatif)"
      />
      <CspInput
        v-model="o.nbPostes"
        type="number"
        label="Nombre de postes"
        hint="Une offre peut couvrir plusieurs postes identiques."
      />
    </FieldRow>
    <FieldRow :cols="2">
      <CspSelect
        v-model="motif"
        label="Motif de recrutement (facultatif)"
        :options="opts(MOTIFS_RECRUTEMENT)"
      />
      <CspSelect
        v-model="depart"
        label="Motif de départ (facultatif)"
        :options="opts(MOTIFS_DEPART)"
      />
    </FieldRow>
    <CspInput
      v-if="avecAgent"
      v-model="o.agentRemplace"
      label="Agent remplacé ou renouvelé (facultatif)"
      hint="Donnée personnelle : elle reste interne."
    />
  </Panel>

  <Panel titre="Rémunération et temps de travail">
    <FieldRow :cols="2">
      <CspSelect
        v-model="rifseep"
        label="Groupe RIFSEEP (facultatif)"
        :options="opts(['Groupe 1', 'Groupe 2', 'Groupe 3', 'Groupe 4'])"
      />
      <ChampOffre
        :offre="o"
        champ="cycleTravail"
        label="Cycle de travail (facultatif)"
        for-id="i-cycle"
      >
        <CspInput
          id="i-cycle"
          v-model="o.cycleTravail"
          placeholder="Ex. : 38 h 30 sur 5 jours"
        />
      </ChampOffre>
    </FieldRow>
    <p class="mention">
      L'organisme peut reprendre le groupe RIFSEEP dans la rémunération de l'annonce s'il le souhaite.
    </p>
  </Panel>

  <Panel titre="Pour les valideurs">
    <ChampOffre
      :offre="o"
      champ="commentaireValideurs"
      label="Commentaire pour les valideurs (facultatif)"
      for-id="i-comm"
    >
      <CspTextarea
        id="i-comm"
        v-model="o.commentaireValideurs"
        :rows="3"
      />
    </ChampOffre>
    <div class="jointe">
      <p class="mention">
        Fiche de poste : <strong>{{ fiche.intitule }}</strong> ({{ fiche.id }})<template v-if="o.ficheJointe">
          · document joint : {{ o.ficheJointe }}
        </template>
      </p>
      <label class="ajout">
        <CspIcon
          name="ri:attachment-2"
          :size="14"
        /> {{ o.ficheJointe ? 'Remplacer le document joint' : 'Joindre la fiche de poste existante (facultatif)' }}
        <input
          type="file"
          class="sr-only"
          @change="joindre"
        >
      </label>
    </div>
  </Panel>
</template>

<style scoped lang="scss">
.note {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-grey);
  background: var(--background-alt-grey);
  font-size: var(--csp-font-size-sm);
}

.mention {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.jointe {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.ajout {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-sm);
  color: var(--text-action-high-blue-france);
  cursor: pointer;

  &:has(:focus-visible) {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
  }
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
