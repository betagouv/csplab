<script setup lang="ts">
import type { Fiche, Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import FieldRow from '../../shared/FieldRow.vue'
import ListEditor from '../../shared/ListEditor.vue'
import Panel from '../../shared/Panel.vue'
import { aMettreEnForme, mettreEnForme } from './aide'
import ApercuCandidat from './ApercuCandidat.vue'
import ChampOffre from './ChampOffre.vue'
import { useNav } from './nav'
import OrigineBadge from './OrigineBadge.vue'
import { changerEtat, contenuDepuisFiche, LIBELLES_CONTENU } from './store'

// Écran 5 — rédaction de l'offre. Le formulaire édite le contenu destiné aux candidats ;
// la fiche de poste source se consulte à côté, sans jamais être modifiée d'ici. L'aperçu suit la saisie.
const props = defineProps<{ offre: Offre, fiche: Fiche }>()
const emit = defineEmits<{ enregistrer: [], onglet: [t: 'suivi' | 'redaction' | 'publication'] }>()
const { notifier } = useNav()
const o = computed(() => props.offre)

const modifiable = computed(() => o.value.etat === 'redaction')
const vue = ref<'apercu' | 'fiche'>('apercu')
const VUES = [
  { value: 'apercu' as const, label: 'Aperçu candidat', icon: 'ri:eye-line' },
  { value: 'fiche' as const, label: 'Fiche de poste source', icon: 'ri:file-text-line' },
]

// « Repris de la fiche » tant que le texte est identique à ce que la fiche propose (création depuis une fiche).
const source = computed(() => contenuDepuisFiche(props.fiche))
type CleTexte = 'titre' | 'presentation' | 'missions' | 'profil' | 'modalites' | 'lieu' | 'teletravail'
const avecFiche = computed(() => o.value.origineContenu === 'fiche' || o.value.origineContenu === 'fichier')
function repris(cle: CleTexte | 'indispensables') {
  const v = source.value[cle]
  return avecFiche.value && Boolean(Array.isArray(v) ? v.length : v) && JSON.stringify(o.value[cle]) === JSON.stringify(v)
}
function modifie(cle: CleTexte | 'indispensables') {
  const v = source.value[cle]
  return avecFiche.value && Boolean(Array.isArray(v) ? v.length : v) && !repris(cle)
}
function restaurer(cle: CleTexte | 'indispensables') {
  const v = source.value[cle]
  ;(o.value as unknown as Record<string, unknown>)[cle] = Array.isArray(v) ? [...v] : v
}

function formater() {
  o.value.missions = mettreEnForme(o.value.missions)
  notifier('Mise en forme appliquée : une mission par ligne. Aucun mot n\'a été changé.')
}

function enregistrer() {
  emit('enregistrer')
  notifier('Brouillon enregistré. Vous pouvez revenir à la rédaction à tout moment.')
}

function revenirEnRedaction() {
  changerEtat(o.value, 'redaction', 'Retour en rédaction pour modifier le contenu')
}
</script>

<template>
  <p
    v-if="!modifiable"
    class="bandeau"
  >
    <CspIcon
      name="ri:lock-line"
      :size="16"
    />
    <span v-if="o.etat === 'validation'">Contenu en lecture seule pendant la validation de la DAR (hypothèse).</span>
    <span v-else-if="o.etat === 'a_publier'">Offre prête à publier.</span>
    <span v-else>Offre {{ o.etat === 'publiee' ? 'publiée' : 'archivée' }} : contenu en lecture seule.</span>
    <CspButton
      v-if="o.etat === 'a_publier'"
      label="Revenir en rédaction pour modifier"
      variant="tertiary-no-outline"
      size="sm"
      @click="revenirEnRedaction"
    />
  </p>
  <p
    v-else-if="o.remarqueDar"
    class="bandeau bandeau--remarque"
  >
    <CspIcon
      name="ri:chat-1-line"
      :size="16"
    />
    <span>Correction demandée lors de la validation : « {{ o.remarqueDar }} »</span>
  </p>

  <div class="redac">
    <fieldset
      class="form"
      :disabled="!modifiable"
    >
      <p class="origine">
        Contenu : {{ LIBELLES_CONTENU[o.origineContenu].toLowerCase() }}<template v-if="o.sourceOffreId">
          ({{ o.sourceOffreId }})
        </template>.
        Vos modifications concernent l'annonce uniquement : la fiche {{ fiche.id }} n'est pas modifiée.
      </p>

      <Panel titre="L'essentiel">
        <ChampOffre
          :offre="o"
          champ="titre"
          label="Titre de l'offre"
          for-id="o-titre"
          :repris="repris('titre')"
          :modifie="modifie('titre')"
          @restaurer="restaurer('titre')"
        >
          <CspInput
            id="o-titre"
            v-model="o.titre"
            :disabled="!modifiable"
          />
        </ChampOffre>
        <ChampOffre
          :offre="o"
          champ="presentation"
          label="Présentation du poste"
          for-id="o-presentation"
          :repris="repris('presentation')"
          :modifie="modifie('presentation')"
          @restaurer="restaurer('presentation')"
        >
          <CspTextarea
            id="o-presentation"
            v-model="o.presentation"
            :rows="3"
            :disabled="!modifiable"
          />
        </ChampOffre>
        <ChampOffre
          :offre="o"
          champ="nbPostes"
          label="Nombre de postes à pourvoir"
          for-id="o-postes"
        >
          <CspInput
            id="o-postes"
            v-model="o.nbPostes"
            type="number"
            class="court"
            :disabled="!modifiable"
          />
        </ChampOffre>
      </Panel>

      <Panel titre="Missions">
        <ChampOffre
          :offre="o"
          champ="missions"
          label="Vos missions"
          for-id="o-missions"
          :repris="repris('missions')"
          :modifie="modifie('missions')"
          @restaurer="restaurer('missions')"
        >
          <CspTextarea
            id="o-missions"
            v-model="o.missions"
            :rows="6"
            :disabled="!modifiable"
          />
        </ChampOffre>
        <div
          v-if="modifiable && aMettreEnForme(o.missions)"
          class="outil"
        >
          <CspButton
            label="Mettre en forme (une mission par ligne)"
            variant="tertiary-no-outline"
            size="sm"
            icon="ri:list-unordered"
            is-icon-left
            @click="formater"
          />
        </div>
      </Panel>

      <Panel titre="Profil recherché">
        <ChampOffre
          :offre="o"
          champ="profil"
          label="Votre profil"
          for-id="o-profil"
          :repris="repris('profil')"
          :modifie="modifie('profil')"
          @restaurer="restaurer('profil')"
        >
          <CspTextarea
            id="o-profil"
            v-model="o.profil"
            :rows="3"
            :disabled="!modifiable"
          />
        </ChampOffre>
        <ChampOffre
          :offre="o"
          champ="indispensables"
        >
          <ListEditor
            v-model="o.indispensables"
            label="Compétences indispensables"
            placeholder="Ex. : Maîtrise d'un logiciel de paie"
            :disabled="!modifiable"
          />
        </ChampOffre>
        <ChampOffre
          :offre="o"
          champ="souhaitables"
        >
          <ListEditor
            v-model="o.souhaitables"
            label="Compétences souhaitables"
            placeholder="Ex. : Première expérience en paie"
            :disabled="!modifiable"
          />
        </ChampOffre>
      </Panel>

      <Panel titre="Modalités et conditions">
        <ChampOffre
          :offre="o"
          champ="modalites"
          label="Modalités de recrutement"
          for-id="o-modalites"
          :repris="repris('modalites')"
          :modifie="modifie('modalites')"
          @restaurer="restaurer('modalites')"
        >
          <CspTextarea
            id="o-modalites"
            v-model="o.modalites"
            :rows="2"
            :disabled="!modifiable"
          />
        </ChampOffre>
        <FieldRow :cols="2">
          <ChampOffre
            :offre="o"
            champ="lieu"
            label="Lieu"
            for-id="o-lieu"
            :repris="repris('lieu')"
          >
            <CspInput
              id="o-lieu"
              v-model="o.lieu"
              :disabled="!modifiable"
            />
          </ChampOffre>
          <ChampOffre
            :offre="o"
            champ="remuneration"
            label="Rémunération (facultatif)"
            for-id="o-remu"
          >
            <CspInput
              id="o-remu"
              v-model="o.remuneration"
              placeholder="Ex. : selon expérience, grille indiciaire"
              :disabled="!modifiable"
            />
          </ChampOffre>
        </FieldRow>
        <FieldRow :cols="2">
          <CspInput
            v-model="o.teletravail"
            label="Télétravail (facultatif)"
            :disabled="!modifiable"
          />
          <CspInput
            v-model="o.conditions"
            label="Conditions d'exercice (facultatif)"
            placeholder="Horaires, déplacements…"
            :disabled="!modifiable"
          />
        </FieldRow>
      </Panel>

      <Panel titre="Candidature">
        <FieldRow :cols="2">
          <ChampOffre
            :offre="o"
            champ="dateLimite"
            label="Date limite de candidature"
            for-id="o-limite"
          >
            <CspInput
              id="o-limite"
              v-model="o.dateLimite"
              placeholder="AAAA-MM-JJ"
              :disabled="!modifiable"
            />
          </ChampOffre>
          <CspInput
            v-model="o.contact"
            label="Contact (facultatif)"
            :disabled="!modifiable"
          />
        </FieldRow>
      </Panel>

      <div
        v-if="modifiable"
        class="pied"
      >
        <CspButton
          label="Enregistrer le brouillon"
          variant="secondary"
          icon="ri:save-3-line"
          is-icon-left
          @click="enregistrer"
        />
        <CspButton
          label="Continuer : validation et publication"
          icon="ri:arrow-right-line"
          @click="emit('onglet', 'publication')"
        />
      </div>
    </fieldset>

    <aside class="cote">
      <CspSegmentedControl
        v-model="vue"
        legend="Afficher"
        hide-legend
        size="sm"
        :options="VUES"
      />
      <ApercuCandidat
        v-if="vue === 'apercu'"
        :offre="o"
      />
      <div
        v-else
        class="source"
      >
        <p class="source__tete">
          <CspIcon
            name="ri:lock-line"
            :size="14"
          />
          {{ fiche.id }} · <OrigineBadge
            :origine="fiche.origine"
            court
          /> · consultation seule
        </p>
        <h3 class="source__titre">
          {{ fiche.intitule }}
        </h3>
        <p class="source__meta">
          {{ fiche.service }} · {{ fiche.localisation }}
        </p>
        <p class="source__label">
          Missions
        </p>
        <p class="source__texte">
          {{ fiche.missions || '—' }}
        </p>
        <ul
          v-if="fiche.activites.length"
          class="source__liste"
        >
          <li
            v-for="a in fiche.activites"
            :key="a"
          >
            {{ a }}
          </li>
        </ul>
        <p class="source__label">
          Compétences
        </p>
        <ul class="source__liste">
          <li
            v-for="c in fiche.competences"
            :key="c"
          >
            {{ c }}
          </li>
        </ul>
        <p class="source__label">
          Profil
        </p>
        <p class="source__texte">
          {{ fiche.profil || '—' }}
        </p>
        <p class="source__note">
          La fiche décrit le poste pour l'organisation ; l'annonce s'adresse aux candidats. Modifier l'une ne change pas l'autre.
        </p>
      </div>
    </aside>
  </div>
</template>

<style scoped lang="scss">
.bandeau {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-blue-france);
  background: var(--background-default-grey);
  font-size: var(--csp-font-size-sm);

  span {
    flex: 1;
  }

  &--remarque {
    background: var(--background-alt-blue-france);
  }
}

