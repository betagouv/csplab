import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { nextTick } from 'vue'
import CompteUtilisateurForm from './CompteUtilisateurForm.vue'

async function fill(wrapper: ReturnType<typeof mount>, name: string, value: string) {
  await wrapper.find(`[name="${name}"]`).setValue(value)
  await nextTick()
}

describe('compteUtilisateurForm', () => {
  it('keeps submit disabled until required fields are filled', async () => {
    const wrapper = mount(CompteUtilisateurForm, {
      props: { submitLabel: 'Créer le compte', lockedType: 'gestionnaire' },
    })
    const submit = () => wrapper.find('button[type="submit"]').element as HTMLButtonElement
    expect(submit().disabled).toBe(true)

    await fill(wrapper, 'email', 'jean.plat@exemple.gouv.fr')
    await fill(wrapper, 'nom', 'Plat')
    expect(submit().disabled).toBe(true)

    await fill(wrapper, 'prenom', 'Jean')
    expect(submit().disabled).toBe(false)
  })

  it('emits the payload with the locked type and disables the choice', async () => {
    const wrapper = mount(CompteUtilisateurForm, {
      props: {
        submitLabel: 'Créer le compte',
        lockedType: 'gestionnaire',
        initialEmail: 'jean.plat@exemple.gouv.fr',
      },
    })
    const radios = wrapper.findAll('[role="radio"]')
    expect(radios.length).toBeGreaterThan(0)
    radios.forEach(radio => expect(radio.attributes('disabled')).toBeDefined())

    await fill(wrapper, 'nom', 'Plat')
    await fill(wrapper, 'prenom', 'Jean')
    await wrapper.find('form').trigger('submit')

    expect(wrapper.emitted('submit')![0][0]).toEqual({
      email: 'jean.plat@exemple.gouv.fr',
      nom: 'Plat',
      prenom: 'Jean',
      poste: '',
      type: 'gestionnaire',
    })
  })
})
