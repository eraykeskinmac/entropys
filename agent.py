#!/usr/bin/env python3
import os
import json
import logging
from typing import Optional, Dict, Any

from strands import Agent, tool
from strands.models.openai import OpenAIModel
from strands_tools import (
    file_read,
    file_write,
    http_request,
    environment,
    shell
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@tool
def use_github(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Execute GitHub GraphQL queries and mutations.
    
    Args:
        query: GraphQL query or mutation string
        variables: Optional variables for the query
    
    Returns:
        dict: Response from GitHub API
    """
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
        logger.error(f"GitHub GraphQL API error: {e}")
        return {"error": f"GitHub API request failed: {str(e)}"}

@tool
def github_rest_api(endpoint: str, method: str = 'GET', data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Make GitHub REST API calls.
    
    Args:
        endpoint: API endpoint (e.g., '/repos/owner/repo/issues')
        method: HTTP method (GET, POST, PUT, PATCH, DELETE)
        data: Request payload for POST/PUT/PATCH requests
    
    Returns:
        dict: Response from GitHub REST API
    """
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
        logger.error(f"GitHub REST API error: {e}")
        return {"error": f"GitHub REST API request failed: {str(e)}"}

@tool
def get_github_context() -> Dict[str, str]:
    """
    Get current GitHub context from environment variables.
    
    Returns:
        dict: GitHub context information
    """
    return {
        'repository': os.getenv('GITHUB_REPOSITORY', ''),
        'event_name': os.getenv('GITHUB_EVENT_NAME', ''),
        'actor': os.getenv('GITHUB_ACTOR', ''),
        'ref': os.getenv('GITHUB_REF', ''),
        'sha': os.getenv('GITHUB_SHA', ''),
        'workflow': os.getenv('GITHUB_WORKFLOW', ''),
        'run_id': os.getenv('GITHUB_RUN_ID', ''),
        'run_number': os.getenv('GITHUB_RUN_NUMBER', '')
    }

@tool
def manage_issue(action: str, issue_number: Optional[int] = None, **kwargs) -> Dict[str, Any]:
    """
    Manage GitHub issues (create, update, close, comment, list).
    
    Args:
        action: Action to perform (create, update, close, comment, list)
        issue_number: Issue number (required for update, close, comment)
        **kwargs: Additional parameters (title, body, labels, assignees)
    
    Returns:
        dict: Response from issue management
    """
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
    elif action in ['update', 'close'] and issue_number:
        endpoint = f"/repos/{repository}/issues/{issue_number}"
        data = {}
        if action == 'close':
            data['state'] = 'closed'
        data.update({k: v for k, v in kwargs.items() if k in ['title', 'body', 'labels', 'assignees']})
        return github_rest_api(endpoint, 'PATCH', data)
    elif action == 'comment' and issue_number:
        endpoint = f"/repos/{repository}/issues/{issue_number}/comments"
        data = {'body': kwargs.get('body', '')}
        return github_rest_api(endpoint, 'POST', data)
    else:
        return {"error": f"Invalid action '{action}' or missing parameters"}

@tool
def manage_pull_request(action: str, pr_number: Optional[int] = None, **kwargs) -> Dict[str, Any]:
    """
    Manage GitHub pull requests (create, update, close, merge, comment, list).
    
    Args:
        action: Action to perform (create, update, close, merge, comment, list)
        pr_number: Pull request number (required for update, close, merge, comment)
        **kwargs: Additional parameters
    
    Returns:
        dict: Response from PR management
    """
    repository = os.getenv('GITHUB_REPOSITORY')
    if not repository:
        return {"error": "GITHUB_REPOSITORY environment variable is required"}
    
    if action == 'list':
        endpoint = f"/repos/{repository}/pulls"
        return github_rest_api(endpoint)
    elif action == 'create':
        endpoint = f"/repos/{repository}/pulls"
        data = {
            'title': kwargs.get('title', 'New Pull Request'),
            'body': kwargs.get('body', ''),
            'head': kwargs.get('head', ''),
            'base': kwargs.get('base', 'main'),
            'draft': kwargs.get('draft', False)
        }
        return github_rest_api(endpoint, 'POST', data)
    elif action in ['update', 'close'] and pr_number:
        endpoint = f"/repos/{repository}/pulls/{pr_number}"
        data = {}
        if action == 'close':
            data['state'] = 'closed'
        data.update({k: v for k, v in kwargs.items() if k in ['title', 'body', 'base']})
        return github_rest_api(endpoint, 'PATCH', data)
    elif action == 'merge' and pr_number:
        endpoint = f"/repos/{repository}/pulls/{pr_number}/merge"
        data = {
            'commit_title': kwargs.get('commit_title', ''),
            'commit_message': kwargs.get('commit_message', ''),
            'merge_method': kwargs.get('merge_method', 'merge')
        }
        return github_rest_api(endpoint, 'PUT', data)
    elif action == 'comment' and pr_number:
        endpoint = f"/repos/{repository}/issues/{pr_number}/comments"
        data = {'body': kwargs.get('body', '')}
        return github_rest_api(endpoint, 'POST', data)
    else:
        return {"error": f"Invalid action '{action}' or missing parameters"}

@tool
def analyze_repository_health() -> Dict[str, Any]:
    """
    Analyze repository health and identify areas for improvement.
    
    Returns:
        dict: Analysis results with recommendations
    """
    context = get_github_context()
    repository = context.get('repository', '')
    
    if not repository:
        return {"error": "Repository context not available"}
    
    analysis = {
        "issues_analysis": github_rest_api(f"/repos/{repository}/issues?state=open"),
        "pulls_analysis": github_rest_api(f"/repos/{repository}/pulls?state=open"),
        "recent_commits": github_rest_api(f"/repos/{repository}/commits?per_page=10"),
        "repository_info": github_rest_api(f"/repos/{repository}")
    }
    
    return analysis

@tool
def create_maintenance_issue(title: str, body: str, labels: Optional[list] = None) -> Dict[str, Any]:
    """
    Create a maintenance or improvement issue.
    
    Args:
        title: Issue title
        body: Issue description
        labels: Optional labels (defaults to ['maintenance'])
    
    Returns:
        dict: Created issue response
    """
    if not labels:
        labels = ['maintenance']
    
    return manage_issue('create', title=title, body=body, labels=labels)

@tool
def dispatch_workflow(workflow_file: str, inputs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Dispatch a GitHub Actions workflow.
    
    Args:
        workflow_file: Workflow filename (e.g., 'agent.yml')
        inputs: Optional inputs for the workflow
    
    Returns:
        dict: Response from workflow dispatch
    """
    repository = os.getenv('GITHUB_REPOSITORY')
    if not repository:
        return {"error": "GITHUB_REPOSITORY environment variable is required"}
    
    endpoint = f"/repos/{repository}/actions/workflows/{workflow_file}/dispatches"
    data = {
        'ref': 'main',
        'inputs': inputs or {}
    }
    
    return github_rest_api(endpoint, 'POST', data)

def create_model():
    """Create and configure the AI model"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    model_id = os.getenv('OPENAI_MODEL_ID', 'gpt-4o-mini')
    max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '32000'))
    
    return OpenAIModel(
        client_args={'api_key': api_key},
        model_id=model_id,
        params={
            'max_completion_tokens': max_tokens,
            'temperature': 0.1
        }
    )

# System prompt focused on GitHub operations
SYSTEM_PROMPT = """
You are an autonomous GitHub agent powered by Strands Agents SDK and OpenAI.

**CORE RESPONSIBILITIES:**
- Manage GitHub issues: create, update, close, comment, label
- Manage pull requests: create, update, merge, close, review
- Manage GitHub Projects V2: add items, update fields, move through workflows
- Manage GitHub Discussions: create, respond, classify threads
- Handle GitHub Actions workflows and dispatch new ones
- Update repository files, documentation, and maintain code quality
- Work with branches, commits, and repository management

**AVAILABLE TOOLS:**
- use_github: Execute GraphQL queries for advanced GitHub operations
- github_rest_api: Make REST API calls to GitHub
- manage_issue: Handle issue operations (create/update/close/comment/list)
- manage_pull_request: Handle PR operations (create/update/merge/close/comment/list)
- dispatch_workflow: Trigger GitHub Actions workflows
- get_github_context: Get current GitHub environment context
- analyze_repository_health: Analyze repo health and identify improvement areas
- create_maintenance_issue: Create maintenance/improvement issues
- file_read/file_write: Read and write repository files
- environment: Access environment variables
- shell: Execute shell commands when needed

**OPERATIONAL GUIDELINES:**
1. Always check the GitHub context first to understand the current situation
2. Be PROACTIVE - actively look for ways to improve the repository
3. Analyze repository health: check for stale issues, outdated dependencies, missing documentation
4. Create issues for problems you identify (bugs, improvements, maintenance tasks)
5. Create pull requests to fix issues when appropriate
6. For complex operations, use GraphQL queries via use_github tool
7. For simple operations, use the specialized management tools  
8. When working with files, create feature branches for changes
9. Document all significant changes and decisions
10. Follow GitHub best practices for collaboration
11. Take initiative - don't just respond, actively maintain and improve the repository

**CURRENT CONTEXT:**
- Repository: {repository}
- Event: {event_name}
- Actor: {actor}
- Workflow: {workflow}

Start by understanding the current GitHub context and the task at hand.
""".format(
    repository=os.getenv('GITHUB_REPOSITORY', 'Unknown'),
    event_name=os.getenv('GITHUB_EVENT_NAME', 'Unknown'),
    actor=os.getenv('GITHUB_ACTOR', 'Unknown'),
    workflow=os.getenv('GITHUB_WORKFLOW', 'Unknown')
)

def create_agent():
    """Create the GitHub agent with all necessary tools"""
    model = create_model()
    
    tools = [
        use_github,
        github_rest_api,
        manage_issue,
        manage_pull_request,
        dispatch_workflow,
        get_github_context,
        analyze_repository_health,
        create_maintenance_issue,
        file_read,
        file_write,
        environment,
        shell
    ]
    
    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=tools
    )

def main():
    """Main execution function"""
    try:
        # Create the agent
        agent = create_agent()
        
        # Get the message to process
        message = sys.argv[1] if len(sys.argv) > 1 else None
        
        # Check if running in GitHub Actions (non-interactive environment)
        is_github_actions = os.getenv('GITHUB_ACTIONS') == 'true'
        
        if not message:
            if is_github_actions:
                # Default message for GitHub Actions when no message provided
                message = "Analyze the repository status, check for any issues that need attention, and take proactive actions to improve the repository health."
                logger.info(f"Using default message for GitHub Actions: {message}")
            else:
                # Interactive mode (only for local development)
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
                        logger.error(f"Error processing query: {e}")
                        print(f"Error: {e}")
                return
        
        # Single message mode (for GitHub Actions or direct message)
        logger.info(f"Processing message: {message}")
        result = agent(message)
        logger.info(f"Agent response completed")
        return result
            
    except Exception as e:
        logger.error(f"Failed to initialize or run agent: {e}")
        print(f"Error: {e}")
        return None

# Create global agent instance for import usage
agent = create_agent()

if __name__ == '__main__':
    import sys
    main()