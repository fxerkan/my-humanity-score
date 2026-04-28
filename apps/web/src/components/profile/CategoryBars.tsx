interface ScoreBreakdown {
  social_impact: number;
  environmental: number;
  knowledge_innovation: number;
  economic_contribution: number;
  cultural_artistic: number;
  civic_political: number;
}

interface Props {
  score: ScoreBreakdown;
}

const CATEGORIES = [
  { key: "social_impact",          label: "Social Impact",          weight: 0.25, color: "#7C3AED" },
  { key: "environmental",          label: "Environmental",          weight: 0.20, color: "#22C55E" },
  { key: "knowledge_innovation",   label: "Knowledge & Innovation", weight: 0.20, color: "#3B82F6" },
  { key: "economic_contribution",  label: "Economic Contribution",  weight: 0.15, color: "#F0B429" },
  { key: "cultural_artistic",      label: "Cultural & Artistic",    weight: 0.10, color: "#EC4899" },
  { key: "civic_political",        label: "Civic & Political",      weight: 0.10, color: "#EF4444" },
] as const;

/**
 * Six-category mini progress bars showing each dimension's contribution.
 */
export function CategoryBars({ score }: Props) {
  return (
    <div className="space-y-3">
      {CATEGORIES.map(({ key, label, weight, color }) => {
        const raw = score[key] as number;
        const maxForCategory = 1000 * weight;
        const pct = maxForCategory > 0 ? Math.min(100, (raw / maxForCategory) * 100) : 0;

        return (
          <div key={key}>
            <div className="flex justify-between text-xs text-slate-400 mb-1">
              <span>{label}</span>
              <span>{Math.round(raw)} pts</span>
            </div>
            <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-500"
                style={{ width: `${pct}%`, backgroundColor: color }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
}
