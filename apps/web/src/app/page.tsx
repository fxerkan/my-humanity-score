export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-slate-900 to-slate-800 text-white">
      <div className="text-center space-y-6 px-4">
        <div className="text-6xl">🌍</div>
        <h1 className="text-4xl font-bold tracking-tight">My Humanity Score (MHS)</h1>
        <p className="text-xl text-slate-300">Every person&apos;s impact on humanity — finally measured.</p>
        <p className="text-slate-400 max-w-md">
          Measure, track, and celebrate your positive impact on humanity.
        </p>
        <div className="pt-4">
          <span className="inline-flex items-center gap-2 bg-slate-700 rounded-full px-4 py-2 text-sm text-slate-300">
            <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
            Coming soon — Pre-MVP in progress
          </span>
        </div>
      </div>
    </main>
  );
}
