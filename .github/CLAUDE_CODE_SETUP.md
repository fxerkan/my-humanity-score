# Claude Code GitHub Actions - Setup Guide

This repository uses **Claude Code GitHub Actions** to provide AI-powered assistance directly in your GitHub workflow.

## 🚀 What You Can Do

### 1. **Interactive Assistant** (@claude mentions)

In any PR or issue comment, mention `@claude` to:

```text
@claude implement user authentication for this endpoint
@claude fix the TypeError in the dashboard component
@claude review this PR for security issues
@claude add tests for the new scoring algorithm
```

### 2. **Automatic PR Reviews**

Every PR automatically gets a comprehensive review from Claude covering:
- Code quality, security, performance
- Testing coverage and edge cases
- MHS-specific ethical considerations (no discrimination logic)
- Architecture and best practices

### 3. **Issue Implementation**

Label an issue with `claude` or mention `@claude` in the issue to have Claude:
- Analyze the requirements
- Implement the feature
- Create a PR with tests
- Follow project standards from CLAUDE.md

## 📋 Setup Steps

### 1. Install GitHub App

Choose one of these options:

#### Option A: Official Claude App (Recommended for direct API users)

1. Install the app: https://github.com/apps/claude
2. Select your repository
3. Grant permissions (Contents, Issues, Pull Requests)

#### Option B: Create Custom GitHub App (For organizations)

1. Go to: https://github.com/settings/apps/new
2. Fill in:
   - **Name**: Your org name + "Claude Assistant"
   - **Homepage URL**: Your repository URL
   - **Webhooks**: Uncheck "Active"
3. Set permissions:
   - **Contents**: Read & Write
   - **Issues**: Read & Write
   - **Pull requests**: Read & Write
4. Click "Create GitHub App"
5. Generate a private key and save the `.pem` file
6. Note your App ID
7. Install the app to your repository

### 2. Add Secrets

Go to: **Settings → Secrets and variables → Actions**

#### Required for All Setups:
- `ANTHROPIC_API_KEY`: Your Claude API key from https://console.anthropic.com/

#### Only if using Custom GitHub App:
- `APP_ID`: Your GitHub App's ID
- `APP_PRIVATE_KEY`: Contents of the `.pem` file

### 3. Test the Setup

#### Test Interactive Mode:
```bash
# Create a test branch
git checkout -b test-claude-action

# Make a change
echo "// test" >> apps/web/src/app/page.tsx

# Commit and push
git add .
git commit -m "test: trigger claude action"
git push origin test-claude-action

# Create PR and comment: @claude review this change
```

#### Test Auto Review:
Just create a PR - Claude will automatically review it!

#### Test Issue Handler:
Create an issue and either:
- Add `claude` label, OR
- Comment: `@claude implement this feature`

## 🎯 Workflows Installed

### 1. `claude-interactive.yml`
**Trigger**: `@claude` in PR/issue comments
**Purpose**: Interactive assistance for code changes, questions, implementations

### 2. `claude-auto-review.yml`
**Trigger**: PR opened/updated
**Purpose**: Automatic comprehensive code review

### 3. `claude-issues.yml`
**Trigger**: Issue with `claude` label or `@claude` mention
**Purpose**: Feature implementation from issues

## ⚙️ Configuration

### Customize Claude's Behavior

Edit the `claude_args` in workflow files:

```yaml
claude_args: |
  --model claude-sonnet-4-20250514    # or claude-opus-4-6 for deeper analysis
  --max-turns 10                       # conversation depth
  --append-system-prompt "Custom instructions"
```

### Use CLAUDE.md for Project Standards

Claude automatically reads `CLAUDE.md` in your repo root. Add:
- Coding standards
- Review criteria
- Architecture decisions
- Project-specific rules

## 🔒 Security Best Practices

✅ **DO:**
- Use GitHub Secrets for API keys
- Review Claude's suggestions before merging
- Set appropriate max-turns to avoid runaway costs
- Configure repository permissions carefully

❌ **DON'T:**
- Commit API keys to the repository
- Blindly merge Claude's PRs without review
- Grant excessive permissions to GitHub Apps

## 💰 Cost Considerations

### GitHub Actions Minutes
- Runs on GitHub-hosted runners
- Free tier: 2,000 minutes/month for private repos
- Public repos: unlimited

### Claude API Costs
- Sonnet 4: ~$3 input + ~$15 output per million tokens
- Typical usage:
  - Small PR review: $0.01-0.02
  - Feature implementation: $0.05-0.20
  - Complex refactoring: $0.20-0.50

**Estimated monthly cost**: $10-30 for active development

### Cost Optimization Tips
1. Use `--max-turns` to limit iterations
2. Set workflow timeouts
3. Use concurrency controls for parallel runs
4. Prefer Sonnet over Opus for routine tasks

## 🔧 Troubleshooting

### Claude Not Responding

**Check:**
1. GitHub App is installed and has permissions
2. `ANTHROPIC_API_KEY` is set in secrets
3. Workflow files are on main branch
4. You're using `@claude` (not `/claude`)

**Debug:**
- Go to **Actions** tab and check workflow logs
- Look for authentication or API errors

### Authentication Errors

**For direct API:**
- Verify API key in Anthropic Console
- Check you have API credits

**For custom GitHub App:**
- Verify `APP_ID` and `APP_PRIVATE_KEY` are correct
- Check app is installed to the repository

### CI Not Running on Claude's Commits

This is expected! To avoid infinite loops, workflows don't trigger on bot commits.

If you need CI to run, use a custom GitHub App instead of `GITHUB_TOKEN`.

## 📚 Advanced Usage

### Use with Amazon Bedrock

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    use_bedrock: "true"
    claude_args: '--model us.anthropic.claude-sonnet-4-6'
```

**Additional setup required:**
- AWS OIDC Identity Provider
- IAM role with Bedrock permissions
- See: `.github/workflows/examples/bedrock-example.yml`

### Use with Google Vertex AI

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    use_vertex: "true"
    claude_args: '--model claude-sonnet-4-5@20250929'
  env:
    ANTHROPIC_VERTEX_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
    CLOUD_ML_REGION: us-east5
```

**Additional setup required:**
- Workload Identity Federation
- Service account with Vertex AI permissions
- See: `.github/workflows/examples/vertex-example.yml`

## 📖 Resources

- [Claude Code Action Docs](https://github.com/anthropics/claude-code-action)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Anthropic Console](https://console.anthropic.com/)
- [Security Best Practices](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md)

## 🤝 Examples

### Example 1: Fix a Bug
```text
Issue: "Users can't login with Google OAuth"
Comment: @claude fix the Google OAuth login issue

Claude will:
1. Analyze the auth code
2. Identify the problem
3. Create a PR with the fix
4. Add tests
```

### Example 2: Add a Feature
```text
Issue: "Add export to CSV feature for user scores"
Label: claude

Claude will:
1. Read the issue description
2. Implement the feature
3. Add tests and documentation
4. Create a PR following project standards
```

### Example 3: Code Review
```text
PR: "Implement new scoring algorithm"
Comment: @claude review this for performance and ethical considerations

Claude will:
1. Analyze the changes
2. Check for discrimination logic
3. Review algorithm transparency
4. Suggest optimizations
```

---

**Questions?** Open an issue or ask `@claude` in a comment!

*Last updated: 2026-05-15*
