# GitHub PR Review with Claude AI - Setup Guide

This repository uses Claude AI to automatically review Pull Requests, providing intelligent feedback on code quality, security, architecture, and MHS-specific ethical considerations.

## 🚀 Quick Setup

### 1. Get an Anthropic API Key

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to **API Keys**
4. Click **Create Key**
5. Copy your API key (starts with `sk-ant-...`)

### 2. Add API Key to GitHub Secrets

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `ANTHROPIC_API_KEY`
5. Value: Paste your API key
6. Click **Add secret**

### 3. Test It!

1. Create a new branch: `git checkout -b test-pr-review`
2. Make a small change to any file
3. Commit and push: `git push origin test-pr-review`
4. Open a Pull Request on GitHub
5. Wait ~1-2 minutes for Claude to review your PR
6. You'll see a comment with detailed review feedback

## 🎯 What Gets Reviewed

Claude AI reviews your PR for:

### General Code Quality
- ✅ **Code Quality**: Clean code principles, maintainability, readability
- ✅ **Security**: Vulnerabilities, input validation, auth/access control
- ✅ **Performance**: Bottlenecks, optimization opportunities
- ✅ **Testing**: Coverage, edge cases, test quality
- ✅ **Architecture**: Design patterns, separation of concerns, SOLID principles

### MHS-Specific Checks
- ✅ **No Discrimination Logic**: Ensures scoring doesn't use religion, race, gender, nationality, etc.
- ✅ **Ethical Considerations**: Verifies alignment with MHS mission
- ✅ **Scoring Transparency**: Checks algorithm clarity and fairness

## 🔄 How It Works

```mermaid
graph LR
    A[PR Created/Updated] --> B[GitHub Action Triggered]
    B --> C[Fetch PR Diff & Metadata]
    C --> D[Send to Claude API]
    D --> E[AI Review Generated]
    E --> F[Post Comment on PR]
    F --> G[Check for Critical Issues]
    G --> H[Add Labels if Needed]
```

## 🛠️ Customization

### Change Review Model

Edit `.github/workflows/pr-review.yml` line 82:
```javascript
model: 'claude-sonnet-4-20250514',  // Change to 'claude-opus-4' for deeper analysis
```

### Adjust Review Focus

Modify the prompt in `.github/workflows/pr-review.yml` (lines 60-90) to emphasize different aspects.

### Skip Review for Specific PRs

Add `[skip-review]` to your PR title or description.

## 💡 Best Practices

1. **Keep PRs Focused**: Smaller PRs = better reviews
2. **Write Good Descriptions**: Help Claude understand context
3. **Review AI Feedback**: Claude is smart but not infallible
4. **Iterate**: Use feedback to improve code before merging

## 🔒 Security & Privacy

- API keys are stored securely in GitHub Secrets
- Code is sent to Anthropic's Claude API for review
- Review comments are public (visible to repo members)
- No data is stored by Anthropic beyond standard API retention policies

## 📊 Cost Estimation

Claude Sonnet 4 pricing (as of 2026):
- Input: ~$3 per million tokens
- Output: ~$15 per million tokens

Typical PR review:
- Small PR (~200 lines): ~$0.01-0.02
- Medium PR (~1000 lines): ~$0.05-0.10
- Large PR (~5000 lines): ~$0.25-0.50

Most teams spend **$5-20/month** for regular PR reviews.

## ❓ Troubleshooting

### Review Not Showing Up?
1. Check **Actions** tab for workflow run status
2. Verify `ANTHROPIC_API_KEY` is set correctly
3. Ensure workflow file is on your base branch (usually `main`)

### API Key Not Working?
- Verify key starts with `sk-ant-`
- Check key hasn't expired in Anthropic Console
- Ensure you have API credits/billing set up

### Review Too Generic?
- Add more context in PR description
- Link related issues/tasks
- Include "testing notes" or "approach" sections

## 🤝 Contributing

Found a bug or want to improve the review process? 
Open an issue or PR in this repository!

## 📚 Resources

- [Anthropic API Docs](https://docs.anthropic.com/)
- [Claude Models Overview](https://docs.anthropic.com/en/docs/models-overview)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [MHS Project README](../README.md)

---

*Last updated: 2026-05-15*
