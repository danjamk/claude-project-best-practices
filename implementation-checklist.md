# Claude Code Implementation Checklist

## Phase 1: Initial Setup ✅

### 1. Create Project Structure
```bash
# Create base directories
mkdir -p my-project/{src,tests,scripts,infrastructure,docs}
mkdir -p my-project/.claude/{commands,hooks,agents}
cd my-project
```

### 2. Initialize Git
```bash
git init
# Copy .gitignore from the guide
# Create initial commit
git add .gitignore
git commit -m "Initial commit with gitignore"
```

### 3. Set Up Python Environment
```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Copy pyproject.toml from guide
poetry init --no-interaction
poetry add boto3 aws-cdk-lib constructs pydantic pydantic-settings
poetry add --group dev pytest pytest-cov pytest-asyncio black mypy ruff pre-commit
```

### 4. Create Core Files
- [ ] Copy CLAUDE.md template
- [ ] Copy Makefile template
- [ ] Create .env.example with required variables
- [ ] Copy .claude/settings.json
- [ ] Create TODO.md (and ensure it's in .gitignore)

## Phase 2: Claude Code Configuration 🤖

### 1. Install Safety Hooks
```bash
# Copy all hook files from guide
cd .claude/hooks
chmod +x *.py

# Test each hook
python3 pre-tool-use-safety.py < test-input.json
python3 auto-approve-safe.py < test-input.json
```

### 2. Create Custom Commands
- [ ] Create .claude/commands/setup.md
- [ ] Create .claude/commands/deploy.md
- [ ] Create .claude/commands/destroy.md
- [ ] Create .claude/commands/test.md
- [ ] Create .claude/commands/review.md
- [ ] Create .claude/commands/bastion.md

### 3. Set Up Sub-Agents
- [ ] Create .claude/agents/aws-architect.md
- [ ] Create .claude/agents/python-tester.md
- [ ] Create .claude/agents/security-auditor.md

### 4. Test Claude Code Setup
```bash
# Run setup command
make claude-setup

# Test plan mode
claude "ultrathink about project structure"

# Test custom command
claude "/setup"

# Test safety hooks (should block)
claude "rm -rf /"
```

## Phase 3: AWS Infrastructure Setup 🏗️

### 1. Initialize CDK
```bash
# Create infrastructure directory structure
mkdir -p infrastructure/{stacks,constructs}

# Initialize CDK
cdk init app --language python

# Update CDK dependencies in pyproject.toml
poetry add aws-cdk-lib constructs
```

### 2. Create Base Stack
```python
# infrastructure/app.py
#!/usr/bin/env python3
import os
from aws_cdk import App, Environment
from stacks.base_stack import BaseStack

app = App()

env = Environment(
    account=os.environ.get("AWS_ACCOUNT_ID"),
    region=os.environ.get("AWS_REGION", "us-east-1")
)

BaseStack(app, "MyProjectBase", env=env)

app.synth()
```

### 3. Environment Configuration
- [ ] Create .env.example with all required variables
- [ ] Set up multi-environment support in CDK
- [ ] Configure cost tags and monitoring

## Phase 4: Documentation 📚

### 1. Create Core Documentation
```bash
# Create documentation structure
touch docs/{README.md,SETUP.md,ARCHITECTURE.md,REQUIREMENTS.md}
```

### 2. Document Key Processes
- [ ] Setup instructions in SETUP.md
- [ ] Architecture decisions in ARCHITECTURE.md
- [ ] Project requirements in REQUIREMENTS.md
- [ ] Update main README.md

## Phase 5: Testing & Validation ✅

### 1. Set Up Testing Framework
```bash
# Create test structure
mkdir -p tests/{unit,integration,fixtures}
touch tests/__init__.py
touch tests/conftest.py

# Create sample test
cat > tests/test_example.py << 'EOF'
def test_example():
    """Example test to verify pytest setup"""
    assert True
EOF

# Run tests
poetry run pytest
```

### 2. Validate Claude Code Integration
- [ ] Test all custom commands work
- [ ] Verify hooks block dangerous operations
- [ ] Confirm auto-approval for safe commands
- [ ] Test multi-directory support
- [ ] Verify sub-agents functionality

### 3. Create Validation Scripts
```python
# scripts/validate.py
#!/usr/bin/env python3
"""Validate deployment and configuration"""

import sys
import subprocess

def check_aws_credentials():
    """Verify AWS credentials are configured"""
    try:
        subprocess.run(["aws", "sts", "get-caller-identity"], 
                      check=True, capture_output=True)
        print("✅ AWS credentials configured")
        return True
    except subprocess.CalledProcessError:
        print("❌ AWS credentials not configured")
        return False

def check_environment():
    """Verify environment variables"""
    import os
    required_vars = ["AWS_REGION", "ENVIRONMENT"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print(f"❌ Missing environment variables: {missing}")
        return False
    
    print("✅ Environment variables configured")
    return True

def main():
    checks = [
        check_aws_credentials(),
        check_environment(),
    ]
    
    if not all(checks):
        print("\n❌ Validation failed")
        sys.exit(1)
    
    print("\n✅ All validation checks passed")

if __name__ == "__main__":
    main()
```

## Phase 6: Workflow Implementation 🔄

### 1. Development Workflow
```bash
# Start new feature with plan mode
claude "think hard about implementing user authentication"

# Use TDD approach
claude "/test Authentication service"

# Implement with auto-mode
claude --dangerously-skip-permissions "implement the authentication service based on the tests"

# Review and commit
claude "/review recent changes"
git add .
git commit -m "Add authentication service"
```

### 2. Deployment Workflow
```bash
# Deploy to development
export ENVIRONMENT=dev
make deploy

# Validate deployment
make validate

# Run integration tests
make test

# Destroy when done (cost-conscious)
make destroy
```

## Phase 7: Team Onboarding 👥

### 1. Create Onboarding Guide
- [ ] Document Claude Code setup process
- [ ] Create examples of common workflows
- [ ] Document safety measures and why they exist
- [ ] Create troubleshooting guide

### 2. Share Best Practices
- [ ] Document when to use plan mode vs auto mode
- [ ] Explain thinking levels and when to use each
- [ ] Show examples of effective prompts
- [ ] Create team-specific commands

## Verification Checklist ✓

Before considering setup complete, verify:

- [ ] All hooks are executable and working
- [ ] Custom commands are accessible via `/command`
- [ ] Safety blocks work for dangerous operations
- [ ] Safe commands are auto-approved
- [ ] Make commands are idempotent
- [ ] Documentation is complete and accurate
- [ ] Tests run successfully
- [ ] CDK can synthesize and deploy
- [ ] Multi-environment support works
- [ ] Cost tags are applied to all resources

## Quick Test Commands

```bash
# Test safety (should all be blocked)
claude "rm -rf /"
claude "DROP DATABASE production"
claude "git push --force origin main"
claude "sudo apt-get install something"

# Test auto-approval (should all work without prompts)
claude "ls -la"
claude "git status"
claude "make test"
claude "aws s3 ls"

# Test custom commands
claude "/setup"
claude "/deploy dev"
claude "/test"
claude "/review"

# Test plan mode
# Press Shift+Tab twice after starting
claude "design the database schema"

# Test thinking levels
claude "think about the architecture"
claude "think hard about performance optimization"
claude "ultrathink about the security implications"
```

## Troubleshooting Common Issues

### Hook Not Working
```bash
# Check permissions
ls -la .claude/hooks/
# Should show executable permissions (x)

# Test manually
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | python3 .claude/hooks/pre-tool-use-safety.py
```

### Custom Command Not Found
```bash
# Check file exists
ls .claude/commands/

# Ensure .md extension
# Restart Claude Code after adding new commands
```

### Environment Issues
```bash
# Verify Poetry environment
poetry env info

# Ensure virtual environment is activated
poetry shell

# Check Python version
python --version  # Should be 3.12+
```

## Final Notes

Remember:
1. Start with Plan Mode for new features
2. Use TDD approach - tests first
3. Keep iterations small and focused
4. Use `/clear` frequently to maintain context
5. Always validate before deploying
6. Destroy resources when not in use (cost-conscious)
7. Document as you go

This checklist ensures you implement all the Claude Code best practices systematically. Check off items as you complete them, and customize based on your specific needs.