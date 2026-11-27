<script setup lang="ts">
import type { GroupeOffre, PartieOffre } from './etapes'
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { computed, nextTick, ref, watch } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import { champsObligatoires } from './aide'
import ApercuCandidat from './ApercuCandidat.vue'
import BlocEtape from './BlocEtape.vue'
import ChampDate from './ChampDate.vue'
import { dupliquer } from './dupliquer'
import { ETAPES_OFFRE, groupeDe, GROUPES } from './etapes'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { candidatures } from './recrutement'
import { aujourdhui, CANAUX_DIFFUSION, dateLongue, db, heure, joursRestants, le, noterModification, plusJours, prolonger, retirer, sauvegarder, UTILISATEUR } from './store'

// Page d'une offre, hors création (retour Alice du 25/11/2026), structurée comme un profil Malt : l'en-tête, le bloc
// des champs qui restent à remplir, puis des onglets (revue UI, 27/11/2026) : les trois parties de la création
// (Annonce, Paramètres du recrutement, Diffusion) et l'Activité. Un bloc par étape. Chaque bloc se modifie à part, avec le crayon.
// En préparation → En ligne → En pause (date de fin ou mise en pause) → En ligne (remise en ligne). Publier, prolonger et mettre en pause
// demandent le droit « Publier ».
const props = defineProps<{ id: string, section?: string }>()
const { aller, notifier } = useNav()
const o = computed(() => db.offres.find(x => x.id === props.id)!)

const ETATS = {
  brouillon: { label: 'En préparation', type: 'new' as const },
  publiee: { label: 'En ligne', type: 'success' as const },
  retiree: { label: 'En pause', type: 'warning' as const },
  archivee: { label: 'Archivée', type: 'info' as const },
}
const etat = computed(() => ETATS[o.value.etat])
const peutPublier = computed(() => Boolean(db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier))
const modifiable = computed(() => o.value.etat !== 'archivee')
const restants = computed(() => (o.value.dateFin ? joursRestants(o.value.dateFin) : 0))
const enLigne = computed(() => o.value.etat === 'publiee' || o.value.etat === 'retiree')
// Offre téléversée ou « Diffuser uniquement » : pas de recrutement dans l'ATS (revue UI, 27/11/2026).
const avecRecrutement = computed(() => enLigne.value && o.value.modeCandidature === 'ats')

const enregistre = ref(heure())
watch(() => JSON.stringify(o.value), () => {
  sauvegarder()
  enregistre.value = heure()
})

const nature = computed(() => (o.value.ouvertA.length === 2 ? 'Fonctionnaires et contractuels' : o.value.ouvertA[0] === 'contractuel' ? 'Contractuels' : o.value.ouvertA[0] === 'titulaire' ? 'Fonctionnaires' : ''))
const meta = computed(() => [
  { icon: 'ri:map-pin-2-line', srLabel: 'Lieu', label: o.value.sansLieuFixe ? 'Pas de lieu fixe' : o.value.lieu || 'Lieu à préciser' },
  ...(o.value.categorie ? [{ icon: 'ri:price-tag-3-line', srLabel: 'Catégorie', label: `Catégorie ${o.value.categorie}` }] : []),
  ...(nature.value ? [{ icon: 'ri:user-line', srLabel: 'Nature de l\'emploi', label: nature.value }] : []),
  ...(o.value.nbPostes ? [{ icon: 'ri:group-line', srLabel: 'Postes', label: `${o.value.nbPostes} poste${Number(o.value.nbPostes) > 1 ? 's' : ''}` }] : []),
  o.value.etat === 'publiee'
    ? { icon: 'ri:calendar-line', srLabel: 'Publication', label: `En ligne jusqu'au ${dateLongue(o.value.dateFin)}` }
    : o.value.etat === 'retiree'
      ? { icon: 'ri:calendar-line', srLabel: 'Publication', label: `En pause ${le(o.value.retireeLe)}` }
      : { icon: 'ri:calendar-line', srLabel: 'Création', label: `Créée ${le(o.value.creeLe)}` },
])

