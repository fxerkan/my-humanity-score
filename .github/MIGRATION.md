# Migration: Custom PR Review → Claude Code Actions

## 📋 Changes Overview

You had a custom PR review workflow (`pr-review.yml`) that used the Claude API directly. We've now set up **Claude Code GitHub Actions** which is more powerful and feature-rich.

## 🆚 Comparison

| Feature | Old (pr-review.yml) | New (Claude Code Actions) |
|---------|-------------------|------------------------|
| **PR Reviews** | ✅ Basic text review | ✅ Comprehensive analysis with full context |
| **Code Implementation** | ❌ No | ✅ Can create PRs and implement fixes |
| **Interactive Mode** | ❌ No | ✅ @claude mentions for on-demand help |
| **Issue Handling** | ❌ No | ✅ Can implement features from issues |
| **Tool Access** | ❌ Limited | ✅ Full file system, git, bash access |
| **Context Awareness** | ❌ Only sees PR diff | ✅ Sees full repo, git history, docs |
| **Follow-up Questions** | ❌ No | ✅ Can iterate and refine |
| **Cost per Review** | ~$0.05-0.10 | ~$0.05-0.20 (but does more) |

## 🎯 New Workflows

### 1. **claude-auto-review.yml** (Replaces pr-review.yml)
- Automatic PR reviews (same trigger as old workflow)
- More comprehensive analysis
- Can iterate and refine suggestions
- Access to full codebase context

### 2. **claude-interactive.yml** (NEW)
- Interactive assistance via `@claude` mentions
- Can implement changes, not just suggest them
- Works in PRs and issues

### 3. **claude-issues.yml** (NEW)
- Automatically implement features from issues
- Create PRs with tests
- Follow project standards

## 🔄 Migration Steps

### Step 1: Keep or Remove Old Workflow?

You have two options:

#### Option A: Remove Old Workflow (Recommended)
```bash
# Remove the old custom review workflow
git rm .github/workflows/pr-review.yml

# The new claude-auto-review.yml replaces it with more features
```

#### Option B: Keep Both (Side by Side Comparison)
```bash
# Rename old workflow to disable it
mv .github/workflows/pr-review.yml .github/workflows/pr-review.yml.disabled

# Or keep it as backup
mv .github/workflows/pr-review.yml .github/workflows/legacy-pr-review.yml
```

**Recommendation:** Remove the old workflow since the new one is strictly better.

### Step 2: Test New Workflows

```bash
# Create test branch
git checkout -b test-claude-actions

# Make a small change
echo "// test change" >> apps/web/src/app/page.tsx

# Commit and push
git add .
git commit -m "test: verify claude actions work"
git push origin test-claude-actions

# Create PR and:
# 1. Wait for automatic review from claude-auto-review.yml
# 2. Comment: @claude can you optimize this change?
```

### Step 3: Compare Results

Open the PR and observe:

1. **Automatic Review** (from claude-auto-review.yml):
   - Posted automatically when PR is created
   - Comprehensive analysis
   - Specific suggestions with code examples

2. **Interactive Response** (from claude-interactive.yml):
   - Responds to your `@claude` comment
   - Can make changes and push commits
   - Can create follow-up discussions

## 🔧 Configuration Differences

### Old Workflow (pr-review.yml)
```yaml
# Called Claude API directly with a static prompt
- name: Review PR with Claude
  run: |
    node review.mjs  # Custom script
```

**Limitations:**
- No tool access (can't read files, run tests)
- Single-shot review (no iteration)
- Manual prompt engineering
- No repository context beyond diff

### New Workflow (claude-auto-review.yml)
```yaml
# Uses official Claude Code Action
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "Review this PR..."
    claude_args: |
      --model claude-sonnet-4-20250514
      --max-turns 5
```

**Advantages:**
- Full tool access (Read, Edit, Bash, etc.)
- Can iterate and refine (up to max-turns)
- Reads CLAUDE.md automatically
- Full repository context
- Official support from Anthropic

## 💰 Cost Impact

### Old Workflow Cost per Review
- Single API call: ~$0.05-0.10
- Total per month (20 PRs): ~$1-2

### New Workflow Cost per Review
- Multiple turns (up to 5): ~$0.05-0.20
- Interactive usage (varies): ~$0.10-0.50 per interaction
- Total per month (20 PRs + 10 interactions): ~$2-7

**Note:** While slightly more expensive, you get:
- Implementation capability (not just suggestions)
- Interactive assistance
- Feature implementation from issues
- Much higher quality analysis

## 🎁 Bonus: Features You Didn't Have Before

1. **@claude Implementation Requests**
   ```text
   Issue: "Add CSV export for scores"
   Comment: @claude implement this feature
   
   Claude will:
   - Read the issue
   - Implement the feature
   - Add tests
   - Create a PR
   ```

2. **Interactive Debugging**
   ```text
   PR Comment: @claude the tests are failing, can you fix them?
   
   Claude will:
   - Analyze test failures
   - Fix the issues
   - Push fixes to your branch
   ```

3. **Code Explanations**
   ```text
   PR Comment: @claude explain how the scoring algorithm works
   
   Claude will:
   - Read the relevant code
   - Explain in detail
   - Answer follow-up questions
   ```

4. **Architecture Discussions**
   ```text
   Issue Comment: @claude should we use Redis or Postgres for caching?
   
   Claude will:
   - Analyze your use case
   - Consider your stack
   - Provide recommendations
   ```

## 📊 Recommended Next Steps

1. **Remove old workflow**
   ```bash
   git rm .github/workflows/pr-review.yml
   git commit -m "chore: migrate to Claude Code Actions"
   ```

2. **Update CLAUDE.md** with any review-specific guidelines you had in the old prompt

3. **Test all three workflows** with a test PR

4. **Document for team** how to use `@claude` mentions

5. **Set cost alerts** in Anthropic Console if concerned about usage

## 🆘 Rollback Plan

If something goes wrong:

```bash
# Restore old workflow
git checkout HEAD^ -- .github/workflows/pr-review.yml

# Disable new workflows
mv .github/workflows/claude-*.yml .github/workflows/disabled/

# Push changes
git add .
git commit -m "chore: rollback to old PR review workflow"
git push
```

---

**Questions?** Open an issue and mention `@claude` to get help with the migration!

*Last updated: 2026-05-15*
