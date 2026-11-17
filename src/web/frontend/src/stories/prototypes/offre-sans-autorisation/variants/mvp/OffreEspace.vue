<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import Panel from '../../shared/Panel.vue'
import { manquesAnnonce } from './aide'
import ApercuCandidat from './ApercuCandidat.vue'
import FormAnnonce from './FormAnnonce.vue'
import FormCandidature from './FormCandidature.vue'
import FormEquipe from './FormEquipe.vue'
import FormInterne from './FormInterne.vue'
import FormProcessus from './FormProcessus.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { candidatures } from './recrutement'
import SectionOffre from './SectionOffre.vue'
import { aujourdhui, dateLongue, db, heure, joursRestants, le, plusJours, prolonger, retirer, sauvegarder, UTILISATEUR } from './store'

// Page d'une offre (sans autorisation) : sections modifiables à gauche, encart de l'état à droite.
// Brouillon → Publiée (publication immédiate) → Dépubliée (date de fin ou retrait manuel) → Publiée (prolongation).
// L'offre reste modifiable une fois publiée. Publier, prolonger et retirer demandent le droit « Publier ».
const props = defineProps<{ id: string, section?: string }>()
const { aller, notifier } = useNav()
const o = computed(() => db.offres.find(x => x.id === props.id)!)

const ETATS = {
  brouillon: { label: 'Brouillon', type: 'new' as const },
  publiee: { label: 'Publiée', type: 'success' as const },
  retiree: { label: 'Dépubliée', type: 'warning' as const },
  archivee: { label: 'Archivée', type: 'info' as const },
}
const programmee = computed(() => o.value.etat === 'publiee' && o.value.dateDebut > aujourdhui())
const etat = computed(() => (programmee.value ? { label: 'Programmée', type: 'info' as const } : ETATS[o.value.etat]))
const peutPublier = computed(() => Boolean(db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier))
const modifiable = computed(() => o.value.etat !== 'archivee')
const manques = computed(() => manquesAnnonce(o.value))
const restants = computed(() => (o.value.dateFin ? joursRestants(o.value.dateFin) : 0))

// Enregistrement automatique
const enregistre = ref(heure())
watch(() => JSON.stringify(o.value), () => {
  sauvegarder()
  enregistre.value = heure()
})

const meta = computed(() => [
  { icon: 'ri:calendar-line', srLabel: 'Création', label: `Créée ${le(o.value.creeLe).replace(/^le /, 'le ')}` },
  { icon: 'ri:map-pin-2-line', srLabel: 'Lieu', label: o.value.lieu || 'Lieu à préciser' },
  { icon: 'ri:government-line', srLabel: 'Organisme', label: db.organisme.nom },
  ...(o.value.categorie ? [{ icon: 'ri:price-tag-3-line', srLabel: 'Catégorie', label: `Catégorie ${o.value.categorie}` }] : []),
  { icon: 'ri:group-line', srLabel: 'Postes', label: `${o.value.nbPostes || 1} poste${Number(o.value.nbPostes) > 1 ? 's' : ''}` },
])
const menu = [{
  items: [
    { label: 'Dupliquer l’offre', icon: 'ri:file-copy-2-line', onSelect: () => aller({ nom: 'creation', mode: 'duplication', offreId: o.value.id }) },
  ],
}]
const apercu = ref(false)

