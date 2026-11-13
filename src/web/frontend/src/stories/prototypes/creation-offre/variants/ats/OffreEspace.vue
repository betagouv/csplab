<script setup lang="ts">
import type { EtapeFormulaire } from './aide'
import type { Offre, Proposition } from './store'
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import Panel from '../../shared/Panel.vue'
import { manquesPublication } from './aide'
import ApercuCandidat from './ApercuCandidat.vue'
import BlocValidation from './BlocValidation.vue'
import ChampsPublication from './ChampsPublication.vue'
import CycleOffre from './CycleOffre.vue'
import DecisionValideur from './DecisionValideur.vue'
import DemandeValidation from './DemandeValidation.vue'
import FicheSource from './FicheSource.vue'
import FormAnnonce from './FormAnnonce.vue'
import FormCandidature from './FormCandidature.vue'
import FormInterne from './FormInterne.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import Propositions from './Propositions.vue'
import ResumeValidation from './ResumeValidation.vue'
import SectionOffre from './SectionOffre.vue'
import { archiverOffre, arreterSupport, aValiderParMoi, CANAUX_DIFFUSION, dateLongue, db, differences, heure, joursRestants, le, maintenant, sauvegarder, signalerModification, UTILISATEUR, validationManquante } from './store'

// Page unique de l'offre : on y arrive en créant l'offre et on y revient pour la suivre.
// En haut : résumé pour la validation et encart de l'étape en cours (demander la validation, publier…).
// Dessous, des sections repliables directement modifiables : Annonce, Formulaire de candidature,
// Paramètres, Publication, Journal. Enregistrement automatique. Une fois publiée, l'annonce reste
// modifiable (visible tout de suite des candidats) ; candidature et dates sont verrouillées.
const props = defineProps<{ id: string, section?: EtapeFormulaire }>()
const { aller, notifier } = useNav()

const o = computed(() => db.offres.find(x => x.id === props.id)!)
// Fiche de poste facultative : absente pour une offre partie d'un formulaire vide ou reprise d'une offre sans fiche.
const f = computed(() => db.fiches.find(x => x.id === o.value.ficheId))
// Vue « valideur » : l'offre a été créée par un collègue et le compte connecté doit la valider.
// Tout est en lecture seule ; ses boutons Valider / Refuser sont dans l'encart du haut.
const valideur = computed(() => aValiderParMoi(o.value))
// Offre d'un collègue : consultable seulement, avant comme après la réponse du valideur.
const aTraiter = computed(() => (o.value.propositions ?? []).reduce((n, p) => n + p.champs.filter(c => !c.statut).length, 0))

const lectureSeule = computed(() => Boolean(o.value.creePar) && o.value.creePar !== UTILISATEUR)
const modifiable = computed(() => !lectureSeule.value && (o.value.etat === 'brouillon' || o.value.etat === 'publiee'))
const manques = computed(() => manquesPublication(o.value))
const prete = computed(() => o.value.etat === 'brouillon' && !manques.value.length && !validationManquante(o.value))
const peutPublier = computed(() => db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier)

