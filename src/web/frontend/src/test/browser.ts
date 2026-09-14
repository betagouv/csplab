export function createLocalStorageMock() {
  const storage = new Map<string, string>()

  return {
    getItem: (key: string) => storage.get(key) ?? null,
    setItem: (key: string, value: string) => storage.set(key, value),
    removeItem: (key: string) => storage.delete(key),
    clear: () => storage.clear(),
  }
}

export function createMediaQueryMock(matches: boolean) {
  const listeners = new Set<(event: MediaQueryListEvent) => void>()

  return {
    matches,
    addEventListener: (_: string, listener: (event: MediaQueryListEvent) => void) => {
      listeners.add(listener)
    },
    removeEventListener: (_: string, listener: (event: MediaQueryListEvent) => void) => {
      listeners.delete(listener)
    },
    dispatchChange(newMatches: boolean) {
      this.matches = newMatches
      listeners.forEach(listener => listener({ matches: newMatches } as MediaQueryListEvent))
    },
    get listenerCount() {
      return listeners.size
    },
  }
}
