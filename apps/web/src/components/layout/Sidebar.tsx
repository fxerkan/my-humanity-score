"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Globe,
  Home,
  LayoutDashboard,
  MessageCircle,
  Star,
  Trophy,
  Users,
} from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { href: "/feed",        label: "Feed",        icon: Home },
  { href: "/leaderboard", label: "Leaderboard", icon: Trophy },
  { href: "/claim",       label: "Log Activity",icon: Star },
  { href: "/groups",      label: "Groups",      icon: Users },
  { href: "/angel",       label: "Angel AI",    icon: MessageCircle },
  { href: "/settings",   label: "Settings",    icon: LayoutDashboard },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden lg:flex flex-col w-64 min-h-screen bg-slate-900 border-r border-slate-800 px-4 py-6 gap-2">
      {/* Logo */}
      <Link href="/feed" className="flex items-center gap-2 px-2 mb-6">
        <Globe className="w-7 h-7 text-angel-gold" />
        <span className="font-bold text-white text-lg leading-tight">
          My Humanity<br />Score
        </span>
      </Link>

      {/* Navigation */}
      <nav className="flex flex-col gap-1">
        {NAV_ITEMS.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className={cn(
              "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
              pathname.startsWith(href)
                ? "bg-slate-800 text-white"
                : "text-slate-400 hover:bg-slate-800 hover:text-white",
            )}
          >
            <Icon className="w-4 h-4 shrink-0" />
            {label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
