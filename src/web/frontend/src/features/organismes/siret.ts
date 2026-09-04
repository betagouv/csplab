import { SIRET_LENGTH } from './constants/organisme'

const LUHN_DIGIT_OVERFLOW_THRESHOLD = 9

// La Poste's SIREN predates the INSEE Luhn check and is exempt from it,
// mirroring the backend SIRET value object.
const LA_POSTE_SIREN = '356000000'

function isLuhnValid(digits: string): boolean {
  let total = 0
  for (const [index, char] of [...digits].reverse().entries()) {
    let digit = Number(char)
    if (index % 2 === 1) {
      digit *= 2
      if (digit > LUHN_DIGIT_OVERFLOW_THRESHOLD)
        digit -= LUHN_DIGIT_OVERFLOW_THRESHOLD
    }
    total += digit
  }
  return total % 10 === 0
}

export function isSiretValid(value: string): boolean {
  if (value.length !== SIRET_LENGTH || !/^\d+$/.test(value))
    return false
  return value.startsWith(LA_POSTE_SIREN) || isLuhnValid(value)
}
