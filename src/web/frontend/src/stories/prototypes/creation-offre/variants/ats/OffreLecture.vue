<script setup lang="ts">
import type { EtapeFormulaire } from './aide'
import type { Offre } from './store'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import Panel from '../../shared/Panel.vue'
import { CANAUX_DIFFUSION, dateLongue, db, metier, PIECES, TEMPS_TRAVAIL } from './store'
import SuiviInterne from './SuiviInterne.vue'

// L'offre dans son état rempli, en lecture, rangée comme les cinq étapes du formulaire.
// Le suivi interne (jamais publié) est affiché dans l'annonce, dans un encadré gris.
// « Modifier » ouvre le formulaire directement à l'étape concernée.
const props = defineProps<{ offre: Offre, modifiable?: boolean }>()
const emit = defineEmits<{ modifier: [etape: EtapeFormulaire] }>()
const o = computed(() => props.offre)

const v = (x: string | undefined) => x || '-'
function lignes(texte: string) {
  return texte.split('\n').map(l => l.trim().replace(/^- /, '')).filter(Boolean)
}
const internes = computed(() => [
  { k: 'Référence interne', v: v(o.value.referenceInterne) },
  { k: 'Code poste', v: v(o.value.codePoste) },
  { k: 'Motif de recrutement', v: v(o.value.motifRecrutement) },
  { k: 'Agent remplacé', v: v(o.value.agentRemplace) },
  { k: 'Motif de départ', v: v(o.value.motifDepart) },
  { k: 'Groupe RIFSEEP', v: v(o.value.groupeRifseep) },
  { k: 'Cycle de travail', v: v(o.value.cycleTravail) },
])
const annonce = computed(() => [
  { k: 'Catégorie', v: o.value.categorie ? `Catégorie ${o.value.categorie}` : '-' },
  { k: 'Statut du poste', v: v(o.value.statutPoste) },
  { k: 'Nombre de postes', v: v(o.value.nbPostes) },
  { k: 'Date de vacance', v: o.value.dateVacance ? dateLongue(o.value.dateVacance) : '-' },
  { k: 'Ouvert aux', v: o.value.ouvertA.map(x => (x === 'titulaire' ? 'fonctionnaires' : 'contractuels')).join(' et ') || '-' },
  { k: 'Métier (RMFP+)', v: metier(o.value.metier)?.libelle ?? '-' },
  { k: 'Temps de travail', v: TEMPS_TRAVAIL.find(t => t.value === o.value.tempsTravail)?.label ?? '-' },
  { k: 'Lieu', v: v(o.value.lieu) },
  { k: 'Rémunération', v: v(o.value.remuneration) },
  { k: 'Télétravail', v: v(o.value.teletravail) },
  { k: 'Contact', v: v(o.value.contact) },
])
const MODES = { ats: 'Dans l\'ATS', courriel: 'Par courriel', externe: 'Sur un site externe' }
const EXIGENCES = { non: 'non demandé', facultatif: 'facultatif', obligatoire: 'obligatoire' }
const etapes = computed(() => (o.value.processusPersonnalise ? o.value.etapesProcessus : db.organisme.etapesRecrutement))
const sites = computed(() => CANAUX_DIFFUSION.filter(c => o.value.canaux.includes(c.id)).map(c => c.nom).join(', '))
</script>

