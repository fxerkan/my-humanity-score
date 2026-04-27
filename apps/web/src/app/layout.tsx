import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "My Humanity Score (MHS)",
  description: "Every person's impact on humanity — finally measured. Measure, track, and celebrate your positive impact on humanity.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
