import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { defineComponent, h, nextTick, ref } from 'vue'
import { ORGANISME } from '@/test/fixtures/organismes'
import { setupUser } from '@/test/render'
import OrganismeFormDrawer from './OrganismeFormDrawer.vue'

type DrawerInstance = InstanceType<typeof OrganismeFormDrawer>

async function renderDrawer(organisme: typeof ORGANISME | null = null) {
  const drawer = ref<DrawerInstance | null>(null)
  const Host = defineComponent({
    emits: ['create', 'update'],
    setup(_, { emit }) {
      return () => h(OrganismeFormDrawer, {
        ref: drawer,
        open: true,
        organisme,
        onCreate: (payload: unknown) => emit('create', payload),
        onUpdate: (payload: unknown) => emit('update', payload),
      })
    },
  })
  const result = render(Host)
  await nextTick()
  return { ...result, drawer }
}

function nomInput() {
  return screen.getByRole('textbox', { name: 'Nom de l\'organisme' })
}

function siretInput() {
  return screen.getByRole('textbox', { name: 'SIRET de l\'organisme' })
}

function createButton() {
  return screen.getByRole('button', { name: 'Créer l\'organisme' })
}

async function fillCreation(user: ReturnType<typeof setupUser>, siret: string) {
  await user.type(nomInput(), 'Nouvel organisme')
  await user.click(siretInput())
  await user.paste(siret)
  await user.click(screen.getByRole('radio', { name: 'Fonction Publique Territoriale' }))
}

describe('organismeFormDrawer', () => {
  it('keeps the submit button disabled until required fields are filled', async () => {
    const user = setupUser()
    await renderDrawer()
    expect(createButton()).toBeDisabled()

    await user.type(nomInput(), 'Nouvel organisme')
    await user.type(siretInput(), '123')
    expect(createButton()).toBeDisabled()

    await user.click(screen.getByRole('radio', { name: 'Fonction Publique d\'État' }))
    expect(createButton()).toBeEnabled()
  })

  it('surfaces a length error on submit without emitting', async () => {
    const user = setupUser()
    const { emitted } = await renderDrawer()

    await fillCreation(user, '123')
    await user.click(createButton())

    expect(emitted().create).toBeUndefined()
    expect(screen.getByText('Le SIRET doit comporter 14 chiffres.')).toBeInTheDocument()
  })

  it('strips non digit characters from a pasted siret', async () => {
    const user = setupUser()
    const { emitted } = await renderDrawer()

    await fillCreation(user, '110 046 018 00021')
    await user.click(createButton())

    const [payload] = emitted().create![0] as [{ siret: string }]
    expect(payload.siret).toBe('11004601800021')
  })

  it('emits the payload on create', async () => {
    const user = setupUser()
    const { emitted } = await renderDrawer()

    await fillCreation(user, '11004601800021')
    await user.click(createButton())

    expect(emitted().create).toEqual([[{
      nom: 'Nouvel organisme',
      siret: '11004601800021',
      versant: 'FPT',
      gestion_ats: true,
    }]])
  })

  it('rejects an invalid checksum on submit without emitting', async () => {
    const user = setupUser()
    const { emitted } = await renderDrawer()

    await fillCreation(user, '12345671234567')
    await user.click(createButton())

    expect(emitted().create).toBeUndefined()
    expect(screen.getByText('Ce SIRET n\'est pas valide, vérifiez votre saisie.')).toBeInTheDocument()
  })

  it('prefills the form and locks the siret in edition', async () => {
    await renderDrawer(ORGANISME)

    expect(screen.getByRole('heading', { name: 'Modifier l\'organisme' })).toBeInTheDocument()
    expect(siretInput()).toHaveValue(ORGANISME.siret)
    expect(siretInput()).toBeDisabled()
    expect(nomInput()).toHaveValue(ORGANISME.nom)
  })

  it('emits the payload without the siret on update', async () => {
    const user = setupUser()
    const { emitted } = await renderDrawer(ORGANISME)

    await user.clear(nomInput())
    await user.type(nomInput(), 'Organisme renommé')
    await user.click(screen.getByRole('button', { name: 'Enregistrer les modifications' }))

    expect(emitted().update).toEqual([[{
      nom: 'Organisme renommé',
      versant: 'FPT',
      gestion_ats: false,
    }]])
  })

  it('surfaces a siret conflict on the siret field', async () => {
    const { drawer } = await renderDrawer()

    drawer.value!.setSiretError('Ce SIRET est déjà utilisé par un autre organisme')

    expect(await screen.findByText('Ce SIRET est déjà utilisé par un autre organisme')).toBeInTheDocument()
  })
})
