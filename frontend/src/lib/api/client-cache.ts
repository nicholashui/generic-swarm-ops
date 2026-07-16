/**
 * Short-lived in-memory cache for client-side GET responses.
 * Cuts repeat network calls when navigating back to the same panels.
 */

type Entry<T> = { value: T; expiresAt: number };

const store = new Map<string, Entry<unknown>>();

const DEFAULT_TTL_MS = 30_000;

export function getCached<T>(key: string): T | undefined {
  const hit = store.get(key);
  if (!hit) return undefined;
  if (Date.now() > hit.expiresAt) {
    store.delete(key);
    return undefined;
  }
  return hit.value as T;
}

export function setCached<T>(key: string, value: T, ttlMs = DEFAULT_TTL_MS): T {
  store.set(key, { value, expiresAt: Date.now() + ttlMs });
  return value;
}

export async function cachedFetch<T>(
  key: string,
  loader: () => Promise<T>,
  ttlMs = DEFAULT_TTL_MS,
): Promise<T> {
  const hit = getCached<T>(key);
  if (hit !== undefined) return hit;
  const value = await loader();
  return setCached(key, value, ttlMs);
}

/** Test helper */
export function clearClientCache(): void {
  store.clear();
}
