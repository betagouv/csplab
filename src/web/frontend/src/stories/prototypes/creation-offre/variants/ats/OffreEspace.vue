<script setup lang="ts">
import type { EtapeFormulaire } from './aide'
import { computed, ref } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import Panel from '../../shared/Panel.vue'
import { manquesPublication } from './aide'
import BlocValidation from './BlocValidation.vue'
import CycleOffre from './CycleOffre.vue'
import DemandeValidation from './DemandeValidation.vue'
import EtatBadge from './EtatBadge.vue'
import { useNav } from './nav'
import OffreLecture from './OffreLecture.vue'
import OrigineBadge from './OrigineBadge.vue'
import PageAts from './PageAts.vue'
import ResumeValidation from './ResumeValidation.vue'
import { archiverOffre, arreterSupport, aujourdhui, CANAUX_DIFFUSION, dateLongue, db, joursRestants, le, plusJours, plusUnMois, prolonger, retirer, sauvegarder, UTILISATEUR, validationManquante } from './store'
import ValidationBadge from './ValidationBadge.vue'

// Page d'une offre (« Détails de l'offre ») : l'offre remplie, son suivi et l'action de l'étape en cours.
// On peut modifier l'offre avant et après publication ; pendant la validation aussi.
const props = defineProps<{ id: string }>()
const { aller, notifier } = useNav()

const o = computed(() => db.offres.find(x => x.id === props.id)!)
const f = computed(() => db.fiches.find(x => x.id === o.value.ficheId)!)
const modifiable = computed(() => o.value.etat === 'brouillon' || o.value.etat === 'publiee')
const manques = computed(() => manquesPublication(o.value))
const prete = computed(() => o.value.etat === 'brouillon' && !manques.value.length && !validationManquante(o.value))
const peutPublier = computed(() => db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier)
function modifier(etape?: EtapeFormulaire) {
  aller({ nom: 'formulaire', id: o.value.id, etape })
}

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

