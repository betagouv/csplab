import type { StoryObj } from '@storybook/vue3'
import type { CspTagSize, CspTagVariant } from '@/components/base/CspTag/tag'
import { ref } from 'vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import CspTagGroup from '@/components/base/CspTag/CspTagGroup.vue'

interface CspTagProps {
  label?: string
  variant?: CspTagVariant
  size?: CspTagSize
  icon?: string
  pressed?: boolean
  disabled?: boolean
  href?: string
  value?: string | number
  dismissLabel?: string
}

const meta = {
  title: 'Éléments/Génériques/CspTag',
  component: CspTag,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['label', 'variant', 'size', 'icon', 'pressed', 'disabled', 'href', 'value', 'dismissLabel'],
    },
    docs: {
      description: {
        component: `Étiquette générique. Sert à **catégoriser ou filtrer** les contenus (à ne pas confondre avec \`CspBadge\` qui signale un état).

Construit sur les primitives [reka-ui](https://reka-ui.com) :
- \`static\` et \`clickable\` reposent sur le composant \`Primitive\` de reka et sont polymorphes via \`as\` / \`asChild\` ;
- \`dismissible\` est toujours un \`<button>\` ;
- \`selectable\` repose sur le composant reka \`Toggle\` rendu seul, ou sur \`ToggleGroupItem\` lorsqu'il est placé dans un \`CspTagGroup\`.
`,
      },
    },
  },
  argTypes: {
    label: {
      control: { type: 'text' },
      description: 'Libellé du tag (cas simple). Pour un contenu riche, utiliser le slot par défaut.',
      table: { type: { summary: 'string' } },
    },
    variant: {
      control: { type: 'radio' },
      options: ['static', 'clickable', 'selectable', 'dismissible'] satisfies CspTagVariant[],
      description: 'Mode d\'interaction du tag.',
      table: {
        type: { summary: 'static | clickable | selectable | dismissible' },
        defaultValue: { summary: 'static' },
      },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'] satisfies CspTagSize[],
      description: 'Taille du tag. Héritée du `CspTagGroup` si non précisée.',
      table: {
        type: { summary: 'sm | md | lg' },
        defaultValue: { summary: 'md' },
      },
    },
    icon: {
      control: { type: 'text' },
      description: 'Icône Iconify affichée à gauche. Non disponible sur `dismissible` (croix exclusive).',
      table: { type: { summary: 'string' } },
    },
    pressed: {
      control: { type: 'boolean' },
      description: 'État activé du tag `selectable` autonome. Lier avec `v-model:pressed`.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' },
      },
    },
    disabled: {
      control: { type: 'boolean' },
      description: 'Désactive les variantes interactives. Héritée du `CspTagGroup`.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' },
      },
    },
    href: {
      control: { type: 'text' },
      description: 'URL cible pour la variante `clickable`. Rend un `<a>` si fourni, sinon un `<button>`.',
      table: { type: { summary: 'string' } },
    },
    value: {
      control: { type: 'text' },
      description: 'Identifiant d\'un tag `selectable` au sein d\'un `CspTagGroup`.',
      table: { type: { summary: 'string | number' } },
    },
    dismissLabel: {
      control: { type: 'text' },
      description: 'Label accessible du bouton de suppression (`dismissible`). Par défaut : `Retirer le filtre {label}`.',
      table: { type: { summary: 'string' } },
    },
    as: { control: false, table: { disable: true } },
    asChild: { control: false, table: { disable: true } },
    class: { control: false, table: { disable: true } },
    style: { control: false, table: { disable: true } },
    key: { control: false, table: { disable: true } },
    ref: { control: false, table: { disable: true } },
    ref_for: { control: false, table: { disable: true } },
    ref_key: { control: false, table: { disable: true } },
  },
  args: {
    label: 'Libellé',
    variant: 'static',
    size: 'md',
    pressed: false,
    disabled: false,
  },
  render: (args: CspTagProps) => ({
    components: { CspTag },
    setup() {
      const pressed = ref(Boolean(args.pressed))
      return { args, pressed }
    },
    template: `
      <CspTag
        v-bind="args"
        v-model:pressed="pressed"
        @dismiss="() => {}"
      />
    `,
  }),
}

export default meta
type Story = StoryObj<CspTagProps>

const SIZES = ['sm', 'md', 'lg'] as const

export const Default: Story = {
  name: 'Par défaut',
}

export const Variants: Story = {
  name: 'Variantes',
  render: () => ({
    components: { CspTag },
    setup() {
      const pressed = ref(false)
      const dismissed = ref(false)
      return { pressed, dismissed }
    },
    template: `
      <div class="flex flex-col gap-6">
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">static (étiquette)</p>
          <CspTag label="Catégorie" variant="static" />
        </div>
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">clickable (lien)</p>
          <CspTag label="Voir tout" variant="clickable" href="#" />
        </div>
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">selectable (filtre à bascule / {{ pressed ? 'actif' : 'inactif' }})</p>
          <CspTag label="Filtre A" variant="selectable" v-model:pressed="pressed" />
        </div>
        <div>
          <p class="mb-2 text-sm text-text-mention-grey">dismissible : filtre actif à retirer</p>
          <CspTag v-if="!dismissed" label="Filtre actif" variant="dismissible" @dismiss="dismissed = true" />
          <span v-else class="text-sm text-text-mention-grey italic">retiré</span>
        </div>
      </div>
    `,
  }),
  parameters: { controls: { disable: true } },
}

