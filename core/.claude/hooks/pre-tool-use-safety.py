#!/usr/bin/env python3
"""
Enhanced Safety Validation Hook

Blocks dangerous commands while allowing project-local operations.
Works in conjunction with project-boundary.py to provide layered safety.
"""

import json
import sys
import re
import os
from datetime import datetime


def validate_bash_command(tool_input: dict):
    """Validate bash commands for safety"""
    command = tool_input.get('command', '')
    
    # Always dangerous patterns (never allow)
    critical_patterns = [
        # System destruction
        (r'rm\s+.*-[rf].*/', 'Recursive delete with absolute paths is dangerous'),
        (r'rm\s+-[rf]\s+/', 'Recursive delete of root paths is forbidden'),
        (r':(){ :|:& };:', 'Fork bomb detected'),
        (r'>\s*/dev/(sd|hd|nvme)', 'Direct disk operations are forbidden'),
        (r'dd\s+.*of=/dev/', 'Direct disk operations are forbidden'),
        
        # Database destruction
        (r'DROP\s+(DATABASE|SCHEMA)\s+(?!.*test)', 'Database/schema drops outside test context are forbidden'),
        (r'TRUNCATE\s+TABLE\s+(?!.*test)', 'Table truncation outside test context is forbidden'),
        (r'DELETE\s+FROM.*WHERE\s+1\s*=\s*1', 'Unsafe DELETE without proper WHERE clause'),
        
        # AWS/Cloud destruction (CLI-based)
        (r'aws\s+.*delete(?!\s+.*test)', 'AWS delete operations should be done through IaC'),
        (r'aws\s+.*terminate(?!\s+.*test)', 'AWS terminate operations should be done through IaC'),
        (r'aws\s+.*destroy', 'AWS destroy operations should be done through IaC'),
        (r'terraform\s+destroy(?!\s+.*-target)', 'Terraform destroy should target specific resources'),
        
        # Git destruction
        (r'git\s+push.*--force', 'Force push operations are dangerous'),
        (r'git\s+reset\s+--hard\s+HEAD~[2-9]', 'Hard reset beyond 1 commit is dangerous'),
        (r'git\s+clean\s+-[fd]', 'Git clean can delete untracked files'),
        (r'git\s+filter-branch', 'Git filter-branch is destructive'),
        
        # System modifications
        (r'chmod\s+777', 'World-writable permissions are dangerous'),
        (r'chown\s+-R\s+root', 'Changing ownership to root is forbidden'),
        (r'sudo\s+rm', 'Sudo rm operations are forbidden'),
        (r'sudo\s+chmod.*(/usr/|/etc/|/var/)', 'System directory permission changes forbidden'),
        
        # Network security
        (r'curl.*\|\s*sh', 'Piping downloads to shell is dangerous'),
        (r'wget.*\|\s*bash', 'Piping downloads to shell is dangerous'),
        (r'nc\s+.*-e', 'Netcat with command execution is dangerous'),
        
        # Package management (should be in containers/controlled environments)
        (r'sudo\s+(apt|yum|dnf|pacman)', 'System package management should be done manually'),
        (r'npm\s+install.*-g', 'Global npm installs should be done manually'),
        (r'pip\s+install.*--user', 'User-level pip installs should be done manually'),
    ]
    
    # Check critical patterns
    for pattern, message in critical_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            block_operation(message)
    
    # Conditional warnings for project-local operations
    warning_patterns = [
        (r'rm\s+-[rf]', 'Recursive delete - ensure you\'re in the right directory'),
        (r'git\s+reset\s+--hard', 'Hard reset will lose uncommitted changes'),
        (r'make\s+clean', 'Clean operations may remove generated files'),
    ]
    
    for pattern, message in warning_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            # These are warnings, not blocks - let them through but log
            log_warning(f"WARNING: {message} - Command: {command}")
    
    # Auto-approve known safe commands
    safe_patterns = [
        r'^ls(\s|$)',
        r'^pwd$',
        r'^cd\s+[^/]',  # Relative cd
        r'^cat\s+[^/]',  # Relative file reads
        r'^grep\s+',
        r'^find\s+\.',
        r'^which\s+',
        r'^echo\s+',
        r'^printf\s+',
        r'^git\s+(status|log|diff|branch|remote|show)(\s|$)',
        r'^make\s+(test|lint|format|help|check)(\s|$)',
        r'^python\s+.*\.py$',
        r'^poetry\s+(show|list|env|version)',
        r'^pytest(\s|$)',
        r'^aws\s+.*\s*(describe|list|get).*',
        r'^docker\s+(ps|images|logs)(\s|$)',
        r'^env$',
        r'^printenv$',
    ]
    
    for pattern in safe_patterns:
        if re.match(pattern, command, re.IGNORECASE):
            return  # Safe command, allow through


