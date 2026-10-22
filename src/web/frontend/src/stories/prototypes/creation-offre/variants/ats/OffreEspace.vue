<script setup lang="ts">
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import Panel from '../../shared/Panel.vue'
import CircuitValidation from './CircuitValidation.vue'
import CycleOffre from './CycleOffre.vue'
import EtatBadge from './EtatBadge.vue'
import { useNav } from './nav'
import OffreLecture from './OffreLecture.vue'
import OrigineBadge from './OrigineBadge.vue'
import PageAts from './PageAts.vue'
import { archiverOffre, arreterSupport, CANAUX_DIFFUSION, db, le, sauvegarder } from './store'

// Page d'une offre : son suivi. L'offre est affichée remplie ; on peut la modifier (formulaire, page entière)
// ou l'afficher comme les candidats. Un encart propose l'action de l'étape en cours, dont la publication.
const props = defineProps<{ id: string }>()
const { aller, notifier } = useNav()

const o = computed(() => db.offres.find(x => x.id === props.id)!)
const f = computed(() => db.fiches.find(x => x.id === o.value.ficheId)!)
// Ni modifiable ni publiable pendant la validation ; plus modifiable une fois publiée ou archivée.
const modifiable = computed(() => o.value.etat === 'redaction' || o.value.etat === 'a_publier')

// Informations sous le titre, comme sur la page d'un recrutement de l'application.
const meta = computed(() => [
  { icon: 'ri:calendar-line', srLabel: 'Date de création', label: `Créée ${/^\d/.test(o.value.creeLe) ? `le ${o.value.creeLe}` : o.value.creeLe.toLowerCase()}` },
  { icon: 'ri:map-pin-2-line', srLabel: 'Localisation', label: o.value.lieu || 'Lieu à préciser' },
  { icon: 'ri:government-line', srLabel: 'Organisme', label: db.organisme.nom },
  ...(o.value.categorie ? [{ icon: 'ri:price-tag-3-line', srLabel: 'Catégorie', label: `Catégorie ${o.value.categorie}` }] : []),
  { icon: 'ri:group-line', srLabel: 'Postes', label: `${o.value.nbPostes} poste${Number(o.value.nbPostes) > 1 ? 's' : ''}` },
])
const menu = computed(() => [{
  items: [
    { label: 'Voir la fiche de poste', icon: 'ri:file-text-line', onSelect: () => aller({ nom: 'fiche', id: f.value.id }) },
    { label: 'Dupliquer l’offre', icon: 'ri:file-copy-2-line', onSelect: () => aller({ nom: 'creation', mode: 'duplication', offreId: o.value.id }) },
  ],
}])

const publies = computed(() => CANAUX_DIFFUSION.filter(c => o.value.publications[c.id]))
function arreter(id: string) {
  arreterSupport(o.value, id)
  notifier('Publication arrêtée sur ce site (simulation).')
}
function archiver() {
  archiverOffre(o.value)
  notifier('Offre archivée. Elle reste consultable et peut être dupliquée.')
}

const FREQ = [
  { value: 'chaque', label: 'À chaque candidature' },
  { value: 'cinq', label: 'Toutes les 5 candidatures' },
  { value: 'quotidien', label: 'Un récapitulatif par jour' },
  { value: 'aucune', label: 'Jamais' },
]
</script>

