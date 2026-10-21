<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { CATEGORIES, STATUTS } from '../../data/referentiels'
import FieldRow from '../../shared/FieldRow.vue'
import ListEditor from '../../shared/ListEditor.vue'
import Panel from '../../shared/Panel.vue'
import SimulationNote from '../../shared/SimulationNote.vue'
import EtatBadge from './EtatBadge.vue'
import { useNav } from './nav'
import OrigineBadge from './OrigineBadge.vue'
import PageAts from './PageAts.vue'
import { db, heure, maintenant, offresDe, sauvegarder } from './store'

// Écran 3 — détail d'une fiche de poste : contenu, origine (ATS, SIRH, document), offres rattachées,
// modification (sauvegarde automatique) et « Lancer un recrutement ».
const props = defineProps<{ id: string, edition?: boolean }>()
const { aller, notifier } = useNav()

const f = computed(() => db.fiches.find(x => x.id === props.id)!)
const edition = ref(props.edition ?? false)

// --- Sauvegarde automatique ---
const etat = ref<'' | 'modif' | 'ok'>('')
const heureOk = ref('')
let timer: ReturnType<typeof setTimeout> | undefined
let modifiee = false
watch(() => {
  const x = f.value
  return [x.intitule, x.service, x.localisation, x.categories, x.statuts, x.codePoste, x.missions, x.activites, x.competences, x.profil, x.environnement, x.teletravail, x.conditions]
}, () => {
  if (!edition.value) {
    return
  }
  modifiee = true
  etat.value = 'modif'
  clearTimeout(timer)
  timer = setTimeout(enregistrer, 1000)
}, { deep: true })

function enregistrer() {
  clearTimeout(timer)
  if (modifiee) {
    f.value.modifieLe = maintenant()
    const dernier = f.value.historique.at(-1)
    if (dernier?.texte.startsWith('Fiche modifiée') && dernier.date.startsWith('Aujourd')) {
      dernier.date = maintenant()
    }
    else {
      f.value.historique.push({ date: maintenant(), texte: 'Fiche modifiée par Camille Moreau' })
    }
    modifiee = false
  }
  sauvegarder()
  etat.value = 'ok'
  heureOk.value = heure()
}

function terminer() {
  if (!f.value.intitule.trim()) {
    return
  }
  enregistrer()
  edition.value = false
}

function archiver() {
  f.value.statut = f.value.statut === 'active' ? 'archivee' : 'active'
  f.value.historique.push({ date: maintenant(), texte: f.value.statut === 'archivee' ? 'Fiche archivée' : 'Fiche réactivée' })
  sauvegarder()
  notifier(f.value.statut === 'archivee' ? 'Fiche archivée. Ses offres restent consultables.' : 'Fiche réactivée.')
}

function synchroniser() {
  if (f.value.sirh) {
    f.value.sirh.synchroLe = maintenant()
    f.value.historique.push({ date: maintenant(), texte: 'Synchronisation SIRH (simulée) — aucun changement' })
    sauvegarder()
    notifier('Synchronisation simulée : aucune différence avec le SIRH.')
  }
}

const offres = computed(() => offresDe(f.value.id))
const qui = computed(() => f.value.statuts.length === 2 ? 'Fonctionnaires et contractuels' : f.value.statuts[0] === 'titulaire' ? 'Fonctionnaires' : f.value.statuts[0] === 'contractuel' ? 'Contractuels' : '')
const infos = computed(() => [
  { k: 'Service', v: f.value.service },
  { k: 'Localisation', v: f.value.localisation },
  { k: 'Catégorie', v: f.value.categories.join(', ') },
  { k: 'Ouvert aux', v: qui.value },
  { k: 'Code poste', v: f.value.codePoste },
  { k: 'Télétravail', v: f.value.teletravail },
])
</script>

