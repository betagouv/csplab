import { resolve } from 'node:path'
import { ESLint, RuleTester } from 'eslint'
import { describe, expect, it } from 'vitest'
import noApiModuleMock from '../../../../eslint/no-api-module-mock.mjs'

RuleTester.describe = describe
RuleTester.it = it

const TEST_FILE = '/repo/frontend/src/features/alpha/views/Alpha.test.ts'

new RuleTester().run('no-api-module-mock', noApiModuleMock, {
  valid: [
    { code: `vi.mock('@/features/beta/api')`, filename: TEST_FILE, options: [['alpha']] },
    { code: `vi.mock('@/api/utilisateur')`, filename: TEST_FILE, options: [['alpha']] },
  ],
  invalid: [
    { code: `vi.mock('../api')`, filename: TEST_FILE, options: [['alpha']], errors: [{ messageId: 'handlers' }] },
    { code: `vi.mock('@/features/alpha/api')`, filename: TEST_FILE, options: [['alpha']], errors: [{ messageId: 'handlers' }] },
  ],
})

describe('eslint configuration', () => {
  it('applies no-api-module-mock to the features that have handlers', async () => {
    const eslint = new ESLint({ cwd: resolve(import.meta.dirname, '../../../..') })
    const results = await eslint.lintText(`import { vi } from 'vitest'\nvi.mock('../api')\n`, { filePath: 'frontend/src/features/recrutements/views/Probe.test.ts' })
    const ruleIds = results.flatMap(result => result.messages).map(message => message.ruleId)
    expect(ruleIds).toContain('csplab/no-api-module-mock')
  })
})
