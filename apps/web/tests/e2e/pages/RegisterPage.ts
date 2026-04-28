import type { Page, Locator } from "@playwright/test";

/**
 * Page Object Model for the /register page.
 */
export class RegisterPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel(/email/i);
    this.usernameInput = page.getByLabel(/username/i);
    this.passwordInput = page.getByLabel(/password/i);
    this.submitButton = page.getByRole("button", {
      name: /create account|register|sign up/i,
    });
  }

  async goto(): Promise<void> {
    await this.page.goto("/register");
  }

  async register(
    email: string,
    username: string,
    password: string
  ): Promise<void> {
    await this.emailInput.fill(email);
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}
