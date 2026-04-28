import type { Metadata } from "next";

export const metadata: Metadata = { title: "Group" };

export default async function GroupDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return (
    <div className="max-w-2xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Group {id}</h1>
      <p className="text-slate-400">Group detail coming soon.</p>
    </div>
  );
}
