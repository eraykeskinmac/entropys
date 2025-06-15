#!/usr/bin/env python3
"""
GitHub Agent Setup Script
Bu script GitHub Agent'ı repository'nize kurmak için gerekli dosyaları oluşturur.

Usage:
    python setup.py                    # Tam kurulum
    python setup.py --quick           # Hızlı kurulum (sadana temel dosyalar)
    python setup.py --check          # Mevcut kurulumu kontrol et
    python setup.py --update         # Mevcut kurulumu güncelle
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

class Colors:
    """Terminal renkleri için ANSI kodları"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'
    
    @classmethod
    def disable(cls):
        """Renkleri devre dışı bırak (Windows uyumluluğu için)"""
        cls.RED = cls.GREEN = cls.YELLOW = cls.BLUE = ''
        cls.PURPLE = cls.CYAN = cls.WHITE = cls.BOLD = cls.END = ''

# Windows'da renkleri devre dışı bırak
if os.name == 'nt':
    Colors.disable()

def print_step(message: str, step_type: str = "info"):
    """Renkli step mesajları yazdır"""
    icons = {
        "info": "ℹ️",
        "success": "✅", 
        "warning": "⚠️",
        "error": "❌",
        "question": "❓"
    }
    colors = {
        "info": Colors.BLUE,
        "success": Colors.GREEN,
        "warning": Colors.YELLOW, 
        "error": Colors.RED,
        "question": Colors.CYAN
    }
    
    icon = icons.get(step_type, "📝")
    color = colors.get(step_type, Colors.WHITE)
    
    print(f"{color}{icon} {message}{Colors.END}")

def run_command(command: str, capture_output: bool = True) -> tuple:
    """Shell komutu çalıştır"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=capture_output, 
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def check_prerequisites() -> Dict[str, bool]:
    """Ön koşulları kontrol et"""
    checks = {}
    
    # Python version check
    python_version = sys.version_info
    checks['python'] = python_version >= (3, 10)
    
    # Git check
    success, _, _ = run_command("git --version")
    checks['git'] = success
    
    # pip check
    success, _, _ = run_command("pip --version")
    checks['pip'] = success
    
    # Repository check
    checks['git_repo'] = Path('.git').exists()
    
    # Internet connection check (basit)
    success, _, _ = run_command("ping -c 1 8.8.8.8", capture_output=True)
    checks['internet'] = success
    
    return checks

def validate_openai_key(api_key: str) -> bool:
    """OpenAI API key formatını kontrol et"""
    return api_key.startswith('sk-') and len(api_key) > 20

def check_existing_installation() -> Dict[str, bool]:
    """Mevcut kurulum durumunu kontrol et"""
    files_to_check = {
        'agent.py': Path('agent.py').exists(),
        'requirements.txt': Path('requirements.txt').exists(),
        'workflow': Path('.github/workflows/agent.yml').exists(),
        'gitignore': Path('.gitignore').exists(),
        'env_template': Path('.env.template').exists()
    }
    return files_to_check

def create_directory_structure():
    """Gerekli dizin yapısını oluştur"""
    directories = [
        '.github/workflows',
        'tools',
        'docs',
        'tests',
        '.vscode'
    ]
    
    created_dirs = []
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            created_dirs.append(directory)
    
    if created_dirs:
        print_step(f"Created directories: {', '.join(created_dirs)}", "success")
    
    return created_dirs

def create_agent_files():
    """Ana agent dosyalarını oluştur"""
    files_created = []

    
    # Create agent.py if it doesn't exist
    if not Path('agent.py').exists():
        agent_code = '''#!/usr/bin/env python3
"""
GitHub Agent using Strands Agents SDK
A powerful AI agent that manages GitHub repositories, issues, PRs, and projects.
"""

import os
import sys
import logging
from typing import Optional

from strands import Agent, tool
from strands.models.openai import OpenAIModel
from strands_tools import (
    file_read,
    file_write,
    http_request,
    environment,
    shell,
    current_time,
    python_repl
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_model():
    """Create and configure the AI model"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    return OpenAIModel(
        client_args={'api_key': api_key},
        model_id=os.getenv('OPENAI_MODEL_ID', 'gpt-4'),
        params={
            'max_completion_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '4000')),
            'temperature': 0.1
        }
    )

