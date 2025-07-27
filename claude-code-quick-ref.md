# Claude Code Quick Reference Guide

## 🚀 Essential Commands

### Starting Claude Code
```bash
# Basic start
claude

# Plan mode (research without changes)
claude "your prompt"  # Then press Shift+Tab twice

# Skip permissions (trusted operations)
claude --dangerously-skip-permissions

# Headless mode (for scripts/CI)
claude -p "your prompt" --output-format stream-json

# Resume previous session
claude --resume

# With multiple directories
claude --add-dir ../backend --add-dir ../shared
```

### During Session
- **Shift+Tab** - Toggle auto-accept mode
- **Shift+Tab (twice)** - Enter/exit plan mode
- **Escape** - Stop Claude
- **Escape (twice)** - Jump to previous message
- **/clear** - Clear conversation context
- **/add-dir** - Add directory mid-session
- **Control+V** - Paste images (not Cmd+V on Mac)

## 🧠 Thinking Levels

```bash
# Basic analysis
claude "think about the problem"

# Deeper analysis
claude "think hard about the architecture"

# Very deep analysis
claude "think harder about the security implications"

# Maximum analysis
claude "ultrathink about the performance optimization"
```

## 📁 Custom Commands

Your project includes these slash commands:

- **/setup** - Complete project setup
- **/deploy** - Deploy to AWS
- **/destroy** - Tear down infrastructure
- **/test** - Run comprehensive tests
- **/review** - Code review
- **/bastion** - Database access

Usage: `claude "/deploy dev"`

## 🛡️ Safety Features

### Auto-Blocked Operations
- `rm -rf` commands
- `DROP DATABASE/TABLE`
- `git push --force`
- AWS delete/terminate operations
- Modifications to .env, .pem, .key files
- sudo commands

### Auto-Approved Operations
- ls, pwd, cd, cat, grep
- git status/log/diff
- make test/lint/format
- aws describe/list operations
- Python script execution

## 🔄 Common Workflows

### New Feature Development
```bash
# 1. Start with plan mode
claude "ultrathink about implementing [feature]"
# Press Shift+Tab twice

# 2. Create tests first
claude "write comprehensive tests for [feature]"

# 3. Implement feature
claude "implement [feature] based on the tests"

# 4. Review and refine
claude "/review"
```

### Bug Fixing
```bash
# Analyze the issue
claude "analyze this error: [error message]"

# Fix with context
claude "fix the bug in @file.py related to [issue]"

# Verify fix
claude "create a test that verifies the bug is fixed"
```

### Code Review
```bash
# Review recent changes
claude "/review"

# Review specific files
claude "review @src/module.py for security issues"

# Review PR
claude "review the changes in this PR and suggest improvements"
```

## 📊 Project-Specific Patterns

### AWS Operations
```bash
# Check resources (safe)
claude "list all our AWS resources in the current region"

# Plan infrastructure changes
claude "ultrathink about adding a caching layer to our architecture"

# Generate CDK code
claude "create CDK code for an RDS PostgreSQL instance"
```

### Database Operations
```bash
# Safe read operations
claude "show me the database schema"

# Generate migrations
claude "create a migration to add user_preferences table"

# Query optimization
claude "optimize this SQL query: [query]"
```

### Testing
```bash
# Generate tests
claude "/test uncovered code"

# TDD approach
claude "write tests for a function that calculates user scores"

# Fix failing tests
claude "debug why test_user_auth is failing"
```

## 🎯 Effective Prompting

### Good Prompts
✅ "ultrathink and create a comprehensive plan for implementing OAuth"
✅ "write tests for the UserService class following our TDD approach"
✅ "review this code for security vulnerabilities and AWS best practices"

### Less Effective
❌ "fix the bug"
❌ "make it better"
❌ "optimize this"

## ⚙️ Configuration Locations

- **Project settings**: `.claude/settings.json`
- **Global settings**: `~/.claude/settings.json`
- **Project context**: `CLAUDE.md`
- **Personal prefs**: `CLAUDE.local.md` (gitignored)
- **Custom commands**: `.claude/commands/*.md`
- **Hooks**: `.claude/hooks/*.py`
- **Agents**: `.claude/agents/*.md`

## 🔧 Troubleshooting

### Claude asks for permission repeatedly
```bash
# For trusted operations only:
claude --dangerously-skip-permissions
```

### Context getting cluttered
```bash
# Clear and start fresh
/clear
```

### Need to reference multiple repos
```bash
# Add during session
/add-dir ../other-repo
```

### Hook not working
```bash
# Check permissions
chmod +x .claude/hooks/*.py

# Test manually
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | python3 .claude/hooks/pre-tool-use-safety.py
```

## 📝 Make Commands

Your project includes these make commands:

```bash
make setup          # Initial setup
make deploy         # Deploy infrastructure
make destroy        # Destroy infrastructure
make test          # Run tests
make lint          # Run linters
make format        # Format code
make validate      # Validate deployment
make bastion       # DB access
make bastion-stop  # Stop bastion

# Claude-specific
make claude-setup   # Initialize Claude Code
make claude-plan    # Start in plan mode
make claude-test    # Generate tests
```

## 🎮 Pro Tips

1. **Use Plan Mode** for architecture decisions
2. **Think Commands** scale with complexity
3. **Clear Context** frequently with `/clear`
4. **Multiple Instances** for parallel work
5. **Custom Commands** for repetitive tasks
6. **Hooks** automate safety and formatting
7. **Sub-agents** for specialized tasks

## 🚨 Emergency Commands

```bash
# Stop Claude immediately
Escape

# Exit Claude Code
Ctrl+C

# If something goes wrong
make destroy  # Clean up AWS resources
git reset --hard HEAD  # Reset code changes
poetry env remove python  # Reset Python environment
```

---

**Remember**: 
- Safety hooks protect you, but stay aware
- Always review before committing
- Use plan mode for big decisions
- Keep iterations small and focused
- Document as you go

**Your restrictions**:
- ❌ No Git writes (only read)
- ❌ No AWS CLI writes (only CDK)
- ❌ No DB writes (only read)
- ✅ Generate commit messages
- ✅ All work attributed to you