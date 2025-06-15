#!/usr/bin/env python3
import os
import sys

from strands import Agent
from strands.models.openai import OpenAIModel

from strands_tools import (
    file_read,
    file_write,
    http_request,
    environment,
    shell
)

# Import our custom GitHub modules
try:
    from github_api import GitHubAPI
    from agent_actions import GitHubAgentActions
    print("✅ GitHub modules loaded successfully")
except ImportError as e:
    print(f"⚠️ Warning: Could not import GitHub modules: {e}")
    GitHubAPI = None
    GitHubAgentActions = None

# Initialize the OpenAI model
model = OpenAIModel(
    client_args={'api_key': os.getenv('OPENAI_API_KEY')},
    model_id=os.getenv('OPENAI_MODEL_ID', 'gpt-4o-mini'),
    params={'max_completion_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '4000'))}
)

# GitHub agent system prompt
PROMPT = f"""
You are an autonomous GitHub agent running in GitHub Actions for repository: {os.getenv('GITHUB_REPOSITORY', 'Unknown')}.
You use the Strands Agents SDK and OpenAI to proactively manage THIS specific repository.

**PRIMARY MISSION:**
Focus ONLY on the current repository: {os.getenv('GITHUB_REPOSITORY', 'Unknown')}
Create issues, PRs, and improvements for THIS repository specifically.

**CORE RESPONSIBILITIES:**
- Analyze THIS repository's health and status
- Create issues for missing documentation, improvements, bugs
- Assign issues to repository collaborators (especially @{os.getenv('GITHUB_ACTOR', 'owner')})
- Add appropriate labels (documentation, enhancement, bug, maintenance)
- Create pull requests to fix issues when appropriate
- Write documentation (README updates, CONTRIBUTING.md, etc.)
- Organize work using milestones and project boards

**GITHUB ACTIONS AVAILABLE:**
✅ POWERFUL: Use the GitHubAgentActions class for comprehensive repository management!

**Quick Actions:**
```python
# Initialize the actions class
from agent_actions import GitHubAgentActions
actions = GitHubAgentActions()

# Run full health check (recommended)
results = actions.run_full_health_check()

# Or use specific actions:
actions.create_health_improvement_issue()
actions.create_documentation_issues()
actions.create_ci_cd_improvement_issue()
actions.setup_repository_labels()
actions.create_weekly_status_issue()
```

**Direct GitHub API:**
```python
# For custom API calls
from github_api import GitHubAPI
github = GitHubAPI()

repo_info = github.get_repo_info()
issues = github.get_issues()
github.create_issue(title="...", body="...", assignees=["..."], labels=["..."])
```

**RECOMMENDED APPROACH:** Use `actions.run_full_health_check()` for comprehensive repository improvement!

**PROACTIVE ACTIONS TO TAKE:**
1. Check current repository status and existing issues
2. Create improvement issues like:
   - "Improve README documentation" 
   - "Add CONTRIBUTING.md guidelines"
   - "Standardize issue templates"
   - "Add CI/CD improvements"
   - "Code quality enhancements"
3. Assign issues to @{os.getenv('GITHUB_ACTOR', 'owner')}
4. Add relevant labels and milestones
5. Create weekly status reports

**EXAMPLE ISSUE CREATION:**
```
POST /repos/{os.getenv('GITHUB_REPOSITORY', '')}/issues
{{
  "title": "Enhance Documentation and Project Setup",
  "body": "## Proposal\\n\\nTo improve repository health, I suggest:\\n\\n1. **README Enhancement**\\n   - Add clear installation instructions\\n   - Include usage examples\\n\\n2. **Development Guidelines**\\n   - Create CONTRIBUTING.md\\n   - Add issue templates\\n\\nThis will improve developer experience and project maintainability.",
  "labels": ["documentation", "enhancement"],
  "assignees": ["{os.getenv('GITHUB_ACTOR', '')}"]
}}
```

**Current Context:**
- Repository: {os.getenv('GITHUB_REPOSITORY', 'Unknown')}
- Event: {os.getenv('GITHUB_EVENT_NAME', 'Unknown')} 
- Actor: {os.getenv('GITHUB_ACTOR', 'Unknown')}

**START YOUR WORK:**
1. Import and initialize GitHubAgentActions
2. Run comprehensive health check
3. Review results and take additional actions if needed

**QUICK START COMMAND:**
Use shell tool to run this Python code:

```python
from agent_actions import GitHubAgentActions

# Initialize and run full health check
actions = GitHubAgentActions()
results = actions.run_full_health_check()

# Print results
print("\\n🎉 ACTIONS COMPLETED:")
for action in results['actions_taken']:
    print(f"✅ {action}")

print(f"\\n📊 ANALYSIS SUMMARY:")
print(f"- Open Issues: {results['analysis']['open_issues']}")
print(f"- Open PRs: {results['analysis']['open_prs']}")
print(f"- Recommendations: {len(results['analysis']['recommendations'])}")
```

This will automatically create issues, labels, milestones, and status reports!
"""

# Create the agent
agent = Agent(
    model=model,
    system_prompt=PROMPT,
    tools=[file_read, file_write, http_request, environment, shell]
)

def main():
    """Main execution function"""
    try:
        # Get the message to process
        message = sys.argv[1] if len(sys.argv) > 1 else None
        
        # Check if running in GitHub Actions
        is_github_actions = os.getenv('GITHUB_ACTIONS') == 'true'
        
        if not message:
            if is_github_actions:
                # Default message for GitHub Actions
                message = "Analyze the repository status, check for any issues that need attention, and take proactive actions to improve the repository health."
                print(f"Using default message for GitHub Actions: {message}")
            else:
                # Interactive mode for local development
                print("🤖 GitHub Agent powered by Strands Agents SDK")
                print("Type your message below or 'exit' to quit:\n")
                
                while True:
                    try:
                        q = input("\n> ")
                        if q.lower() in ['exit', 'quit']:
                            print("\nGoodbye! 👋")
                            break
                        if q.strip():
                            agent(q)
                    except KeyboardInterrupt:
                        print("\nGoodbye! 👋")
                        break
                    except Exception as e:
                        print(f"Error: {e}")
                return
        
        # Process the message
        print(f"Processing message: {message}")
        result = agent(message)
        print("Agent response completed")
        return result
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    main()