<script setup lang="ts">
import type { Ecran } from './nav'
import type { Offre } from './store'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import CspTagGroup from '@/components/base/CspTag/CspTagGroup.vue'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { manquesPublication } from './aide'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { aValiderParMoi, db, fiche, joursRestants } from './store'
import { statutListe } from './suivi'

// « Mes offres d'emploi » : uniquement les offres qui ne sont pas encore publiées, en cartes (même modèle que
// « Mes offres sauvegardées » côté candidat), filtrées par puces selon ce qu'il y a à faire.
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
  icone: string
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
      icone: 'ri:checkbox-circle-line',
      titre: 'À valider par vous',
      aide: 'On vous demande votre avis avant publication.',
      offres: moi,
      action: o => ({ label: 'Valider ou refuser', ecran: offre(o), principal: true }),
      detail: o => `Demandée par ${o.creePar ?? '—'}`,
    },
    {
      id: 'validation_refusee',
      icone: 'ri:error-warning-line',
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
      icone: 'ri:send-plane-line',
      titre: 'Prêtes à publier',
      aide: 'Complètes et validées : il ne reste qu\'à publier. La publication ouvre le recrutement.',
      offres: autres.filter(o => statutListe(o) === 'prete'),
      action: o => ({ label: 'Publier', ecran: { nom: 'apercu', id: o.id, publier: true }, principal: true }),
      detail: o => o.validationEtat === 'validee' ? `Validée ${o.validationObtenueLe ? `le ${o.validationObtenueLe}` : ''}` : 'Sans validation requise',
    },
    {
      id: 'brouillon',
      icone: 'ri:edit-line',
      titre: 'En rédaction',
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
      icone: 'ri:time-line',
      titre: 'En attente de validation',
      aide: 'Rien à faire pour l\'instant : vous serez prévenu·e des réponses.',
      offres: autres.filter(o => statutListe(o) === 'validation_attente'),
      detail: avis,
    },
  ]
})
const visibles = computed(() => groupes.value.filter(g => g.offres.length))
const total = computed(() => trouvees.value.length)

// Puces : « Toutes » puis un filtre par chose à faire. « Toutes » garde l'ordre d'urgence (l'attente en dernier).
const DEPUIS_ACCUEIL: Record<string, string> = { a_publier: 'prete', en_attente: 'en_attente', brouillon: 'brouillon', validation_refusee: 'validation_refusee' }
const puce = ref<string | undefined>((props.filtre && DEPUIS_ACCUEIL[props.filtre]) || 'toutes')
// Recliquer la puce active la désélectionne : on revient à « Toutes ».
watch(puce, (v) => {
  if (!v) {
    puce.value = 'toutes'
  }
})
const cartes = computed(() => visibles.value
  .filter(g => !puce.value || puce.value === 'toutes' || g.id === puce.value)
  .flatMap(g => g.offres.map(o => ({ o, g }))))

// Relais vers les recrutements : les offres publiées ces 30 derniers jours.
const publieesRecemment = computed(() => db.offres.filter(o => o.etat === 'publiee' && o.dateDebut && joursRestants(o.dateDebut) >= -30))
</script>

<template>
  <PageAts
    actif="offres"
    titre="Mes offres d'emploi"
    sous-titre="Retrouvez toutes vos offres d'emploi en préparation. Une fois publiée, une offre devient un recrutement et vous pourrez y gérer toutes vos candidatures."
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

    <CspTagGroup
      v-model="puce"
      type="single"
      size="sm"
      aria-label="Filtrer les offres"
    >
      <CspTag
        variant="selectable"
        value="toutes"
        :label="`Toutes (${total})`"
      />
      <CspTag
        v-for="g in visibles"
        :key="g.id"
        variant="selectable"
        :value="g.id"
        :label="`${g.titre} (${g.offres.length})`"
      />
    </CspTagGroup>

    <p
      v-if="!cartes.length"
      class="vide"
    >
      {{ search ? 'Aucune offre ne correspond à votre recherche.' : 'Aucune offre en préparation.' }}
    </p>

    <ul
      v-else
      class="cartes"
    >
      <li
        v-for="{ o, g } in cartes"
        :key="o.id"
        class="carte"
        :class="`carte--${g.id}`"
      >
        <div class="carte__texte">
          <h2 class="carte__titre">
            <button
              type="button"
              class="carte__lien"
              @click="aller({ nom: 'offre', id: o.id })"
            >
              {{ o.titre || 'Sans titre' }}
            </button>
          </h2>
          <p class="carte__sous">
            {{ o.id }} · {{ o.ficheId ? `Fiche ${o.ficheId}` : 'Sans fiche de poste' }}
          </p>
          <p class="carte__etat">
            <CspIcon
              :name="g.icone"
              :size="14"
            />
            <span><strong>{{ g.titre }}</strong> · {{ g.detail(o) }}</span>
          </p>
        </div>
        <CspButton
          v-if="g.action"
          class="carte__action"
          :label="g.action(o).label"
          size="sm"
          :variant="g.action(o).principal ? 'primary' : 'secondary'"
          @click="aller(g.action(o).ecran)"
        />
        <CspIcon
          v-else
          class="carte__chevron"
          name="ri:arrow-right-s-line"
          :size="24"
        />
      </li>
    </ul>

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

.cartes {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  margin: 0;
  padding: 0;
  list-style: none;
}

.carte {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-4);
  padding: var(--csp-space-5);
  border: 1px solid var(--border-default-grey);
  border-radius: 4px;
  background: var(--background-default-grey);

  &:hover {
    background: var(--background-default-grey-hover);
  }
}

.carte__texte {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  min-width: 0;
}

.carte__titre {
  margin: 0;
  font-size: 1.25rem;
  line-height: 1.4;
}

// Toute la carte est cliquable (lien étendu) ; le bouton d'action reste au-dessus.
.carte__lien {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
  text-align: left;
  cursor: pointer;

  &::after {
    content: '';
    position: absolute;
    inset: 0;
  }

  &:focus-visible {
    outline: none;

    &::after {
      outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
      outline-offset: 2px;
    }
  }
}

.carte__sous {
  margin: 0;
}

.carte__etat {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);

  :deep(svg) {
    flex-shrink: 0;
    margin-top: 3px;
  }

  strong {
    font-weight: 500;
  }

  .carte--validation_refusee & strong {
    color: var(--text-default-error);
  }

  .carte--prete & strong {
    color: var(--text-default-success);
  }

  .carte--a_valider & strong {
    color: var(--text-action-high-blue-france);
  }
}

.carte__action {
  position: relative;
  z-index: 1;
  flex-shrink: 0;
}

.carte__chevron {
  flex-shrink: 0;
  color: var(--text-action-high-blue-france);
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