// --- Sections et raccourcis « Accéder à » ---
const ouverts = reactive<Record<string, boolean>>({ annonce: true, validation: true, interne: true, candidature: true, publication: true, journal: false })
// Le résumé pour la validation ne sert qu'avant publication ; ensuite l'historique est dans le journal.
const avecValidation = computed(() => o.value.etat === 'brouillon' && (db.organisme.validationActive || o.value.validationEtat !== 'non_demandee'))
const RACCOURCIS = computed(() => [
  { id: 'annonce', label: 'Annonce' },
  { id: 'interne', label: 'Informations internes' },
  ...(avecValidation.value ? [{ id: 'validation', label: 'Validation' }] : []),
  { id: 'candidature', label: 'Formulaire de candidature' },
  { id: 'publication', label: 'Publication' },
  { id: 'journal', label: 'Journal d\'activité' },
])
const active = ref('')
// Après un clic sur un raccourci, la pastille cliquée reste active pendant le défilement automatique
// (utile pour les dernières sections, qu'on ne peut pas amener tout en haut).
let choisie = ''
let finChoix: ReturnType<typeof setTimeout> | undefined
async function allerA(id: string) {
  if (id in ouverts) {
    ouverts[id] = true
  }
  choisie = id
  active.value = id
  await nextTick()
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
// --- Valideur : propositions de modification préparées section par section, envoyées avec la décision ---
const propositionsEnCours = ref<Proposition[]>([])
const edition = ref<{ section: Proposition['section'], copie: Offre } | null>(null)
function commencerProposition(section: Proposition['section']) {
  const copie = JSON.parse(JSON.stringify(o.value)) as Offre
  // Reprend les changements déjà préparés pour cette section.
  for (const c of propositionsEnCours.value.find(p => p.section === section)?.champs ?? []) {
    (copie as unknown as Record<string, unknown>)[c.cle] = JSON.parse(JSON.stringify(c.apres))
  }
  edition.value = { section, copie }
  // Laisse le menu se refermer (il rend le focus au bouton) avant de faire défiler jusqu'à la section.
  setTimeout(() => void allerA(section), 200)
}
function ajouterProposition() {
  if (!edition.value) {
    return
  }
  const { section, copie } = edition.value
  const champs = differences(o.value, copie, section)
  propositionsEnCours.value = [
    ...propositionsEnCours.value.filter(p => p.section !== section),
    ...(champs.length ? [{ par: UTILISATEUR, le: maintenant(), section, champs }] : []),
  ]
  edition.value = null
  notifier(champs.length ? `${champs.length} modification${champs.length > 1 ? 's' : ''} ajoutée${champs.length > 1 ? 's' : ''} à votre réponse.` : 'Aucune modification : rien n\'a été ajouté.')
  // Retour sur « Votre réponse », là où la liste des propositions s'affiche.
  void nextTick(() => document.querySelector('.decision__reponse')?.scrollIntoView({ behavior: 'smooth', block: 'start' }))
}
function retirerProposition(section: Proposition['section']) {
  propositionsEnCours.value = propositionsEnCours.value.filter(p => p.section !== section)
}
function reponseEnvoyee() {
  propositionsEnCours.value = []
  edition.value = null
}
const enEdition = (section: Proposition['section']) => edition.value?.section === section
const MODE_PROPOSITION = 'Mode modification : changez les champs voulus puis « Valider les modifications ». L\'offre n\'est pas modifiée ; vos propositions partiront avec votre réponse.'

// Barre « Accéder à » fixe au défilement : la section visible est mise en avant.
let defileur: HTMLElement | null = null
function suivreSection() {
  if (!defileur) {
    return
  }
  if (choisie) {
    // Le défilement automatique est fini quand plus aucun événement n'arrive pendant 150 ms.
    clearTimeout(finChoix)
    finChoix = setTimeout(() => (choisie = ''), 150)
    return
  }
  const ids = RACCOURCIS.value.map(r => r.id)
  // En bas de page, la dernière section est forcément celle qu'on regarde.
  if (defileur.scrollTop + defileur.clientHeight >= defileur.scrollHeight - 4) {
    active.value = ids.at(-1) ?? ''
    return
  }
  const repere = (document.querySelector('.raccourcis')?.getBoundingClientRect().bottom ?? 0) + 120
  active.value = ids.filter(id => (document.getElementById(id)?.getBoundingClientRect().top ?? Infinity) <= repere).at(-1) ?? ''
}
onMounted(() => {
  if (props.section) {
    allerA(props.section)
  }
  defileur = document.querySelector('.csp-page-container')
  defileur?.addEventListener('scroll', suivreSection, { passive: true })
  suivreSection()
})
onBeforeUnmount(() => defileur?.removeEventListener('scroll', suivreSection))
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

// Phrase sous le titre « Annonce » : d'où vient le contenu, et la fiche de poste rattachée.
const origineAnnonce = computed(() => {
  if (!f.value) {
    return o.value.origineContenu === 'duplication' ? 'Annonce reprise d\'une offre existante, sans fiche de poste.' : 'Annonce saisie directement, sans fiche de poste.'
  }
  return {
    fiche: 'Annonce écrite à partir de la fiche de poste',
    fichier: 'Annonce écrite à partir d\'un document, rattachée à la fiche de poste',
    manuel: 'Annonce saisie directement, rattachée à la fiche de poste',
    duplication: 'Annonce reprise d\'une offre existante, rattachée à la fiche de poste',
  }[o.value.origineContenu]
})

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
    ...(f.value ? [{ label: 'Voir la fiche de poste', icon: 'ri:file-text-line', onSelect: () => aller({ nom: 'fiche', id: f.value!.id }) }] : []),
    { label: 'Dupliquer l’offre', icon: 'ri:file-copy-2-line', onSelect: () => aller({ nom: 'creation', mode: 'duplication', offreId: o.value.id }) },
  ],
}])