<template>
  <PageAts
    actif="fiches"
    :titre="f.intitule || 'Nouvelle fiche de poste'"
    :fil="[{ label: 'Fiches de poste', action: () => aller({ nom: 'fiches' }) }, { label: f.id }]"
  >
    <template #titre-fin>
      <OrigineBadge :origine="f.origine" />
      <CspBadge
        v-if="f.statut === 'archivee'"
        label="Archivée"
        type="info"
        variant="outline"
        size="sm"
      />
    </template>
    <template #actions>
      <span
        v-if="edition && etat"
        class="save"
        aria-live="polite"
      >
        <template v-if="etat === 'modif'">Modifications en cours…</template>
        <template v-else><CspIcon
          name="ri:check-line"
          :size="14"
        /> Enregistré à {{ heureOk }}</template>
      </span>
      <template v-if="!edition">
        <CspButton
          :label="f.statut === 'active' ? 'Archiver' : 'Réactiver'"
          variant="tertiary-no-outline"
          size="sm"
          @click="archiver"
        />
        <CspButton
          label="Modifier la fiche"
          variant="secondary"
          size="sm"
          icon="ri:edit-line"
          is-icon-left
          @click="edition = true"
        />
        <CspButton
          v-if="f.statut === 'active'"
          label="Lancer un recrutement"
          size="sm"
          icon="ri:send-plane-line"
          is-icon-left
          @click="aller({ nom: 'creation', mode: 'fiche', ficheId: f.id })"
        />
      </template>
      <CspButton
        v-else
        label="Terminer la modification"
        size="sm"
        icon="ri:check-line"
        is-icon-left
        @click="terminer"
      />
    </template>

    <div class="grille">
      <div class="col">
        <!-- Consultation -->
        <template v-if="!edition">
          <Panel titre="Le poste">
            <dl class="dl">
              <div
                v-for="i in infos"
                :key="i.k"
              >
                <dt>{{ i.k }}</dt>
                <dd :class="{ vide: !i.v }">
                  {{ i.v || 'Non renseigné' }}
                </dd>
              </div>
            </dl>
          </Panel>
          <Panel titre="Missions et activités">
            <p
              class="texte"
              :class="[{ vide: !f.missions }]"
            >
              {{ f.missions || 'Non renseigné' }}
            </p>
            <ul
              v-if="f.activites.length"
              class="liste"
            >
              <li
                v-for="a in f.activites"
                :key="a"
              >
                {{ a }}
              </li>
            </ul>
          </Panel>
          <Panel titre="Compétences et profil">
            <ul
              v-if="f.competences.length"
              class="liste"
            >
              <li
                v-for="c in f.competences"
                :key="c"
              >
                {{ c }}
              </li>
            </ul>
            <p
              class="texte"
              :class="[{ vide: !f.profil }]"
            >
              {{ f.profil || 'Profil non renseigné' }}
            </p>
          </Panel>
          <Panel
            v-if="f.environnement || f.conditions"
            titre="Environnement et conditions"
          >
            <p
              v-if="f.environnement"
              class="texte"
            >
              {{ f.environnement }}
            </p>
            <p
              v-if="f.conditions"
              class="texte"
            >
              {{ f.conditions }}
            </p>
          </Panel>
        </template>

        <!-- Modification -->
        <template v-else>
          <p
            v-if="f.origine === 'sirh'"
            class="note"
          >
            Fiche récupérée du SIRH. Règle à définir : une modification faite ici pourrait être remplacée à la prochaine synchronisation.
          </p>
          <Panel
            titre="Le poste"
            description="Enregistrement automatique. Les offres existantes ne sont pas modifiées."
          >
            <CspInput
              v-model="f.intitule"
              label="Intitulé du poste"
              :error="!f.intitule.trim()"
              :error-message="!f.intitule.trim() ? 'Indiquez l\'intitulé du poste.' : undefined"
            />
            <FieldRow :cols="2">
              <CspInput
                v-model="f.service"
                label="Service"
              />
              <CspInput
                v-model="f.localisation"
                label="Localisation"
                placeholder="Ville (département)"
              />
            </FieldRow>
            <FieldRow :cols="2">
              <CspCheckboxGroup
                v-model="f.categories"
                label="Catégorie(s)"
                :options="CATEGORIES"
              />
              <CspCheckboxGroup
                v-model="f.statuts"
                label="Ouvert aux"
                :options="STATUTS"
              />
            </FieldRow>
            <FieldRow :cols="2">
              <CspInput
                v-model="f.codePoste"
                label="Code poste"
              />
              <CspInput
                v-model="f.teletravail"
                label="Télétravail"
                placeholder="Ex. : 2 jours par semaine"
              />
            </FieldRow>
          </Panel>
          <Panel titre="Missions et activités">
            <CspTextarea
              v-model="f.missions"
              label="Missions"
              :rows="4"
            />
            <ListEditor
              v-model="f.activites"
              label="Activités"
            />
          </Panel>
          <Panel titre="Compétences et profil">
            <ListEditor
              v-model="f.competences"
              label="Compétences"
            />
            <CspTextarea
              v-model="f.profil"
              label="Profil"
              :rows="2"
            />
          </Panel>
          <Panel titre="Environnement et conditions">
            <CspTextarea
              v-model="f.environnement"
              label="Environnement de travail"
              :rows="2"
            />
            <CspInput
              v-model="f.conditions"
              label="Conditions particulières"
            />
          </Panel>
        </template>
      </div>

      <aside class="col">
        <Panel titre="Origine">
          <template v-if="f.origine === 'sirh' && f.sirh">
            <p class="texte">
              Récupérée du SIRH ministériel (simulation), réf. {{ f.sirh.reference }}.
            </p>
            <p class="mention">
              Dernière synchronisation : {{ f.sirh.synchroLe.toLowerCase() }}. Les règles de mise à jour entre le SIRH et l'ATS restent à définir.
            </p>
            <SimulationNote>
              <CspButton
                label="Synchroniser"
                size="sm"
                variant="tertiary"
                icon="ri:refresh-line"
                is-icon-left
                @click="synchroniser"
              />
            </SimulationNote>
          </template>
          <template v-else-if="f.origine === 'document' && f.document">
            <p class="texte">
              Constituée à partir du document <strong>{{ f.document.nom }}</strong>, ajouté le {{ f.document.ajouteLe }}.
            </p>
            <p class="mention">
              Extraction simulée ; le document reste rattaché à la fiche.
            </p>
          </template>
          <p
            v-else
            class="texte"
          >
            Créée et maintenue dans l'ATS.
          </p>
        </Panel>

        <Panel titre="Offres rattachées">
          <p
            v-if="!offres.length"
            class="mention"
          >
            Aucune offre pour l'instant. Une fiche peut exister sans offre.
          </p>
          <ul
            v-else
            class="offres"
          >
            <li
              v-for="o in offres"
              :key="o.id"
            >
              <button
                type="button"
                class="offre"
                @click="aller({ nom: 'offre', id: o.id })"
              >
                <span class="offre__tete">
                  <strong>{{ o.titre }}</strong>
                  <EtatBadge :etat="o.etat" />
                </span>
                <small>{{ o.id }} · {{ o.nbPostes }} poste(s) · modifiée {{ o.modifieLe.toLowerCase() }}</small>
              </button>
            </li>
          </ul>
          <p class="mention">
            Modifier la fiche ne modifie pas le texte des offres existantes.
          </p>
        </Panel>

        <Panel titre="Historique">
          <ol class="histo">
            <li
              v-for="(h, i) in [...f.historique].reverse()"
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

.save {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.dl {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--csp-space-3) var(--csp-space-6);
  margin: 0;

  dt {
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }

  dd {
    margin: 0;
    font-size: var(--csp-font-size-sm);
  }
}

.texte {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  line-height: var(--csp-line-height-relaxed);
}

.liste {
  margin: 0;
  padding-left: var(--csp-space-5);
  list-style: disc;
  font-size: var(--csp-font-size-sm);
}

.vide {
  color: var(--text-mention-grey);
  font-style: italic;
}

.mention {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.note {
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-blue-france);
  background: var(--background-default-grey);
  font-size: var(--csp-font-size-sm);
}

.offres,
.histo {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

.offre {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  width: 100%;
  padding: var(--csp-space-2) var(--csp-space-3);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  font: inherit;
  font-size: var(--csp-font-size-sm);
  text-align: left;
  color: var(--text-default-grey);
  cursor: pointer;

  small {
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }

  &:hover {
    background: var(--background-default-grey-hover);
  }
}

.offre__tete {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--csp-space-2);
}

.histo {
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
</style>
