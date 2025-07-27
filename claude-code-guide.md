# Claude Code Best Practices - Complete Implementation Guide

## Table of Contents
1. [Overview](#overview)
2. [Core Features & Configuration](#core-features--configuration)
3. [Project Structure](#project-structure)
4. [Safety & Security](#safety--security)
5. [Workflows & Best Practices](#workflows--best-practices)
6. [Implementation Files](#implementation-files)

## Overview

This guide provides a comprehensive implementation of Claude Code best practices based on extensive research and your specific development preferences. It includes safety mechanisms, optimal workflows, and project structure recommendations for AWS/Python development.

### Your Development Profile
- **Role**: Fractional CTO who programs for learning/sharing and customer development
- **Stack**: AWS + Python, with experimentation in other technologies
- **Philosophy**: Projects created for others to use, often open source
- **Key Requirements**:
  - Infrastructure as Code with AWS CDK (Python)
  - Poetry for Python package management
  - Cost-conscious development (destroy resources after sessions)
  - Multi-environment support (dev, stage, prod)
  - No manual infrastructure patches - everything through code

## Core Features & Configuration

### 1. Claude Code Modes & Features

#### **Plan Mode** (Shift+Tab twice)
- Creates read-only research phase before code changes
- Allows comprehensive analysis without file modifications
- Perfect for architecture decisions and complex problem solving
- Exit with `exit_plan_mode` tool

#### **Thinking Levels**
Use progressively deeper analysis:
- `"think"` - Basic analysis
- `"think hard"` - More thorough evaluation
- `"think harder"` - Deep analysis
- `"ultrathink"` - Maximum reasoning power

#### **Auto-Accept Mode**
- Toggle with Shift+Tab
- Allows Claude to work without permission prompts
- Use `--dangerously-skip-permissions` for trusted workflows

#### **Multi-Directory Support**
```bash
# Start with multiple directories
claude --add-dir ../backend --add-dir ../shared-libs

# Add directories mid-session
/add-dir ../related-service
```

### 2. Configuration Hierarchy

Claude Code settings are applied in order (highest to lowest precedence):
1. Command-line flags
2. `.claude/settings.json` (project-specific)
3. `~/.claude/settings.json` (user global)
4. System defaults

## Project Structure

```
project-root/
├── .claude/
│   ├── settings.json           # Project-specific Claude settings
│   ├── commands/               # Custom slash commands
│   │   ├── setup.md           # Project setup automation
│   │   ├── deploy.md          # AWS deployment command
│   │   ├── destroy.md         # Resource cleanup command
│   │   ├── test.md            # Test execution command
│   │   ├── review.md          # Code review command
│   │   └── bastion.md         # Database access command
│   ├── agents/                 # Specialized sub-agents
│   │   ├── aws-architect.md   # AWS CDK specialist
│   │   ├── python-tester.md   # Python testing specialist
│   │   └── security-auditor.md # Security review specialist
│   ├── hooks/                  # Automation hooks
│   │   ├── pre-tool-use-safety.py      # Safety validation
│   │   ├── auto-approve-safe.py        # Auto-approve safe commands
│   │   ├── post-edit-validation.py     # Post-edit checks
│   │   └── prompt-safety-check.py      # Prompt injection protection
│   └── hooks.config.json       # Hook configuration rules
├── CLAUDE.md                   # Project context (checked in)
├── CLAUDE.local.md            # Personal preferences (gitignored)
├── Makefile                   # Standard DevOps commands
├── pyproject.toml             # Poetry configuration
├── .env.example               # Environment template
├── .gitignore                 # Including TODO.md
├── infrastructure/            # AWS CDK code
│   ├── app.py
│   ├── stacks/
│   └── requirements.txt
├── src/                       # Application code
├── tests/                     # Test suite
├── scripts/                   # Utility scripts
│   ├── setup.py              # Project setup script
│   └── validate.py           # Validation script
└── docs/
    ├── README.md             # Project overview
    ├── SETUP.md              # Detailed setup guide
    ├── ARCHITECTURE.md       # System architecture
    └── REQUIREMENTS.md       # Project requirements
```

## Safety & Security

### Hook System Overview

Claude Code hooks provide deterministic control at key lifecycle points:

1. **UserPromptSubmit**: Before Claude processes prompts
2. **PreToolUse**: Before tool execution (can block)
3. **PostToolUse**: After tool completion
4. **Notification**: When Claude sends notifications
5. **Stop**: When Claude finishes responding
6. **SubagentStop**: When sub-agents complete

### Safety Implementation

The safety system includes multiple layers:

1. **Command Validation**: Blocks dangerous operations (rm -rf, DROP DATABASE, etc.)
2. **File Protection**: Prevents modification of sensitive files (.env, .pem, etc.)
3. **AWS Safety**: Blocks destructive AWS operations
4. **Git Safety**: Prevents force pushes and destructive operations
5. **Auto-Approval**: Reduces friction for safe operations

## Workflows & Best Practices

### Development Workflow

1. **Start with Plan Mode**
   ```
   claude "think hard about implementing user authentication"
   # Press Shift+Tab twice for plan mode
   ```

2. **Use Test-Driven Development**
   ```
   claude "Create comprehensive tests for the user service"
   # After tests pass, implement the service
   ```

3. **Iterative Development**
   - Keep changes small and reviewable
   - Use `/clear` frequently to maintain context clarity
   - Commit after each successful iteration

4. **Multi-Instance Development**
   - Run multiple Claude instances for different components
   - Each maintains separate context but shares CLAUDE.md

### Common Commands

```bash
# Start in plan mode
claude "ultrathink and plan the database schema changes"

# Skip permissions for trusted operations
claude --dangerously-skip-permissions "fix all linting errors"

# Headless mode for CI/CD
claude -p "run tests and format code" --output-format stream-json

# Continue previous session
claude --resume
```

## Implementation Files

### 1. CLAUDE.md Template

```markdown
# Project Context for Claude Code

## Project Overview
[Brief description of the project and its purpose]

## Development Principles
- Infrastructure as Code with AWS CDK (Python)
- Poetry for dependency management (Python 3.12+)
- pytest for testing with TDD approach
- Cost-conscious development (destroy resources after sessions)
- Multi-environment support (dev, stage, prod)

## Technical Stack
- **Cloud**: AWS (designed for portability)
- **IaC**: AWS CDK with Python
- **Backend**: Python 3.12+
- **Database**: PostgreSQL on RDS
- **Package Management**: Poetry
- **Testing**: pytest with coverage

## Coding Standards
- Follow PEP 8 for Python code
- Use type hints for all functions
- Docstrings for all public functions
- Meaningful variable names (but concise in artifacts)
- Extract functions for testability

## Project Structure
@docs/ARCHITECTURE.md

## AWS Architecture
- VPC with public/private subnets
- RDS PostgreSQL in private subnet
- Lambda functions for operations
- ECS for long-running tasks
- S3 for data storage

## Restrictions & Safety
- NO Git write operations (only read)
- NO AWS write operations via CLI (only through CDK)
- NO Database write operations via CLI (only read)
- NO direct infrastructure patches
- Generate commit messages but don't execute
- All work attributed to human developer

## Automation Requirements
- Virtual environment must be active for all operations
- Make commands must be idempotent
- All infrastructure changes via CDK only
- Secrets via .env (never committed)
- Support for macOS, Windows, and Linux

## Common Operations
- `make setup` - Initialize project
- `make deploy` - Deploy infrastructure
- `make test` - Run test suite
- `make destroy` - Clean up resources
- `make bastion` - Database access

## Environment Configuration
- Development: Public RDS for easy access
- Staging: Private RDS with bastion
- Production: Private RDS, minimal access

## Next Steps
Check TODO.md for current tasks (local only, not in git)
```

### 2. .claude/settings.json

```json
{
  "model": "claude-3-5-sonnet-20241022",
  "temperature": 0.2,
  "memoryBankName": "project-memory",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/auto-approve-safe.py"
          },
          {
            "type": "command",
            "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/pre-tool-use-safety.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/post-edit-validation.py"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date): $CLAUDE_TOOL_INPUT\" >> ~/.claude/bash-history.log"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/prompt-safety-check.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"Session completed at $(date)\" >> ~/.claude/session-log.txt"
          }
        ]
      }
    ]
  },
  "allowedTools": [
    "Read", "Edit", "Write", "MultiEdit",
    "Bash(ls*)", "Bash(cat*)", "Bash(grep*)",
    "Bash(git status)", "Bash(git log)", "Bash(git diff)",
    "Bash(make test)", "Bash(make lint)",
    "Bash(python*)", "Bash(pytest*)",
    "Bash(aws * describe*)", "Bash(aws * list*)",
    "WebSearch", "WebFetch"
  ]
}
```

### 3. Makefile Template

```makefile
.PHONY: help setup deploy destroy test lint format validate bastion claude-setup

# Default target
help:
	@echo "Available commands:"
	@echo "  setup       - Set up development environment"
	@echo "  deploy      - Deploy infrastructure"
	@echo "  destroy     - Destroy infrastructure"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code"
	@echo "  validate    - Validate deployment"
	@echo "  bastion     - Start bastion for DB access"
	@echo ""
	@echo "Claude-specific commands:"
	@echo "  claude-setup - Initialize Claude Code for this project"
	@echo "  claude-plan  - Start Claude in plan mode"
	@echo "  claude-test  - Use Claude to develop tests"

# Environment setup
setup:
	@echo "🔧 Setting up development environment..."
	@python scripts/setup.py
	@poetry install
	@echo "✅ Setup complete"

# AWS deployment
deploy:
	@echo "🚀 Deploying infrastructure..."
	@python scripts/check_env.py
	@poetry run cdk deploy --all --require-approval never
	@echo "✅ Deployment complete"

# Cleanup
destroy:
	@echo "🗑️  Destroying infrastructure..."
	@read -p "Are you sure? (y/N) " confirm && \
	[ "$$confirm" = "y" ] && poetry run cdk destroy --all --force
	@echo "✅ Cleanup complete"

# Testing
test:
	@echo "🧪 Running tests..."
	@poetry run pytest tests/ -v --cov=src --cov-report=term-missing

# Code quality
lint:
	@echo "🔍 Running linters..."
	@poetry run black src/ tests/ --check
	@poetry run mypy src/
	@poetry run ruff check src/ tests/

format:
	@echo "✨ Formatting code..."
	@poetry run black src/ tests/
	@poetry run ruff check src/ tests/ --fix

# Validation
validate:
	@echo "✔️  Validating deployment..."
	@python scripts/validate.py

# Database access
bastion:
	@echo "🔐 Starting bastion host..."
	@python scripts/bastion.py start

bastion-stop:
	@echo "🛑 Stopping bastion host..."
	@python scripts/bastion.py stop

# Claude Code specific
claude-setup:
	@echo "🤖 Setting up Claude Code..."
	@mkdir -p .claude/commands .claude/hooks .claude/agents
	@chmod +x .claude/hooks/*.py
	@echo "✅ Claude Code setup complete"

claude-plan:
	@echo "🧠 Starting Claude in plan mode..."
	@echo "Press Shift+Tab twice to enter plan mode"
	claude "Review project structure and suggest improvements"

claude-test:
	@echo "🧪 Using Claude for test development..."
	claude "ultrathink and develop comprehensive tests for uncovered code"
```

### 4. Custom Commands

#### .claude/commands/setup.md
```markdown
Complete project setup from fresh clone:

1. Check Python version (must be 3.12+)
2. Create virtual environment with poetry
3. Install all dependencies
4. Set up pre-commit hooks
5. Create .env from .env.example
6. Initialize AWS CDK
7. Create TODO.md and add to .gitignore
8. Validate setup completeness

Run each step with proper error handling and clear output.
Remember to activate the virtual environment for all subsequent operations.
```

#### .claude/commands/deploy.md
```markdown
Deploy infrastructure to AWS:

1. Validate environment variables are set
2. Check AWS credentials are configured
3. Ensure virtual environment is active
4. Run CDK diff to show changes
5. Deploy all stacks with --require-approval never
6. Run post-deployment validation
7. Display resource information and endpoints

For the environment $ARGUMENTS (default: dev).
Ensure all resources are tagged appropriately.
```

#### .claude/commands/review.md
```markdown
Comprehensive code review focusing on:

1. **Security**: Check for exposed secrets, SQL injection, XSS
2. **Performance**: Identify N+1 queries, inefficient algorithms
3. **Code Quality**: PEP 8 compliance, type hints, docstrings
4. **Testing**: Coverage gaps, edge cases
5. **Architecture**: SOLID principles, proper abstractions
6. **AWS Best Practices**: Cost optimization, security groups
7. **Documentation**: Update needed for new features

Create a report with specific actionable items.
Focus on high-impact improvements.
```

### 5. Safety Hooks

#### .claude/hooks/pre-tool-use-safety.py
```python
#!/usr/bin/env python3
"""
Comprehensive safety validation for Claude Code operations.
Blocks dangerous commands and protects sensitive resources.
"""

import json
import sys
import re
import os
from datetime import datetime

def main():
    try:
        # Read input from Claude Code
        data = json.load(sys.stdin)
        tool_name = data.get('tool_name', '')
        tool_input = data.get('tool_input', {})
        
        # Log for debugging (optional)
        log_operation(tool_name, tool_input)
        
        # Route to appropriate validator
        if tool_name == 'Bash':
            validate_bash_command(tool_input)
        elif tool_name in ['Write', 'Edit', 'MultiEdit']:
            validate_file_operation(tool_input)
        elif tool_name == 'Read':
            validate_file_read(tool_input)
        
    except Exception as e:
        # Log error but don't block operation
        sys.stderr.write(f"Hook error: {str(e)}\n")
        sys.exit(0)

def validate_bash_command(tool_input):
    """Validate bash commands for safety"""
    command = tool_input.get('command', '')
    
    # Dangerous command patterns
    dangerous_patterns = [
        # Destructive file operations
        (r'rm\s+.*-[rf]', 'Dangerous rm command detected. Use with extreme caution.'),
        (r'rm\s+-[rf]', 'Dangerous rm flags detected.'),
        (r'>\s*/dev/(sd|hd|nvme)', 'Direct disk write operations are forbidden.'),
        (r'dd\s+.*of=/dev/', 'Direct disk operations are forbidden.'),
        
        # System destruction
        (r':(){ :|:& };:', 'Fork bomb detected - this would crash the system.'),
        (r'/dev/null\s*>\s*/', 'Attempting to overwrite system files.'),
        
        # Database operations
        (r'DROP\s+(DATABASE|TABLE|SCHEMA)', 'Database drop operations are forbidden.'),
        (r'TRUNCATE\s+TABLE', 'Table truncation is forbidden.'),
        (r'DELETE\s+FROM.*WHERE\s+1\s*=\s*1', 'Unsafe DELETE without proper WHERE clause.'),
        
        # AWS destruction
        (r'aws.*delete', 'AWS delete operations are forbidden.'),
        (r'aws.*terminate', 'AWS terminate operations are forbidden.'),
        (r'aws.*destroy', 'AWS destroy operations are forbidden.'),
        (r'cdk\s+destroy', 'CDK destroy operations must be run manually.'),
        
        # Git operations
        (r'git\s+push.*--force', 'Force push operations are dangerous.'),
        (r'git\s+reset\s+--hard', 'Hard reset operations can lose work.'),
        (r'git\s+clean\s+-[fd]', 'Git clean can delete untracked files.'),
        
        # System modifications
        (r'chmod\s+777', 'Setting world-writable permissions is dangerous.'),
        (r'chown\s+-R\s+root', 'Changing ownership to root is forbidden.'),
        (r'>\s*/etc/', 'Writing to system directories is forbidden.'),
        
        # Package management
        (r'npm\s+install.*-g', 'Global npm installs should be done manually.'),
        (r'pip\s+install.*--user', 'User-level pip installs should be done manually.'),
        (r'sudo\s+', 'Sudo operations are forbidden.'),
    ]
    
    # Check each pattern
    for pattern, message in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            block_operation(message)
    
    # Additional checks for specific commands
    if 'curl' in command or 'wget' in command:
        if re.search(r'\|\s*sh', command) or re.search(r'\|\s*bash', command):
            block_operation('Piping downloads directly to shell is dangerous.')
    
    # Check for command chaining that bypasses safety
    if '&&' in command or ';' in command or '||' in command:
        # Split and check each command
        sub_commands = re.split(r'[;&|]+', command)
        for sub_cmd in sub_commands:
            # Recursively check each sub-command
            validate_bash_command({'command': sub_cmd.strip()})

def validate_file_operation(tool_input):
    """Validate file write/edit operations"""
    file_path = tool_input.get('file_path', '')
    
    # Sensitive file patterns
    sensitive_patterns = [
        # Environment and secrets
        (r'\.env', 'Cannot modify environment files directly.'),
        (r'\.env\.', 'Cannot modify environment files directly.'),
        (r'secrets\.', 'Cannot modify secret files.'),
        (r'credentials', 'Cannot modify credential files.'),
        (r'\.pem$', 'Cannot modify certificate files.'),
        (r'\.key$', 'Cannot modify key files.'),
        
        # System files
        (r'^/etc/', 'Cannot modify system configuration files.'),
        (r'^/usr/', 'Cannot modify system files.'),
        (r'^/var/', 'Cannot modify system files.'),
        (r'~/.ssh/', 'Cannot modify SSH configuration.'),
        (r'~/.aws/', 'Cannot modify AWS configuration.'),
        
        # Git files
        (r'\.git/', 'Cannot modify git internals.'),
        (r'\.gitignore$', 'Gitignore changes need manual review.'),
        
        # Project protection
        (r'package-lock\.json', 'Package lock files should not be edited directly.'),
        (r'poetry\.lock', 'Poetry lock files should not be edited directly.'),
        (r'Pipfile\.lock', 'Pipfile lock files should not be edited directly.'),
    ]
    
    for pattern, message in sensitive_patterns:
        if re.search(pattern, file_path, re.IGNORECASE):
            block_operation(message)
    
    # Check for path traversal
    if '../' in file_path or '/..' in file_path:
        block_operation('Path traversal detected.')

def validate_file_read(tool_input):
    """Validate file read operations for sensitive data"""
    file_path = tool_input.get('file_path', '')
    
    # Files that should never be read
    forbidden_patterns = [
        (r'\.pem$', 'Cannot read certificate files.'),
        (r'\.key$', 'Cannot read private key files.'),
        (r'/etc/shadow', 'Cannot read password files.'),
        (r'~/.ssh/id_', 'Cannot read SSH private keys.'),
    ]
    
    for pattern, message in forbidden_patterns:
        if re.search(pattern, file_path, re.IGNORECASE):
            block_operation(message)

def block_operation(reason):
    """Block the operation with a clear reason"""
    response = {
        "decision": "block",
        "reason": f"🛡️ SAFETY BLOCK: {reason}\nThis operation requires manual execution for safety."
    }
    print(json.dumps(response))
    sys.exit(0)

def approve_operation(reason=""):
    """Explicitly approve an operation"""
    response = {
        "decision": "approve",
        "reason": reason
    }
    print(json.dumps(response))
    sys.exit(0)

def log_operation(tool_name, tool_input):
    """Log operations for debugging and audit"""
    log_dir = os.path.expanduser("~/.claude/logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "input": tool_input
    }
    
    with open(f"{log_dir}/operations.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

if __name__ == "__main__":
    main()
```

#### .claude/hooks/auto-approve-safe.py
```python
#!/usr/bin/env python3
"""
Auto-approve known safe commands to reduce friction.
This runs before the safety validator to fast-track safe operations.
"""

import json
import sys
import re

def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get('tool_name', '')
        tool_input = data.get('tool_input', {})
        
        if tool_name == 'Bash':
            command = tool_input.get('command', '')
            
            # Safe command patterns to auto-approve
            safe_patterns = [
                # File system navigation
                r'^ls(\s|$)',
                r'^pwd$',
                r'^cd\s',
                r'^tree(\s|$)',
                
                # File reading
                r'^cat\s',
                r'^head\s',
                r'^tail\s',
                r'^less\s',
                r'^more\s',
                
                # Searching
                r'^grep\s',
                r'^find\s.*-name',
                r'^which\s',
                r'^whereis\s',
                
                # Git read operations
                r'^git\s+(status|log|diff|branch|remote|show)(\s|$)',
                
                # Python operations
                r'^python\s+.*\.py$',
                r'^poetry\s+(show|list|env)',
                r'^pytest(\s|$)',
                
                # Make commands (safe ones)
                r'^make\s+(test|lint|format|help)(\s|$)',
                
                # AWS read operations
                r'^aws\s+.*\s*(describe|list|get).*',
                
                # Docker read operations
                r'^docker\s+(ps|images|logs)(\s|$)',
                
                # Environment checks
                r'^echo\s+\$',
                r'^env$',
                r'^printenv$',
            ]
            
            for pattern in safe_patterns:
                if re.match(pattern, command, re.IGNORECASE):
                    response = {
                        "decision": "approve",
                        "reason": "Auto-approved safe command"
                    }
                    print(json.dumps(response))
                    sys.exit(0)
        
        elif tool_name in ['Read']:
            # Auto-approve all read operations unless blocked by safety check
            response = {
                "decision": "approve",
                "reason": "Read operations are generally safe"
            }
            print(json.dumps(response))
            sys.exit(0)
        
    except Exception:
        pass
    
    # Default: let Claude's normal flow continue
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 6. Sub-Agents

#### .claude/agents/aws-architect.md
```markdown
---
name: AWS Architect
description: Specialized in AWS CDK and cloud architecture decisions
tools: ["Read", "Edit", "Write", "WebSearch"]
---

You are an AWS Solutions Architect specializing in:
- AWS CDK with Python
- Cost optimization
- Security best practices
- Multi-environment deployments
- Infrastructure as Code

When designing infrastructure:
1. Always consider cost implications
2. Use least-privilege IAM policies
3. Implement proper tagging strategies
4. Design for multi-region capability
5. Include CloudWatch alarms and monitoring

Prefer:
- Managed services over self-managed
- Serverless where appropriate
- Private subnets for databases
- VPC endpoints for AWS services
- Parameter Store/Secrets Manager for configuration

Always validate CDK code with `cdk diff` before suggesting deployment.
```

#### .claude/agents/python-tester.md
```markdown
---
name: Python Testing Specialist
description: Expert in pytest and test-driven development
tools: ["Read", "Edit", "Write", "Bash"]
---

You are a Python testing expert specializing in:
- pytest and its ecosystem
- Test-driven development (TDD)
- Mock and patch strategies
- Fixture design
- Coverage optimization

Testing principles:
1. Write tests BEFORE implementation
2. One assertion per test when possible
3. Use descriptive test names
4. Proper fixture scoping
5. Meaningful test data

Test structure:
- Arrange: Set up test data
- Act: Execute the function
- Assert: Verify the result

Always aim for:
- 90%+ code coverage
- Fast test execution
- Isolated unit tests
- Integration tests for critical paths
- Clear failure messages
```

### 7. pyproject.toml Template

```toml
[tool.poetry]
name = "your-project-name"
version = "0.1.0"
description = "A project following Claude Code best practices"
authors = ["Your Name <email@example.com>"]
readme = "README.md"
python = "^3.12"

[tool.poetry.dependencies]
python = "^3.12"
boto3 = "^1.34.0"
aws-cdk-lib = "^2.124.0"
constructs = "^10.3.0"
pydantic = "^2.5.0"
pydantic-settings = "^2.1.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
pytest-asyncio = "^0.21.0"
black = "^23.12.0"
mypy = "^1.8.0"
ruff = "^0.1.9"
pre-commit = "^3.6.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88
target-version = ['py312']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[tool.ruff]
target-version = "py312"
line-length = 88
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "C",   # flake8-comprehensions
    "B",   # flake8-bugbear
    "UP",  # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by black)
    "B008",  # do not perform function calls in argument defaults
    "C901",  # too complex
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_functions = ["test_*"]
python_classes = ["Test*"]
addopts = """
    -ra
    --strict-markers
    --ignore=docs/conf.py
    --ignore=setup.py
    --ignore=ci
    --ignore=.eggs
    --doctest-modules
    --doctest-glob=*.md
    --tb=short
    --cov=src
    --cov-report=term-missing:skip-covered
    --cov-report=html
    --cov-report=xml
    --cov-branch
"""

[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = true
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "class .*\bProtocol\):",
    "@(abc\\.)?abstractmethod",
]
```

### 8. .gitignore additions

```gitignore
# Claude Code specific
TODO.md
CLAUDE.local.md
.claude/logs/
.claude/session-history/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Poetry
poetry.lock

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.coverage
.coverage.*
.cache
.pytest_cache/
htmlcov/
.tox/
.nox/
coverage.xml
*.cover
*.py,cover
.hypothesis/

# AWS
.aws-sam/
cdk.out/
cdk.context.json

# Environment
.env
.env.*
!.env.example

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
```

## Next Steps

1. **Initialize Project**: 
   ```bash
   mkdir my-project && cd my-project
   git init
   # Copy all files from this guide
   make setup
   make claude-setup
   ```

2. **Configure Claude Code**:
   ```bash
   # Test hooks
   cd .claude/hooks
   chmod +x *.py
   # Test dangerous command blocking
   echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | python3 pre-tool-use-safety.py
   ```

3. **Start Development**:
   ```bash
   # Begin with plan mode
   claude "ultrathink about the project architecture"
   
   # Or skip permissions for trusted operations
   claude --dangerously-skip-permissions "set up the initial project structure"
   ```

4. **Customize for Your Needs**:
   - Add project-specific commands in `.claude/commands/`
   - Create specialized agents in `.claude/agents/`
   - Extend safety rules in hooks configuration
   - Update CLAUDE.md with project context

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [AWS CDK Python Reference](https://docs.aws.amazon.com/cdk/api/v2/python/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [pytest Documentation](https://docs.pytest.org/)

## Safety Reminders

1. **Never commit**: .env files, AWS credentials, private keys
2. **Always test locally**: Especially infrastructure changes
3. **Use Plan Mode**: For architectural decisions
4. **Review git commits**: Before pushing
5. **Validate deployments**: Run `make validate` after deploy

This setup provides a secure, efficient, and scalable foundation for developing with Claude Code while maintaining all the safety and best practices you require.