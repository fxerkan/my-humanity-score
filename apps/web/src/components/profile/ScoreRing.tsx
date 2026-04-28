import type { LevelInfo } from "@/lib/utils";

interface Props {
  score: number;
  level: LevelInfo;
}

const RADIUS = 52;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

/**
 * Circular SVG ring showing MHS score as a progress arc (0–1000).
 */
export function ScoreRing({ score, level }: Props) {
  const clamped = Math.max(0, Math.min(1000, score));
  const fraction = clamped / 1000;
  const dash = fraction * CIRCUMFERENCE;
  const gap = CIRCUMFERENCE - dash;

  return (
    <div data-testid="mhs-score-ring" className="relative flex items-center justify-center shrink-0">
      <svg width="130" height="130" viewBox="0 0 130 130" aria-hidden>
        {/* Track */}
        <circle
          cx="65"
          cy="65"
          r={RADIUS}
          fill="none"
          stroke="#1E293B"
          strokeWidth="10"
        />
        {/* Progress arc */}
        <circle
          cx="65"
          cy="65"
          r={RADIUS}
          fill="none"
          stroke={level.color}
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={`${dash} ${gap}`}
          transform="rotate(-90 65 65)"
        />
      </svg>
      {/* Centre label */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-2xl">{level.emoji}</span>
      </div>
    </div>
  );
}
