import type { Page, Locator } from "@playwright/test";

/**
 * Page Object Model for /u/{username} profile page.
 */
export class ProfilePage {
  readonly page: Page;
  readonly scoreRing: Locator;
  readonly levelBadge: Locator;
  readonly badgeGrid: Locator;
  readonly onboardingCta: Locator;
  readonly logoutButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.scoreRing = page.getByTestId("mhs-score-ring");
    this.levelBadge = page.getByTestId("mhs-level-badge");
    this.badgeGrid = page.getByTestId("badge-grid");
    this.onboardingCta = page.getByTestId("onboarding-cta");
    this.logoutButton = page.getByRole("button", { name: /sign out/i });
  }

  /** Full page navigation — use for unauthenticated access (SSR). In-memory tokens are lost. */
  async goto(username: string): Promise<void> {
    await this.page.goto(`/u/${username}`);
  }

  /**
   * Soft navigation via the header profile link — preserves in-memory auth state.
   * Only works when the user is already logged in and the header link is visible.
   */
  async softGoto(username: string): Promise<void> {
    await this.page.locator(`header a[href="/u/${username}"]`).click();
    await this.page.waitForURL(`**/u/${username}`);
  }

  async logout(): Promise<void> {
    await this.logoutButton.click();
  }
}