@tool
def use_github(query: str, variables: Optional[dict] = None) -> dict:
    """Execute GitHub GraphQL queries and mutations."""
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        return {"error": "GITHUB_TOKEN environment variable is required"}
    
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'query': query,
        'variables': variables or {}
    }
    
    try:
        response = http_request(
            method='POST',
            url='https://api.github.com/graphql',
            headers=headers,
            json=payload
        )
        return response
    except Exception as e:
        return {"error": f"GitHub API request failed: {str(e)}"}

@tool
def github_rest_api(endpoint: str, method: str = 'GET', data: Optional[dict] = None) -> dict:
    """Make GitHub REST API calls."""
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        return {"error": "GITHUB_TOKEN environment variable is required"}
    
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    url = f"https://api.github.com{endpoint}"
    
    try:
        if method.upper() in ['POST', 'PUT', 'PATCH'] and data:
            response = http_request(method=method, url=url, headers=headers, json=data)
        else:
            response = http_request(method=method, url=url, headers=headers)
        return response
    except Exception as e:
        return {"error": f"GitHub REST API request failed: {str(e)}"}

@tool
def manage_issue(action: str, issue_number: Optional[int] = None, **kwargs) -> dict:
    """Manage GitHub issues (create, update, close, comment)."""
    repository = os.getenv('GITHUB_REPOSITORY')
    if not repository:
        return {"error": "GITHUB_REPOSITORY environment variable is required"}
    
    if action == 'list':
        endpoint = f"/repos/{repository}/issues"
        return github_rest_api(endpoint)
    elif action == 'create':
        endpoint = f"/repos/{repository}/issues"
        data = {
            'title': kwargs.get('title', 'New Issue'),
            'body': kwargs.get('body', ''),
            'labels': kwargs.get('labels', []),
            'assignees': kwargs.get('assignees', [])
        }
        return github_rest_api(endpoint, 'POST', data)
    
    return {"error": "Invalid action or missing parameters"}

# System prompt
SYSTEM_PROMPT = """
You are an intelligent GitHub agent running in GitHub Actions.
You help manage repositories, issues, pull requests, and provide insights.
Use your tools wisely and always be helpful.
"""

def create_agent():
    """Create and configure the GitHub agent"""
    try:
        model = create_model()
        
        agent = Agent(
            model=model,
            system_prompt=SYSTEM_PROMPT,
            tools=[
                use_github,
                github_rest_api,
                manage_issue,
                file_read,
                file_write,
                shell,
                http_request,
                python_repl,
                current_time,
                environment
            ]
        )
        
        return agent
    except Exception as e:
        logger.error(f"Failed to create agent: {e}")
        raise

def main():
    """Main function to run the agent"""
    try:
        agent = create_agent()
        
        if len(sys.argv) > 1:
            message = ' '.join(sys.argv[1:])
        else:
            message = os.getenv('AGENT_MESSAGE', 'Hello! I am ready to help manage this GitHub repository.')
        
        logger.info(f"GitHub Agent starting with message: {message}")
        
        response = agent(message)
        
        logger.info("GitHub Agent completed successfully")
        print(f"\\nAgent Response:\\n{response.message}")
        
    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
'''
        
        with open('agent.py', 'w', encoding='utf-8') as f:
            f.write(agent_code)
        files_created.append('agent.py')
    
    # Create requirements.txt if it doesn't exist
    if not Path('requirements.txt').exists():
        requirements = '''# Strands Agents SDK and Tools
strands-agents>=0.1.0
strands-agents-tools>=0.1.0

