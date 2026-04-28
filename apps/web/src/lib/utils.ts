import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/** Merge Tailwind classes without conflicts. */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/** Format a raw MHS score number for display. */
export function formatScore(score: number): string {
  return Math.round(score).toLocaleString();
}

export interface LevelInfo {
  name: string;
  emoji: string;
  color: string;
  minScore: number;
  maxScore: number;
}

const LEVELS: LevelInfo[] = [
  { name: "Awakening",    emoji: "🌱", color: "#94A3B8", minScore: 0,   maxScore: 99  },
  { name: "Contributor",  emoji: "🌿", color: "#22C55E", minScore: 100, maxScore: 249 },
  { name: "Advocate",     emoji: "🌍", color: "#3B82F6", minScore: 250, maxScore: 449 },
  { name: "Champion",     emoji: "⭐", color: "#F0B429", minScore: 450, maxScore: 649 },
  { name: "Luminary",     emoji: "🌟", color: "#A855F7", minScore: 650, maxScore: 849 },
  { name: "Legend",       emoji: "🏆", color: "#EF4444", minScore: 850, maxScore: 1000 },
];

/**
 * Map an MHS score (0–1000) to its level name, emoji, and colour.
 * Always returns a valid level even for out-of-range inputs.
 */
export function getLevelInfo(score: number): LevelInfo {
  const clamped = Math.max(0, Math.min(1000, Math.round(score)));
  return LEVELS.find((l) => clamped >= l.minScore && clamped <= l.maxScore) ?? LEVELS[0];
}
