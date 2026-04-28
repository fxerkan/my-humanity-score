/**
 * E2E tests for public profile viewing.
 *
 * Runs against the full Docker Compose stack.
 * Depends on: TASK-005 (Next.js App Shell) and TASK-006 (User Profile Page).
 */

import { test, expect } from "@playwright/test";
import { ProfilePage } from "./pages/ProfilePage";
import { RegisterPage } from "./pages/RegisterPage";

const TEST_USER = {
  email: `e2e_profile_${Date.now()}@test.example`,
  username: `e2e_profile_${Date.now()}`,
  password: "E2eTestPass123!",
};

test.describe("public profile viewing", () => {
  test.beforeAll(async ({ browser }) => {
    // Seed: create a user so the profile exists to view
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    const register = new RegisterPage(page);
    await register.goto();
    await register.register(
      TEST_USER.email,
      TEST_USER.username,
      TEST_USER.password
    );
    await ctx.close();
  });

  test("unauthenticated user can view a public profile", async ({ page }) => {
    const profile = new ProfilePage(page);

    // 1. Navigate to /u/{username} (unauthenticated)
    await profile.goto(TEST_USER.username);

    // 2. MHS score ring is visible
    await expect(profile.scoreRing).toBeVisible();

    // 3. "Awakening" level badge visible for new user
    await expect(profile.levelBadge).toContainText(/awakening/i);

    // 4. Empty badge grid shows onboarding CTA
    await expect(profile.onboardingCta).toBeVisible();
  });
});
