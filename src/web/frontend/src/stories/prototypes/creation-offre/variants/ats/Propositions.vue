<script setup lang="ts">
import type { Offre, Proposition } from './store'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import { useNav } from './nav'
import { decider, sauvegarder, valeurLisible } from './store'

// Propositions de modification reçues avec les réponses des valideurs (section « Validation pour publication »).
// Chaque champ montre la valeur actuelle et la valeur proposée ; la personne qui rédige l'offre accepte ou ignore.
const props = defineProps<{ offre: Offre, redacteur?: boolean }>()
const emit = defineEmits<{ aller: [section: string] }>()
const { notifier } = useNav()
const o = computed(() => props.offre)

const SECTIONS: Record<Proposition['section'], string> = { annonce: 'Annonce', candidature: 'Formulaire de candidature', publication: 'Publication' }

function choisir(ip: number, ic: number, statut: 'acceptee' | 'ignoree') {
  decider(o.value, ip, ic, statut)
  sauvegarder()
  notifier(statut === 'acceptee' ? 'Modification appliquée à l\'offre.' : 'Proposition ignorée.')
}
const restants = (p: Proposition) => p.champs.filter(c => !c.statut).length
</script>

<template>
  <div class="props">
    <h4 class="props__titre">
      Propositions de modification
    </h4>
    <p class="mention">
      Les valideurs proposent ; vous décidez, champ par champ, d'accepter ou d'ignorer.
    </p>
    <p
      v-if="!o.propositions?.length"
      class="vide"
    >
      Aucune proposition.
    </p>
    <article
      v-for="(p, ip) in o.propositions"
      :key="ip"
      class="prop"
    >
      <header class="prop__tete">
        <span><strong>{{ p.par }}</strong> · {{ p.le }} · {{ SECTIONS[p.section] }}</span>
        <span class="prop__etat">{{ restants(p) ? `${restants(p)} à traiter` : 'Traitée' }}</span>
        <CspButton
          v-if="redacteur && restants(p)"
          :label="`Voir : ${SECTIONS[p.section]}`"
          size="sm"
          variant="tertiary-no-outline"
          icon="ri:arrow-down-line"
          is-icon-left
          @click="emit('aller', p.section)"
        />
      </header>
      <ul class="champs">
        <li
          v-for="(c, ic) in p.champs"
          :key="c.cle"
          class="champ"
          :class="c.statut && `champ--${c.statut}`"
        >
          <p class="champ__libelle">
            {{ c.libelle }}
          </p>
          <div class="champ__valeurs">
            <p>
              <small>Actuel</small>
              <span class="avant">{{ valeurLisible(c.avant) }}</span>
            </p>
            <p>
              <small>Proposé</small>
              <span class="apres">{{ valeurLisible(c.apres) }}</span>
            </p>
          </div>
          <div
            v-if="redacteur && !c.statut"
            class="champ__actions"
          >
            <CspButton
              label="Accepter"
              size="sm"
              icon="ri:check-line"
              is-icon-left
              @click="choisir(ip, ic, 'acceptee')"
            />
            <CspButton
              label="Ignorer"
              size="sm"
              variant="secondary"
              @click="choisir(ip, ic, 'ignoree')"
            />
          </div>
          <p
            v-else-if="c.statut"
            class="champ__statut"
          >
            {{ c.statut === 'acceptee' ? 'Acceptée : appliquée à l\'offre' : 'Ignorée' }}
          </p>
        </li>
      </ul>
    </article>
  </div>
</template>

<style scoped lang="scss">
.props {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  max-width: 48rem;
}

.props__titre {
  margin: 0;
  font-size: var(--csp-font-size-md, 1rem);
  font-weight: var(--csp-font-weight-bold);
}

.mention {
  margin: calc(-1 * var(--csp-space-2)) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.vide {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-style: italic;
  color: var(--text-mention-grey);
}

.prop {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  border-left: 3px solid var(--border-plain-blue-france);
}

.prop__tete {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-2) var(--csp-space-3);
  font-size: var(--csp-font-size-sm);
}

.prop__etat {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.champs {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  list-style: none;
}

.champ {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  padding-top: var(--csp-space-3);
  border-top: 1px solid var(--border-default-grey);

  &--acceptee,
  &--ignoree {
    color: var(--text-mention-grey);
  }
}

.champ__libelle {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
}

.champ__valeurs {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--csp-space-4);

  p {
    display: flex;
    flex-direction: column;
    gap: 2px;
    margin: 0;
    font-size: var(--csp-font-size-sm);
    white-space: pre-line;
  }

  small {
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.avant {
  text-decoration: line-through;
  text-decoration-color: var(--text-mention-grey);
}

.apres {
  padding: 0 var(--csp-space-1);
  background: var(--background-contrast-success, #e6feda);

  .champ--ignoree & {
    background: none;
  }
}

.champ__actions {
  display: flex;
  gap: var(--csp-space-2);
}

.champ__statut {
  margin: 0;
  font-size: var(--csp-font-size-xs);
}
</style>
