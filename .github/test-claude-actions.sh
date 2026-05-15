#!/bin/bash
# Test script for Claude Code GitHub Actions
# Usage: ./.github/test-claude-actions.sh

set -e

echo "🧪 Testing Claude Code GitHub Actions Setup"
echo "==========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "CLAUDE.md" ]; then
    echo -e "${RED}❌ Error: CLAUDE.md not found. Run this from the repository root.${NC}"
    exit 1
fi

echo "📋 Pre-flight Checklist:"
echo ""

# Check workflow files exist
echo "1. Checking workflow files..."
if [ -f ".github/workflows/claude-interactive.yml" ]; then
    echo -e "   ${GREEN}✅ claude-interactive.yml exists${NC}"
else
    echo -e "   ${RED}❌ claude-interactive.yml missing${NC}"
fi

if [ -f ".github/workflows/claude-auto-review.yml" ]; then
    echo -e "   ${GREEN}✅ claude-auto-review.yml exists${NC}"
else
    echo -e "   ${RED}❌ claude-auto-review.yml missing${NC}"
fi

if [ -f ".github/workflows/claude-issues.yml" ]; then
    echo -e "   ${GREEN}✅ claude-issues.yml exists${NC}"
else
    echo -e "   ${RED}❌ claude-issues.yml missing${NC}"
fi

echo ""

# Check if on correct branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "   ${YELLOW}⚠️  You're on branch '$CURRENT_BRANCH', not 'main'${NC}"
    echo "   Workflows must be on 'main' branch to run"
else
    echo -e "   ${GREEN}✅ On main branch${NC}"
fi

echo ""
echo "2. Required GitHub Secrets (you must add these manually):"
echo ""
echo "   Go to: Settings → Secrets and variables → Actions"
echo ""
echo "   Required:"
echo "   • ANTHROPIC_API_KEY - Your Claude API key"
echo "     Get it from: https://console.anthropic.com/"
echo ""
echo "   Optional (for custom GitHub App):"
echo "   • APP_ID - Your GitHub App ID"
echo "   • APP_PRIVATE_KEY - Your GitHub App private key"
echo ""

# Check if actionlint is available
echo "3. Validating workflow syntax..."
if command -v actionlint >/dev/null 2>&1; then
    echo "   Running actionlint..."

    for workflow in .github/workflows/claude-*.yml; do
        if actionlint "$workflow" 2>/dev/null; then
            echo -e "   ${GREEN}✅ $(basename "$workflow") syntax valid${NC}"
        else
            echo -e "   ${RED}❌ $(basename "$workflow") has syntax errors${NC}"
        fi
    done
else
    echo -e "   ${YELLOW}⚠️  actionlint not installed${NC}"
    echo "   Install with: brew install actionlint"
fi

echo ""
echo "4. Test Instructions:"
echo ""
echo "   📝 To test interactive mode (@claude mentions):"
echo "   ------------------------------------------------"
echo "   1. Create test branch:"
echo "      git checkout -b test-claude-interactive"
echo ""
echo "   2. Make a small change:"
echo "      echo '// test change' >> apps/web/src/app/page.tsx"
echo ""
echo "   3. Commit and push:"
echo "      git add ."
echo "      git commit -m 'test: claude interactive mode'"
echo "      git push origin test-claude-interactive"
echo ""
echo "   4. Create a PR on GitHub"
echo ""
echo "   5. Comment on the PR:"
echo "      @claude review this change"
echo ""
echo "   6. Wait ~30-60 seconds for Claude to respond"
echo ""
echo "   🤖 To test automatic review:"
echo "   ----------------------------"
echo "   1. Just create any PR - no @claude mention needed"
echo "   2. Claude will automatically post a review comment"
echo ""
echo "   📋 To test issue handling:"
echo "   --------------------------"
echo "   1. Create an issue on GitHub"
echo "   2. Either:"
echo "      • Add 'claude' label to the issue, OR"
echo "      • Comment: @claude implement this"
echo "   3. Claude will analyze and create a PR"
echo ""

echo "5. Monitoring:"
echo ""
echo "   • Workflow runs: https://github.com/fxerkan/my-humanity-score/actions"
echo "   • Check logs for errors or API issues"
echo "   • Look for 'Claude Code' or 'Claude Auto Code Review' workflows"
echo ""

echo "6. Troubleshooting Common Issues:"
echo ""
echo "   ${YELLOW}Issue: Claude not responding to @claude${NC}"
echo "   Fix: Check API key is set in secrets"
echo "        Verify workflow is on main branch"
echo "        Ensure you used @claude (not /claude)"
echo ""
echo "   ${YELLOW}Issue: 'API key invalid' error${NC}"
echo "   Fix: Regenerate key at console.anthropic.com"
echo "        Update ANTHROPIC_API_KEY secret"
echo ""
echo "   ${YELLOW}Issue: Workflow not triggering${NC}"
echo "   Fix: Ensure workflows are enabled in Settings → Actions"
echo "        Check branch protection rules"
echo "        Verify workflow syntax with actionlint"
echo ""

echo "7. Cost Monitoring:"
echo ""
echo "   • Check usage: https://console.anthropic.com/settings/usage"
echo "   • Typical costs:"
echo "     - PR review: ~\$0.05-0.20"
echo "     - Feature implementation: ~\$0.10-0.50"
echo "     - Interactive session: ~\$0.05-0.30"
echo "   • Set billing alerts in Anthropic Console"
echo ""

echo -e "${GREEN}✅ Setup guide complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Ensure ANTHROPIC_API_KEY is added to GitHub Secrets"
echo "2. Push workflow files to main branch (if not already)"
echo "3. Run a test by creating a PR and commenting @claude"
echo ""
echo "Full docs: .github/CLAUDE_CODE_SETUP.md"
echo ""
