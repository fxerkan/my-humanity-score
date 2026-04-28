"use client";

import Link from "next/link";
import { useAuthStore } from "@/store/authStore";

// Country code → flag emoji helper
function flagEmoji(code: string): string {
  return code
    .toUpperCase()
    .split("")
    .map((c) => String.fromCodePoint(0x1f1e6 + c.charCodeAt(0) - 65))
    .join("");
}

interface Profile {
  username: string;
  display_name: string | null;
  avatar_url: string | null;
  bio: string | null;
  country_code: string | null;
  created_at: string;
}

interface Props {
  profile: Profile;
}

function Initials({ name }: { name: string }) {
  const parts = name.trim().split(/\s+/);
  const initials =
    parts.length >= 2
      ? `${parts[0][0]}${parts[parts.length - 1][0]}`
      : name.slice(0, 2);
  return <span className="text-2xl font-bold uppercase">{initials}</span>;
}

export function ProfileHeader({ profile }: Props) {
  const { user } = useAuthStore();
  const isOwnProfile = user?.username === profile.username;
  const displayName = profile.display_name ?? profile.username;

  const joinedDate = new Date(profile.created_at).toLocaleDateString("en-US", {
    month: "long",
    year: "numeric",
  });

  return (
    <div className="bg-slate-800 rounded-2xl p-6 flex flex-col sm:flex-row items-start gap-5">
      {/* Avatar */}
      <div className="w-24 h-24 rounded-full bg-gradient-to-br from-community-purple to-peace-blue flex items-center justify-center shrink-0 overflow-hidden shadow-lg">
        {profile.avatar_url ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={profile.avatar_url} alt={displayName} className="w-full h-full object-cover" />
        ) : (
          <Initials name={displayName} />
        )}
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0 space-y-1">
        <h1 className="text-2xl font-bold text-white leading-tight">{displayName}</h1>
        <p className="text-slate-400 text-sm">@{profile.username}</p>

        {/* Meta row */}
        <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-slate-500 pt-0.5">
          {profile.country_code && (
            <span className="flex items-center gap-1">
              <span>{flagEmoji(profile.country_code)}</span>
              <span>{profile.country_code.toUpperCase()}</span>
            </span>
          )}
          <span className="flex items-center gap-1">
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            Joined {joinedDate}
          </span>
        </div>

        {profile.bio && (
          <p className="text-slate-300 text-sm mt-2 leading-relaxed line-clamp-3">{profile.bio}</p>
        )}
      </div>

      {/* Action buttons */}
      <div className="flex gap-2 shrink-0 self-start">
        {isOwnProfile ? (
          <Link
            href="/settings"
            className="rounded-lg border border-slate-600 px-4 py-2 text-sm text-slate-300 hover:bg-slate-700 transition-colors"
          >
            Edit profile
          </Link>
        ) : (
          <button
            disabled
            className="rounded-lg bg-peace-blue/80 px-4 py-2 text-sm font-semibold text-white opacity-70 cursor-not-allowed"
            title="Follow feature coming soon"
          >
            Follow
          </button>
        )}
      </div>
    </div>
  );
}
