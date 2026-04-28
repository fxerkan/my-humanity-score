import type { Metadata } from "next";

export const metadata: Metadata = { title: "Angel AI" };

export default function AngelPage() {
  return (
    <div className="max-w-2xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Angel AI</h1>
      <p className="text-slate-400">Your compassionate AI guide — coming soon.</p>
    </div>
  );
}