// --- Champs obligatoires qui restent à remplir (bloc « À compléter ») ---
const champs = computed(() => champsObligatoires(o.value))
const reste = computed(() => champs.value.filter(c => !c.ok).length)
const aCompleter = computed(() => ETAPES_OFFRE
  .map(e => ({ ...e, manquants: champs.value.filter(c => c.partie === e.id && !c.ok).map(c => c.label) }))
  .filter(e => e.manquants.length))

// --- Onglets (revue UI équipe, 27/11/2026) : les trois parties de la création, puis l'activité. Remplacent « Accéder à ». ---
type Onglet = GroupeOffre | 'activite'
const onglet = ref<Onglet>('annonce')
const LIBELLES_ONGLET: Record<GroupeOffre, string> = { annonce: 'Annonce', candidature: 'Paramètres du recrutement', diffusion: 'Diffusion' }
const onglets = computed<CspTabItem<Onglet>[]>(() => [
  ...GROUPES.map(g => ({ value: g.id, label: LIBELLES_ONGLET[g.id], icon: g.icone })),
  { value: 'activite', label: 'Activité', icon: 'ri:history-line' },
])
const groupeActif = computed(() => GROUPES.find(g => g.id === onglet.value))
// Sites de diffusion et leur état, dans l'onglet « Diffusion » d'une offre déjà publiée.
const sites = computed(() => CANAUX_DIFFUSION.filter(c => o.value.publications[c.id]).map(c => ({ ...c, ...o.value.publications[c.id]! })))
// Historique d'activité, le plus récent d'abord.
const activites = computed(() => [...o.value.historique].reverse())

