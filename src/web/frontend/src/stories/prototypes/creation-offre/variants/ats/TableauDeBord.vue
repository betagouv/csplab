<script setup lang="ts">
import type { EtatOffre } from './store'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import EtatBadge from './EtatBadge.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { db, fiche, LIBELLES_ETAT, nouvelleFiche } from './store'

// Écran 1 — tableau de bord : accès aux deux espaces et quelques compteurs, sans analytique.
const { aller } = useNav()

const COMPTEURS: { etat: EtatOffre, aide: string }[] = [
  { etat: 'redaction', aide: 'à terminer' },
  { etat: 'validation', aide: 'DAR en attente' },
  { etat: 'a_publier', aide: 'prêtes, non visibles' },
  { etat: 'publiee', aide: 'en ligne' },
]
const n = (e: EtatOffre) => db.offres.filter(o => o.etat === e).length
function creerFiche() {
  const f = nouvelleFiche({}, 'ats', 'Fiche créée dans l\'ATS par Camille Moreau')
  aller({ nom: 'fiche', id: f.id, edition: true })
}
const aTraiter = computed(() => db.offres.filter(o => ['redaction', 'a_publier'].includes(o.etat)))
</script>

<template>
  <PageAts
    actif="accueil"
    titre="Bonjour Camille"
    sous-titre="Vos fiches de poste et vos offres d'emploi."
  >
    <template #actions>
      <CspButton
        label="Lancer un recrutement"
        icon="ri:add-line"
        is-icon-left
        @click="aller({ nom: 'creation' })"
      />
    </template>

    <section
      class="tdb__compteurs"
      aria-label="Offres par état"
    >
      <button
        v-for="c in COMPTEURS"
        :key="c.etat"
        type="button"
        class="tdb__compteur"
        @click="aller({ nom: 'offres', filtre: c.etat })"
      >
        <span class="tdb__nb">{{ n(c.etat) }}</span>
        <span class="tdb__lib">{{ LIBELLES_ETAT[c.etat] }}</span>
        <small>{{ c.aide }}</small>
      </button>
    </section>

    <div class="tdb__grille">
      <section class="tdb__bloc">
        <div class="tdb__bloc-tete">
          <h2 class="tdb__h2">
            Offres à faire avancer
          </h2>
          <CspButton
            label="Toutes les offres"
            variant="tertiary-no-outline"
            size="sm"
            @click="aller({ nom: 'offres' })"
          />
        </div>
        <ul class="tdb__liste">
          <li
            v-for="o in aTraiter"
            :key="o.id"
          >
            <button
              type="button"
              class="tdb__ligne"
              @click="aller({ nom: 'offre', id: o.id })"
            >
              <span>
                <strong>{{ o.titre }}</strong>
                <small>{{ o.id }} · fiche {{ fiche(o.ficheId)?.id }} · {{ o.nbPostes }} poste(s) · modifiée {{ o.modifieLe.toLowerCase() }}</small>
              </span>
              <EtatBadge :etat="o.etat" />
            </button>
          </li>
        </ul>
      </section>

      <section class="tdb__bloc">
        <div class="tdb__bloc-tete">
          <h2 class="tdb__h2">
            Fiches de poste
          </h2>
          <CspButton
            label="Le référentiel"
            variant="tertiary-no-outline"
            size="sm"
            @click="aller({ nom: 'fiches' })"
          />
        </div>
        <p class="tdb__texte">
          {{ db.fiches.filter(f => f.statut === 'active').length }} fiches actives, dont
          {{ db.fiches.filter(f => f.origine === 'sirh').length }} récupérées du SIRH et
          {{ db.fiches.filter(f => f.origine === 'document').length }} issues d'un document.
          Une fiche décrit durablement un poste ; elle sert de base à une ou plusieurs offres.
        </p>
        <CspButton
          label="Nouvelle fiche de poste"
          variant="secondary"
          size="sm"
          icon="ri:add-line"
          is-icon-left
          @click="creerFiche"
        />
      </section>
    </div>
  </PageAts>
</template>

<style scoped lang="scss">
.tdb__compteurs {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.tdb__compteur {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
  padding: var(--csp-space-4) var(--csp-space-5);
  border: 0;
  background: none;
  font: inherit;
  text-align: left;
  color: var(--text-default-grey);
  cursor: pointer;

  & + & {
    border-left: 1px solid var(--border-default-grey);
  }

  &:hover {
    background: var(--background-default-grey-hover);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
    outline-offset: -2px;
  }

  small {
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.tdb__nb {
  font-size: var(--csp-font-size-2xl);
  font-weight: var(--csp-font-weight-bold);
  line-height: 1;
}

.tdb__lib {
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
}

.tdb__grille {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(0, 1fr);
  gap: var(--csp-space-5);
  align-items: start;
}

.tdb__bloc {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-3);
  padding: var(--csp-space-5);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.tdb__bloc-tete {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.tdb__h2 {
  margin: 0;
  font-size: var(--csp-font-size-lg);
}

.tdb__texte {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.tdb__liste {
  width: 100%;
  margin: 0;
  padding: 0;
  list-style: none;
}

.tdb__ligne {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-3);
  width: 100%;
  padding: var(--csp-space-3) 0;
  border: 0;
  border-top: 1px solid var(--border-default-grey);
  background: none;
  font: inherit;
  text-align: left;
  color: var(--text-default-grey);
  cursor: pointer;

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }

  &:hover strong {
    color: var(--text-action-high-blue-france);
  }
}
</style>
