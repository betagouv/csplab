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
import { db, fiche, le, maintenant, nouvelleFiche, nouvelleOffre, offresDe } from './store'

// Écran 4 — choisir le mode de création. Quel que soit le mode, l'offre est rattachée à une fiche
// de poste : existante, constituée à partir d'un document, créée à partir de la saisie, ou celle de l'offre reprise.
type Mode = 'fiche' | 'fichier' | 'manuel' | 'duplication'
const props = defineProps<{ mode?: Mode, ficheId?: string, offreId?: string }>()
const { aller, notifier } = useNav()

const MODES: { id: Mode, titre: string, desc: string, rattachement: string, icon: string }[] = [
  { id: 'fiche', titre: 'Depuis une fiche de poste', desc: 'Les informations de la fiche préremplissent l\'offre.', rattachement: 'Rattachée à la fiche choisie', icon: 'ri:file-text-line' },
  { id: 'fichier', titre: 'Depuis un fichier', desc: 'Ajoutez un document (fiche de poste, ancienne annonce) qui sert de référence.', rattachement: 'Une fiche est constituée à partir du document', icon: 'ri:upload-2-line' },
  { id: 'manuel', titre: 'Par saisie manuelle', desc: 'Saisissez l\'essentiel du poste, sans document de départ.', rattachement: 'Une fiche de référence est créée avec votre saisie', icon: 'ri:edit-line' },
  { id: 'duplication', titre: 'Depuis une ancienne offre', desc: 'Le contenu d\'une offre publiée est copié dans une nouvelle offre indépendante.', rattachement: 'Rattachée à la fiche de l\'offre reprise (modifiable)', icon: 'ri:file-copy-2-line' },
]

const mode = ref<Mode | null>(props.mode ?? null)
const nbPostes = ref('1')
const erreur = ref('')

// 1. Fiche existante
const recherche = ref('')
const ficheChoisie = ref<string | null>(props.ficheId ?? null)
const fichesActives = computed(() => {
  const q = recherche.value.toLowerCase().trim()
  return db.fiches.filter(f => f.statut === 'active' && (!q || [f.intitule, f.codePoste, f.id].join(' ').toLowerCase().includes(q)))
})

// 2. Fichier
const fichier = ref<string | null>(null)
const analyse = ref(false)
const extrait = ref({ intitule: '', service: '', localisation: '' })
const rattachementFichier = ref<'nouvelle' | 'existante'>('nouvelle')
const ficheExistanteFichier = ref<string>()
function choisirFichier(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0]
  if (!f) {
    return
  }
  fichier.value = f.name
  analyse.value = true
  setTimeout(() => {
    analyse.value = false
    // Extraction simulée : l'intitulé est déduit du nom du fichier, à vérifier.
    const nom = f.name.replace(/\.[^.]+$/, '').replace(/[_-]+/g, ' ').replace(/\b(?:fiche|poste|de|v\d+)\b/gi, ' ').replace(/\s+/g, ' ').trim()
    extrait.value = { intitule: nom.length > 3 ? nom.charAt(0).toUpperCase() + nom.slice(1) : 'Chargé·e de communication', service: 'Secrétariat général', localisation: 'Toulouse (31)' }
  }, 1300)
}

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
    case 'fichier': return rattachementFichier.value === 'nouvelle' ? (fichier.value ? 'une nouvelle fiche constituée à partir du document' : 'ajoutez un document') : (ficheExistanteFichier.value ? `${fiche(ficheExistanteFichier.value)?.intitule} (${ficheExistanteFichier.value})` : 'choisissez une fiche')
    case 'manuel': return manuel.value.intitule ? `une nouvelle fiche « ${manuel.value.intitule} » (à compléter dans le référentiel)` : 'une nouvelle fiche créée à partir de votre saisie'
    case 'duplication': return ficheDuplication.value ? `${fiche(ficheDuplication.value)?.intitule} (${ficheDuplication.value})` : 'choisissez une offre'
    default: return ''
  }
})

