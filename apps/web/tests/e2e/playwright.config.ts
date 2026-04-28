import { defineConfig, devices } from "@playwright/test";

/**
 * Playwright E2E configuration for My Humanity Score.
 * Runs against the full Docker Compose stack (localhost:3000).
 *
 * CI: headless Chromium only.
 * Local dev: all browsers available via `pnpm test:e2e:all`.
 */
export default defineConfig({
  testDir: ".",
  testMatch: "**/*.spec.ts",
  /* Fail fast in CI — report all failures locally */
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  /* Reporter */
  reporter: [
    ["list"],
    ["html", { outputFolder: "playwright-report", open: "never" }],
  ],
  /* Capture screenshots and traces on failure */
  use: {
    baseURL: process.env.E2E_BASE_URL ?? "http://localhost:3000",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
    trace: "on-first-retry",
  },
  /* Global timeout: 2 minutes for the full suite */
  timeout: 30_000,
  /* Projects */
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    /* These only run locally (not in CI) */
    ...(process.env.CI
      ? []
      : [
          { name: "firefox", use: { ...devices["Desktop Firefox"] } },
          { name: "webkit", use: { ...devices["Desktop Safari"] } },
        ]),
  ],
  /* Start/stop the local dev server if not already running */
  webServer: process.env.CI
    ? undefined
    : {
        command: "pnpm dev",
        url: "http://localhost:3000",
        reuseExistingServer: true,
        timeout: 60_000,
      },
  outputDir: "test-results",
});
