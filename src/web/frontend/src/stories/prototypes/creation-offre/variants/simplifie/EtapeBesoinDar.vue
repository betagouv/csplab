<script setup lang="ts">
import { computed, ref } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { CATEGORIES, personne } from '../../data/referentiels'
import { useOffre } from '../../data/useOffre'
import Disclosure from '../../shared/Disclosure.vue'
import Panel from '../../shared/Panel.vue'
import EtapeFooter from './EtapeFooter.vue'
import RemarquesSection from './RemarquesSection.vue'

// Étape 1 quand la DAR est soumise ou validée : on la consulte, on ne la modifie pas.
// Ses informations sont déjà reprises dans l'offre (étapes 2 et 3) ; rien à ressaisir.
const { state, etapeEnCours } = useOffre()
const b = state.besoin

const d = computed(() => state.darContenu)
const validee = computed(() => b.darStatut === 'validee')
const texteOuvert = ref(false)
const enAttente = computed(() => `Soumise le ${d.value?.date ?? ''}${etapeEnCours.value ? `, en attente de ${personne(etapeEnCours.value.personneId).nom}` : ''}.`)

const lignes = computed(() => {
  const src = d.value
  const liste = src?.statuts ?? b.statuts
  const statuts = liste.length === 2 ? 'Fonctionnaires et contractuels' : liste[0] === 'titulaire' ? 'Fonctionnaires' : liste[0] === 'contractuel' ? 'Contractuels' : ''
  return [
    { k: 'Intitulé', v: src?.intitule ?? b.intitule },
    { k: 'Service', v: src?.service ?? b.service },
    { k: 'Localisation', v: src?.localisation ?? b.localisation },
    { k: 'Catégorie', v: (src?.categories ?? b.categories).map(c => CATEGORIES.find(x => x.value === c)?.label).join(', ') },
    { k: 'Ouvert aux', v: statuts },
    { k: 'Postes', v: `${src?.nbPostes ?? b.nbPostes}${(src?.codesPostes ?? b.codesPostes).length ? ` (${(src?.codesPostes ?? b.codesPostes).join(', ')})` : ''}` },
    { k: 'Fiche de poste', v: b.ficheRef || '—' },
  ]
})
</script>

<template>
  <header>
    <h2 class="title">
      Préparer le besoin
    </h2>
    <p class="desc">
      L'offre part de la demande d'autorisation de recrutement. Ses informations sont déjà reprises : vous n'avez rien à ressaisir.
    </p>
  </header>

  <RemarquesSection :step-ids="['besoin', 'poste']" />

  <Panel>
    <div class="dar-head">
      <div>
        <p class="dar-head__kicker">
          <CspIcon
            name="ri:lock-line"
            :size="14"
          />
          Demande d'autorisation de recrutement
        </p>
        <h3 class="dar-head__ref">
          {{ b.darRef }}
        </h3>
      </div>
      <CspBadge
        :label="validee ? 'DAR validée' : 'DAR soumise à validation'"
        :type="validee ? 'success' : 'new'"
        variant="soft"
        size="sm"
      />
    </div>
    <p class="dar-meta">
      <template v-if="validee">
        Validée le {{ d?.date ?? '2 octobre 2026' }}<template v-if="d?.validePar">
          par {{ personne(d.validePar).nom }}
        </template>, telle que soumise. Son contenu ne change pas quand vous rédigez l'offre.
      </template>
      <template v-else>
        {{ enAttente }} Vous pouvez préparer l'offre dès maintenant ; elle pourra être créée une fois la DAR validée.
      </template>
    </p>
    <dl class="dar-dl">
      <div
        v-for="l in lignes"
        :key="l.k"
      >
        <dt>{{ l.k }}</dt>
        <dd>{{ l.v || '—' }}</dd>
      </div>
    </dl>
    <Disclosure
      v-if="d"
      v-model:ouvert="texteOuvert"
      titre="Texte de la DAR"
      resume="Missions, compétences, profil et environnement, tels que validés"
    >
      <div class="dar-text">
        <p class="dar-text__label">
          Missions
        </p>
        <p class="dar-text__body">
          {{ d.missions }}
        </p>
        <template v-if="d.competences.length">
          <p class="dar-text__label">
            Compétences
          </p>
          <p class="dar-text__body">
            {{ d.competences.join(' ; ') }}
          </p>
        </template>
        <template v-if="d.profil">
          <p class="dar-text__label">
            Profil
          </p>
          <p class="dar-text__body">
            {{ d.profil }}
          </p>
        </template>
        <template v-if="d.environnement">
          <p class="dar-text__label">
            Environnement
          </p>
          <p class="dar-text__body">
            {{ d.environnement }}
          </p>
        </template>
      </div>
    </Disclosure>
  </Panel>

  <p class="hypo">
    Hypothèse à confirmer : modifier une information de la DAR (intitulé, localisation, nombre de postes…) passerait par une nouvelle version de la DAR, pas par l'offre.
  </p>

  <EtapeFooter />
</template>

<style scoped lang="scss">
.title {
  margin: 0;
  font-size: var(--csp-font-size-2xl);
}

.desc {
  margin: var(--csp-space-1) 0 0;
  color: var(--text-mention-grey);
}

.dar-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--csp-space-3);
}

.dar-head__kicker {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.dar-head__ref {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-lg);
}

.dar-meta {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.dar-dl {
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

.dar-text {
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-alt-grey);
  font-size: var(--csp-font-size-sm);

  p {
    margin: 0;
  }
}

.dar-text__label {
  margin-top: var(--csp-space-3) !important;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);

  &:first-child {
    margin-top: 0 !important;
  }
}

.dar-text__body {
  white-space: pre-line;
}

.hypo {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}
</style>
