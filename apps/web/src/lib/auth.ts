/**
 * Token store — keeps access/refresh tokens in memory for the current tab,
 * with localStorage backup so page refreshes don't force re-login.
 *
 * A non-sensitive `mhs_session=1` cookie is maintained in parallel so
 * Next.js middleware can redirect unauthenticated requests server-side
 * without exposing the actual JWT.
 */

const LS_ACCESS  = "mhs_access_token";
const LS_REFRESH = "mhs_refresh_token";

let _access:  string | null = null;
let _refresh: string | null = null;

// ── Cookie helpers ────────────────────────────────────────────────────────────

function setSessionCookie(): void {
  if (typeof document !== "undefined") {
    document.cookie = "mhs_session=1; path=/; SameSite=Strict";
  }
}

function clearSessionCookie(): void {
  if (typeof document !== "undefined") {
    document.cookie =
      "mhs_session=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Strict";
  }
}

// ── Internal hydration (called once on first getAccessToken / app boot) ───────

function _hydrate(): void {
  if (_access !== null) return; // already hydrated
  if (typeof localStorage === "undefined") return;
  _access  = localStorage.getItem(LS_ACCESS);
  _refresh = localStorage.getItem(LS_REFRESH);
}

// ── Public API ────────────────────────────────────────────────────────────────

export function getAccessToken(): string | null {
  _hydrate();
  return _access;
}

export function getRefreshToken(): string | null {
  _hydrate();
  return _refresh;
}

export function setTokens(access: string, refresh: string): void {
  _access  = access;
  _refresh = refresh;
  if (typeof localStorage !== "undefined") {
    localStorage.setItem(LS_ACCESS,  access);
    localStorage.setItem(LS_REFRESH, refresh);
  }
  setSessionCookie();
}

export function clearTokens(): void {
  _access  = null;
  _refresh = null;
  if (typeof localStorage !== "undefined") {
    localStorage.removeItem(LS_ACCESS);
    localStorage.removeItem(LS_REFRESH);
  }
  clearSessionCookie();
}

export function isAuthenticated(): boolean {
  _hydrate();
  return _access !== null;
}
