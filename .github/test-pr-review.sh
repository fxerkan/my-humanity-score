#!/bin/bash
# Test script for PR review workflow
# Usage: ./.github/test-pr-review.sh

set -e

echo "🧪 Testing PR Review Workflow Setup"
echo "===================================="
echo ""

# Check if ANTHROPIC_API_KEY is set in GitHub secrets
echo "📋 Checklist:"
echo ""
echo "1. ✅ Workflow file exists: .github/workflows/pr-review.yml"
echo "2. ⚠️  ANTHROPIC_API_KEY secret must be set in GitHub:"
echo "   → Go to: Settings → Secrets and variables → Actions"
echo "   → Add secret: ANTHROPIC_API_KEY"
echo ""
echo "3. 🔍 To test the workflow:"
echo "   → Create a test branch: git checkout -b test-pr-review"
echo "   → Make a small change: echo '// test' >> apps/web/src/app/page.tsx"
echo "   → Commit: git add . && git commit -m 'test: trigger PR review'"
echo "   → Push: git push origin test-pr-review"
echo "   → Create a PR on GitHub"
echo "   → Wait ~1-2 minutes for Claude's review"
echo ""
echo "4. 📊 Monitor the workflow:"
echo "   → GitHub Actions tab: https://github.com/fxerkan/my-humanity-score/actions"
echo ""
echo "5. 🐛 If issues occur:"
echo "   → Check workflow logs in Actions tab"
echo "   → Verify API key is correct"
echo "   → Ensure you have API credits in Anthropic Console"
echo ""

# Validate workflow syntax
if command -v actionlint >/dev/null 2>&1; then
    echo "🔍 Running actionlint..."
    actionlint .github/workflows/pr-review.yml && echo "✅ Workflow syntax is valid" || echo "❌ Workflow has syntax errors"
else
    echo "💡 Install actionlint for workflow validation:"
    echo "   brew install actionlint"
fi

echo ""
echo "✅ Setup guide complete!"
echo "   Full docs: .github/PR_REVIEW_SETUP.md"
