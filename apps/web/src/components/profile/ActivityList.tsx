import Link from "next/link";

interface Props {
  username: string;
}

/**
 * Activity history list — placeholder until the activity feed endpoint
 * supports public access by username (current endpoint requires auth).
 * Shows an onboarding CTA when empty.
 */
// eslint-disable-next-line @typescript-eslint/no-unused-vars
export function ActivityList({ username }: Props) {
  // Activities will be fetched once /users/{username}/activities is public.
  const activities: unknown[] = [];

  if (activities.length === 0) {
    return (
      <div className="text-center py-8 space-y-3">
        <p className="text-4xl">📋</p>
        <p className="text-slate-400 text-sm">No activities logged yet.</p>
        <Link
          href="/claim"
          className="inline-block text-sm text-angel-gold hover:underline"
        >
          Log your first activity →
        </Link>
      </div>
    );
  }

  return (
    <ul className="space-y-2">
      {activities.map((_, i) => (
        <li key={i} className="bg-slate-700 rounded-xl p-3 text-sm text-slate-300">
          Activity {i + 1}
        </li>
      ))}
    </ul>
  );
}