export const WithIcon: Story = {
  name: 'Avec icône',
  render: () => ({
    components: { CspTag },
    template: `
      <div class="flex flex-row gap-4 flex-wrap">
        <CspTag label="Étiquette" variant="static" icon="ri:bookmark-line" />
        <CspTag label="Lien" variant="clickable" icon="ri:external-link-line" href="#" />
        <CspTag label="Filtre" variant="selectable" icon="ri:filter-line" />
      </div>
    `,
  }),
  parameters: { controls: { disable: true } },
}

export const Sizes: Story = {
  name: 'Tailles',
  render: () => ({
    components: { CspTag },
    setup() {
      return { sizes: SIZES }
    },
    template: `
      <div class="flex flex-col gap-6">
        <div v-for="s in sizes" :key="s">
          <p class="mb-2 text-sm text-text-mention-grey">{{ s }}</p>
          <div class="flex flex-row gap-3 flex-wrap">
            <CspTag :label="'Étiquette ' + s" :size="s" variant="static" />
            <CspTag :label="'Lien ' + s" :size="s" variant="clickable" href="#" />
            <CspTag :label="'Filtre ' + s" :size="s" variant="selectable" />
            <CspTag :label="'Sélectionné ' + s" :size="s" variant="selectable" :pressed="true" />
            <CspTag :label="'Actif ' + s" :size="s" variant="dismissible" />
          </div>
        </div>
      </div>
    `,
  }),
  parameters: { controls: { disable: true } },
}

export const Selectable: Story = {
  name: 'Sélectionnable (autonome)',
  render: () => ({
    components: { CspTag },
    setup() {
      const a = ref(false)
      const b = ref(true)
      const c = ref(false)
      return { a, b, c }
    },
    template: `
      <div class="flex flex-col gap-3">
        <p class="text-sm text-text-mention-grey">Tags <code>selectable</code> autonomes : chacun son <code>v-model:pressed</code>.</p>
        <div class="flex flex-row gap-2 flex-wrap">
          <CspTag label="Design" variant="selectable" v-model:pressed="a" />
          <CspTag label="Développement" variant="selectable" v-model:pressed="b" />
          <CspTag label="Produit" variant="selectable" v-model:pressed="c" />
        </div>
      </div>
    `,
  }),
  parameters: { controls: { disable: true } },
}

export const SelectableGroup: Story = {
  name: 'Sélectionnable (groupe)',
  render: () => ({
    components: { CspTag, CspTagGroup },
    setup() {
      const single = ref<string>('dev')
      const multiple = ref<string[]>(['design', 'data'])
      const domains = [
        { value: 'design', label: 'Design' },
        { value: 'dev', label: 'Développement' },
        { value: 'produit', label: 'Produit' },
        { value: 'data', label: 'Data' },
      ]
      return { single, multiple, domains }
    },
    template: `
    <p class="text-sm mb-2 text-text-mention-grey">(navigable avec les flèches directionnelles)</p>
      <div class="flex flex-col gap-6">
        <div class="flex flex-col gap-2">
          <p class="text-sm text-text-mention-grey">Groupe multiple</p>
          <CspTagGroup v-model="multiple" type="multiple">
            <CspTag
              v-for="d in domains"
              :key="d.value"
              :value="d.value"
              :label="d.label"
              variant="selectable"
            />
          </CspTagGroup>
        </div>
        <div class="flex flex-col gap-2">
          <p class="text-sm text-text-mention-grey">Groupe single</p>
          <CspTagGroup v-model="single" type="single">
            <CspTag
              v-for="d in domains"
              :key="d.value"
              :value="d.value"
              :label="d.label"
              variant="selectable"
            />
          </CspTagGroup>
        </div>
      </div>
    `,
  }),
  parameters: { controls: { disable: true } },
}

export const Dismissible: Story = {
  name: 'Supprimable',
  render: () => ({
    components: { CspTag },
    setup() {
      const active = ref(['Accessibilité', 'Vue', 'TypeScript'])
      return { active }
    },
    template: `
      <div class="flex flex-col gap-3">
        <p class="text-sm text-text-mention-grey">Filtres actifs :</p>
        <div class="flex flex-row gap-2 flex-wrap">
          <CspTag
            v-for="label in active"
            :key="label"
            :label="label"
            variant="dismissible"
            @dismiss="active = active.filter(l => l !== label)"
          />
          <span v-if="active.length === 0" class="text-sm text-text-mention-grey italic">Aucun filtre actif</span>
        </div>
      </div>
    `,
  }),
  parameters: { controls: { disable: true } },
}

export const States: Story = {
  name: 'États',
  render: () => ({
    components: { CspTag },
    template: `
      <div class="flex flex-col gap-4">
        <div class="flex flex-row gap-3 flex-wrap items-center">
          <p class="w-28 text-sm text-text-mention-grey">Normal</p>
          <CspTag label="Clickable" variant="clickable" href="#" />
          <CspTag label="Sélectionnable" variant="selectable" />
          <CspTag label="Sélectionné" variant="selectable" :pressed="true" />
          <CspTag label="Actif" variant="dismissible" />
        </div>
        <div class="flex flex-row gap-3 flex-wrap items-center">
          <p class="w-28 text-sm text-text-mention-grey">Désactivé</p>
          <CspTag label="Clickable" variant="clickable" :disabled="true" />
          <CspTag label="Sélectionnable" variant="selectable" :disabled="true" />
          <CspTag label="Sélectionné" variant="selectable" :pressed="true" :disabled="true" />
          <CspTag label="Supprimable" variant="dismissible" :disabled="true" />
        </div>
      </div>
    `,
  }),
  parameters: { controls: { disable: true } },
}
