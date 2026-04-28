import Link from "next/link";

interface Props {
  username: string;
}

/**
 * Badge grid — placeholder until the badge engine is implemented (task-8).
 * Shows an onboarding CTA for users with no badges yet.
 */
// eslint-disable-next-line @typescript-eslint/no-unused-vars
export function BadgeGrid({ username }: Props) {
  // Badges will be fetched from /users/{username}/badges once task-8 lands.
  const badges: unknown[] = [];

  if (badges.length === 0) {
    return (
      <div data-testid="onboarding-cta" className="text-center py-8 space-y-3">
        <p className="text-4xl">🏅</p>
        <p className="text-slate-400 text-sm">No badges earned yet.</p>
        <Link
          href="/claim"
          className="inline-block text-sm text-angel-gold hover:underline"
        >
          Start your journey →
        </Link>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-4 sm:grid-cols-6 gap-3">
      {badges.map((_, i) => (
        <div
          key={i}
          className="aspect-square bg-slate-700 rounded-xl flex items-center justify-center text-2xl"
        >
          🏅
        </div>
      ))}
    </div>
  );
}