// --- Sections et raccourcis « Accéder à » (dans l'ordre de la page) ---
const RACCOURCIS = [
  { id: 'annonce', label: 'Annonce' },
  { id: 'interne', label: 'Informations internes' },
  { id: 'candidature', label: 'Formulaire de candidature' },
  { id: 'processus', label: 'Processus' },
  { id: 'equipe', label: 'Équipe' },
  { id: 'journal', label: 'Journal d\'activité' },
]
const ouverts = reactive<Record<string, boolean>>({ annonce: true, interne: true, candidature: true, processus: true, equipe: true, journal: false })
const active = ref('')
let choisie = ''
let finChoix: ReturnType<typeof setTimeout> | undefined
async function allerA(id: string) {
  ouverts[id] = true
  choisie = id
  active.value = id
  await nextTick()
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
let defileur: HTMLElement | null = null
function suivreSection() {
  if (!defileur) {
    return
  }
  if (choisie) {
    clearTimeout(finChoix)
    finChoix = setTimeout(() => (choisie = ''), 150)
    return
  }
  const ids = RACCOURCIS.map(r => r.id)
  if (defileur.scrollTop + defileur.clientHeight >= defileur.scrollHeight - 4) {
    active.value = ids.at(-1) ?? ''
    return
  }
  const repere = (document.querySelector('.raccourcis')?.getBoundingClientRect().bottom ?? 0) + 120
  active.value = ids.filter(id => (document.getElementById(id)?.getBoundingClientRect().top ?? Infinity) <= repere).at(-1) ?? ''
}
onMounted(() => {
  defileur = document.querySelector('.csp-page-container')
  defileur?.addEventListener('scroll', suivreSection, { passive: true })
  if (props.section) {
    void allerA(props.section)
  }
})
onBeforeUnmount(() => defileur?.removeEventListener('scroll', suivreSection))

// --- Prolonger (publiée ou dépubliée) ---
const prolongation = ref(false)
const nouvelleFin = ref('')
const erreurFin = ref('')
function ouvrirProlongation() {
  const base = o.value.dateFin && o.value.dateFin > aujourdhui() ? o.value.dateFin : aujourdhui()
  nouvelleFin.value = plusJours(base, 15)
  erreurFin.value = ''
  prolongation.value = true
}
function confirmerProlongation() {
  if (!nouvelleFin.value || nouvelleFin.value <= aujourdhui()) {
    erreurFin.value = 'La nouvelle date de fin doit être après aujourd\'hui.'
    return
  }
  const remise = o.value.etat === 'retiree'
  prolonger(o.value, nouvelleFin.value)
  prolongation.value = false
  notifier(remise ? `Offre remise en ligne jusqu'au ${dateLongue(nouvelleFin.value)}.` : `Publication prolongée jusqu'au ${dateLongue(nouvelleFin.value)}.`)
}

// --- Retirer (publiée → dépubliée) ---
const retrait = ref(false)
function confirmerRetrait() {
  retirer(o.value, 'manuel')
  retrait.value = false
  notifier('Offre retirée. Le recrutement continue : les candidatures reçues restent à traiter.')
}
</script>

<template>
  <PageAts
    actif="offres"
    largeur="full"
    :titre="o.titre || 'Offre sans titre'"
    :fil="[{ label: 'Mes offres d\'emploi', to: '/offres' }, { label: o.titre || o.id }]"
    :retour="{ to: '/offres', label: 'Retour à mes offres d\'emploi' }"
  >
    <template #meta>
      <div class="meta">
        <CspBadge
          :label="etat.label"
          :type="etat.type"
          size="sm"
        />
        <CspMetaList :items="meta" />
      </div>
    </template>
    <template #actions>
      <span class="save">Enregistré automatiquement à {{ enregistre }}</span>
      <CspButton
        label="Aperçu candidat"
        size="sm"
        variant="secondary"
        icon="ri:eye-line"
        is-icon-left
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
            variant="tertiary"
            size="sm"
            aria-label="Actions sur l’offre"
          />
        </template>
      </CspDropdownMenu>
    </template>

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

    <div class="colonnes">
      <!-- Encart de l'état et des actions -->
      <aside class="tete">
        <Panel
          v-if="o.etat === 'brouillon'"
          class="encart encart--action"
          titre="Brouillon"
          :description="manques.length ? 'Enregistré à tout moment, rien n\'est exigé. Pour publier, complétez :' : 'L\'annonce est complète : il ne reste qu\'à choisir la date de fin et publier.'"
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
                @click="allerA(m.etape === 'candidature' ? 'candidature' : 'annonce')"
              >
                Compléter
              </button>
            </li>
          </ul>
          <div v-if="peutPublier">
            <CspButton
              label="Publier"
              icon="ri:send-plane-line"
              is-icon-left
              @click="aller({ nom: 'publier', id: o.id })"
            />
          </div>
          <p
            v-else
            class="texte"
          >
            Vous n'avez pas le droit « Publier » : un agent qui l'a mettra l'offre en ligne.
          </p>
        </Panel>

        <Panel
          v-else-if="o.etat === 'publiee' || o.etat === 'retiree'"
          class="encart"
          :class="o.etat === 'publiee' && restants <= 7 ? 'encart--attention' : 'encart--action'"
          :titre="o.etat === 'publiee' ? (programmee ? 'Programmée' : 'En ligne') : 'Dépubliée'"
          :description="programmee
            ? `Mise en ligne prévue le ${dateLongue(o.dateDebut)}, jusqu'au ${dateLongue(o.dateFin)} (date limite de candidature). Vous pouvez toujours modifier l'offre.`
            : o.etat === 'publiee'
              ? `Publiée ${le(o.publieeLe)}, jusqu'au ${dateLongue(o.dateFin)} (date limite de candidature). Vous pouvez toujours modifier l'offre.`
              : `Retirée ${le(o.retireeLe)}. Les candidatures reçues restent à traiter. Prolonger remet l'offre en ligne.`"
        >
          <p
            v-if="o.etat === 'publiee' && restants <= 7"
            class="alerte"
          >
            Se termine {{ restants <= 0 ? 'aujourd\'hui' : `dans ${restants} jour${restants > 1 ? 's' : ''}` }}.
          </p>
          <p class="texte">
            <button
              type="button"
              class="lien"
              @click="aller({ nom: 'recrutements' })"
            >
              {{ candidatures(o).total }} candidature{{ candidatures(o).total > 1 ? 's' : '' }}
            </button>
            dans le recrutement.
          </p>
          <div
            v-if="prolongation"
            class="prolonger"
          >
            <CspInput
              v-model="nouvelleFin"
              placeholder="AAAA-MM-JJ"
              label="Nouvelle date de fin"
              :error="Boolean(erreurFin)"
              :error-message="erreurFin || undefined"
            />
            <div class="actions">
              <CspButton
                label="Annuler"
                variant="tertiary-no-outline"
                size="sm"
                @click="prolongation = false"
              />
              <CspButton
                :label="o.etat === 'retiree' ? 'Prolonger et remettre en ligne' : 'Prolonger'"
                size="sm"
                @click="confirmerProlongation"
              />
            </div>
          </div>
          <div
            v-else-if="peutPublier"
            class="actions"
          >
            <CspButton
              :label="o.etat === 'retiree' ? 'Prolonger et remettre en ligne' : 'Prolonger'"
              size="sm"
              :variant="o.etat === 'retiree' ? 'primary' : 'secondary'"
              icon="ri:calendar-line"
              is-icon-left
              @click="ouvrirProlongation"
            />
            <CspButton
              v-if="o.etat === 'publiee'"
              label="Retirer l'offre"
              size="sm"
              variant="tertiary"
              icon="ri:stop-circle-line"
              is-icon-left
              @click="retrait = true"
            />
          </div>
          <p
            v-else
            class="texte"
          >
            Prolonger ou retirer l'offre demande le droit « Publier ».
          </p>
        </Panel>
      </aside>

      <div class="sections">
        <SectionOffre
          id="annonce"
          v-model:ouvert="ouverts.annonce"
          titre="Annonce"
          :description="o.etat === 'publiee' ? 'Offre en ligne : vos modifications sont visibles tout de suite par les candidats.' : undefined"
        >
          <fieldset
            class="verrou"
            :disabled="!modifiable"
          >
            <FormAnnonce
              :offre="o"
              :lecture-seule="!modifiable"
            />
          </fieldset>
        </SectionOffre>

        <SectionOffre
          id="interne"
          v-model:ouvert="ouverts.interne"
          titre="Informations internes"
        >
          <template #intro>
            <p class="source">
              Jamais publiées.
            </p>
          </template>
          <fieldset
            class="verrou"
            :disabled="!modifiable"
          >
            <FormInterne
              :offre="o"
              :lecture-seule="!modifiable"
            />
          </fieldset>
        </SectionOffre>

        <SectionOffre
          id="candidature"
          v-model:ouvert="ouverts.candidature"
          titre="Formulaire de candidature"
        >
          <fieldset
            class="verrou"
            :disabled="!modifiable"
          >
            <FormCandidature
              :offre="o"
              :verrouille="o.etat !== 'brouillon'"
            />
          </fieldset>
        </SectionOffre>

        <SectionOffre
          id="processus"
          v-model:ouvert="ouverts.processus"
          titre="Processus"
        >
          <template #intro>
            <p class="source">
              Facultatif. Ne bloque pas la publication.
            </p>
          </template>
          <FormProcessus
            :offre="o"
            :lecture-seule="!modifiable"
          />
        </SectionOffre>

        <SectionOffre
          id="equipe"
          v-model:ouvert="ouverts.equipe"
          titre="Équipe"
        >
          <template #intro>
            <p class="source">
              Facultatif. Le créateur de l'offre en est Responsable.
            </p>
          </template>
          <FormEquipe
            :offre="o"
            :lecture-seule="!modifiable"
          />
        </SectionOffre>

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
      </div>
    </div>

    <CspDialog
      v-model:open="retrait"
      title="Retirer l'offre ?"
      size="sm"
    >
      <p class="texte">
        L'offre ne sera plus visible des candidats. Le recrutement continue : les candidatures reçues restent à traiter.
        Vous pourrez la remettre en ligne en la prolongeant.
      </p>
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="retrait = false"
        />
        <CspButton
          label="Retirer l'offre"
          @click="confirmerRetrait"
        />
      </template>
    </CspDialog>

    <CspDrawer
      :open="apercu"
      title="Aperçu candidat"
      description="Mise en page indicative ; elle suit votre saisie."
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
  gap: var(--csp-space-2);
}

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

