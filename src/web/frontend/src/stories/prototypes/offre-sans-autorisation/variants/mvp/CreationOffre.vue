<script setup lang="ts">
import type { Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import Panel from '../../shared/Panel.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { db, le, nouvelleOffre } from './store'

// Créer une offre (MVP) : on choisit seulement entre formulaire vide et duplication (retour Alice) ; tout le reste
// se saisit dans les étapes du formulaire. Pas de fiche de poste (post-MVP).
// Le créateur devient Responsable. La duplication remet à zéro le nombre de postes (1), toutes les dates et
// les champs d'autorisation. La nouvelle offre démarre en brouillon.
type Mode = 'manuel' | 'duplication'
const props = defineProps<{ mode?: Mode, offreId?: string }>()
const { aller, notifier } = useNav()

const MODES: { id: Mode, titre: string, desc: string }[] = [
  { id: 'manuel', titre: 'Formulaire vide', desc: 'Saisissez l\'offre de toutes pièces.' },
  { id: 'duplication', titre: 'Dupliquer une offre existante', desc: 'Reprenez le contenu d\'une offre dans une nouvelle offre.' },
]
const mode = ref<Mode | null>(props.mode ?? (props.offreId ? 'duplication' : null))
const erreur = ref('')

const offreSource = ref<string | null>(props.offreId ?? null)
const offresReprenables = computed(() => db.offres.filter(o => o.etat !== 'archivee'))
const ETATS: Record<Offre['etat'], string> = { brouillon: 'Brouillon', publiee: 'Publiée', retiree: 'Dépubliée', archivee: 'Archivée' }

function creer() {
  erreur.value = ''
  if (!mode.value) {
    return
  }
  let source: Offre | undefined
  if (mode.value === 'duplication') {
    source = db.offres.find(o => o.id === offreSource.value)
    if (!source) {
      erreur.value = 'Choisissez l\'offre à dupliquer.'
      return
    }
  }
  const o = nouvelleOffre(undefined, mode.value, source)
  notifier(source ? `Offre ${o.id} créée par duplication. Nombre de postes, dates et champs d'autorisation remis à zéro.` : `Offre ${o.id} créée. Vous en êtes Responsable.`)
  aller({ nom: 'rediger', id: o.id })
}
</script>

<template>
  <PageAts
    actif="offres"
    titre="Créer une offre"
    sous-titre="Partez d'un formulaire vide ou d'une offre existante."
    :fil="[{ label: 'Mes offres d\'emploi', to: '/offres' }, { label: 'Créer une offre' }]"
    :retour="{ to: '/offres', label: 'Retour à mes offres d\'emploi' }"
  >
    <div
      class="modes"
      role="radiogroup"
      aria-label="Mode de création"
    >
      <label
        v-for="m in MODES"
        :key="m.id"
        class="mode"
        :class="{ 'mode--on': mode === m.id }"
      >
        <input
          v-model="mode"
          type="radio"
          name="mode"
          :value="m.id"
          class="mode__radio"
        >
        <strong class="mode__titre">{{ m.titre }}</strong>
        <span class="mode__desc">{{ m.desc }}</span>
      </label>
    </div>

    <Panel
      v-if="mode === 'duplication'"
      titre="Choisir l'offre à dupliquer"
      description="Le contenu est copié. Le nombre de postes revient à 1 ; les dates et les champs d'autorisation sont vidés."
    >
      <fieldset class="choix">
        <legend class="sr-only">
          Offre à dupliquer
        </legend>
        <label
          v-for="o in offresReprenables"
          :key="o.id"
          class="choix__ligne"
          :class="{ 'choix__ligne--on': offreSource === o.id }"
        >
          <input
            v-model="offreSource"
            type="radio"
            name="source"
            :value="o.id"
          >
          <span class="choix__corps">
            <strong>{{ o.titre || 'Sans titre' }}</strong>
            <small>{{ o.id }} · {{ ETATS[o.etat] }}{{ o.publieeLe ? ` · publiée ${le(o.publieeLe)}` : '' }}</small>
          </span>
        </label>
      </fieldset>
    </Panel>

    <div
      v-if="mode"
      class="final"
    >
      <div class="final__infos" />
      <div class="final__actions">
        <p
          v-if="erreur"
          class="final__err"
          role="alert"
        >
          {{ erreur }}
        </p>
        <CspButton
          label="Créer l'offre"
          icon="ri:arrow-right-line"
          @click="creer"
        />
      </div>
    </div>
  </PageAts>
</template>

<style scoped lang="scss">
.modes {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--csp-space-3);
}

.mode {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  cursor: pointer;

  &:hover {
    background: var(--background-default-grey-hover);
  }

  &:has(:focus-visible) {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
    outline-offset: 2px;
  }

  &--on {
    border-color: var(--border-active-blue-france);
    box-shadow: inset 0 0 0 1px var(--border-active-blue-france);
  }
}

.mode__radio {
  position: absolute;
  top: var(--csp-space-4);
  right: var(--csp-space-4);
  accent-color: var(--background-action-high-blue-france);
}

.mode__titre {
  padding-right: var(--csp-space-5);
}

.mode__desc {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.choix {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  border: 0;
  max-height: 22rem;
  overflow-y: auto;
}

.legende {
  margin-bottom: var(--csp-space-2);
  color: var(--text-label-grey);
}

.choix__ligne {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3);
  border: 1px solid var(--border-default-grey);
  cursor: pointer;

  input {
    accent-color: var(--background-action-high-blue-france);
  }

  &--on {
    border-color: var(--border-active-blue-france);
    background: var(--background-alt-blue-france);
  }

  &--simple {
    border: 0;
    padding: var(--csp-space-1) 0;
    font-size: var(--csp-font-size-sm);
  }
}

.choix__corps {
  flex: 1;
  min-width: 0;

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.depot {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  padding: var(--csp-space-5);
  border: 1px dashed var(--border-plain-grey);
  background: var(--background-alt-grey);
  color: var(--text-action-high-blue-france);
  cursor: pointer;

  &:has(:focus-visible) {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
  }
}

.mention {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.final {
  position: sticky;
  bottom: 0;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: var(--csp-space-4);
  padding: var(--csp-space-4) var(--csp-space-5);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  box-shadow: var(--csp-shadow-md);
}

.final__infos {
  display: flex;
  align-items: flex-end;
  gap: var(--csp-space-5);
  min-width: 0;
}

.final__postes {
  width: 9rem;
}

.final__ratt {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0 0 var(--csp-space-2);
  font-size: var(--csp-font-size-sm);
}

.final__actions {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  flex-shrink: 0;
}

.final__err {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-error);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