// --- Blocs : un seul en modification à la fois ---
const edition = ref<PartieOffre | null>(null)
const verrouCandidature = computed(() => (o.value.etat === 'brouillon' ? undefined : 'Verrouillé : des candidats ont déjà postulé'))
async function allerBloc(partie: PartieOffre, modifier = false) {
  onglet.value = groupeDe(partie).id
  if (modifier) {
    edition.value = partie
  }
  await nextTick()
  document.getElementById(`bloc-${partie}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
function enregistreBloc(titre: string, champsModifies: string[]) {
  if (champsModifies.length) {
    noterModification(o.value, titre, champsModifies)
  }
  // Offre en ligne : un site ajouté dans « Diffusion » est publié tout de suite.
  if (o.value.etat === 'publiee') {
    for (const id of o.value.canaux.filter(c => !o.value.publications[c])) {
      o.value.publications[id] = { etat: 'publiee', debut: dateLongue(aujourdhui()), fin: o.value.dateFin }
    }
  }
  notifier(o.value.etat === 'publiee' ? `« ${titre} » enregistré : la modification est en ligne.` : `« ${titre} » enregistré.`)
}
// Depuis la liste, « Compléter » peut viser une étape.
if (props.section && ETAPES_OFFRE.some(e => e.id === props.section)) {
  void allerBloc(props.section as PartieOffre, true)
}

const apercu = ref(false)
const retrait = ref(false)
const menu = computed(() => [
  {
    items: [
      ...(avecRecrutement.value ? [{ label: 'Voir le recrutement', icon: 'ri:team-line', onSelect: () => aller({ nom: 'recrutement', id: o.value.id }) }] : []),
      { label: 'Dupliquer l’offre', icon: 'ri:file-copy-2-line', onSelect: () => dupliquer(o.value, { aller, notifier }) },
      { label: 'Activité', icon: 'ri:history-line', onSelect: () => (onglet.value = 'activite') },
    ],
  },
  ...(o.value.etat === 'publiee' && peutPublier.value
    ? [{ items: [{ label: 'Mettre en pause', icon: 'ri:stop-circle-line', onSelect: () => (retrait.value = true) }] }]
    : []),
])
// Le rappel « offre en ligne » est affiché près des boutons du bloc modifié (BlocEtape), plus en bandeau (Alice, 26/11/2026).
const bandeaux = computed<string[]>(() => [])

// --- Prolonger (publiée ou dépubliée) ---
const prolongation = ref(false)
const nouvelleFin = ref('')
const erreurFin = ref('')
// Une offre en pause n'est pas forcément à prolonger (Alice, 25/11/2026) : on la remet en ligne, en gardant
// sa date de fin si elle n'est pas passée.
const pause = computed(() => o.value.etat === 'retiree')
const finPassee = computed(() => !o.value.dateFin || o.value.dateFin <= aujourdhui())
function ouvrirProlongation() {
  const base = o.value.dateFin && o.value.dateFin > aujourdhui() ? o.value.dateFin : aujourdhui()
  nouvelleFin.value = pause.value && !finPassee.value ? o.value.dateFin : plusJours(base, 15)
  erreurFin.value = ''
  prolongation.value = true
}
// Depuis la liste : « Remettre en ligne » et « Prolonger » ouvrent directement la fenêtre.
if ((props.section === 'remettre' && o.value.etat === 'retiree') || (props.section === 'prolonger' && o.value.etat === 'publiee')) {
  ouvrirProlongation()
}
function confirmerProlongation() {
  if (!nouvelleFin.value || nouvelleFin.value <= aujourdhui()) {
    erreurFin.value = 'La nouvelle date de fin doit être après aujourd\'hui.'
    return
  }
  const remise = o.value.etat === 'retiree'
  prolonger(o.value, nouvelleFin.value)
  prolongation.value = false
  notifier(remise ? `Offre remise en ligne jusqu'au ${dateLongue(nouvelleFin.value)}. Elle peut de nouveau recevoir des candidatures.` : `Publication prolongée jusqu'au ${dateLongue(nouvelleFin.value)}.`)
}

// --- Mettre en pause (en ligne → en pause) ---
function confirmerRetrait() {
  retirer(o.value, 'pause')
  retrait.value = false
  notifier('Offre mise en pause. Le recrutement continue : les candidatures reçues restent à traiter.')
}
</script>

<template>
  <PageAts
    v-model:onglet="onglet"
    actif="offres"
    largeur="full"
    :titre="o.titre || 'Offre sans titre'"
    :fil="[{ label: 'Mes offres d\'emploi', to: '/offres' }, { label: o.titre || o.id }]"
    :retour="{ to: '/offres', label: 'Retour à mes offres d\'emploi' }"
    :bandeaux="bandeaux"
    :onglets="onglets"
  >
    <template #meta>
      <div class="meta">
        <CspBadge
          :label="etat.label"
          :type="etat.type"
          size="sm"
        />
        <span class="meta__ref">{{ o.id }}</span>
        <CspMetaList :items="meta" />
        <span
          v-if="o.origineContenu === 'televersement' || (enLigne && !avecRecrutement)"
          class="meta__ref"
        >{{ o.origineContenu === 'televersement' ? 'Offre téléversée · ' : '' }}Candidatures gérées hors ATS</span>
        <button
          v-if="avecRecrutement"
          type="button"
          class="lien"
          @click="aller({ nom: 'recrutement', id: o.id })"
        >
          {{ candidatures(o).total }} candidature{{ candidatures(o).total > 1 ? 's' : '' }}
        </button>
      </div>
    </template>
    <template #actions>
      <span class="save">Enregistré à {{ enregistre }}</span>
      <CspButton
        icon="ri:eye-line"
        variant="tertiary-no-outline"
        size="sm"
        aria-label="Aperçu candidat"
        title="Aperçu candidat"
        @click="apercu = true"
      />
      <CspDropdownMenu
        :sections="menu"
        side="bottom"
        align="end"
      >
        <template #trigger>
          <CspButton
            icon="ri:more-fill"
            variant="tertiary-no-outline"
            size="sm"
            aria-label="Actions sur l’offre"
          />
        </template>
      </CspDropdownMenu>
      <template v-if="peutPublier">
        <CspButton
          v-if="o.etat === 'brouillon'"
          label="Publier"
          size="sm"
          icon="ri:send-plane-line"
          is-icon-left
          :disabled="Boolean(reste)"
          :title="reste ? `Encore ${reste} champ${reste > 1 ? 's' : ''} obligatoire${reste > 1 ? 's' : ''} à remplir` : undefined"
          @click="aller({ nom: 'publier', id: o.id })"
        />
        <CspButton
          v-else-if="enLigne"
          :label="pause ? 'Remettre en ligne' : 'Prolonger'"
          size="sm"
          :variant="pause || restants <= 7 ? 'primary' : 'secondary'"
          :icon="pause ? 'ri:play-circle-line' : 'ri:calendar-line'"
          is-icon-left
          @click="ouvrirProlongation"
        />
      </template>
    </template>

    <template #avant-onglets>
      <div
        v-if="(o.etat === 'publiee' && restants <= 7) || reste || o.etat === 'brouillon'"
        class="fond fond--haut"
      >
        <p
          v-if="o.etat === 'publiee' && restants <= 7"
          class="alerte"
        >
          <CspIcon
            name="ri:time-line"
            :size="16"
          />
          L'offre se termine {{ restants <= 0 ? 'aujourd\'hui' : `dans ${restants} jour${restants > 1 ? 's' : ''}` }}.
          Prolongez-la pour continuer à recevoir des candidatures.
        </p>

        <!-- Champs qui restent à remplir, étape par étape -->
        <section
          v-if="reste || o.etat === 'brouillon'"
          class="completion"
          :class="{ 'completion--ok': !reste }"
        >
          <header class="completion__tete">
            <h2 class="completion__titre">
              {{ reste ? 'À compléter avant de publier' : 'Tout est prêt' }}
            </h2>
            <span class="completion__compte">{{ champs.length - reste }} / {{ champs.length }} champs obligatoires remplis</span>
          </header>
          <div
            class="jauge"
            role="progressbar"
            :aria-valuenow="champs.length - reste"
            :aria-valuemax="champs.length"
            aria-label="Champs obligatoires remplis"
          >
            <span :style="{ width: `${((champs.length - reste) / champs.length) * 100}%` }" />
          </div>
          <div
            v-if="reste"
            class="cartes"
          >
            <article
              v-for="e in aCompleter"
              :key="e.id"
              class="carte"
            >
              <h3 class="carte__titre">
                {{ e.titre }}
              </h3>
              <p class="carte__texte">
                {{ e.manquants.join(', ') }}
              </p>
              <CspButton
                v-if="modifiable"
                label="Compléter"
                size="sm"
                variant="secondary"
                @click="allerBloc(e.id, true)"
              />
            </article>
          </div>
          <div
            v-else
            class="completion__fin"
          >
            <p>
              <CspIcon
                name="ri:checkbox-circle-fill"
                :size="18"
                class="ok"
              />
              Tous les champs obligatoires sont remplis.
              {{ peutPublier ? 'Vous pouvez publier l\'offre.' : 'Un agent qui a le droit « Publier » la mettra en ligne.' }}
            </p>
            <CspButton
              v-if="peutPublier"
              label="Publier"
              icon="ri:send-plane-line"
              is-icon-left
              @click="aller({ nom: 'publier', id: o.id })"
            />
          </div>
        </section>
      </div>
    </template>

    <div class="fond">
      <section
        v-if="groupeActif"
        :key="groupeActif.id"
        class="partie"
      >
        <header class="partie__tete">
          <h2 class="partie__titre">
            <CspIcon
              :name="groupeActif.icone"
              :size="20"
            />
            {{ groupeActif.titre }}
          </h2>
          <p class="partie__aide">
            {{ groupeActif.aide }}
          </p>
        </header>
        <BlocEtape
          v-for="e in ETAPES_OFFRE.filter(x => x.groupe === groupeActif!.id)"
          :key="e.id"
          :offre="o"
          :partie="e.id"
          :modifiable="modifiable"
          :verrouille="groupeActif.id === 'candidature' ? verrouCandidature : undefined"
          :edition="edition === e.id"
          @update:edition="(v: boolean) => (edition = v ? e.id : null)"
          @enregistre="enregistreBloc"
        />
        <section
          v-if="groupeActif.id === 'diffusion' && sites.length"
          class="sites"
        >
          <h3 class="sites__titre">
            Publication sur les sites
          </h3>
          <ul class="sites__liste">
            <li
              v-for="s in sites"
              :key="s.id"
              class="site"
            >
              <span class="site__nom">{{ s.nom }}</span>
              <CspBadge
                :label="s.etat === 'publiee' ? 'En ligne' : 'Arrêtée'"
                :type="s.etat === 'publiee' ? 'success' : 'info'"
                size="sm"
              />
              <span class="site__dates">Depuis le {{ s.debut }} · jusqu'au {{ dateLongue(s.fin) }}</span>
            </li>
          </ul>
        </section>
      </section>

      <!-- Historique d'activité : toutes les modifications de l'offre, et par qui (revue UI, 27/11/2026) -->
      <section
        v-else
        class="activite"
        aria-labelledby="activite-titre"
      >
        <header class="partie__tete">
          <h2
            id="activite-titre"
            class="partie__titre"
          >
            <CspIcon
              name="ri:history-line"
              :size="20"
            />
            Historique d'activité
          </h2>
          <p class="partie__aide">
            Toutes les modifications de l'offre, et qui les a faites. Le plus récent en premier.
          </p>
        </header>
        <ol class="fil">
          <li
            v-for="(h, i) in activites"
            :key="i"
            class="fil__item"
          >
            <span class="fil__date">{{ h.date }}</span>
            <span class="fil__texte">{{ h.texte }}</span>
            <span class="fil__par">
              <CspIcon
                :name="h.par ? 'ri:user-line' : 'ri:time-line'"
                :size="14"
              />
              {{ h.par ?? 'Automatique' }}
            </span>
          </li>
        </ol>
      </section>
    </div>

    <CspDialog
      v-model:open="prolongation"
      :title="pause ? 'Remettre l\'offre en ligne' : 'Prolonger la publication'"
      size="sm"
    >
      <p
        v-if="pause"
        class="texte"
      >
        L'offre sera de nouveau visible des candidats et pourra recevoir de nouvelles candidatures.
        {{ finPassee ? 'Sa date de fin est passée : choisissez-en une nouvelle.' : 'Vous pouvez garder sa date de fin ou la modifier.' }}
      </p>
      <ChampDate
        v-model="nouvelleFin"
        :label="pause ? 'Date de fin de publication' : 'Nouvelle date de fin'"
        hint="C'est aussi la date limite de candidature."
        :error="Boolean(erreurFin)"
        :error-message="erreurFin || undefined"
      />
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="prolongation = false"
        />
        <CspButton
          :label="pause ? 'Remettre en ligne' : 'Prolonger'"
          @click="confirmerProlongation"
        />
      </template>
    </CspDialog>

    <CspDialog
      v-model:open="retrait"
      title="Mettre l'offre en pause ?"
      size="sm"
    >
      <p class="texte">
        L'offre ne sera plus visible des candidats et ne recevra plus de candidatures. Les candidatures reçues restent à traiter.
        Vous pourrez la remettre en ligne à tout moment.
      </p>
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="retrait = false"
        />
        <CspButton
          label="Mettre en pause"
          @click="confirmerRetrait"
        />
      </template>
    </CspDialog>

    <CspDrawer
      :open="apercu"
      title="Aperçu candidat"
      description="Mise en page indicative."
      size="lg"
      :modal="false"
      :overlay="false"
      @update:open="(v: boolean) => (apercu = v)"
    >
      <ApercuCandidat
        :offre="o"
        :organisme="db.organisme.nom"
      />
    </CspDrawer>
  </PageAts>
</template>

<style scoped lang="scss">
.meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-2) var(--csp-space-3);
}

.meta__ref {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.meta :deep(.csp-meta-list) {
  flex-wrap: wrap;
  gap: var(--csp-space-2) var(--csp-space-4);
}

.meta :deep(.csp-meta-list__item) {
  &::before,
  &::after {
    content: none;
    display: none;
  }
}

.save {
  align-self: center;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.fond {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
  max-width: 64rem;
  margin: 0 auto;
  width: 100%;
}

.alerte {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-warning);
  background: var(--background-contrast-warning);
  font-size: var(--csp-font-size-sm);
}

.completion {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  padding: var(--csp-space-6) var(--csp-space-8);
  border: 1px solid var(--border-default-grey);
  border-radius: 0.75rem;
  background: var(--background-alt-blue-france);
}

.completion__tete {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: baseline;
  gap: var(--csp-space-2);
}

.completion__titre {
  margin: 0;
  font-size: 1.25rem;
}

.completion__compte {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.jauge {
  height: 0.375rem;
  border-radius: 1rem;
  background: var(--background-contrast-grey);
  overflow: hidden;

  span {
    display: block;
    height: 100%;
    background: var(--background-action-high-blue-france);
  }
}

.completion--ok .jauge span {
  background: var(--border-plain-success);
}

.cartes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(14rem, 1fr));
  gap: var(--csp-space-3);
}

.carte {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-1);
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  border-radius: 0.75rem;
  background: var(--background-default-grey);

  .csp-button,
  :deep(.csp-button) {
    margin-top: auto;
  }
}

.carte__titre {
  margin: 0;
  font-size: var(--csp-font-size-md, 1rem);
}

.carte__texte {
  margin: 0 0 var(--csp-space-3);
  font-size: var(--csp-font-size-sm);
}

.completion__fin {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-3);

  p {
    display: flex;
    align-items: center;
    gap: var(--csp-space-2);
    margin: 0;
  }
}

.ok {
  color: var(--text-default-success);
}

.partie {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  scroll-margin-top: 4rem;
}

.partie__tete {
  margin-top: var(--csp-space-4);
}

.partie__titre {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: 1.5rem;
}

.partie__aide {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.lien {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  font-size: var(--csp-font-size-sm);
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}

.texte {
  margin: 0;
  font-size: var(--csp-font-size-sm);
}

.fond--haut {
  gap: var(--csp-space-4);
}

.sites {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-5) var(--csp-space-6);
  border: 1px solid var(--border-default-grey);
}

.sites__titre {
  margin: 0;
  font-size: 1.125rem;
}

.sites__liste,
.fil {
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  list-style: none;
}

.site {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-2) var(--csp-space-3);
  padding: var(--csp-space-3) 0;
  border-bottom: 1px solid var(--border-default-grey);
  font-size: var(--csp-font-size-sm);

  &:last-child {
    border-bottom: 0;
  }
}

.site__nom {
  font-weight: 700;
}

.site__dates,
.fil__date {
  color: var(--text-mention-grey);
}

.activite {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.fil {
  border: 1px solid var(--border-default-grey);
}

.fil__item {
  display: grid;
  grid-template-columns: 11rem minmax(0, 1fr) auto;
  gap: var(--csp-space-1) var(--csp-space-4);
  align-items: baseline;
  padding: var(--csp-space-3) var(--csp-space-5);
  border-bottom: 1px solid var(--border-default-grey);
  font-size: var(--csp-font-size-sm);

  &:last-child {
    border-bottom: 0;
  }

  @media (width <= 48rem) {
    grid-template-columns: minmax(0, 1fr);
  }
}

.fil__par {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--text-mention-grey);
  white-space: nowrap;
}
</style>