function creer() {
  erreur.value = ''
  if (!(Number(nbPostes.value) >= 1)) {
    erreur.value = 'Indiquez au moins 1 poste.'
    return
  }
  let f: Fiche | undefined
  let source: Offre | undefined
  if (mode.value === 'fiche') {
    f = ficheChoisie.value ? fiche(ficheChoisie.value) : undefined
    if (!f) {
      erreur.value = 'Choisissez la fiche de poste.'
      return
    }
  }
  else if (mode.value === 'fichier') {
    if (!fichier.value) {
      erreur.value = 'Ajoutez un document.'
      return
    }
    if (rattachementFichier.value === 'existante') {
      f = ficheExistanteFichier.value ? fiche(ficheExistanteFichier.value) : undefined
      if (!f) {
        erreur.value = 'Choisissez la fiche à laquelle rattacher le document.'
        return
      }
    }
    else {
      if (!extrait.value.intitule.trim()) {
        erreur.value = 'Vérifiez l\'intitulé détecté.'
        return
      }
      f = nouvelleFiche({ ...extrait.value, document: { nom: fichier.value, ajouteLe: maintenant() } }, 'document', `Fiche constituée à partir du document ${fichier.value} (extraction simulée)`)
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
  const o = nouvelleOffre(f, mode.value, nbPostes.value, source)
  notifier(`Offre ${o.id} créée et rattachée à la fiche ${f.id}.`)
  aller({ nom: 'offre', id: o.id, onglet: 'redaction' })
}
</script>

<template>
  <PageAts
    actif="offres"
    titre="Créer une offre d'emploi"
    sous-titre="Une offre est toujours rattachée à une fiche de poste. Choisissez d'où part son contenu."
    :fil="[{ label: 'Offres d\'emploi', action: () => aller({ nom: 'offres' }) }, { label: 'Nouvelle offre' }]"
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
      v-else-if="mode === 'fichier'"
      titre="Ajouter un document"
      description="Fiche de poste, ancienne annonce… Prototype : le document n'est pas envoyé, son contenu est simulé."
    >
      <label class="depot">
        <CspIcon
          name="ri:upload-cloud-2-line"
          :size="24"
        />
        <span>{{ fichier ? `Document : ${fichier}` : 'Choisir un fichier (.docx, .pdf, .odt)' }}</span>
        <input
          type="file"
          accept=".doc,.docx,.pdf,.odt,.txt"
          class="sr-only"
          @change="choisirFichier"
        >
      </label>
      <p
        v-if="analyse"
        class="mention"
      >
        <CspIcon
          name="ri:loader-4-line"
          :size="14"
          class="spin"
        /> Lecture du document…
      </p>
      <template v-else-if="fichier">
        <fieldset class="choix">
          <legend class="legende">
            Fiche de poste de rattachement
          </legend>
          <label class="choix__ligne choix__ligne--simple">
            <input
              v-model="rattachementFichier"
              type="radio"
              value="nouvelle"
            >
            <span>Constituer une nouvelle fiche à partir du document</span>
          </label>
          <label class="choix__ligne choix__ligne--simple">
            <input
              v-model="rattachementFichier"
              type="radio"
              value="existante"
            >
            <span>Rattacher le document à une fiche existante</span>
          </label>
        </fieldset>
        <FieldRow
          v-if="rattachementFichier === 'nouvelle'"
          :cols="3"
        >
          <CspInput
            v-model="extrait.intitule"
            label="Intitulé détecté"
          />
          <CspInput
            v-model="extrait.service"
            label="Service"
          />
          <CspInput
            v-model="extrait.localisation"
            label="Localisation"
          />
        </FieldRow>
        <CspSelect
          v-else
          v-model="ficheExistanteFichier"
          label="Fiche existante"
          placeholder="Choisir…"
          :options="db.fiches.filter(f => f.statut === 'active').map(f => ({ value: f.id, label: `${f.intitule} (${f.id})` }))"
        />
      </template>
    </Panel>

    <Panel
      v-else-if="mode === 'manuel'"
      titre="L'essentiel du poste"
      description="Ces informations créent la fiche de poste de référence ; vous rédigerez l'annonce à l'étape suivante."
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
        <CspInput
          v-model="nbPostes"
          type="number"
          label="Postes à pourvoir"
          class="final__postes"
        />
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
          label="Créer l'offre et rédiger"
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
  grid-template-columns: repeat(4, minmax(0, 1fr));
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
