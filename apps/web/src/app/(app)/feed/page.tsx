import type { Metadata } from "next";

export const metadata: Metadata = { title: "Feed" };

/**
 * Community feed page.
 * Unauthenticated access is blocked server-side by src/middleware.ts —
 * no client-side auth guard needed here.
 */
export default function FeedPage() {
  return (
    <div className="max-w-2xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Community Feed</h1>
      <p className="text-slate-400">Activity stream coming soon.</p>
    </div>
  );
}
