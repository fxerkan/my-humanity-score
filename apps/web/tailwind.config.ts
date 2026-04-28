import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // MHS design tokens
        "angel-gold": "#F0B429",
        "crisis-red": "#EF4444",
        "peace-blue": "#3B82F6",
        "earth-brown": "#92400E",
        "community-purple": "#7C3AED",
        "bg-dark": "#0F172A",
        "bg-light": "#F8FAFC",
        // Semantic aliases
        brand: {
          DEFAULT: "#F0B429",
          foreground: "#0F172A",
        },
        muted: {
          DEFAULT: "#1E293B",
          foreground: "#94A3B8",
        },
      },
      borderRadius: {
        lg: "0.5rem",
        md: "calc(0.5rem - 2px)",
        sm: "calc(0.5rem - 4px)",
      },
    },
  },
  plugins: [],
};

export default config;
