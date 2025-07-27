# Claude Code Project Best Practices

A modular system for bootstrapping Claude Code projects with domain-specific configurations and safety measures.

## 🚀 Quick Start

### Option A: Bootstrap Script (Recommended)

```bash
# Interactive setup
curl -sSL https://raw.githubusercontent.com/yourusername/claude-project-best-practices/main/core/scripts/bootstrap.py | python3 - --interactive

# Or specify options directly
curl -sSL https://raw.githubusercontent.com/yourusername/claude-project-best-practices/main/core/scripts/bootstrap.py | python3 - --name "my-api" --domains python,aws
```

### Option B: Manual Setup

1. **Download core files**:
   ```bash
   # Create project directory
   mkdir my-project && cd my-project
   
   # Download and run bootstrap script locally
   wget https://raw.githubusercontent.com/yourusername/claude-project-best-practices/main/core/scripts/bootstrap.py
   python3 bootstrap.py --interactive
   ```

## 🏗️ System Architecture

### Core Components

- **`core/`** - Base Claude Code configuration
  - `.claude/settings.json` - Core Claude settings
  - `.claude/hooks/` - Safety and boundary enforcement
  - `.claude/commands/` - Universal commands
  - `scripts/bootstrap.py` - Project initialization

### Domain Modules

- **`domains/python/`** - Python/Poetry development
- **`domains/aws/`** - AWS/CDK infrastructure (coming soon)
- **`domains/git/`** - Git workflows and safety (coming soon)
- **`domains/docker/`** - Container development (coming soon)

### Features

- **🛡️ Safety System**: Multi-layered protection against dangerous operations
- **🔧 Modular Domains**: Mix and match technology stacks
- **📦 Auto-Fetching**: Downloads latest configurations from repository
- **🎯 Project Boundaries**: Enforces operations within project directory
- **🧠 Memory Banks**: Project-specific Claude memory management
- **⚡ Interactive Setup**: Guided project initialization

## 🛡️ Safety Features

### Project Boundary Enforcement
- Operations restricted to project directory
- Automatic detection of project root via `.claude/` directory
- Blocks access to system directories and sensitive files

### Command Filtering
- **Blocked**: `rm -rf /`, `sudo` commands, AWS delete operations
- **Auto-approved**: `ls`, `git status`, `make test`, read operations
- **Logged**: All operations for audit trail

### Configuration Protection
- Always prompts for configuration file changes
- Blocks modification of secrets and credentials
- Protects lock files and generated files

## 📋 Available Domains

### Python Domain
- **Tools**: Poetry, pytest, black, ruff, mypy
- **Structure**: `src/`, `tests/`, proper packaging
- **Features**: Coverage reporting, pre-commit hooks, TDD workflow
- **Commands**: `/test`, `/lint`, `/format`, `/setup-python`

### Coming Soon
- **AWS**: CDK, infrastructure as code, multi-environment
- **Git**: Advanced workflows, safety hooks, commit templates
- **Docker**: Multi-stage builds, development containers
- **Database**: Migration management, connection pooling

## 🎯 Usage Examples

### Python API Project
```bash
# Bootstrap with Python domain
python3 bootstrap.py --name "user-api" --domains python --type "Web API"

# Result: Ready-to-use Python project with:
# - Poetry configuration
# - Test framework setup
# - Linting and formatting tools
# - Claude Code integration
```

### Full-Stack Project
```bash
# Multiple domains
python3 bootstrap.py --domains python,aws,docker --interactive

# Creates project with:
# - Python backend setup
# - AWS infrastructure templates
# - Docker development environment
```

## 🚀 Getting Started with Your Project

After running the bootstrap script:

1. **Review Configuration**
   ```bash
   # Check what was created
   ls -la
   cat CLAUDE.md
   ```

2. **Initialize Development Environment**
   ```bash
   # For Python projects
   make setup  # or poetry install
   
   # Start Claude Code
   claude
   ```

3. **Explore Available Commands**
   ```bash
   # In Claude Code session
   claude "/help"
   
   # See domain-specific commands
   claude "/test"      # Run tests
   claude "/lint"      # Code quality
   ```

## 📖 Project Structure

After bootstrap, your project will have:

```
my-project/
├── .claude/
│   ├── settings.json          # Claude configuration
│   ├── commands/              # Custom slash commands
│   ├── hooks/                 # Safety and automation
│   └── agents/                # Specialized sub-agents
├── CLAUDE.md                  # Project context
├── .gitignore                 # Including Claude-specific entries
├── Makefile                   # Standard commands (if applicable)
└── [domain-specific files]    # Based on selected domains
```

## 🔧 Customization

### Adding Custom Commands
```bash
# Create custom command
echo "Your command description" > .claude/commands/my-command.md
```

### Extending Safety Rules
```python
# Edit .claude/hooks/pre-tool-use-safety.py
# Add custom validation logic
```

### Domain-Specific Agents
```markdown
# Create .claude/agents/my-specialist.md
---
name: My Specialist
description: Expert in specific technology
---
You are a specialist in...
```

## 🔍 Troubleshooting

### Bootstrap Script Issues
```bash
# Check Python version (3.8+ required)
python3 --version

# Test network connectivity
curl -I https://raw.githubusercontent.com/yourusername/claude-project-best-practices/main/core/scripts/bootstrap.py
```

### Hook Failures
```bash
# Check hook permissions
ls -la .claude/hooks/
chmod +x .claude/hooks/*.py

# Test hook manually
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | python3 .claude/hooks/pre-tool-use-safety.py
```

### Claude Code Integration
```bash
# Verify Claude Code can find configuration
claude --help

# Check settings are loaded
claude "show me the current project configuration"
```

## 🤝 Contributing

### Adding New Domains

1. **Create domain structure**:
   ```bash
   mkdir -p domains/my-domain/.claude/{commands,agents}
   ```

2. **Create manifest**:
   ```json
   {
     "name": "my-domain",
     "version": "1.0.0", 
     "description": "My domain description",
     "files": { ... },
     "prompts": { ... }
   }
   ```

3. **Add domain files**:
   - Commands in `.claude/commands/`
   - Agents in `.claude/agents/`
   - Templates and configurations

### Extending Safety Rules

Safety rules are in `core/.claude/hooks/`. Add patterns to:
- `pre-tool-use-safety.py` - Command validation
- `project-boundary.py` - Project boundary enforcement

## 📚 Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Project Examples](./examples/)
- [Domain Specifications](./domains/)
- [Safety System Details](./core/.claude/hooks/)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## ⚡ Pro Tips

1. **Use Plan Mode**: Press `Shift+Tab` twice for research-only mode
2. **Thinking Levels**: Use `think`, `think hard`, `think harder`, `ultrathink`
3. **Clear Context**: Use `/clear` frequently to maintain clarity
4. **Multiple Instances**: Run parallel Claude sessions for different components
5. **Memory Banks**: Each project gets its own memory for context persistence

---

**Ready to build something amazing with Claude Code?** 🚀

Start with: `curl -sSL https://raw.githubusercontent.com/yourusername/claude-project-best-practices/main/core/scripts/bootstrap.py | python3 - --interactive`