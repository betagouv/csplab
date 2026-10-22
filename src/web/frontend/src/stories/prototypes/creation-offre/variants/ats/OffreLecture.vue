<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import Panel from '../../shared/Panel.vue'
import { verrouilleParDar } from './store'

// L'offre dans son état rempli, en lecture : mêmes rubriques que le formulaire.
const props = defineProps<{ offre: Offre }>()
const o = computed(() => props.offre)

function lignes(texte: string) {
  return texte.split('\n').map(l => l.trim().replace(/^- /, '')).filter(Boolean)
}
const essentiel = computed(() => [
  { k: 'Titre de l\'offre', v: o.value.titre, champ: 'titre' },
  { k: 'Catégorie', v: o.value.categorie ? `Catégorie ${o.value.categorie}` : '', champ: 'categorie' },
  { k: 'Nombre de postes', v: o.value.nbPostes, champ: 'nbPostes' },
  { k: 'Lieu', v: o.value.lieu, champ: 'lieu' },
  { k: 'Télétravail', v: o.value.teletravail, champ: '' },
  { k: 'Rémunération', v: o.value.remuneration, champ: '' },
  { k: 'Conditions d\'exercice', v: o.value.conditions, champ: '' },
])
</script>

<template>
  <Panel titre="L'essentiel">
    <dl class="dl">
      <div
        v-for="i in essentiel"
        :key="i.k"
      >
        <dt>
          {{ i.k }}
          <span
            v-if="i.champ && verrouilleParDar(o, i.champ)"
            class="valide"
          >· validé</span>
        </dt>
        <dd>{{ i.v || '-' }}</dd>
      </div>
    </dl>
    <div v-if="o.presentation">
      <p class="label">
        Présentation du poste
      </p>
      <p class="texte">
        {{ o.presentation }}
      </p>
    </div>
  </Panel>

  <Panel titre="Missions">
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
  </Panel>

  <Panel titre="Profil recherché">
    <p class="texte">
      {{ o.profil || '-' }}
    </p>
    <div class="cols">
      <div>
        <p class="label">
          Compétences indispensables
        </p>
        <ul class="liste">
          <li
            v-for="c in o.indispensables"
            :key="c"
          >
            {{ c }}
          </li>
        </ul>
      </div>
      <div v-if="o.souhaitables.length">
        <p class="label">
          Compétences souhaitables
        </p>
        <ul class="liste">
          <li
            v-for="c in o.souhaitables"
            :key="c"
          >
            {{ c }}
          </li>
        </ul>
      </div>
    </div>
  </Panel>

  <Panel titre="Modalités de candidature">
    <dl class="dl">
      <div>
        <dt>Modalités de recrutement</dt>
        <dd>{{ o.modalites || '-' }}</dd>
      </div>
      <div>
        <dt>Contact</dt>
        <dd>{{ o.contact || '-' }}</dd>
      </div>
      <div v-if="o.dateLimite">
        <dt>Date limite de candidature</dt>
        <dd>{{ o.dateLimite }}</dd>
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

.valide {
  color: var(--text-default-success);
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

.cols {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--csp-space-4);
}
</style>
