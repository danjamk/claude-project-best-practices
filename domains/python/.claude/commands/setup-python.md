Set up Python development environment with Poetry and all dependencies.

## Environment Setup

1. **Verify Python Version**
   - Check Python 3.12+ is available
   - Show current Python version
   - Warn if version doesn't match project requirements

2. **Poetry Installation**
   - Verify Poetry is installed
   - Show installation instructions if missing
   - Update Poetry to latest version if requested

3. **Virtual Environment**
   - Create new virtual environment with Poetry
   - Install all dependencies (main + dev groups)
   - Activate virtual environment
   - Verify installation success

4. **Development Tools**
   - Install pre-commit hooks if configured
   - Set up IDE configuration files
   - Verify linting tools work
   - Run initial test to ensure setup

5. **Project Structure**
   - Create missing directories (src/, tests/, scripts/)
   - Initialize __init__.py files
   - Set up basic test configuration
   - Create example files if project is empty

## Validation

After setup, verify:
- Poetry environment is active
- All dependencies are installed
- Tests can run successfully
- Linting tools are functional
- Pre-commit hooks work (if enabled)

## Troubleshooting

Handle common issues:
- Python version conflicts
- Poetry lock file issues
- Dependency resolution problems
- Permission errors
- Path configuration issues

Always provide clear next steps and helpful error messages.