.save {
  align-self: center;
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

.colonnes {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 24rem;
  grid-template-areas: 'sections tete';
  gap: var(--csp-space-6);
  align-items: start;

  @media (max-width: 75rem) {
    grid-template-columns: minmax(0, 1fr);
    grid-template-areas: 'tete' 'sections';
  }
}

.tete {
  grid-area: tete;
  position: sticky;
  top: 4rem;

  @media (max-width: 75rem) {
    position: static;
  }
}

.sections {
  grid-area: sections;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  min-width: 0;
}

.encart {
  &--action {
    border-top: 3px solid var(--border-plain-blue-france);
  }

  &--attention {
    border-top: 3px solid var(--border-plain-warning);
  }
}

.manques {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding-left: var(--csp-space-5);
  font-size: var(--csp-font-size-sm);
}

.lien {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;

  li > & {
    margin-left: var(--csp-space-2);
  }
}

.texte {
  margin: 0;
  font-size: var(--csp-font-size-sm);
}

.alerte {
  margin: 0;
  font-weight: 600;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-warning);
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
}

.prolonger {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.source {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.verrou {
  min-width: 0;
  margin: 0;
  padding: 0;
  border: 0;
}

.histo {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: var(--csp-font-size-sm);

  small {
    display: block;
    color: var(--text-mention-grey);
  }
}
</style>