<template>
  <PageAts
    actif="offres"
    largeur="full"
    :titre="o.titre || 'Offre sans titre'"
    :fil="[{ label: 'Offres d\'emploi', to: '/offres' }, { label: o.titre || o.id }]"
    :retour="{ to: '/offres', label: 'Retour aux offres d\'emploi' }"
  >
    <template #meta>
      <div class="meta">
        <EtatBadge :etat="o.etat" />
        <CspMetaList :items="meta" />
      </div>
    </template>
    <template #actions>
      <CspButton
        label="Afficher comme les candidats"
        variant="tertiary"
        icon="ri:eye-line"
        is-icon-left
        @click="aller({ nom: 'apercu', id: o.id })"
      />
      <CspButton
        v-if="modifiable"
        label="Modifier"
        variant="secondary"
        icon="ri:pencil-line"
        is-icon-left
        @click="aller({ nom: 'formulaire', id: o.id })"
      />
      <CspDropdownMenu
        :sections="menu"
        side="bottom"
        align="end"
      >
        <template #trigger>
          <CspButton
            icon="ri:more-fill"
            variant="tertiary"
            size="sm"
            aria-label="Actions sur l’offre"
          />
        </template>
      </CspDropdownMenu>
    </template>

    <CycleOffre :offre="o" />

    <!-- Encart de l'étape en cours -->
    <Panel
      v-if="o.etat === 'redaction' && o.darStatut === 'refusee'"
      class="encart encart--attention"
      titre="Offre refusée"
      :description="`Refusée par ${o.remarqueDar}. Corrigez l'offre puis renvoyez-la pour validation.`"
    >
      <div>
        <CspButton
          label="Corriger l'offre"
          icon="ri:pencil-line"
          is-icon-left
          @click="aller({ nom: 'formulaire', id: o.id })"
        />
      </div>
    </Panel>
    <Panel
      v-else-if="o.etat === 'redaction'"
      class="encart"
      titre="Brouillon"
      :description="o.dar === 'requise' ? 'Complétez le formulaire puis envoyez l\'offre pour validation (votre organisme l\'exige).' : 'Complétez le formulaire puis créez l\'offre.'"
    >
      <div>
        <CspButton
          label="Reprendre le formulaire"
          icon="ri:pencil-line"
          is-icon-left
          @click="aller({ nom: 'formulaire', id: o.id })"
        />
      </div>
    </Panel>
    <Panel
      v-else-if="o.etat === 'validation'"
      class="encart"
      titre="En attente de validation"
      :description="`Envoyée ${le(o.darSoumiseLe)}. Tant que la validation n'est pas terminée, l'offre ne peut être ni modifiée ni publiée.`"
    >
      <CircuitValidation :offre="o" />
    </Panel>
    <Panel
      v-else-if="o.etat === 'a_publier'"
      class="encart encart--action"
      titre="Prête à être publiée"
      :description="o.dar === 'requise' ? `Validation terminée ${le(o.darValideeLe)}. L'offre n'est jamais publiée automatiquement : c'est vous qui décidez.` : 'L\'offre n\'est jamais publiée automatiquement : c\'est vous qui décidez.'"
    >
      <div>
        <CspButton
          label="Publier"
          icon="ri:send-plane-line"
          is-icon-left
          @click="aller({ nom: 'apercu', id: o.id, publier: true })"
        />
      </div>
    </Panel>
    <Panel
      v-else-if="o.etat === 'publiee'"
      class="encart encart--action"
      titre="Publication"
      :description="`${o.diffusion === 'multi' ? 'Multi-diffusion' : 'Simple diffusion'} · publiée ${le(o.publieeLe)} · candidatures jusqu'au ${o.dateLimite || '-'}.`"
    >
      <table class="supports">
        <thead>
          <tr>
            <th scope="col">
              Site
            </th>
            <th scope="col">
              État
            </th>
            <th scope="col">
              Depuis
            </th>
            <th scope="col">
              <span class="sr-only">Action</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="c in publies"
            :key="c.id"
          >
            <td>{{ c.nom }}<small>{{ c.detail }}</small></td>
            <td>
              <span
                class="etat"
                :class="{ 'etat--on': o.publications[c.id]?.etat === 'publiee' }"
              >{{ o.publications[c.id]?.etat === 'publiee' ? 'En ligne' : 'Arrêtée' }}</span>
            </td>
            <td>{{ o.publications[c.id]?.debut }}</td>
            <td class="droite">
              <CspButton
                v-if="o.publications[c.id]?.etat === 'publiee'"
                label="Arrêter"
                size="sm"
                variant="tertiary-no-outline"
                @click="arreter(c.id)"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <div>
        <CspButton
          label="Arrêter les publications et archiver"
          variant="secondary"
          icon="ri:archive-line"
          is-icon-left
          @click="archiver"
        />
      </div>
    </Panel>
    <Panel
      v-else
      class="encart"
      titre="Offre archivée"
      description="Elle n'est plus visible des candidats. Son contenu peut servir de base à un nouveau recrutement."
    >
      <div>
        <CspButton
          label="Dupliquer cette offre"
          variant="secondary"
          icon="ri:file-copy-2-line"
          is-icon-left
          @click="aller({ nom: 'creation', mode: 'duplication', offreId: o.id })"
        />
      </div>
    </Panel>

    <div class="grille">
      <div class="col">
        <OffreLecture :offre="o" />
      </div>
      <aside class="col">
        <Panel titre="Fiche de poste rattachée">
          <div class="fiche">
            <div>
              <strong>{{ f.intitule }}</strong>
              <p class="mention">
                {{ f.id }} · {{ f.service }}
              </p>
            </div>
            <OrigineBadge
              :origine="f.origine"
              court
            />
          </div>
          <div>
            <CspButton
              label="Ouvrir la fiche de poste"
              variant="secondary"
              size="sm"
              @click="aller({ nom: 'fiche', id: f.id })"
            />
          </div>
        </Panel>

        <Panel
          v-if="o.validations?.length && o.etat !== 'validation'"
          titre="Circuit de validation"
        >
          <CircuitValidation :offre="o" />
        </Panel>

        <Panel
          v-if="o.etat === 'publiee'"
          titre="Mes notifications"
        >
          <CspRadioGroup
            v-model="o.notifications"
            label="Courriel pour les nouvelles candidatures"
            :options="FREQ"
            size="sm"
            @update:model-value="sauvegarder"
          />
        </Panel>

        <Panel titre="Historique">
          <ol class="histo">
            <li
              v-for="(h, i) in [...o.historique].reverse()"
              :key="i"
            >
              <small>{{ h.date }}</small>{{ h.texte }}
            </li>
          </ol>
        </Panel>
      </aside>
    </div>
  </PageAts>
</template>

<style scoped lang="scss">
.meta {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);

  > :last-child {
    flex: 1;
  }
}

.encart {
  border-left: 4px solid var(--border-plain-grey);

  &--action {
    border-left-color: var(--border-plain-blue-france);
  }

  &--attention {
    border-left-color: var(--border-plain-warning);
  }
}

.grille {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 21rem;
  gap: var(--csp-space-5);
  align-items: start;
}

.col {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.fiche {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--csp-space-3);
}

.mention {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.supports {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--csp-font-size-sm);

  th,
  td {
    padding: var(--csp-space-2);
    border-bottom: 1px solid var(--border-default-grey);
    text-align: left;
    vertical-align: middle;
  }

  thead th {
    font-size: var(--csp-font-size-xs);
    font-weight: var(--csp-font-weight-medium);
    color: var(--text-mention-grey);
  }

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.droite {
  text-align: right !important;
}

.etat {
  color: var(--text-mention-grey);

  &--on {
    color: var(--text-default-success);
    font-weight: var(--csp-font-weight-bold);
  }
}

.histo {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: var(--csp-font-size-sm);

  li {
    padding-left: var(--csp-space-3);
    border-left: 2px solid var(--border-default-grey);
  }

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
