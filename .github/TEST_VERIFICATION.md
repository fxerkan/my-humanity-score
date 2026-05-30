# Claude Code Actions - Test Verification

This file is used to test the Claude Code GitHub Actions integration.

## Test Checklist

### 1. Automatic PR Review (claude-auto-review.yml)
- [ ] Workflow triggers on PR creation
- [ ] Claude posts a comprehensive review comment
- [ ] Review covers code quality, security, and MHS ethics
- [ ] Review includes specific, actionable feedback

### 2. Interactive Mode (claude-interactive.yml)
- [ ] Responds to @claude mentions in PR comments
- [ ] Can answer questions about the code
- [ ] Can make code changes and push commits
- [ ] Follows CLAUDE.md project standards

### 3. Issue Handler (claude-issues.yml)
- [ ] Responds to issues with 'claude' label
- [ ] Responds to @claude mentions in issue comments
- [ ] Can implement features and create PRs
- [ ] Follows project coding standards

## Expected Behavior

When this test PR is created:
1. **Automatic Review**: Claude should post a review comment within 1-2 minutes
2. **Interactive Test**: Comment "@claude what does this file test?" to verify interactive mode
3. **Quality**: Review should be specific and reference actual code changes

## Test Commands

Try these in PR comments:
```
@claude review this test change
@claude explain the purpose of this file
@claude can you add a timestamp to this file?
```

## Success Criteria

✅ All workflows run successfully
✅ Claude responds appropriately to mentions
✅ API key authentication works
✅ Reviews include MHS-specific checks (ethics, discrimination)
✅ No errors in workflow logs

---

*Created: 2026-05-15 for Claude Code Actions integration testing*
