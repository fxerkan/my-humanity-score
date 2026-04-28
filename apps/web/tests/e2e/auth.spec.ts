/**
 * E2E tests for authentication flows.
 *
 * Runs against the full Docker Compose stack (localhost:3000 + API at 8001).
 * Depends on: TASK-005 (Next.js App Shell) and TASK-006 (User Profile Page).
 */

import { test, expect } from "@playwright/test";
import { RegisterPage } from "./pages/RegisterPage";
import { LoginPage } from "./pages/LoginPage";
import { ProfilePage } from "./pages/ProfilePage";

const TEST_USER = {
  email: `e2e_${Date.now()}@test.example`,
  username: `e2e_user_${Date.now()}`,
  password: "E2eTestPass123!",
};

test.describe("register and login flow", () => {
  test("register → profile shows score 0 → logout → login again", async ({
    page,
  }) => {
    const register = new RegisterPage(page);
    const login = new LoginPage(page);
    const profile = new ProfilePage(page);

    // 1. Navigate to /register
    await register.goto();
    await expect(page).toHaveURL(/register/);

    // 2. Fill form and submit
    await register.register(
      TEST_USER.email,
      TEST_USER.username,
      TEST_USER.password
    );

    // 3. Redirected to feed or profile after registration
    await expect(page).toHaveURL(/\/feed|\/u\//);

    // 4. Navigate to own profile via header link (soft nav — preserves in-memory tokens).
    await profile.softGoto(TEST_USER.username);
    await expect(profile.scoreRing).toBeVisible();
    await expect(profile.levelBadge).toContainText(/awakening/i);

    // 5. Log out → redirected to /login
    await profile.logout();
    await expect(page).toHaveURL(/login/);

    // 6. Log in with same credentials → back to profile/feed
    await login.login(TEST_USER.email, TEST_USER.password);
    await expect(page).toHaveURL(/\/feed|\/u\//);
  });
});

test.describe("unauthenticated redirect", () => {
  test("accessing /feed redirects to /login, then back after login", async ({
    page,
  }) => {
    const login = new LoginPage(page);

    // 1. Navigate to /feed without being logged in
    await page.goto("/feed");

    // 2. Should be redirected to /login
    await expect(page).toHaveURL(/login/);

    // 3. Log in → redirected back to /feed
    await login.login(TEST_USER.email, TEST_USER.password);
    await expect(page).toHaveURL(/feed/);
  });
});
