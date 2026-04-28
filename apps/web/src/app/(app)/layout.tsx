import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { MobileNav } from "@/components/layout/MobileNav";

/**
 * Authenticated app layout — wraps all pages inside the (app) route group.
 * Actual auth gating is handled client-side via AuthProvider + Zustand.
 */
export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex flex-col flex-1 min-h-screen">
        <Header />
        <main className="flex-1 p-4 pb-20 lg:pb-4">{children}</main>
      </div>
      <MobileNav />
    </div>
  );
}
