#!/usr/bin/env python3
"""
Project Boundary Detection Hook

Ensures Claude operations stay within the project directory boundary.
Detects project root by looking for .claude/ directory.
"""

import json
import sys
import os
import re
from pathlib import Path


def find_project_root(start_path: Path = None) -> Path:
    """Find project root by looking for .claude directory"""
    if start_path is None:
        start_path = Path.cwd()
    
    current = start_path.resolve()
    
    # Walk up the directory tree looking for .claude
    while current != current.parent:
        if (current / ".claude").exists():
            return current
        current = current.parent
    
    # If no .claude found, consider current directory as project root
    return start_path.resolve()


def is_within_project(file_path: str, project_root: Path) -> bool:
    """Check if a file path is within the project boundary"""
    try:
        resolved_path = Path(file_path).resolve()
        return project_root in resolved_path.parents or resolved_path == project_root
    except Exception:
        # If path resolution fails, be conservative and block
        return False


def validate_file_operation(tool_input: dict, project_root: Path):
    """Validate file operations stay within project boundary"""
    file_path = tool_input.get('file_path', '')
    
    if not file_path:
        return  # No file path to validate
    
    if not is_within_project(file_path, project_root):
        block_operation(f"File operation outside project boundary: {file_path}")
    
    # Check for sensitive system paths even within project
    system_patterns = [
        r'^/etc/',
        r'^/usr/',
        r'^/var/',
        r'^/bin/',
        r'^/sbin/',
        r'~/.ssh/',
        r'~/.aws/',
        r'/dev/',
        r'/proc/',
        r'/sys/'
    ]
    
    for pattern in system_patterns:
        if re.match(pattern, file_path):
            block_operation(f"Access to system directory blocked: {file_path}")


def validate_bash_command(tool_input: dict, project_root: Path):
    """Validate bash commands for project boundary compliance"""
    command = tool_input.get('command', '')
    
    # Check for operations that might escape project boundary
    dangerous_patterns = [
        # File operations outside project
        (r'(cp|mv|rm|ln)\s+.*\.\./', 'File operations using ../ can escape project boundary'),
        (r'(cp|mv|rm|ln)\s+.*/.*/', 'Absolute file paths may escape project boundary'),
        
        # System modifications
        (r'sudo\s+', 'System-level operations are forbidden'),
        (r'su\s+', 'User switching is forbidden'),
        (r'chmod\s+.*(/usr/|/etc/|/var/)', 'System directory permission changes forbidden'),
        
        # Network operations that might affect system
        (r'(wget|curl).*\|\s*(sh|bash)', 'Piping downloads to shell is dangerous'),
        
        # Package management outside project
        (r'(apt|yum|brew|pacman)\s+install', 'System package installation should be manual'),
    ]
    
    for pattern, message in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            block_operation(message)
    
    # Allow operations that are clearly within project directory
    safe_local_patterns = [
        r'^ls\s',
        r'^pwd$',
        r'^cd\s+[^/]',  # Relative cd only
        r'^find\s+\.\s',  # find starting from current dir
        r'^grep\s+.*\s+\.',  # grep in current dir
    ]
    
    for pattern in safe_local_patterns:
        if re.match(pattern, command):
            return  # Explicitly safe, allow
    
    # For cd commands, ensure they stay within project
    cd_match = re.match(r'^cd\s+(.+)$', command.strip())
    if cd_match:
        target_path = cd_match.group(1).strip('\'"')
        if target_path.startswith('/'):
            # Absolute path - check if within project
            if not is_within_project(target_path, project_root):
                block_operation(f"Cannot cd outside project boundary: {target_path}")


def block_operation(reason: str):
    """Block the operation with a clear reason"""
    response = {
        "decision": "block",
        "reason": f"🚧 PROJECT BOUNDARY: {reason}\n\nOperations must stay within the project directory for safety."
    }
    print(json.dumps(response))
    sys.exit(0)


def approve_operation(reason: str = ""):
    """Approve the operation"""
    response = {
        "decision": "approve",
        "reason": reason
    }
    print(json.dumps(response))
    sys.exit(0)


def main():
    try:
        # Read input from Claude Code
        data = json.load(sys.stdin)
        tool_name = data.get('tool_name', '')
        tool_input = data.get('tool_input', {})
        
        # Find project root
        project_root = find_project_root()
        
        # Store project root in environment for other hooks
        os.environ['CLAUDE_PROJECT_ROOT'] = str(project_root)
        
        # Validate based on tool type
        if tool_name in ['Write', 'Edit', 'MultiEdit', 'Read']:
            validate_file_operation(tool_input, project_root)
        elif tool_name == 'Bash':
            validate_bash_command(tool_input, project_root)
        
        # If we get here, the operation is allowed
        approve_operation("Operation within project boundary")
        
    except Exception as e:
        # Log error but don't block operation to avoid breaking workflows
        sys.stderr.write(f"Project boundary hook error: {str(e)}\n")
        approve_operation("Hook error - defaulting to allow")


if __name__ == "__main__":
    main()