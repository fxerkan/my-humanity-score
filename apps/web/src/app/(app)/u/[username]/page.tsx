import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ScoreRing } from "@/components/profile/ScoreRing";
import { CategoryBars } from "@/components/profile/CategoryBars";
import { BadgeGrid } from "@/components/profile/BadgeGrid";
import { ActivityList } from "@/components/profile/ActivityList";
import { ProfileHeader } from "@/components/profile/ProfileHeader";
import { getLevelInfo } from "@/lib/utils";

/**
 * SSR fetch uses the internal Docker network URL (API_INTERNAL_URL) when
 * running inside the container, falling back to NEXT_PUBLIC_API_URL for local
 * dev without Docker, and finally a hardcoded default for cold starts.
 *
 * NEXT_PUBLIC_* vars are baked into the client bundle at build time.
 * API_INTERNAL_URL is a runtime server-only env var — safe to use in
 * server components but never exposed to the browser.
 */
const API_BASE =
  process.env.API_INTERNAL_URL ??
  process.env.NEXT_PUBLIC_API_URL ??
  "http://localhost:8000";

interface ScoreSummary {
  total_score: number;
  score_level: string;
  social_impact: number;
  environmental: number;
  knowledge_innovation: number;
  economic_contribution: number;
  cultural_artistic: number;
  civic_political: number;
  calculated_at: string;
}

interface UserPublicProfile {
  username: string;
  display_name: string | null;
  avatar_url: string | null;
  bio: string | null;
  country_code: string | null;
  created_at: string;
  score: ScoreSummary | null;
}

/** Fetch public profile server-side (SSR). */
async function fetchProfile(username: string): Promise<UserPublicProfile | null> {
  try {
    const res = await fetch(`${API_BASE}/users/${encodeURIComponent(username)}`, {
      next: { revalidate: 60 },
    });
    if (res.status === 404) return null;
    if (!res.ok) throw new Error(`API error ${res.status}`);
    return res.json() as Promise<UserPublicProfile>;
  } catch {
    return null;
  }
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ username: string }>;
}): Promise<Metadata> {
  const { username } = await params;
  const profile = await fetchProfile(username);
  if (!profile) return { title: "User not found" };

  const displayName = profile.display_name ?? profile.username;
  const score = profile.score?.total_score ?? 0;
  const level = getLevelInfo(score);

  return {
    title: `${displayName} (@${profile.username})`,
    description: `${displayName}'s My Humanity Score: ${Math.round(score)} — ${level.emoji} ${level.name}`,
    openGraph: {
      title: `${displayName} | My Humanity Score`,
      description: profile.bio ?? `MHS score: ${Math.round(score)}`,
      images: [
        {
          // og:image must use the public-facing URL, not the internal Docker URL.
          url: `${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8001"}/og/user/${profile.username}`,
          width: 1200,
          height: 630,
          alt: `${displayName}'s MHS profile`,
        },
      ],
    },
  };
}

/** Zero-state score used for new users who have no score record yet. */
const ZERO_SCORE: ScoreSummary = {
  total_score: 0,
  score_level: "awakening",
  social_impact: 0,
  environmental: 0,
  knowledge_innovation: 0,
  economic_contribution: 0,
  cultural_artistic: 0,
  civic_political: 0,
  calculated_at: new Date().toISOString(),
};

export default async function UserProfilePage({
  params,
}: {
  params: Promise<{ username: string }>;
}) {
  const { username } = await params;
  const profile = await fetchProfile(username);
  if (!profile) notFound();

  const score = profile.score ?? ZERO_SCORE;
  const level = getLevelInfo(score.total_score);

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-8">
      <ProfileHeader profile={profile} />

      {/* Score ring + level */}
      <section className="bg-slate-800 rounded-2xl p-6 flex flex-col sm:flex-row items-center gap-6">
        <ScoreRing score={score.total_score} level={level} />
        <div className="text-center sm:text-left">
          <p className="text-slate-400 text-sm">MHS Score</p>
          <p className="text-5xl font-black text-white">{Math.round(score.total_score)}</p>
          <p data-testid="mhs-level-badge" className="text-lg font-semibold mt-1" style={{ color: level.color }}>
            {level.emoji} {level.name}
          </p>
          <p className="text-slate-500 text-xs mt-1">
            Last updated {new Date(score.calculated_at).toLocaleDateString()}
          </p>
        </div>
      </section>

      {/* Category breakdown */}
      <section className="bg-slate-800 rounded-2xl p-6">
        <h2 className="text-lg font-bold mb-4">Score Breakdown</h2>
        <CategoryBars score={score} />
      </section>

      {/* Badge grid */}
      <section className="bg-slate-800 rounded-2xl p-6">
        <h2 className="text-lg font-bold mb-4">Badges</h2>
        <BadgeGrid username={username} />
      </section>

      {/* Activity history */}
      <section className="bg-slate-800 rounded-2xl p-6">
        <h2 className="text-lg font-bold mb-4">Activity History</h2>
        <ActivityList username={username} />
      </section>
    </div>
  );
}