// --- Publication en cours : arrêter un site. Prolonger et retirer se font dans « Mes recrutements ». ---
const restants = computed(() => (o.value.dateFin ? joursRestants(o.value.dateFin) : 0))
const publies = computed(() => CANAUX_DIFFUSION.filter(c => o.value.publications[c.id]))
function arreter(id: string) {
  arreterSupport(o.value, id)
  notifier('Publication arrêtée sur ce site (simulation).')
}
function archiver() {
  archiverOffre(o.value)
  notifier('Offre archivée. Elle reste consultable et peut être dupliquée.')
}
</script>

<template>
  <PageAts
    :actif="o.etat === 'brouillon' ? 'offres' : 'recrutements'"
    largeur="full"
    :titre="o.titre || 'Offre sans titre'"
    :fil="[o.etat === 'brouillon' ? { label: 'Offres d\'emploi', to: '/offres' } : { label: 'Mes recrutements', to: '/recrutements' }, { label: o.titre || o.id }]"
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
        :class="{ 'raccourci--actif': active === r.id }"
        :aria-current="active === r.id ? 'location' : undefined"
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

    <p
      v-if="!lectureSeule && aTraiter"
      class="bandeau bandeau--action"
    >
      <CspIcon
        name="ri:chat-3-line"
        :size="16"
      />
      <span>{{ aTraiter }} proposition{{ aTraiter > 1 ? 's' : '' }} de modification des valideurs à traiter.</span>
      <button
        type="button"
        class="lien"
        @click="allerA('validation')"
      >
        Voir {{ aTraiter > 1 ? 'les propositions' : 'la proposition' }}
      </button>
    </p>

    <div
      class="tete tete--seule"
    >
      <div class="tete__etat">
        <!-- Encart de l'étape en cours -->
        <template v-if="o.etat === 'brouillon'">
          <DecisionValideur
            v-if="valideur"
            :offre="o"
            :fiche="f"
            :propositions="propositionsEnCours"
            @proposer="commencerProposition"
            @retirer="retirerProposition"
            @envoye="reponseEnvoyee"
          />
          <Panel
            v-else-if="prete"
            class="encart encart--action"
            titre="Prête à être publiée"
            :description="db.organisme.validationActive ? `Validation obtenue ${le(o.validationObtenueLe)} et annonce complète. L'offre n'est jamais publiée automatiquement.` : 'Annonce complète. L\'offre n\'est jamais publiée automatiquement.'"
          >
            <!-- Commentaires laissés par les valideurs avec leur accord -->
            <BlocValidation
              v-if="o.validations?.some(v => v.commentaire)"
              :offre="o"
            />
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
            <div
              v-if="!lectureSeule"
              class="actions"
            >
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
            :description="valideur ? `Demandée ${le(o.validationDemandeeLe)} par ${o.creePar}. Consultez l'offre et le résumé pour la validation, puis donnez votre réponse.` : `Demandée ${le(o.validationDemandeeLe)}. Vous pouvez continuer à modifier l'offre en attendant.`"
          >
            <BlocValidation
              :offre="o"
              simulation
              :moi="valideur ? UTILISATEUR : undefined"
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
                  v-if="!lectureSeule"
                  type="button"
                  class="lien"
                  @click="allerA(m.etape)"
                >
                  Compléter
                </button>
              </li>
            </ul>
            <div
              v-if="!lectureSeule"
              class="actions"
            >
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
          titre="Publiée · le recrutement est ouvert"
          :description="`En ligne du ${dateLongue(o.dateDebut)} au ${dateLongue(o.dateFin)}. Les candidatures, la prolongation et le retrait se gèrent désormais dans Mes recrutements.`"
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
          <div class="actions">
            <CspButton
              label="Voir le recrutement"
              size="sm"
              icon="ri:arrow-right-line"
              @click="aller({ nom: 'recrutements' })"
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

    <div class="sections">
      <SectionOffre
        id="annonce"
        v-model:ouvert="ouverts.annonce"
        titre="Annonce"
        :description="enEdition('annonce') ? MODE_PROPOSITION : lectureSeule ? `Lecture seule : seule la personne qui suit l'offre (${o.creePar}) peut la modifier.` : o.etat === 'publiee' ? 'Offre en ligne : vos modifications sont visibles tout de suite par les candidats.' : undefined"
      >
        <template
          v-if="valideur"
          #actions
        >
          <template v-if="enEdition('annonce')">
            <CspButton
              label="Annuler"
              size="sm"
              variant="tertiary-no-outline"
              @click="edition = null"
            />
            <CspButton
              label="Valider les modifications"
              size="sm"
              icon="ri:check-line"
              is-icon-left
              @click="ajouterProposition"
            />
          </template>
        </template>
        <template #intro>
          <p class="source">
            <span>
              {{ origineAnnonce }}
              <template v-if="f">
                <strong>{{ f.intitule }}</strong> ({{ f.id }})
              </template>
            </span>
            <CspButton
              v-if="f"
              label="Voir la fiche de poste"
              variant="tertiary-no-outline"
              size="sm"
              icon="ri:file-text-line"
              is-icon-left
              @click="panneau = 'fiche'"
            />
          </p>
        </template>
        <fieldset
          class="verrou"
          :class="{ 'verrou--proposition': enEdition('annonce') }"
          :disabled="!modifiable && !enEdition('annonce')"
        >
          <FormAnnonce
            :offre="enEdition('annonce') ? edition!.copie : o"
            :fiche="f"
          />
        </fieldset>
        <div
          v-if="enEdition('annonce')"
          class="barre-proposition"
        >
          <CspButton
            label="Annuler"
            variant="tertiary-no-outline"
            @click="edition = null"
          />
          <CspButton
            label="Valider les modifications"
            icon="ri:check-line"
            is-icon-left
            @click="ajouterProposition"
          />
        </div>
      </SectionOffre>

      <SectionOffre
        id="interne"
        v-model:ouvert="ouverts.interne"
        titre="Informations internes"
      >
        <template #intro>
          <p class="source">
            Jamais publiées. Elles servent au suivi et au résumé pour les valideurs.
          </p>
        </template>
        <fieldset
          class="verrou"
          :disabled="!modifiable"
        >
          <FormInterne :offre="o" />
        </fieldset>
      </SectionOffre>

      <SectionOffre
        v-if="avecValidation && !valideur"
        id="validation"
        v-model:ouvert="ouverts.validation"
        titre="Validation pour publication"
        :description="lectureSeule ? 'Lecture seule.' : undefined"
      >
        <template #intro>
          <p class="source">
            Ce que voient les valideurs. Repris automatiquement de l'annonce, jamais publié tel quel.
          </p>
        </template>
        <ResumeValidation
          :offre="o"
          :fiche="f"
          integre
        />
        <Propositions
          v-if="o.validationEtat !== 'non_demandee'"
          :offre="o"
          :redacteur="!lectureSeule"
          @aller="allerA"
        />
      </SectionOffre>

      <SectionOffre
        id="candidature"
        v-model:ouvert="ouverts.candidature"
        titre="Formulaire de candidature"
        :description="enEdition('candidature') ? MODE_PROPOSITION : undefined"
      >
        <template
          v-if="valideur"
          #actions
        >
          <template v-if="enEdition('candidature')">
            <CspButton
              label="Annuler"
              size="sm"
              variant="tertiary-no-outline"
              @click="edition = null"
            />
            <CspButton
              label="Valider les modifications"
              size="sm"
              icon="ri:check-line"
              is-icon-left
              @click="ajouterProposition"
            />
          </template>
        </template>
        <fieldset
          class="verrou"
          :class="{ 'verrou--proposition': enEdition('candidature') }"
          :disabled="!modifiable && !enEdition('candidature')"
        >
          <FormCandidature
            :offre="enEdition('candidature') ? edition!.copie : o"
            :verrouille="o.etat !== 'brouillon'"
          />
        </fieldset>
        <div
          v-if="enEdition('candidature')"
          class="barre-proposition"
        >
          <CspButton
            label="Annuler"
            variant="tertiary-no-outline"
            @click="edition = null"
          />
          <CspButton
            label="Valider les modifications"
            icon="ri:check-line"
            is-icon-left
            @click="ajouterProposition"
          />
        </div>
      </SectionOffre>

      <SectionOffre
        id="publication"
        v-model:ouvert="ouverts.publication"
        titre="Publication"
        :description="enEdition('publication') ? MODE_PROPOSITION : o.etat === 'brouillon' ? undefined : 'Pour changer la date de fin, utilisez « Prolonger » dans Mes recrutements.'"
      >
        <template
          v-if="valideur"
          #actions
        >
          <template v-if="enEdition('publication')">
            <CspButton
              label="Annuler"
              size="sm"
              variant="tertiary-no-outline"
              @click="edition = null"
            />
            <CspButton
              label="Valider les modifications"
              size="sm"
              icon="ri:check-line"
              is-icon-left
              @click="ajouterProposition"
            />
          </template>
        </template>
        <fieldset
          class="verrou"
          :class="{ 'verrou--proposition': enEdition('publication') }"
          :disabled="!modifiable && !enEdition('publication')"
        >
          <div class="publication">
            <ChampsPublication
              :offre="enEdition('publication') ? edition!.copie : o"
              :disabled="o.etat !== 'brouillon'"
            />
          </div>
        </fieldset>
        <div
          v-if="enEdition('publication')"
          class="barre-proposition"
        >
          <CspButton
            label="Annuler"
            variant="tertiary-no-outline"
            @click="edition = null"
          />
          <CspButton
            label="Valider les modifications"
            icon="ri:check-line"
            is-icon-left
            @click="ajouterProposition"
          />
        </div>
      </SectionOffre>
    </div>

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
      <FicheSource
        v-if="f"
        :fiche="f"
      />
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
  position: sticky;
  top: 0;
  z-index: 5;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-2) var(--csp-space-5);
  margin: var(--csp-space-2) calc(-1 * var(--csp-space-2)) calc(-1 * var(--csp-space-2));
  padding: var(--csp-space-3) var(--csp-space-2);
  background: var(--background-default-grey);
  box-shadow: 0 1px 0 var(--border-default-grey);
  font-size: var(--csp-font-size-sm);

  > span {
    margin-right: var(--csp-space-1);
  }
}

