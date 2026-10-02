type MultipartBody = Record<string, string | File[] | undefined>

export function toMultipartFormData(body: MultipartBody): FormData {
  const formData = new FormData()
  for (const [key, value] of Object.entries(body)) {
    if (value === undefined)
      continue
    if (Array.isArray(value))
      value.forEach(file => formData.append(key, file))
    else
      formData.append(key, value)
  }
  return formData
}
