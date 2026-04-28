/**
 * Next.js edge middleware — server-side auth guard.
 *
 * Protected routes require the `mhs_session` cookie to be present.
 * The cookie is set by lib/auth.ts whenever tokens are stored in memory.
 * It is NOT a JWT — just a flag so middleware can redirect without
 * exposing sensitive values.
 *
 * Unauthenticated requests to protected routes are redirected to
 * /login?next=<original-path>.
 */
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

/** Route prefixes that require authentication. */
const PROTECTED_PREFIXES = [
  "/feed",
  "/settings",
  "/angel",
  "/groups",
  "/leaderboard",
];

export function middleware(request: NextRequest): NextResponse {
  const { pathname } = request.nextUrl;

  const isProtected = PROTECTED_PREFIXES.some(
    (prefix) => pathname === prefix || pathname.startsWith(prefix + "/"),
  );

  if (isProtected && !request.cookies.has("mhs_session")) {
    const loginUrl = request.nextUrl.clone();
    loginUrl.pathname = "/login";
    loginUrl.searchParams.set("next", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  /**
   * Run on all routes EXCEPT:
   * - Next.js internals (_next/*)
   * - Static files (anything with a file extension like .ico, .png, etc.)
   */
  matcher: ["/((?!_next|api|favicon\\.ico|.*\\..*).*)" ],
};
