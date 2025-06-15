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

# Model configuration
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
        return {"error": f"GitHub API request failed: {str(e)}"}

@tool
def github_rest_api(endpoint: str, method: str = 'GET', data: Optional[dict] = None) -> dict:
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
        return {"error": f"GitHub REST API request failed: {str(e)}"}

@tool
def get_github_context() -> dict:
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
def dispatch_workflow(workflow_file: str, inputs: Optional[dict] = None) -> dict:
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

@tool
def manage_issue(action: str, issue_number: Optional[int] = None, **kwargs) -> dict:
    """
    Manage GitHub issues (create, update, close, comment).
    
    Args:
        action: Action to perform (create, update, close, comment, list)
        issue_number: Issue number (required for update, close, comment)
        **kwargs: Additional parameters based on action
    
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
def manage_pull_request(action: str, pr_number: Optional[int] = None, **kwargs) -> dict:
    """
    Manage GitHub pull requests.
    
    Args:
        action: Action to perform (list, create, update, merge, close, comment, review)
        pr_number: PR number (required for some actions)
        **kwargs: Additional parameters based on action
    
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
            'base': kwargs.get('base', 'main')
        }
        return github_rest_api(endpoint, 'POST', data)
    elif pr_number:
        if action == 'merge':
            endpoint = f"/repos/{repository}/pulls/{pr_number}/merge"
            data = {
                'commit_title': kwargs.get('commit_title', ''),
                'commit_message': kwargs.get('commit_message', ''),
                'merge_method': kwargs.get('merge_method', 'merge')
            }
            return github_rest_api(endpoint, 'PUT', data)
        elif action == 'comment':
            endpoint = f"/repos/{repository}/issues/{pr_number}/comments"
            data = {'body': kwargs.get('body', '')}
            return github_rest_api(endpoint, 'POST', data)
        elif action == 'review':
            endpoint = f"/repos/{repository}/pulls/{pr_number}/reviews"
            data = {
                'body': kwargs.get('body', ''),
                'event': kwargs.get('event', 'COMMENT')  # APPROVE, REQUEST_CHANGES, COMMENT
            }
            return github_rest_api(endpoint, 'POST', data)
    
    return {"error": f"Invalid action '{action}' or missing parameters"}

# System prompt for the GitHub agent
SYSTEM_PROMPT = f"""
You are an intelligent GitHub agent running in GitHub Actions with advanced repository management capabilities.

You use the Strands Agents SDK and have access to powerful tools for managing GitHub repositories.

## Your Responsibilities:
- Manage issues: create, update, close, comment, and organize
- Manage pull requests: review, merge, comment, and track
- Execute GitHub GraphQL and REST API operations
- Read and write repository files
- Execute shell commands for git operations
- Analyze code and provide insights
- Automate repository workflows
- Dispatch additional GitHub Actions workflows when needed

## Available Tools:
- use_github: Execute GitHub GraphQL queries and mutations
- github_rest_api: Make GitHub REST API calls
- get_github_context: Get current GitHub context and environment
- dispatch_workflow: Trigger other GitHub Actions workflows
- manage_issue: Comprehensive issue management
- manage_pull_request: Comprehensive PR management
- file_read, file_write: Repository file operations
- shell: Execute git and system commands
- http_request: Make external API calls
- python_repl: Execute Python code for analysis
- current_time: Get current timestamp
- environment: Check environment variables

## Guidelines:
- Always be helpful and proactive in repository management
- When handling events, understand the context and take appropriate actions
- Provide clear explanations of your actions
- Use git commands through shell tool for version control operations
- Be security-conscious with file operations and API calls
- Document your actions and decisions
- When in doubt, ask for clarification or provide multiple options

## Current Context:
Repository: {os.getenv('GITHUB_REPOSITORY', 'Not set')}
Event: {os.getenv('GITHUB_EVENT_NAME', 'Not set')}
Actor: {os.getenv('GITHUB_ACTOR', 'Not set')}
Workflow: {os.getenv('GITHUB_WORKFLOW', 'Not set')}

You are ready to help manage this repository efficiently and intelligently!
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
                get_github_context,
                dispatch_workflow,
                manage_issue,
                manage_pull_request,
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
        # Create the agent
        agent = create_agent()
        
        # Get the message from command line arguments or environment
        if len(sys.argv) > 1:
            message = ' '.join(sys.argv[1:])
        else:
            message = os.getenv('AGENT_MESSAGE', 'Hello! I am ready to help manage this GitHub repository.')
        
        logger.info(f"GitHub Agent starting with message: {message}")
        
        # Run the agent
        response = agent(message)
        
        logger.info("GitHub Agent completed successfully")
        print(f"\nAgent Response:\n{response.message}")
        
    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()