// --- Publication en cours : prolonger, retirer, arrêter un site ---
const restants = computed(() => (o.value.dateFin ? joursRestants(o.value.dateFin) : 0))
const publies = computed(() => CANAUX_DIFFUSION.filter(c => o.value.publications[c.id]))
const prolongation = ref(false)
const nouvelleFin = ref('')
function ouvrirProlongation() {
  nouvelleFin.value = plusJours(o.value.dateFin, 15)
  prolongation.value = true
}
function confirmerProlongation() {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(nouvelleFin.value) || nouvelleFin.value <= o.value.dateFin) {
    return
  }
  prolonger(o.value, nouvelleFin.value)
  prolongation.value = false
  notifier(`Publication prolongée jusqu'au ${dateLongue(nouvelleFin.value)}, sans nouvelle validation.`)
}
// Retirer avant un mois de publication : seulement en cas d'urgence.
const retrait = ref(false)
const urgence = ref(false)
const avantUnMois = computed(() => Boolean(o.value.dateDebut) && plusUnMois(o.value.dateDebut) > aujourdhui())
function confirmerRetrait() {
  if (avantUnMois.value && !urgence.value) {
    return
  }
  retirer(o.value, avantUnMois.value ? 'urgence' : 'manuel')
  retrait.value = false
  notifier('Offre retirée. Les candidatures reçues restent à traiter.')
}
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
        <ValidationBadge
          v-if="db.organisme.validationActive || o.validationEtat !== 'non_demandee'"
          :offre="o"
        />
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
        @click="modifier()"
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
    <template v-if="o.etat === 'brouillon'">
      <Panel
        v-if="prete"
        class="encart encart--action"
        titre="Prête à être publiée"
        :description="db.organisme.validationActive ? `Validation obtenue ${le(o.validationObtenueLe)} et annonce complète. L'offre n'est jamais publiée automatiquement.` : 'Annonce complète. L\'offre n\'est jamais publiée automatiquement.'"
      >
        <div v-if="peutPublier">
          <CspButton
            label="Publier"
            icon="ri:send-plane-line"
            is-icon-left
            @click="aller({ nom: 'apercu', id: o.id, publier: true })"
          />
        </div>
        <p
          v-else
          class="texte"
        >
          Vous n'avez pas le droit « Publier » : une personne habilitée publiera l'offre.
        </p>
      </Panel>
      <Panel
        v-else-if="o.validationEtat === 'refusee'"
        class="encart encart--attention"
        titre="Validation refusée"
        description="Complétez l'offre puis redemandez la validation. Les accords déjà donnés restent acquis."
      >
        <BlocValidation :offre="o" />
        <div class="actions">
          <CspButton
            label="Compléter l'offre"
            variant="secondary"
            icon="ri:pencil-line"
            is-icon-left
            @click="modifier()"
          />
          <DemandeValidation
            :offre="o"
            variant="primary"
          />
        </div>
      </Panel>
      <Panel
        v-else-if="o.validationEtat === 'en_attente'"
        class="encart"
        titre="Validation en cours"
        :description="`Demandée ${le(o.validationDemandeeLe)}. Vous pouvez continuer à modifier l'offre en attendant.`"
      >
        <BlocValidation
          :offre="o"
          simulation
        />
      </Panel>
      <Panel
        v-else
        class="encart"
        :titre="o.validationEtat === 'validee' ? 'Validée — à compléter avant publication' : 'Brouillon'"
        :description="validationManquante(o) ? 'Votre organisme fait valider les offres avant publication. Vous pouvez demander la validation à tout moment, sans attendre que l\'offre soit complète.' : 'Pour publier, l\'annonce doit être complète.'"
      >
        <ul
          v-if="manques.length"
          class="manques"
        >
          <li
            v-for="m in manques"
            :key="m.label"
          >
            {{ m.label }}
            <button
              type="button"
              class="lien"
              @click="modifier(m.etape)"
            >
              Compléter
            </button>
          </li>
        </ul>
        <div class="actions">
          <CspButton
            label="Reprendre le formulaire"
            variant="secondary"
            icon="ri:pencil-line"
            is-icon-left
            @click="modifier()"
          />
          <DemandeValidation
            :offre="o"
            variant="primary"
          />
        </div>
      </Panel>
    </template>

    <Panel
      v-else-if="o.etat === 'publiee'"
      class="encart encart--action"
      titre="En ligne"
      :description="`Du ${dateLongue(o.dateDebut)} au ${dateLongue(o.dateFin)}, date limite de candidature. Retrait automatique ce jour-là.`"
    >
      <p
        v-if="restants <= 7"
        class="alerte"
      >
        Se termine {{ restants <= 0 ? 'aujourd\'hui' : `dans ${restants} jour${restants > 1 ? 's' : ''}` }}.
      </p>
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
                v-if="o.publications[c.id]?.etat === 'publiee' && c.id !== 'csp'"
                label="Arrêter"
                size="sm"
                variant="tertiary-no-outline"
                @click="arreter(c.id)"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <div
        v-if="prolongation"
        class="prolonger"
      >
        <CspInput
          v-model="nouvelleFin"
          label="Nouvelle date limite"
          placeholder="AAAA-MM-JJ"
          :hint="dateLongue(nouvelleFin)"
        />
        <CspButton
          label="Prolonger"
          @click="confirmerProlongation"
        />
        <CspButton
          label="Annuler"
          variant="tertiary-no-outline"
          @click="prolongation = false"
        />
      </div>
      <div
        v-else
        class="actions"
      >
        <CspButton
          label="Prolonger"
          variant="secondary"
          icon="ri:calendar-line"
          is-icon-left
          @click="ouvrirProlongation"
        />
        <CspButton
          label="Retirer l'offre"
          variant="tertiary"
          icon="ri:stop-circle-line"
          is-icon-left
          @click="retrait = true"
        />
      </div>
    </Panel>

    <Panel
      v-else-if="o.etat === 'retiree'"
      class="encart"
      titre="Retirée"
      :description="`Retirée ${le(o.retireeLe)}. Retirer l'offre ne clôt pas le recrutement : les candidatures restent à traiter.`"
    >
      <div>
        <CspButton
          label="Archiver l'offre"
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
        <OffreLecture
          :offre="o"
          :modifiable="modifiable"
          @modifier="modifier"
        />
      </div>
      <aside class="col">
        <ResumeValidation
          v-if="db.organisme.validationActive || o.validationEtat !== 'non_demandee'"
          :offre="o"
          :fiche="f"
          compact
        />
        <Panel
          v-if="o.validations?.length && o.etat !== 'brouillon'"
          titre="Validation"
        >
          <BlocValidation :offre="o" />
        </Panel>
        <Panel
          v-else-if="o.validationEtat === 'validee'"
          titre="Validation"
        >
          <CspBadge
            v-if="o.modifieeDepuisValidation"
            label="Modifiée depuis la validation"
            type="warning"
            variant="soft"
            size="sm"
          />
          <BlocValidation :offre="o" />
        </Panel>

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

        <Panel titre="Journal d'activité">
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

    <CspDialog
      v-model:open="retrait"
      title="Retirer l'offre ?"
      size="sm"
    >
      <p class="texte">
        L'offre ne sera plus visible des candidats. Les candidatures déjà reçues restent à traiter.
      </p>
      <CspCheckbox
        v-if="avantUnMois"
        v-model="urgence"
        label="L'offre est en ligne depuis moins d'un mois : je confirme qu'il s'agit d'une urgence"
      />
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="retrait = false"
        />
        <CspButton
          label="Retirer l'offre"
          :disabled="avantUnMois && !urgence"
          @click="confirmerRetrait"
        />
      </template>
    </CspDialog>
  </PageAts>
</template>

<style scoped lang="scss">
.meta {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);

  > :last-child {
    flex: 1;
    margin-left: var(--csp-space-2);
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

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
}

.prolonger {
  display: grid;
  grid-template-columns: minmax(0, 16rem) auto auto;
  gap: var(--csp-space-2);
  align-items: end;
  justify-content: start;
}

.alerte {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-default-warning);
}

.texte {
  margin: 0 0 var(--csp-space-3);
  font-size: var(--csp-font-size-sm);
}

.manques {
  margin: 0;
  padding-left: var(--csp-space-5);
  font-size: var(--csp-font-size-sm);
}

.lien {
  margin-left: var(--csp-space-2);
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
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
