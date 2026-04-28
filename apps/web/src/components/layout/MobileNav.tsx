"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, MessageCircle, Star, Trophy, Users } from "lucide-react";
import { cn } from "@/lib/utils";

const MOBILE_NAV = [
  { href: "/feed",        label: "Feed",      icon: Home },
  { href: "/leaderboard", label: "Top",       icon: Trophy },
  { href: "/claim",       label: "Log",       icon: Star },
  { href: "/groups",      label: "Groups",    icon: Users },
  { href: "/angel",       label: "Angel",     icon: MessageCircle },
];

export function MobileNav() {
  const pathname = usePathname();

  return (
    <nav className="lg:hidden fixed bottom-0 inset-x-0 bg-slate-900 border-t border-slate-800 flex">
      {MOBILE_NAV.map(({ href, label, icon: Icon }) => (
        <Link
          key={href}
          href={href}
          className={cn(
            "flex-1 flex flex-col items-center justify-center py-2 text-xs gap-1 transition-colors",
            pathname.startsWith(href)
              ? "text-angel-gold"
              : "text-slate-400 hover:text-white",
          )}
        >
          <Icon className="w-5 h-5" />
          {label}
        </Link>
      ))}
    </nav>
  );
}