.redac {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: var(--csp-space-5);
  align-items: start;
}

.form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  margin: 0;
  padding: 0;
  border: 0;
  min-width: 0;
}

.origine {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.court {
  max-width: 8rem;
}

.outil {
  margin: calc(-1 * var(--csp-space-3)) 0 0 calc(-1 * var(--csp-space-2));
}

.pied {
  position: sticky;
  bottom: 0;
  display: flex;
  justify-content: space-between;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  box-shadow: var(--csp-shadow-md);
}

.cote {
  position: sticky;
  top: 9rem;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  max-height: calc(100vh - 11rem);
  overflow-y: auto;
}

.source {
  padding: var(--csp-space-5);
  border: 1px dashed var(--border-plain-grey);
  background: var(--background-alt-grey);
  font-size: var(--csp-font-size-sm);

  p {
    margin: 0;
  }
}

.source__tete {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.source__titre {
  margin: var(--csp-space-2) 0 0;
  font-size: var(--csp-font-size-lg);
}

.source__meta {
  color: var(--text-mention-grey);
}

.source__label {
  margin-top: var(--csp-space-3) !important;
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.source__liste {
  margin: 0;
  padding-left: var(--csp-space-5);
  list-style: disc;
}

.source__note {
  margin-top: var(--csp-space-4) !important;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}
</style>