def validate_file_operation(tool_input: dict):
    """Validate file write/edit operations"""
    file_path = tool_input.get('file_path', '')
    
    # Critical file patterns (never allow modification)
    critical_patterns = [
        # Secrets and credentials
        (r'\.pem$', 'Certificate files cannot be modified'),
        (r'\.key$', 'Private key files cannot be modified'),
        (r'\.p12$', 'Certificate store files cannot be modified'),
        (r'credentials', 'Credential files cannot be modified'),
        (r'secrets\.(json|yaml|yml)$', 'Secret files cannot be modified'),
        
        # System files
        (r'^/etc/', 'System configuration files cannot be modified'),
        (r'^/usr/', 'System files cannot be modified'),
        (r'^/var/log/', 'System logs cannot be modified'),
        (r'~/.ssh/', 'SSH configuration cannot be modified'),
        (r'~/.aws/credentials', 'AWS credentials cannot be modified'),
        
        # Git internals
        (r'\.git/(?!hooks/)', 'Git internals cannot be modified directly'),
        
        # Lock files (should be managed by tools)
        (r'package-lock\.json', 'Package lock files should not be edited directly'),
        (r'poetry\.lock', 'Poetry lock files should not be edited directly'),
        (r'Pipfile\.lock', 'Pipfile lock files should not be edited directly'),
        (r'yarn\.lock', 'Yarn lock files should not be edited directly'),
    ]
    
    for pattern, message in critical_patterns:
        if re.search(pattern, file_path, re.IGNORECASE):
            block_operation(message)
    
    # Configuration files that need prompting
    config_patterns = [
        r'\.env$',
        r'\.env\.',
        r'config\.(json|yaml|yml|toml)$',
        r'pyproject\.toml$',
        r'package\.json$',
        r'Dockerfile$',
        r'docker-compose\.(yml|yaml)$',
        r'\.claude/settings\.json$',
    ]
    
    for pattern in config_patterns:
        if re.search(pattern, file_path, re.IGNORECASE):
            # These require user confirmation but aren't blocked
            log_warning(f"Configuration file modification: {file_path}")
            return


def validate_file_read(tool_input: dict):
    """Validate file read operations for sensitive data"""
    file_path = tool_input.get('file_path', '')
    
    # Files that should never be read
    forbidden_patterns = [
        (r'\.pem$', 'Private certificate files cannot be read'),
        (r'\.key$', 'Private key files cannot be read'),
        (r'/etc/shadow', 'Password files cannot be read'),
        (r'~/.ssh/id_', 'SSH private keys cannot be read'),
        (r'~/.aws/credentials', 'AWS credentials should not be read by Claude'),
    ]
    
    for pattern, message in forbidden_patterns:
        if re.search(pattern, file_path, re.IGNORECASE):
            block_operation(message)


def block_operation(reason: str):
    """Block the operation with a clear reason"""
    response = {
        "decision": "block",
        "reason": f"🛡️ SAFETY BLOCK: {reason}\n\nThis operation requires manual execution for safety."
    }
    print(json.dumps(response))
    sys.exit(0)


def log_warning(message: str):
    """Log a warning message"""
    log_dir = os.path.expanduser("~/.claude/logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "level": "WARNING",
        "message": message
    }
    
    try:
        with open(f"{log_dir}/safety-warnings.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass  # Don't fail if logging fails


def main():
    try:
        # Read input from Claude Code
        data = json.load(sys.stdin)
        tool_name = data.get('tool_name', '')
        tool_input = data.get('tool_input', {})
        
        # Route to appropriate validator
        if tool_name == 'Bash':
            validate_bash_command(tool_input)
        elif tool_name in ['Write', 'Edit', 'MultiEdit']:
            validate_file_operation(tool_input)
        elif tool_name == 'Read':
            validate_file_read(tool_input)
        
        # If we get here, operation is allowed
        
    except Exception as e:
        # Log error but don't block operation
        sys.stderr.write(f"Safety hook error: {str(e)}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()