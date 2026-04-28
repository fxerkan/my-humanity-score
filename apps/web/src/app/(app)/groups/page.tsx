import type { Metadata } from "next";

export const metadata: Metadata = { title: "Groups" };

export default function GroupsPage() {
  return (
    <div className="max-w-2xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Groups</h1>
      <p className="text-slate-400">Group management coming soon.</p>
    </div>
  );
}
