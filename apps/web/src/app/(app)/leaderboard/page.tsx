import type { Metadata } from "next";

export const metadata: Metadata = { title: "Leaderboard" };

export default function LeaderboardPage() {
  return (
    <div className="max-w-2xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Leaderboard</h1>
      <p className="text-slate-400">Top contributors coming soon.</p>
    </div>
  );
}
