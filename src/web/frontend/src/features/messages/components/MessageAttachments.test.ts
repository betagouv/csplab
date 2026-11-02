import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { defineComponent, h, ref } from 'vue'
import { setupUser } from '@/test/render'
import MessageAttachments from './MessageAttachments.vue'

const CV = new File(['cv'], 'cv.pdf', { type: 'application/pdf' })
const NOTES = new File(['notes'], 'notes.txt', { type: 'text/plain' })

function renderAttachments(files: File[]) {
  return render(MessageAttachments, { props: { 'modelValue': files, 'onUpdate:modelValue': () => {} } })
}

describe('messageAttachments', () => {
  it('lists the attached files with the error of a refused format', () => {
    renderAttachments([CV, NOTES])

    expect(screen.getByRole('list', { name: 'Pièces jointes' })).toBeInTheDocument()
    expect(screen.getByText('cv.pdf')).toBeInTheDocument()
    expect(screen.getByText('Format non supporté. Formats acceptés : PDF, PNG, JPEG.')).toBeInTheDocument()
  })

  it('removes the file whose button is pressed', async () => {
    const { emitted } = renderAttachments([CV, NOTES])

    await setupUser().click(screen.getByRole('button', { name: 'Retirer notes.txt' }))

    expect(emitted('update:modelValue')).toEqual([[[CV]]])
  })

  it('moves the focus to the attach button once the last file is removed', async () => {
    const Host = defineComponent({
      setup() {
        const files = ref([CV])
        return () => h(MessageAttachments, { 'modelValue': files.value, 'onUpdate:modelValue': (value: File[]) => {
          files.value = value
        } })
      },
    })
    render(Host)

    await setupUser().click(screen.getByRole('button', { name: 'Retirer cv.pdf' }))

    expect(screen.getByRole('button', { name: 'Pièce jointe' })).toHaveFocus()
  })
})