# HTTP client for API interactions
requests>=2.28.0

# Additional utility libraries
colorama>=0.4.6
rich>=13.0.0
python-dateutil>=2.8.2
jsonschema>=4.0.0
python-dotenv>=1.0.0
GitPython>=3.1.0
markdown>=3.4.0
PyYAML>=6.0
'''
        
        with open('requirements.txt', 'w', encoding='utf-8') as f:
            f.write(requirements)
        files_created.append('requirements.txt')
    
    return files_created

def create_workflow_file():
    """GitHub Actions workflow dosyası oluştur"""
    workflow_path = Path('.github/workflows/agent.yml')
    
    if workflow_path.exists():
        return False
    
    workflow_content = '''name: GitHub Agent

on:
  issues:
    types: [opened, edited, closed, reopened, assigned, unassigned, labeled, unlabeled]
  issue_comment:
    types: [created, edited, deleted]
  pull_request:
    types: [opened, closed, edited, reopened, synchronize, ready_for_review]
  pull_request_review:
    types: [submitted, edited]
  pull_request_review_comment:
    types: [created, edited]
  workflow_dispatch:
    inputs:
      message:
        description: 'Message to pass to the agent'
        required: false
        default: 'What are my active pull requests and issues?'
        type: string

permissions:
  contents: write
  issues: write
  pull-requests: write
  actions: write
  discussions: write
  metadata: read

