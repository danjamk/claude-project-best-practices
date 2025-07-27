#!/usr/bin/env python3
"""
Prompt Safety Check Hook

Basic protection against prompt injection and unsafe requests.
Logs suspicious patterns for review.
"""

import json
import sys
import re
import os
from datetime import datetime


def check_prompt_safety(prompt: str) -> bool:
    """Check prompt for safety issues"""
    
    # Patterns that might indicate prompt injection or unsafe requests
    suspicious_patterns = [
        # Prompt injection attempts
        (r'ignore\s+(previous|all)\s+instructions', 'Possible prompt injection'),
        (r'forget\s+(everything|all)', 'Possible prompt injection'),
        (r'you\s+are\s+now\s+a', 'Possible role hijacking'),
        (r'act\s+as\s+if\s+you\s+are', 'Possible role hijacking'),
        (r'pretend\s+you\s+are', 'Possible role hijacking'),
        
        # Requests to bypass safety
        (r'disable\s+(safety|security)', 'Request to disable safety'),
        (r'ignore\s+(safety|security)', 'Request to ignore safety'),
        (r'bypass\s+(safety|security)', 'Request to bypass safety'),
        (r'override\s+(safety|security)', 'Request to override safety'),
        
        # Requests for harmful operations
        (r'delete\s+everything', 'Request for destructive operations'),
        (r'destroy\s+(all|everything)', 'Request for destructive operations'),
        (r'wipe\s+(all|everything)', 'Request for destructive operations'),
        
        # Attempts to access sensitive information
        (r'show\s+me\s+(passwords|keys|secrets)', 'Request for sensitive information'),
        (r'give\s+me\s+(passwords|keys|secrets)', 'Request for sensitive information'),
        (r'what\s+are\s+the\s+(passwords|keys|secrets)', 'Request for sensitive information'),
    ]
    
    prompt_lower = prompt.lower()
    
    for pattern, description in suspicious_patterns:
        if re.search(pattern, prompt_lower):
            log_suspicious_prompt(prompt, description)
            # For now, just log - don't block
            # Could be made more restrictive if needed
    
    return True  # Allow all prompts for now


def log_suspicious_prompt(prompt: str, reason: str):
    """Log suspicious prompts for review"""
    log_dir = os.path.expanduser("~/.claude/logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "suspicious_prompt",
        "reason": reason,
        "prompt": prompt[:200] + "..." if len(prompt) > 200 else prompt
    }
    
    try:
        with open(f"{log_dir}/prompt-safety.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass  # Don't fail if logging fails


def main():
    try:
        # Read input from Claude Code
        data = json.load(sys.stdin)
        prompt = data.get('prompt', '')
        
        # Check prompt safety
        if check_prompt_safety(prompt):
            # Allow prompt to continue
            sys.exit(0)
        else:
            # Block prompt (currently not implemented - all prompts allowed)
            response = {
                "decision": "block",
                "reason": "Prompt blocked for safety reasons"
            }
            print(json.dumps(response))
            sys.exit(0)
            
    except Exception as e:
        # Log error but don't block
        sys.stderr.write(f"Prompt safety hook error: {str(e)}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()