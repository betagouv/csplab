<script setup lang="ts">
import type { Ecran } from './nav'
import type { Offre } from './store'
import { computed, nextTick, onMounted } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { manquesPublication } from './aide'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { aValiderParMoi, db, fiche, joursRestants } from './store'
import { statutListe } from './suivi'

// « Mes offres d'emploi » : uniquement les offres qui ne sont pas encore publiées, rangées par ce qu'il y a à faire.
// Volontairement différent du tableau « Mes recrutements » : une offre publiée devient un recrutement et quitte cette page.
const props = defineProps<{ filtre?: string }>()
const { aller } = useNav()

const enPreparation = computed(() => db.offres.filter(o => o.etat === 'brouillon'))
const { search, filtered: trouvees } = useTextSearch(enPreparation, o => [o.titre, o.id, fiche(o.ficheId)?.intitule])

interface Groupe {
  id: string
  titre: string
  aide: string
  offres: Offre[]
  /** Bouton de la ligne ; absent quand il n'y a rien à faire (on attend). */
  action?: (o: Offre) => { label: string, ecran: Ecran, principal?: boolean }
  detail: (o: Offre) => string
}

const offre = (o: Offre): Ecran => ({ nom: 'offre', id: o.id })
const derniereReponse = (o: Offre) => [...(o.validations ?? [])].reverse().find(v => v.decision === 'refus')
function avis(o: Offre) {
  const v = o.validations ?? []
  const attente = v.filter(x => x.decision === 'attente').map(x => x.nom)
  return `${v.length - attente.length} avis sur ${v.length}${attente.length ? ` · en attente : ${attente.join(', ')}` : ''}`
}

const groupes = computed<Groupe[]>(() => {
  const l = trouvees.value
  const moi = l.filter(aValiderParMoi)
  const autres = l.filter(o => !aValiderParMoi(o))
  return [
    {
      id: 'a_valider',
      titre: 'À valider par vous',
      aide: 'On vous demande votre avis avant publication.',
      offres: moi,
      action: o => ({ label: 'Valider ou refuser', ecran: offre(o), principal: true }),
      detail: o => `Demandée par ${o.creePar ?? '—'}`,
    },
    {
      id: 'validation_refusee',
      titre: 'À corriger',
      aide: 'La validation a été refusée : corrigez puis redemandez-la.',
      offres: autres.filter(o => statutListe(o) === 'validation_refusee'),
      action: o => ({ label: 'Corriger l\'offre', ecran: offre(o), principal: true }),
      detail: (o) => {
        const r = derniereReponse(o)
        return r ? `Refusée par ${r.par} (${r.nom})${r.commentaire ? ` : « ${r.commentaire} »` : ''}` : 'Validation refusée'
      },
    },
    {
      id: 'prete',
      titre: 'Prêtes à publier',
      aide: 'Complètes et validées : il ne reste qu\'à publier. La publication ouvre le recrutement.',
      offres: autres.filter(o => statutListe(o) === 'prete'),
      action: o => ({ label: 'Publier', ecran: { nom: 'apercu', id: o.id, publier: true }, principal: true }),
      detail: o => o.validationEtat === 'validee' ? `Validée ${o.validationObtenueLe ? `le ${o.validationObtenueLe}` : ''}` : 'Sans validation requise',
    },
    {
      id: 'brouillon',
      titre: 'En cours de rédaction',
      aide: 'Brouillons à terminer.',
      offres: autres.filter(o => statutListe(o) === 'brouillon'),
      action: o => ({ label: 'Reprendre', ecran: offre(o) }),
      detail: (o) => {
        const n = manquesPublication(o).length
        return n ? `${n} élément${n > 1 ? 's' : ''} à compléter` : 'Annonce complète, validation à demander'
      },
    },
    {
      id: 'en_attente',
      titre: 'En attente de validation',
      aide: 'Rien à faire pour l\'instant : vous serez prévenu·e des réponses.',
      offres: autres.filter(o => statutListe(o) === 'validation_attente'),
      detail: avis,
    },
  ]
})
const visibles = computed(() => groupes.value.filter(g => g.offres.length))
const total = computed(() => trouvees.value.length)

// Relais vers les recrutements : les offres publiées ces 30 derniers jours.
const publieesRecemment = computed(() => db.offres.filter(o => o.etat === 'publiee' && o.dateDebut && joursRestants(o.dateDebut) >= -30))

// Accès direct depuis le tableau de bord : on descend jusqu'au groupe demandé.
const ANCRES: Record<string, string> = { a_publier: 'prete', en_attente: 'en_attente', brouillon: 'brouillon', validation_refusee: 'validation_refusee' }
onMounted(async () => {
  const id = props.filtre && ANCRES[props.filtre]
  if (id) {
    await nextTick()
    document.getElementById(`groupe-${id}`)?.scrollIntoView({ block: 'start' })
  }
})
</script>