.raccourci {
  padding: 2px var(--csp-space-3);
  border: 0;
  border-radius: 1rem;
  background: var(--background-action-low-blue-france);
  font: inherit;
  color: var(--text-action-high-blue-france);
  cursor: pointer;

  &:hover {
    background: var(--background-action-low-blue-france-hover);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }

  &--actif,
  &--actif:hover {
    background: var(--background-action-high-blue-france);
    color: var(--text-inverted-blue-france);
  }
}

.bandeau.bandeau--action {
  background: var(--background-alt-blue-france);
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
    scroll-margin-top: 4.5rem;
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
}

// Lecture seule (valideur, offre retirée ou archivée) : seuls les champs sont verrouillés,
// pas l'ouverture des sections ni la consultation de la fiche.
.barre-proposition {
  position: sticky;
  bottom: 0;
  z-index: 4;
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-2);
  margin: 0 calc(-1 * var(--csp-space-2));
  padding: var(--csp-space-3) var(--csp-space-2);
  background: var(--background-default-grey);
  box-shadow: 0 -1px 0 var(--border-default-grey);
}

.verrou {
  min-width: 0;
  margin: 0;
  padding: 0;
  border: 0;

  &--proposition {
    padding: var(--csp-space-4);
    outline: 2px dashed var(--border-plain-blue-france);
    outline-offset: var(--csp-space-2);
  }
}

.source {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-1) var(--csp-space-3);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);

  strong {
    color: var(--text-default-grey);
  }
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
