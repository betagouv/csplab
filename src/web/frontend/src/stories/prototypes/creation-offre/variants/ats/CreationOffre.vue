<script setup lang="ts">
import type { Fiche, Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import { CATEGORIES } from '../../data/referentiels'
import FieldRow from '../../shared/FieldRow.vue'
import Panel from '../../shared/Panel.vue'
import EtatBadge from './EtatBadge.vue'
import { useNav } from './nav'
import OrigineBadge from './OrigineBadge.vue'
import PageAts from './PageAts.vue'
import { db, fiche, le, nouvelleFiche, nouvelleOffre, offresDe } from './store'

// Lancer un recrutement : 3 sources (fiche de poste, offre existante, saisie manuelle). Quelle que soit la source,
// l'offre est rattachée à une fiche de poste : existante, créée à partir de la saisie, ou celle de l'offre reprise.
// Le nombre de postes se renseigne dans le formulaire de l'offre.
type Mode = 'fiche' | 'manuel' | 'duplication'
const props = defineProps<{ mode?: Mode, ficheId?: string, offreId?: string }>()
const { aller, notifier } = useNav()

const MODES: { id: Mode, titre: string, desc: string, rattachement: string, icon: string }[] = [
  { id: 'fiche', titre: 'Depuis une fiche de poste', desc: 'Les informations de la fiche préremplissent l\'offre.', rattachement: 'Rattachée à la fiche choisie', icon: 'ri:file-text-line' },
  { id: 'manuel', titre: 'Saisie manuelle', desc: 'Sans fiche de poste préexistante : saisissez l\'essentiel du poste.', rattachement: 'Une fiche de référence est créée avec votre saisie', icon: 'ri:edit-line' },
  { id: 'duplication', titre: 'Depuis une offre existante', desc: 'Dupliquer un recrutement similaire : le contenu est copié dans une nouvelle offre indépendante.', rattachement: 'Rattachée à la fiche de l\'offre reprise (modifiable)', icon: 'ri:file-copy-2-line' },
]

const mode = ref<Mode | null>(props.mode ?? null)
const erreur = ref('')

// 1. Fiche existante
const recherche = ref('')
const ficheChoisie = ref<string | null>(props.ficheId ?? null)
const fichesActives = computed(() => {
  const q = recherche.value.toLowerCase().trim()
  return db.fiches.filter(f => f.statut === 'active' && (!q || [f.intitule, f.codePoste, f.id].join(' ').toLowerCase().includes(q)))
})

// 3. Saisie manuelle
const manuel = ref({ intitule: '', service: '', localisation: '', categories: [] as string[] })

// 4. Duplication
const offreSource = ref<string | null>(props.offreId ?? null)
const offresReprenables = computed(() => db.offres.filter(o => o.etat === 'publiee' || o.etat === 'archivee'))
const ficheDuplication = ref<string | null>(props.offreId ? db.offres.find(o => o.id === props.offreId)?.ficheId ?? null : null)
function choisirSource(id: string) {
  offreSource.value = id
  ficheDuplication.value = db.offres.find(o => o.id === id)!.ficheId
}
const optionsFiches = computed(() => db.fiches.filter(f => f.statut === 'active' || f.id === ficheDuplication.value).map(f => ({ value: f.id, label: `${f.intitule} (${f.id})` })))

/** Ce à quoi l'offre sera rattachée : toujours affiché avant de créer. */
const rattachement = computed(() => {
  switch (mode.value) {
    case 'fiche': return ficheChoisie.value ? `${fiche(ficheChoisie.value)?.intitule} (${ficheChoisie.value})` : 'choisissez une fiche'
    case 'manuel': return manuel.value.intitule ? `une nouvelle fiche « ${manuel.value.intitule} » (à compléter dans le référentiel)` : 'une nouvelle fiche créée à partir de votre saisie'
    case 'duplication': return ficheDuplication.value ? `${fiche(ficheDuplication.value)?.intitule} (${ficheDuplication.value})` : 'choisissez une offre'
    default: return ''
  }
})

function creer() {
  erreur.value = ''
  let f: Fiche | undefined
  let source: Offre | undefined
  if (mode.value === 'fiche') {
    f = ficheChoisie.value ? fiche(ficheChoisie.value) : undefined
    if (!f) {
      erreur.value = 'Choisissez la fiche de poste.'
      return
    }
  }
  else if (mode.value === 'manuel') {
    if (!manuel.value.intitule.trim()) {
      erreur.value = 'Indiquez au moins l\'intitulé du poste : il sert à créer la fiche de référence.'
      return
    }
    f = nouvelleFiche({ ...manuel.value }, 'ats', 'Fiche créée à partir d\'une saisie manuelle d\'offre')
  }
  else if (mode.value === 'duplication') {
    source = offreSource.value ? db.offres.find(o => o.id === offreSource.value) : undefined
    f = ficheDuplication.value ? fiche(ficheDuplication.value) : undefined
    if (!source || !f) {
      erreur.value = 'Choisissez l\'offre à reprendre.'
      return
    }
  }
  if (!f || !mode.value) {
    return
  }
  const o = nouvelleOffre(f, mode.value, source)
  notifier(`Offre ${o.id} créée et rattachée à la fiche ${f.id}.`)
  aller({ nom: 'offre', id: o.id, onglet: 'redaction' })
}
</script>

<template>
  <PageAts
    actif="offres"
    titre="Lancer un recrutement"
    sous-titre="Créez l'offre à partir de la source la plus adaptée. Elle reste toujours rattachée à une fiche de poste."
    :fil="[{ label: 'Offres d\'emploi', action: () => aller({ nom: 'offres' }) }, { label: 'Lancer un recrutement' }]"
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
        <CspIcon
          :name="m.icon"
          :size="20"
          class="mode__icon"
        />
        <strong class="mode__titre">{{ m.titre }}</strong>
        <span class="mode__desc">{{ m.desc }}</span>
        <span class="mode__ratt"><CspIcon
          name="ri:link"
          :size="12"
        /> {{ m.rattachement }}</span>
      </label>
    </div>

    <Panel
      v-if="mode === 'fiche'"
      titre="Choisir la fiche de poste"
    >
      <CspInput
        v-model="recherche"
        type="search"
        label="Rechercher une fiche"
        placeholder="Intitulé, code poste…"
      />
      <fieldset class="choix">
        <legend class="sr-only">
          Fiche de poste
        </legend>
        <label
          v-for="f in fichesActives"
          :key="f.id"
          class="choix__ligne"
          :class="{ 'choix__ligne--on': ficheChoisie === f.id }"
        >
          <input
            v-model="ficheChoisie"
            type="radio"
            name="fiche"
            :value="f.id"
          >
          <span class="choix__corps">
            <strong>{{ f.intitule }}</strong>
            <small>{{ f.id }} · {{ f.service }} · {{ offresDe(f.id).length }} offre(s)</small>
          </span>
          <OrigineBadge
            :origine="f.origine"
            court
          />
        </label>
      </fieldset>
    </Panel>

    <Panel
      v-else-if="mode === 'manuel'"
      titre="L'essentiel du poste"
      description="Ces informations créent la fiche de poste de référence ; vous compléterez le formulaire de l'offre à l'étape suivante."
    >
      <FieldRow :cols="3">
        <CspInput
          v-model="manuel.intitule"
          label="Intitulé du poste"
        />
        <CspInput
          v-model="manuel.service"
          label="Service"
        />
        <CspInput
          v-model="manuel.localisation"
          label="Localisation"
        />
      </FieldRow>
      <CspCheckboxGroup
        v-model="manuel.categories"
        label="Catégorie(s)"
        :options="CATEGORIES"
      />
    </Panel>

    <Panel
      v-else-if="mode === 'duplication'"
      titre="Choisir l'offre à reprendre"
      description="Le contenu est copié ; la nouvelle offre est indépendante de l'ancienne."
    >
      <fieldset class="choix">
        <legend class="sr-only">
          Offre à reprendre
        </legend>
        <label
          v-for="o in offresReprenables"
          :key="o.id"
          class="choix__ligne"
          :class="{ 'choix__ligne--on': offreSource === o.id }"
        >
          <input
            type="radio"
            name="source"
            :checked="offreSource === o.id"
            @change="choisirSource(o.id)"
          >
          <span class="choix__corps">
            <strong>{{ o.titre }}</strong>
            <small>{{ o.id }} · publiée {{ le(o.publieeLe) }} · fiche {{ o.ficheId }}</small>
          </span>
          <EtatBadge :etat="o.etat" />
        </label>
      </fieldset>
      <CspSelect
        v-if="offreSource"
        :model-value="ficheDuplication ?? undefined"
        label="Fiche de poste de rattachement"
        hint="Par défaut celle de l'offre reprise. Vérifiez qu'elle correspond toujours au poste."
        :options="optionsFiches"
        @update:model-value="v => (ficheDuplication = v ?? null)"
      />
    </Panel>

    <div
      v-if="mode"
      class="final"
    >
      <div class="final__infos">
        <p class="final__ratt">
          <CspIcon
            name="ri:link"
            :size="14"
          />
          L'offre sera rattachée à : <strong>{{ rattachement }}</strong>
        </p>
      </div>
      <div class="final__actions">
        <p
          v-if="erreur"
          class="final__err"
          role="alert"
        >
          {{ erreur }}
        </p>
        <CspButton
          label="Continuer vers le formulaire de l'offre"
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
  grid-template-columns: repeat(3, minmax(0, 1fr));
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

.mode__icon {
  color: var(--text-action-high-blue-france);
  margin-bottom: var(--csp-space-2);
}

.mode__titre {
  padding-right: var(--csp-space-5);
}

.mode__desc {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.mode__ratt {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin-top: auto;
  padding-top: var(--csp-space-2);
  font-size: var(--csp-font-size-xs);
  color: var(--text-action-high-blue-france);
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