<template>
  <PageAts
    actif="offres"
    titre="Mes offres d'emploi"
    sous-titre="Les offres en préparation, jusqu'à leur publication. Une fois publiée, une offre devient un recrutement."
    :fil="[{ label: 'Mes offres d\'emploi' }]"
  >
    <template #actions>
      <CspButton
        label="Créer une offre"
        size="sm"
        icon="ri:add-line"
        is-icon-left
        @click="aller({ nom: 'creation' })"
      />
    </template>

    <div class="barre">
      <p class="compte">
        {{ total }} offre{{ total > 1 ? 's' : '' }} en préparation
      </p>
      <CspSearchBar
        v-model="search"
        mode="live"
        label="Rechercher une offre"
        hide-label
        placeholder="Rechercher un intitulé d'offre, une référence"
        class="recherche"
      />
    </div>

    <p
      v-if="!visibles.length"
      class="vide"
    >
      {{ search ? 'Aucune offre ne correspond à votre recherche.' : 'Aucune offre en préparation.' }}
    </p>

    <section
      v-for="g in visibles"
      :id="`groupe-${g.id}`"
      :key="g.id"
      class="groupe"
      :class="`groupe--${g.id}`"
      :aria-labelledby="`titre-${g.id}`"
    >
      <header class="groupe__tete">
        <h2
          :id="`titre-${g.id}`"
          class="groupe__titre"
        >
          {{ g.titre }} <span class="groupe__nb">{{ g.offres.length }}</span>
        </h2>
        <p class="groupe__aide">
          {{ g.aide }}
        </p>
      </header>
      <ul class="lignes">
        <li
          v-for="o in g.offres"
          :key="o.id"
          class="ligne"
        >
          <div class="ligne__texte">
            <button
              type="button"
              class="ligne__titre"
              @click="aller({ nom: 'offre', id: o.id })"
            >
              {{ o.titre || 'Sans titre' }}
            </button>
            <p class="ligne__meta">
              {{ o.id }} · {{ o.ficheId ? `fiche ${o.ficheId}` : 'sans fiche de poste' }} · modifiée {{ o.modifieLe.toLowerCase() }}
            </p>
            <p class="ligne__detail">
              {{ g.detail(o) }}
            </p>
          </div>
          <CspButton
            v-if="g.action"
            :label="g.action(o).label"
            size="sm"
            :variant="g.action(o).principal ? 'primary' : 'secondary'"
            @click="aller(g.action(o).ecran)"
          />
        </li>
      </ul>
    </section>

    <aside
      v-if="!search"
      class="relais"
    >
      <div>
        <p class="relais__titre">
          Offres publiées : elles sont devenues des recrutements
        </p>
        <p class="relais__texte">
          {{ publieesRecemment.length ? `${publieesRecemment.length} offre${publieesRecemment.length > 1 ? 's publiées' : ' publiée'} ces 30 derniers jours.` : 'Aucune offre publiée ces 30 derniers jours.' }}
          Candidatures, prolongation et retrait se gèrent dans Mes recrutements.
        </p>
      </div>
      <CspButton
        label="Voir mes recrutements"
        size="sm"
        variant="tertiary"
        icon="ri:arrow-right-line"
        @click="aller({ nom: 'recrutements' })"
      />
    </aside>
  </PageAts>
</template>

<style scoped lang="scss">
.barre {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-4);
}

.compte {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}

.recherche {
  min-width: 20rem;
}

.vide {
  margin: 0;
  font-style: italic;
  color: var(--text-mention-grey);
}

.groupe {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  scroll-margin-top: var(--csp-space-4);
}

.groupe__titre {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: 1.25rem;
  line-height: 1.3;
}

.groupe__nb {
  display: inline-flex;
  justify-content: center;
  min-width: 1.75rem;
  padding: 0 var(--csp-space-2);
  border-radius: 1rem;
  background: var(--background-contrast-grey);
  font-size: var(--csp-font-size-sm);
}

.groupe__aide {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.lignes {
  margin: 0;
  padding: 0;
  list-style: none;
  border: 1px solid var(--border-default-grey);
  border-left: 4px solid var(--border-default-grey);
  background: var(--background-default-grey);

  .groupe--a_valider & {
    border-left-color: var(--border-plain-blue-france);
  }

  .groupe--validation_refusee & {
    border-left-color: var(--border-plain-error);
  }

  .groupe--prete & {
    border-left-color: var(--border-plain-success);
  }
}

.ligne {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-4);
  padding: var(--csp-space-4) var(--csp-space-5);

  & + & {
    border-top: 1px solid var(--border-default-grey);
  }
}

.ligne__texte {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.ligne__titre {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
  text-align: left;
  cursor: pointer;

  &:hover {
    text-decoration: underline;
  }
}

.ligne__meta,
.ligne__detail {
  margin: 0;
  font-size: var(--csp-font-size-sm);
}

.ligne__meta {
  color: var(--text-mention-grey);
}

.relais {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-4);
  padding: var(--csp-space-4) var(--csp-space-5);
  border: 1px dashed var(--border-default-grey);
}

.relais__titre {
  margin: 0;
  font-weight: var(--csp-font-weight-bold);
}

.relais__texte {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}
</style>
