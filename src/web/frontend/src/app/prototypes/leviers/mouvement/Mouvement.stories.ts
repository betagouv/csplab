import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import { keepTheme } from '../../keepTheme'
import { withLevierOption } from '../options'
import MouvementPlanche from './MouvementPlanche.vue'
import MouvementScene from './MouvementScene.vue'
import { MOUVEMENT } from './pistes'

// Each track has a screen that plays the demo in a loop on the kanban, and a plate that frames this screen above the
// timeline of the track; each gesture has a plate that compares the tracks, in real time and slowed down four times
const meta = {
  title: 'Prototypes/Leviers/Mouvement',
  decorators: [keepTheme],
  parameters: { layout: 'fullscreen' },
  globals: { interfaceTheme: 'kit' },
} satisfies Meta

export default meta

type Story = StoryObj<{ demo?: string, ralenti?: number }>

const ECRAN = {
  decorators: [withLevierOption(MOUVEMENT)],
  parameters: { appRoute: `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}` },
  argTypes: {
    demo: { control: 'select' as const, options: ['parcours', 'menu', 'panneau', 'depot', 'dialogue'] },
    ralenti: { control: 'select' as const, options: [1, 4] },
  },
  args: { demo: 'parcours', ralenti: 1 },
  render: (args: Record<string, unknown>) => ({
    components: { MouvementScene },
    setup: () => ({ demo: args.demo, ralenti: Number(args.ralenti) }),
    template: '<MouvementScene :demo="demo" :ralenti="ralenti" />',
  }),
}

export const SceneKit: Story = { ...ECRAN, name: 'Écran, instantané', parameters: { ...ECRAN.parameters, option: 'kit' } }
export const SceneDsfr: Story = { ...ECRAN, name: 'Écran, 300 ms du DSFR', parameters: { ...ECRAN.parameters, option: 'dsfr' } }
export const SceneRoles: Story = { ...ECRAN, name: 'Écran, durées par rôle', parameters: { ...ECRAN.parameters, option: 'roles' } }
export const SceneTrajectoires: Story = {
  ...ECRAN,
  name: 'Écran, trajectoires',
  parameters: { ...ECRAN.parameters, option: 'trajectoires' },
}

function planche(props: Record<string, unknown>): Pick<Story, 'render'> {
  return {
    render: () => ({
      components: { MouvementPlanche },
      setup: () => ({ props }),
      template: '<MouvementPlanche v-bind="props" />',
    }),
  }
}

export const RegleKit: Story = { name: 'Règle, instantané', ...planche({ piste: 'kit' }) }
export const RegleDsfr: Story = { name: 'Règle, 300 ms du DSFR', ...planche({ piste: 'dsfr' }) }
export const RegleRoles: Story = { name: 'Règle, durées par rôle', ...planche({ piste: 'roles' }) }
export const RegleTrajectoires: Story = { name: 'Règle, trajectoires', ...planche({ piste: 'trajectoires' }) }

export const Panneau: Story = { name: 'Comparaison, panneau', ...planche({ geste: 'panneau' }) }
export const Menu: Story = { name: 'Comparaison, menu', ...planche({ geste: 'menu' }) }
export const Dialogue: Story = { name: 'Comparaison, dialogue', ...planche({ geste: 'dialogue' }) }
export const Depot: Story = { name: 'Comparaison, carte déposée', ...planche({ geste: 'depot' }) }

export const PanneauRalenti: Story = { name: 'Comparaison, panneau, ralenti', ...planche({ geste: 'panneau', ralenti: 4 }) }
export const MenuRalenti: Story = { name: 'Comparaison, menu, ralenti', ...planche({ geste: 'menu', ralenti: 4 }) }
export const DialogueRalenti: Story = { name: 'Comparaison, dialogue, ralenti', ...planche({ geste: 'dialogue', ralenti: 4 }) }
export const DepotRalenti: Story = { name: 'Comparaison, carte déposée, ralenti', ...planche({ geste: 'depot', ralenti: 4 }) }
