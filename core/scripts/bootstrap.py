#!/usr/bin/env python3
"""
Claude Code Project Bootstrap Script

Fetches and configures Claude Code best practices for new projects.
Supports interactive setup and domain-specific configurations.
"""

import os
import sys
import json
import argparse
import subprocess
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Dict, List, Optional


class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


class ProjectBootstrap:
    """Handles project initialization and domain configuration"""
    
    def __init__(self, base_url: str = "https://raw.githubusercontent.com/user/claude-project-best-practices/main"):
        self.base_url = base_url
        self.project_root = Path.cwd()
        self.available_domains = ["git", "python", "aws", "docker", "database"]
        
    def print_banner(self):
        """Display welcome banner"""
        print(f"{Colors.BLUE}{Colors.BOLD}")
        print("🤖 Claude Code Project Bootstrap")
        print("=" * 40)
        print(f"{Colors.END}")
    
    def interactive_setup(self) -> Dict:
        """Run interactive project setup"""
        config = {}
        
        # Project name
        default_name = self.project_root.name
        config['name'] = input(f"📝 Project name [{default_name}]: ").strip() or default_name
        
        # Project type
        print(f"\n📁 Project type:")
        project_types = [
            "Web API",
            "Data Pipeline", 
            "CLI Tool",
            "Web Application",
            "Library/Package",
            "Custom"
        ]
        
        for i, ptype in enumerate(project_types, 1):
            print(f"   {i}. {ptype}")
        
        while True:
            try:
                choice = int(input("Select project type [1]: ") or "1")
                if 1 <= choice <= len(project_types):
                    config['type'] = project_types[choice - 1]
                    break
            except ValueError:
                pass
            print(f"{Colors.RED}Invalid choice. Please enter 1-{len(project_types)}{Colors.END}")
        
        # Technology domains
        print(f"\n🔧 Technology domains:")
        print(f"   ✅ Git (included by default)")
        
        selected_domains = ["git"]
        
        for domain in self.available_domains[1:]:  # Skip git as it's mandatory
            response = input(f"   ❓ Add {domain.title()}? (y/n) [n]: ").strip().lower()
            if response in ['y', 'yes']:
                selected_domains.append(domain)
        
        config['domains'] = selected_domains
        
        # Project description
        config['description'] = input(f"\n🎯 Project description: ").strip()
        
        return config
    
    def fetch_file(self, path: str, destination: Path) -> bool:
        """Fetch a file from the repository"""
        url = f"{self.base_url}/{path}"
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(url, destination)
            return True
        except Exception as e:
            print(f"{Colors.RED}Failed to fetch {path}: {e}{Colors.END}")
            return False
    
    def fetch_domain_manifest(self, domain: str) -> Optional[Dict]:
        """Fetch domain manifest file"""
        manifest_path = f"domains/{domain}/manifest.json"
        try:
            url = f"{self.base_url}/{manifest_path}"
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"{Colors.RED}Failed to fetch manifest for {domain}: {e}{Colors.END}")
            return None
    
    def apply_domain(self, domain: str, config: Dict) -> bool:
        """Apply a domain configuration to the project"""
        print(f"   📦 Applying {domain} domain...")
        
        manifest = self.fetch_domain_manifest(domain)
        if not manifest:
            return False
        
        # Fetch files specified in manifest
        for dest_dir, files in manifest.get('files', {}).items():
            for file_name in files:
                source_path = f"domains/{domain}/{dest_dir}/{file_name}".replace('//', '/')
                dest_path = self.project_root / dest_dir / file_name
                
                if not self.fetch_file(source_path, dest_path):
                    print(f"{Colors.YELLOW}Warning: Could not fetch {file_name}{Colors.END}")
        
        return True
    
    def create_claude_md(self, config: Dict):
        """Create the CLAUDE.md file from template"""
        template_content = f"""# Claude Code Project Context

## Project Overview
**Name**: {config['name']}
**Type**: {config['type']}
**Description**: {config.get('description', 'A project following Claude Code best practices')}

## Technology Stack
**Domains**: {', '.join(config['domains'])}

## Development Principles
- Follow domain-specific best practices
- Use test-driven development (TDD)
- Maintain clean, documented code
- Infrastructure as Code where applicable

## Project Structure
This project uses modular Claude Code configuration with the following domains:
{chr(10).join(f'- **{domain.title()}**: Domain-specific tooling and practices' for domain in config['domains'])}

## Safety & Restrictions
- File operations allowed within project directory only
- Always prompt for configuration changes
- No destructive operations outside project scope
- All infrastructure changes through code, not CLI

## Next Steps
1. Review domain-specific documentation
2. Run project setup: `make setup` or equivalent
3. Start development with Claude Code
4. Check TODO.md for current tasks

## Memory Bank
This project uses memory bank: `project-{config['name'].lower().replace(' ', '-')}`
"""
        
        claude_md_path = self.project_root / "CLAUDE.md"
        claude_md_path.write_text(template_content)
        print(f"   ✅ Created CLAUDE.md")
    
    def create_gitignore(self, config: Dict):
        """Create .gitignore with Claude-specific entries"""
        gitignore_content = """# Claude Code specific
TODO.md
CLAUDE.local.md
.claude/logs/
.claude/session-history/

# OS
.DS_Store
.DS_Store?
._*
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
"""
        
        gitignore_path = self.project_root / ".gitignore"
        if not gitignore_path.exists():
            gitignore_path.write_text(gitignore_content)
            print(f"   ✅ Created .gitignore")
        else:
            # Append Claude-specific entries if not present
            existing = gitignore_path.read_text()
            if "# Claude Code specific" not in existing:
                gitignore_path.write_text(existing + "\n" + gitignore_content)
                print(f"   ✅ Updated .gitignore")
    
    def setup_project(self, config: Dict):
        """Set up the complete project structure"""
        print(f"\n🚀 Setting up project: {config['name']}")
        
        # Create base .claude directory
        claude_dir = self.project_root / ".claude"
        claude_dir.mkdir(exist_ok=True)
        
        # Fetch core configuration
        print("   📦 Fetching core configuration...")
        core_files = [
            "core/.claude/settings.json",
            "core/.claude/hooks/pre-tool-use-safety.py",
            "core/.claude/hooks/project-boundary.py",
            "core/.claude/commands/help.md"
        ]
        
        for file_path in core_files:
            dest_path = self.project_root / file_path.replace("core/", "")
            self.fetch_file(file_path, dest_path)
        
        # Apply domains
        print(f"   🔧 Applying domains: {', '.join(config['domains'])}")
        for domain in config['domains']:
            self.apply_domain(domain, config)
        
        # Create project files
        self.create_claude_md(config)
        self.create_gitignore(config)
        
        # Make hooks executable
        hooks_dir = claude_dir / "hooks"
        if hooks_dir.exists():
            for hook_file in hooks_dir.glob("*.py"):
                hook_file.chmod(0o755)
        
        print(f"{Colors.GREEN}✅ Project setup complete!{Colors.END}")
        self.print_next_steps(config)
    
    def print_next_steps(self, config: Dict):
        """Print next steps for the user"""
        print(f"\n{Colors.BOLD}🎯 Next Steps:{Colors.END}")
        print(f"1. Review CLAUDE.md for project context")
        print(f"2. Initialize git repository: {Colors.BLUE}git init{Colors.END}")
        print(f"3. Start Claude Code: {Colors.BLUE}claude{Colors.END}")
        
        if "python" in config['domains']:
            print(f"4. Set up Python environment: {Colors.BLUE}make setup{Colors.END}")
        
        if "aws" in config['domains']:
            print(f"5. Configure AWS credentials")
        
        print(f"\n{Colors.YELLOW}💡 Pro tip: Use 'claude \"/help\"' to see available commands{Colors.END}")


def main():
    parser = argparse.ArgumentParser(description="Bootstrap a new Claude Code project")
    parser.add_argument("--interactive", action="store_true", 
                       help="Run interactive setup")
    parser.add_argument("--name", help="Project name")
    parser.add_argument("--domains", help="Comma-separated list of domains")
    parser.add_argument("--type", help="Project type")
    parser.add_argument("--base-url", default="https://raw.githubusercontent.com/user/claude-project-best-practices/main",
                       help="Base URL for fetching configurations")
    
    args = parser.parse_args()
    
    bootstrap = ProjectBootstrap(args.base_url)
    bootstrap.print_banner()
    
    if args.interactive or not (args.name and args.domains):
        # Interactive mode
        config = bootstrap.interactive_setup()
    else:
        # Non-interactive mode
        config = {
            'name': args.name,
            'type': args.type or 'Custom',
            'domains': ['git'] + [d.strip() for d in args.domains.split(',') if d.strip() != 'git'],
            'description': f"A {args.type or 'custom'} project"
        }
    
    bootstrap.setup_project(config)


if __name__ == "__main__":
    main()