jobs:
  run-agent:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Cache Python dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}-strands-agents
          restore-keys: |
            ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}-
            ${{ runner.os }}-pip-
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install strands-agents strands-agents-tools
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
          fi
      
      - name: Configure Git
        run: |
          git config --global user.name "GitHub Agent"
          git config --global user.email "github-agent@users.noreply.github.com"
      
      - name: Prepare agent message
        id: prepare
        run: |
          EVENT_TYPE="${{ github.event_name }}"
          
          if [[ "$EVENT_TYPE" == "workflow_dispatch" ]]; then
            MESSAGE="${{ github.event.inputs.message }}"
            echo "AGENT_MESSAGE=$MESSAGE" >> $GITHUB_ENV
          else
            case "$EVENT_TYPE" in
              issues)
                if [[ "${{ github.event.action }}" == "opened" ]]; then
                  echo "AGENT_MESSAGE=New issue opened: #${{ github.event.issue.number }} '${{ github.event.issue.title }}' by @${{ github.event.issue.user.login }}. Please analyze and take appropriate action." >> $GITHUB_ENV
                else
                  echo "AGENT_MESSAGE=Issue #${{ github.event.issue.number }} was ${{ github.event.action }}. Please review and respond appropriately." >> $GITHUB_ENV
                fi
                ;;
              issue_comment)
                echo "AGENT_MESSAGE=New comment on issue #${{ github.event.issue.number }} by @${{ github.event.comment.user.login }}. Please review and respond if appropriate." >> $GITHUB_ENV
                ;;
              pull_request)
                if [[ "${{ github.event.action }}" == "opened" ]]; then
                  echo "AGENT_MESSAGE=New pull request opened: #${{ github.event.pull_request.number }} '${{ github.event.pull_request.title }}' by @${{ github.event.pull_request.user.login }}. Please review and provide feedback." >> $GITHUB_ENV
                else
                  echo "AGENT_MESSAGE=Pull request #${{ github.event.pull_request.number }} was ${{ github.event.action }}. Please review the changes." >> $GITHUB_ENV
                fi
                ;;
              *)
                echo "AGENT_MESSAGE=GitHub event '$EVENT_TYPE' triggered. Please analyze the situation and take appropriate action." >> $GITHUB_ENV
                ;;
            esac
          fi
      
      - name: Run GitHub Agent
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
          GITHUB_EVENT_NAME: ${{ github.event_name }}
          GITHUB_ACTOR: ${{ github.actor }}
          GITHUB_REF: ${{ github.ref }}
          GITHUB_SHA: ${{ github.sha }}
          GITHUB_WORKFLOW: ${{ github.workflow }}
          GITHUB_RUN_ID: ${{ github.run_id }}
          GITHUB_RUN_NUMBER: ${{ github.run_number }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          OPENAI_MODEL_ID: ${{ secrets.OPENAI_MODEL_ID || 'gpt-4' }}
          OPENAI_MAX_TOKENS: "4000"
          BYPASS_TOOL_CONSENT: "true"
          STRANDS_TOOL_CONSOLE_MODE: "enabled"
          AGENT_MESSAGE: ${{ env.AGENT_MESSAGE }}
        
        run: |
          echo "🤖 Starting GitHub Agent..."
          echo "Repository: $GITHUB_REPOSITORY"
          echo "Event: $GITHUB_EVENT_NAME"
          echo "Message: $AGENT_MESSAGE"
          echo ""
          
          python -u agent.py "$AGENT_MESSAGE"
      
      - name: Create workflow summary
        if: always()
        run: |
          echo "## 🤖 GitHub Agent Execution Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "- **Repository:** ${{ github.repository }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Event:** ${{ github.event_name }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Triggered by:** @${{ github.actor }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Timestamp:** $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          
          if [[ "${{ job.status }}" == "success" ]]; then
            echo "✅ **Status:** Completed successfully" >> $GITHUB_STEP_SUMMARY
          else
            echo "❌ **Status:** Failed or cancelled" >> $GITHUB_STEP_SUMMARY
          fi
'''
    
    with open(workflow_path, 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    
    return True

def interactive_setup():
    """Interaktif setup süreci"""
    print_step("GitHub Agent Interactive Setup", "info")
    print()
    
    # OpenAI API Key input
    while True:
        api_key = input(f"{Colors.CYAN}❓ OpenAI API Key'inizi girin (sk-... ile başlamalı): {Colors.END}").strip()
        if validate_openai_key(api_key):
            break
        print_step("Geçersiz API key formatı! 'sk-' ile başlamalı ve 20+ karakter olmalı.", "error")
    
    # Model selection
    models = ['gpt-4', 'gpt-3.5-turbo', 'gpt-4-turbo']
    print(f"{Colors.CYAN}❓ Kullanmak istediğiniz model:{Colors.END}")
    for i, model in enumerate(models, 1):
        print(f"   {i}. {model}")
    
    while True:
        try:
            choice = int(input("Seçiminiz (1-3): ").strip())
            if 1 <= choice <= len(models):
                selected_model = models[choice - 1]
                break
        except ValueError:
            pass
        print_step("Geçersiz seçim! 1-3 arası bir sayı girin.", "error")
    
    # Create .env file
    env_content = f"""# GitHub Agent Environment Variables
# Auto-generated by setup script

# OpenAI Configuration
OPENAI_API_KEY={api_key}
OPENAI_MODEL_ID={selected_model}
OPENAI_MAX_TOKENS=4000

# Strands Configuration
BYPASS_TOOL_CONSENT=true
STRANDS_TOOL_CONSOLE_MODE=enabled

# Development Settings
DEBUG=false
LOG_LEVEL=INFO
AGENT_LANGUAGE=tr
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print_step("Created .env file with your configuration", "success")
    return True

def print_next_steps():
    """Sonraki adımları göster"""
    print()
    print(f"{Colors.BOLD}{Colors.GREEN}🎉 GitHub Agent kurulumu tamamlandı!{Colors.END}")
    print()
    print(f"{Colors.BOLD}📋 Sonraki Adımlar:{Colors.END}")
    print()
    print("1. GitHub Repository Secrets ayarlayın:")
    print("   • Repository Settings → Secrets and variables → Actions")
    print("   • OPENAI_API_KEY secret'ını ekleyin")
    print()
    print("2. Workflow Permissions ayarlayın:")
    print("   • Repository Settings → Actions → General → Workflow permissions")
    print("   • 'Read and write permissions' seçin")
    print("   • 'Allow GitHub Actions to create and approve pull requests' seçin")
    print()
    print("3. Dosyaları commit edin:")
    print("   git add .")
    print("   git commit -m 'Add GitHub Agent with Strands SDK'")
    print("   git push")
    print()
    print("4. Test edin:")
    print("   • Actions sekmesi → GitHub Agent → Run workflow")
    print("   • Veya yeni bir issue/PR oluşturun")
    print()
    print(f"{Colors.YELLOW}⚠️  Önemli: .env dosyasını GitHub'a push etmeyin! (zaten .gitignore'da){Colors.END}")

def main():
    """Ana setup fonksiyonu"""
    parser = argparse.ArgumentParser(description='GitHub Agent Setup Script')
    parser.add_argument('--quick', action='store_true', help='Quick setup (basic files only)')
    parser.add_argument('--check', action='store_true', help='Check existing installation')
    parser.add_argument('--update', action='store_true', help='Update existing installation')
    parser.add_argument('--interactive', action='store_true', help='Interactive setup with prompts')
    
    args = parser.parse_args()
    
    print(f"{Colors.BOLD}{Colors.BLUE}🚀 GitHub Agent Setup Script{Colors.END}")
    print("=" * 50)
    
    # Check prerequisites
    print_step("Checking prerequisites...", "info")
    prereqs = check_prerequisites()
    
    failed_prereqs = [k for k, v in prereqs.items() if not v]
    if failed_prereqs:
        print_step(f"Missing prerequisites: {', '.join(failed_prereqs)}", "error")
        if 'python' in failed_prereqs:
            print_step("Python 3.10+ is required", "error")
        if 'git' in failed_prereqs:
            print_step("Git is required", "error")
        if 'pip' in failed_prereqs:
            print_step("pip is required", "error")
        sys.exit(1)
    else:
        print_step("All prerequisites met", "success")
    
    # Check existing installation
    if args.check:
        existing = check_existing_installation()
        print_step("Checking existing installation...", "info")
        for file, exists in existing.items():
            status = "✅" if exists else "❌"
            print(f"   {status} {file}")
        return
    
    # Warn if not in git repository
    if not prereqs['git_repo']:
        print_step("Warning: This doesn't appear to be a Git repository", "warning")
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response != 'y':
            print_step("Setup cancelled.", "info")
            sys.exit(0)
    
    try:
        # Create directory structure
        print_step("Creating directory structure...", "info")
        created_dirs = create_directory_structure()
        
        # Create main files
        print_step("Creating agent files...", "info")
        created_files = create_agent_files()
        
        # Create workflow
        print_step("Creating GitHub Actions workflow...", "info")
        workflow_created = create_workflow_file()
        if workflow_created:
            print_step("Created .github/workflows/agent.yml", "success")
        else:
            print_step("Workflow file already exists", "warning")
        
        # Create .gitignore and .env.template
        if not Path('.gitignore').exists():
            create_gitignore()
            print_step("Created .gitignore", "success")
        
        if not Path('.env.template').exists():
            create_env_template()
            print_step("Created .env.template", "success")
        
        # Interactive setup
        if args.interactive or (not args.quick and not args.update):
            response = input(f"{Colors.CYAN}❓ Do you want to configure environment variables interactively? (y/N): {Colors.END}").strip().lower()
            if response == 'y':
                interactive_setup()
        
        # Print summary
        if created_files:
            print_step(f"Created files: {', '.join(created_files)}", "success")
        
        # Print next steps
        print_next_steps()
        
    except KeyboardInterrupt:
        print_step("\nSetup interrupted by user", "warning")
        sys.exit(1)
    except Exception as e:
        print_step(f"Setup failed: {e}", "error")
        sys.exit(1)

if __name__ == "__main__":
    main()