<template>
  <Panel titre="1. Annonce">
    <template
      v-if="modifiable"
      #actions
    >
      <CspButton
        label="Modifier"
        size="sm"
        variant="tertiary-no-outline"
        icon="ri:pencil-line"
        is-icon-left
        @click="emit('modifier', 'annonce')"
      />
    </template>
    <p class="intitule">
      {{ o.titre || 'Intitulé à renseigner' }}
    </p>
    <dl class="dl">
      <div
        v-for="i in annonce"
        :key="i.k"
      >
        <dt>{{ i.k }}</dt>
        <dd>{{ i.v }}</dd>
      </div>
    </dl>
    <div v-if="o.presentation">
      <p class="label">
        Descriptif du service
      </p>
      <p class="texte">
        {{ o.presentation }}
      </p>
    </div>
    <div>
      <p class="label">
        Missions
      </p>
      <ul
        v-if="lignes(o.missions).length"
        class="liste"
      >
        <li
          v-for="(m, i) in lignes(o.missions)"
          :key="i"
        >
          {{ m }}
        </li>
      </ul>
      <p
        v-else
        class="texte vide"
      >
        À compléter.
      </p>
    </div>
    <div>
      <p class="label">
        Profil recherché
      </p>
      <p class="texte">
        {{ o.profil || '-' }}
      </p>
    </div>
    <div v-if="o.competences.length">
      <p class="label">
        Compétences
      </p>
      <ul class="liste">
        <li
          v-for="c in o.competences"
          :key="c"
        >
          {{ c }}
        </li>
      </ul>
    </div>
    <div v-if="o.conditions">
      <p class="label">
        Conditions particulières
      </p>
      <p class="texte">
        {{ o.conditions }}
      </p>
    </div>
    <SuiviInterne>
      <dl class="dl">
        <div
          v-for="i in internes"
          :key="i.k"
        >
          <dt>{{ i.k }}</dt>
          <dd>{{ i.v }}</dd>
        </div>
      </dl>
    </SuiviInterne>
  </Panel>

  <Panel titre="2. Formulaire de candidature">
    <template
      v-if="modifiable"
      #actions
    >
      <CspButton
        label="Modifier"
        size="sm"
        variant="tertiary-no-outline"
        icon="ri:pencil-line"
        is-icon-left
        @click="emit('modifier', 'candidature')"
      />
    </template>
    <dl class="dl">
      <div>
        <dt>Mode de candidature</dt>
        <dd>
          {{ MODES[o.modeCandidature] }}<template v-if="o.modeCandidature === 'courriel'">
            ({{ o.courrielCandidature || 'adresse à renseigner' }})
          </template><template v-if="o.modeCandidature === 'externe'">
            ({{ o.urlCandidature || 'lien à renseigner' }})
          </template>
        </dd>
      </div>
      <div>
        <dt>Pièces demandées</dt>
        <dd>{{ PIECES.map(p => `${p.label} : ${EXIGENCES[o.pieces[p.id]]}`).join(' · ') }}</dd>
      </div>
    </dl>
    <div v-if="o.questions.length">
      <p class="label">
        Questions aux candidats
      </p>
      <ul class="liste">
        <li
          v-for="q in o.questions"
          :key="q"
        >
          {{ q }}
        </li>
      </ul>
    </div>
  </Panel>

  <Panel titre="3. Processus et 4. Équipe">
    <template
      v-if="modifiable"
      #actions
    >
      <CspButton
        label="Modifier"
        size="sm"
        variant="tertiary-no-outline"
        icon="ri:pencil-line"
        is-icon-left
        @click="emit('modifier', 'processus')"
      />
    </template>
    <dl class="dl">
      <div>
        <dt>Étapes de recrutement{{ o.processusPersonnalise ? ' (personnalisées)' : '' }}</dt>
        <dd>{{ etapes.join(' › ') }}</dd>
      </div>
      <div>
        <dt>Équipe</dt>
        <dd>{{ o.equipe.map(m => `${m.nom} (${m.role})`).join(', ') }}</dd>
      </div>
    </dl>
  </Panel>

  <Panel titre="5. Publication">
    <template
      v-if="modifiable"
      #actions
    >
      <CspButton
        label="Modifier"
        size="sm"
        variant="tertiary-no-outline"
        icon="ri:pencil-line"
        is-icon-left
        @click="emit('modifier', 'publication')"
      />
    </template>
    <dl class="dl">
      <div>
        <dt>Début de publication</dt>
        <dd>{{ o.dateDebut ? dateLongue(o.dateDebut) : '-' }}</dd>
      </div>
      <div>
        <dt>Fin (date limite de candidature)</dt>
        <dd>{{ o.dateFin ? dateLongue(o.dateFin) : '-' }}{{ o.urgence ? ' · urgence' : '' }}</dd>
      </div>
      <div>
        <dt>Diffusion</dt>
        <dd>{{ o.diffusion === 'multi' ? 'Multi-diffusion' : 'Simple diffusion' }} — {{ sites }}</dd>
      </div>
    </dl>
  </Panel>
</template>

<style scoped lang="scss">
.dl {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--csp-space-3) var(--csp-space-6);
  margin: 0;

  dt {
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }

  dd {
    margin: 0;
    font-size: var(--csp-font-size-sm);
  }
}

.intitule {
  margin: 0;
  font-weight: var(--csp-font-weight-bold);
}

.label {
  margin: 0 0 var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.texte {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  white-space: pre-line;
}

.vide {
  color: var(--text-mention-grey);
}

.liste {
  margin: 0;
  padding-left: var(--csp-space-5);
  font-size: var(--csp-font-size-sm);
  list-style: disc;
}
</style>
