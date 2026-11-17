<script setup lang="ts">
import CspSwitch from '@/components/base/CspSwitch/CspSwitch.vue'
import Panel from '../../shared/Panel.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { db, sauvegarder } from './store'

// Paramètres de l'organisme (Superviseur) : droits « Créer » et « Publier » de chaque Agent, processus de
// recrutement par défaut. Le circuit d'autorisation (avant la publication) est désactivé par défaut.
const { notifier } = useNav()
function changer(nom: string, droit: 'creer' | 'publier', v: boolean) {
  const a = db.organisme.agents.find(x => x.nom === nom)
  if (a) {
    a[droit] = v
    sauvegarder()
    notifier(`${nom} : droit « ${droit === 'creer' ? 'Créer des offres' : 'Publier des offres'} » ${v ? 'donné' : 'retiré'}.`)
  }
}
</script>

<template>
  <PageAts
    actif="parametres"
    titre="Paramètres de l'organisme"
    :sous-titre="`${db.organisme.nom} · réservé au Superviseur (${db.organisme.superviseur})`"
    :fil="[{ label: 'Paramètres de l\'organisme' }]"
  >
    <Panel
      titre="Droits des agents"
      description="Deux droits indépendants : un agent peut avoir l'un, l'autre, les deux ou aucun. Le créateur d'une offre en devient Responsable."
    >
      <table class="droits">
        <thead>
          <tr>
            <th scope="col">
              Agent
            </th>
            <th scope="col">
              Créer des offres
            </th>
            <th scope="col">
              Publier des offres
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="a in db.organisme.agents"
            :key="a.nom"
          >
            <th scope="row">
              {{ a.nom }}
            </th>
            <td>
              <CspSwitch
                :model-value="a.creer"
                :label="`${a.nom} peut créer des offres`"
                hide-label
                @update:model-value="(v: boolean) => changer(a.nom, 'creer', v)"
              />
            </td>
            <td>
              <CspSwitch
                :model-value="a.publier"
                :label="`${a.nom} peut publier des offres`"
                hide-label
                @update:model-value="(v: boolean) => changer(a.nom, 'publier', v)"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </Panel>

    <Panel
      titre="Processus de recrutement"
      description="Étapes appliquées par défaut à chaque offre. Elles peuvent être adaptées offre par offre."
    >
      <ol class="etapes">
        <li
          v-for="e in db.organisme.etapesRecrutement"
          :key="e"
        >
          {{ e }}
        </li>
      </ol>
    </Panel>

    <Panel
      titre="Avant la publication : autorisation de recrutement"
      description="Désactivée : les offres passent directement du brouillon à la publication. Le circuit d'autorisation sera prototypé dans un second temps."
    >
      <CspSwitch
        :model-value="false"
        label="Faire autoriser les offres avant publication"
        disabled
      />
    </Panel>
  </PageAts>
</template>

<style scoped lang="scss">
.droits {
  width: 100%;
  max-width: 40rem;
  border-collapse: collapse;
  font-size: var(--csp-font-size-sm);

  th,
  td {
    padding: var(--csp-space-2) var(--csp-space-3);
    border-bottom: 1px solid var(--border-default-grey);
    text-align: left;
  }

  thead th {
    color: var(--text-mention-grey);
    font-weight: 600;
  }

  tbody th {
    font-weight: 600;
  }
}

.etapes {
  margin: 0;
  padding-left: var(--csp-space-5);
  font-size: var(--csp-font-size-sm);
}
</style>
