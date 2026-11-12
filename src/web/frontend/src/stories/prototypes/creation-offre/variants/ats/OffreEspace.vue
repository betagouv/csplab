<script setup lang="ts">
import type { EtapeFormulaire } from './aide'
import { computed, nextTick, onMounted, reactive, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import Panel from '../../shared/Panel.vue'
import { manquesPublication } from './aide'
import ApercuCandidat from './ApercuCandidat.vue'
import BlocValidation from './BlocValidation.vue'
import ChampsPublication from './ChampsPublication.vue'
import CycleOffre from './CycleOffre.vue'
import DemandeValidation from './DemandeValidation.vue'
import FicheSource from './FicheSource.vue'
import FormAnnonce from './FormAnnonce.vue'
import FormCandidature from './FormCandidature.vue'
import { useNav } from './nav'
import OrigineBadge from './OrigineBadge.vue'
import PageAts from './PageAts.vue'
import ResumeValidation from './ResumeValidation.vue'
import SectionOffre from './SectionOffre.vue'
import { archiverOffre, arreterSupport, aujourdhui, CANAUX_DIFFUSION, dateLongue, db, heure, joursRestants, le, maintenant, plusJours, plusUnMois, prolonger, retirer, sauvegarder, signalerModification, UTILISATEUR, validationManquante } from './store'

// Page unique de l'offre : on y arrive en créant l'offre et on y revient pour la suivre.
// En haut : résumé pour la validation et encart de l'étape en cours (demander la validation, publier…).
// Dessous, des sections repliables directement modifiables : Annonce, Formulaire de candidature,
// Paramètres, Publication, Journal. Enregistrement automatique. Une fois publiée, l'annonce reste
// modifiable (visible tout de suite des candidats) ; candidature et dates sont verrouillées.
const props = defineProps<{ id: string, section?: EtapeFormulaire }>()
const { aller, notifier } = useNav()

const o = computed(() => db.offres.find(x => x.id === props.id)!)
const f = computed(() => db.fiches.find(x => x.id === o.value.ficheId)!)
const modifiable = computed(() => o.value.etat === 'brouillon' || o.value.etat === 'publiee')
const manques = computed(() => manquesPublication(o.value))
const prete = computed(() => o.value.etat === 'brouillon' && !manques.value.length && !validationManquante(o.value))
const peutPublier = computed(() => db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier)

// --- Sections et raccourcis « Accéder à » ---
const ouverts = reactive<Record<string, boolean>>({ annonce: true, candidature: true, parametres: true, publication: true, journal: false })
// Le résumé pour la validation ne sert qu'avant publication ; ensuite l'historique est dans le journal.
const avecValidation = computed(() => o.value.etat === 'brouillon' && (db.organisme.validationActive || o.value.validationEtat !== 'non_demandee'))
const RACCOURCIS = computed(() => [
  ...(avecValidation.value ? [{ id: 'validation', label: 'Validation' }] : []),
  { id: 'annonce', label: 'Annonce' },
  { id: 'candidature', label: 'Formulaire de candidature' },
  { id: 'parametres', label: 'Paramètres' },
  { id: 'publication', label: 'Publication' },
  { id: 'journal', label: 'Journal d\'activité' },
])
async function allerA(id: string) {
  if (id in ouverts) {
    ouverts[id] = true
  }
  await nextTick()
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
onMounted(() => props.section && allerA(props.section))
const panneau = ref<'apercu' | 'fiche' | null>(null)

// --- Enregistrement automatique ; une modification après validation est signalée, sans relancer le circuit ---
const sauvegarde = ref<'' | 'modif' | 'ok'>('')
const heureOk = ref('')
let timer: ReturnType<typeof setTimeout> | undefined
let aEnregistrer = false
const contenu = computed(() => {
  const { historique: _h, modifieLe: _m, validations: _v, validationEtat: _e, modifieeDepuisValidation: _d, notifications: _n, ...reste } = o.value
  return JSON.stringify(reste)
})
watch(contenu, () => {
  aEnregistrer = true
  sauvegarde.value = 'modif'
  clearTimeout(timer)
  timer = setTimeout(enregistrerAuto, 1200)
})
function enregistrerAuto() {
  clearTimeout(timer)
  if (aEnregistrer) {
    o.value.modifieLe = maintenant()
    signalerModification(o.value)
    const dernier = o.value.historique.at(-1)
    if (dernier?.texte === 'Contenu de l\'offre modifié' && dernier.date.startsWith('Aujourd')) {
      dernier.date = maintenant()
    }
    else {
      o.value.historique.push({ date: maintenant(), texte: 'Contenu de l\'offre modifié' })
    }
    aEnregistrer = false
  }
  sauvegarder()
  sauvegarde.value = 'ok'
  heureOk.value = heure()
}

// --- Paramètres : responsable du recrutement ---
const responsable = computed({
  get: () => o.value.equipe.find(m => m.role === 'Responsable')?.nom ?? UTILISATEUR,
  set: (nom: string) => {
    o.value.equipe = [{ nom, role: 'Responsable' as const }, ...o.value.equipe.filter(m => m.role !== 'Responsable' && m.nom !== nom)]
  },
})
const OPTIONS_AGENTS = computed(() => db.organisme.agents.map(a => ({ value: a.nom, label: a.nom })))

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
        <CspMetaList :items="meta" />
      </div>
    </template>
    <template #actions>
      <span
        v-if="modifiable"
        class="save"
        aria-live="polite"
      >
        <template v-if="sauvegarde === 'modif'">Modifications en cours…</template>
        <template v-else-if="sauvegarde === 'ok'"><CspIcon
          name="ri:check-line"
          :size="14"
        /> Enregistré à {{ heureOk }}</template>
        <template v-else>Enregistrement automatique</template>
      </span>
      <CspButton
        label="Aperçu candidat"
        icon="ri:eye-line"
        is-icon-left
        variant="secondary"
        size="sm"
        @click="panneau = 'apercu'"
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

    <nav
      class="raccourcis"
      aria-label="Accéder à une section"
    >
      <span>Accéder à :</span>
      <button
        v-for="r in RACCOURCIS"
        :key="r.id"
        type="button"
        class="raccourci"
        @click="allerA(r.id)"
      >
        {{ r.label }}
      </button>
    </nav>

    <p
      v-if="o.modifieeDepuisValidation && o.validationEtat === 'validee'"
      class="bandeau"
    >
      <CspIcon
        name="ri:information-line"
        :size="16"
      />
      Modifiée depuis la validation. Le circuit n'est pas relancé ; le détail figure dans le journal d'activité.
    </p>

    <div
      class="tete"
      :class="{ 'tete--seule': !avecValidation }"
    >
      <ResumeValidation
        v-if="avecValidation"
        id="validation"
        :offre="o"
        :fiche="f"
        :editable="modifiable"
      />
      <div class="tete__etat">
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
            :description="validationManquante(o) ? 'Vous pouvez demander la validation à tout moment, même si l\'offre n\'est pas complète.' : 'Pour publier, l\'annonce doit être complète.'"
          >
            <p
              v-if="manques.length"
              class="texte"
            >
              À compléter pour publier :
            </p>
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
                  @click="allerA(m.etape)"
                >
                  Compléter
                </button>
              </li>
            </ul>
            <div class="actions">
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
              size="sm"
              icon="ri:calendar-line"
              is-icon-left
              @click="ouvrirProlongation"
            />
            <CspButton
              label="Retirer l'offre"
              variant="tertiary"
              size="sm"
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
      </div>
    </div>

    <fieldset
      class="sections"
      :disabled="!modifiable"
    >
      <legend class="sr-only">
        Contenu de l'offre
      </legend>
      <SectionOffre
        id="annonce"
        v-model:ouvert="ouverts.annonce"
        titre="Annonce"
        :description="o.etat === 'publiee' ? 'Offre en ligne : vos modifications sont visibles tout de suite par les candidats.' : undefined"
      >
        <template #actions>
          <CspButton
            label="Fiche de poste source"
            variant="tertiary-no-outline"
            size="sm"
            icon="ri:file-text-line"
            is-icon-left
            @click="panneau = 'fiche'"
          />
        </template>
        <FormAnnonce
          :offre="o"
          :fiche="f"
        />
      </SectionOffre>

      <SectionOffre
        id="candidature"
        v-model:ouvert="ouverts.candidature"
        titre="Formulaire de candidature"
      >
        <FormCandidature
          :offre="o"
          :verrouille="o.etat !== 'brouillon'"
        />
      </SectionOffre>

      <SectionOffre
        id="parametres"
        v-model:ouvert="ouverts.parametres"
        titre="Paramètres de l'offre"
      >
        <div class="parametres">
          <CspSelect
            v-model="responsable"
            label="Responsable du recrutement"
            :options="OPTIONS_AGENTS"
          />
          <CspInput
            v-model="o.contact"
            label="Contact (facultatif)"
            hint="Visible sur l'offre, pour les questions des candidats."
          />
          <div class="fiche">
            <div>
              <p class="mention">
                Fiche de poste rattachée
              </p>
              <strong>{{ f.intitule }}</strong>
              <p class="mention">
                {{ f.id }} · {{ f.service }}
              </p>
            </div>
            <OrigineBadge
              :origine="f.origine"
              court
            />
            <CspButton
              label="Ouvrir la fiche"
              variant="tertiary-no-outline"
              size="sm"
              @click="aller({ nom: 'fiche', id: f.id })"
            />
          </div>
          <CspRadioGroup
            v-if="o.etat === 'publiee'"
            v-model="o.notifications"
            label="Mes notifications : courriel pour les nouvelles candidatures"
            :options="FREQ"
            size="sm"
            @update:model-value="sauvegarder"
          />
        </div>
      </SectionOffre>

      <SectionOffre
        id="publication"
        v-model:ouvert="ouverts.publication"
        titre="Publication"
        :description="o.etat === 'brouillon' ? undefined : 'Pour changer la date de fin, utilisez « Prolonger » en haut de la page.'"
      >
        <div class="publication">
          <ChampsPublication
            :offre="o"
            :disabled="o.etat !== 'brouillon'"
          />
        </div>
      </SectionOffre>
    </fieldset>

    <SectionOffre
      id="journal"
      v-model:ouvert="ouverts.journal"
      titre="Journal d'activité"
    >
      <ol class="histo">
        <li
          v-for="(h, i) in [...o.historique].reverse()"
          :key="i"
        >
          <small>{{ h.date }}</small>{{ h.texte }}
        </li>
      </ol>
    </SectionOffre>

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

    <CspDrawer
      :open="panneau === 'apercu'"
      title="Aperçu candidat"
      description="Mise en page indicative ; elle suit votre saisie."
      size="lg"
      :modal="false"
      :overlay="false"
      @update:open="(v: boolean) => !v && (panneau = null)"
    >
      <ApercuCandidat
        :offre="o"
        :organisme="db.organisme.nom"
      />
    </CspDrawer>

    <CspDrawer
      :open="panneau === 'fiche'"
      title="Fiche de poste source"
      description="Consultation seule : modifier l'annonce ne modifie pas la fiche."
      size="md"
      :modal="false"
      :overlay="false"
      @update:open="(v: boolean) => !v && (panneau = null)"
    >
      <FicheSource :fiche="f" />
    </CspDrawer>
  </PageAts>
</template>

<style scoped lang="scss">
.meta :deep(.csp-meta-list) {
  flex-wrap: wrap;
  gap: var(--csp-space-2);
}

.meta :deep(.csp-meta-list__item) {
  padding: 2px var(--csp-space-3);
  border-radius: 1rem;
  background: var(--background-contrast-grey);
  color: var(--text-default-grey);

  &::before,
  &::after {
    content: none;
    display: none;
  }
}

.encart {
  &--action {
    border-top: 3px solid var(--border-plain-blue-france);
  }

  &--attention {
    border-top: 3px solid var(--border-plain-warning);
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

.save {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.raccourcis {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-1) var(--csp-space-5);
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.raccourci {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  text-decoration-color: transparent;
  text-underline-offset: 3px;
  cursor: pointer;

  &:hover {
    text-decoration-color: currentColor;
  }
}

.bandeau {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-contrast-info);
  font-size: var(--csp-font-size-sm);
}

.tete {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: var(--csp-space-5);
  align-items: stretch;

  &--seule {
    grid-template-columns: minmax(0, 1fr);
  }

  > #validation {
    scroll-margin-top: var(--csp-space-6);
  }
}

.tete__etat {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  min-width: 0;

  > :last-child {
    flex: 1;
  }
}

.sections {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  min-width: 0;
  margin: 0;
  padding: 0;
  border: 0;
}

.parametres,
.publication {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  max-width: 60rem;
}

.fiche {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-3);

  > div {
    flex: 1;
  }
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
