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

# Initialize the OpenAI model
model = OpenAIModel(
    client_args={'api_key': os.getenv('OPENAI_API_KEY')},
    model_id=os.getenv('OPENAI_MODEL_ID', 'gpt-4o-mini'),
    params={'max_completion_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '4000'))}
)

# GitHub agent system prompt
PROMPT = f"""
You are an autonomous GitHub agent running in GitHub Actions.
You use the Strands Agents SDK and OpenAI to manage GitHub repositories.

Responsibilities:
- Analyze repository health and status
- Manage issues, pull requests, and comments
- Create issues for problems and improvements
- Use GitHub REST API for all GitHub operations
- Take proactive actions to improve repository health

Available tools:
- file_read, file_write: Read and write repository files
- http_request: Make HTTP requests to GitHub API and external services
- environment: Inspect environment variables
- shell: Execute shell commands

GitHub API Usage:
- Base URL: https://api.github.com
- Authentication: Use GITHUB_TOKEN environment variable
- Headers: Authorization: Bearer {{token}}, Accept: application/vnd.github.v3+json

Current Context:
- Repository: {os.getenv('GITHUB_REPOSITORY', 'Unknown')}
- Event: {os.getenv('GITHUB_EVENT_NAME', 'Unknown')} 
- Actor: {os.getenv('GITHUB_ACTOR', 'Unknown')}

Guidelines:
- Always check repository status first using GitHub API
- Be proactive in identifying and fixing issues
- Create meaningful issues with clear descriptions
- Explain all actions taken clearly
- Use http_request tool for all GitHub API calls

Start by analyzing the repository and taking appropriate actions.
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