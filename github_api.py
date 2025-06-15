#!/usr/bin/env python3
"""
GitHub API Helper Module
Handles all GitHub API interactions with proper authentication
"""

import os
import json
from typing import Dict, List, Optional, Any

def get_github_token() -> str:
    """Get GitHub token from environment"""
    token = os.getenv('GITHUB_TOKEN', '')
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not found")
    return token

def get_github_headers() -> Dict[str, str]:
    """Get properly formatted GitHub API headers with authentication"""
    token = get_github_token()
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "GitHub-Agent/1.0"
    }

def get_repository_info() -> str:
    """Get current repository from environment"""
    repo = os.getenv('GITHUB_REPOSITORY', '')
    if not repo:
        raise ValueError("GITHUB_REPOSITORY environment variable not found")
    return repo

def get_github_actor() -> str:
    """Get current GitHub actor (user who triggered the action)"""
    return os.getenv('GITHUB_ACTOR', 'owner')

class GitHubAPI:
    """GitHub API client with authentication and helper methods"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.repo = get_repository_info()
        self.actor = get_github_actor()
        self.headers = get_github_headers()
    
    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """Make authenticated GitHub API request"""
        from strands_tools import http_request
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        print(f"🔗 GitHub API: {method.upper()} {endpoint}")
        
        try:
            if method.upper() == "GET":
                return http_request(method="GET", url=url, headers=self.headers)
            elif method.upper() == "POST":
                return http_request(method="POST", url=url, headers=self.headers, data=data)
            elif method.upper() == "PATCH":
                return http_request(method="PATCH", url=url, headers=self.headers, data=data)
            elif method.upper() == "PUT":
                return http_request(method="PUT", url=url, headers=self.headers, data=data)
            elif method.upper() == "DELETE":
                return http_request(method="DELETE", url=url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        except Exception as e:
            print(f"❌ GitHub API Error: {e}")
            return None
    
    def get_repo_info(self) -> Optional[Dict]:
        """Get repository information"""
        return self.make_request("GET", f"repos/{self.repo}")
    
    def get_issues(self, state: str = "open") -> Optional[List[Dict]]:
        """Get repository issues"""
        return self.make_request("GET", f"repos/{self.repo}/issues?state={state}")
    
    def get_pull_requests(self, state: str = "open") -> Optional[List[Dict]]:
        """Get repository pull requests"""
        return self.make_request("GET", f"repos/{self.repo}/pulls?state={state}")
    
    def create_issue(self, title: str, body: str, assignees: Optional[List[str]] = None, 
                    labels: Optional[List[str]] = None, milestone: Optional[int] = None) -> Optional[Dict]:
        """Create a new issue"""
        issue_data = {
            "title": title,
            "body": body
        }
        
        if assignees:
            issue_data["assignees"] = assignees
        
        if labels:
            issue_data["labels"] = labels
            
        if milestone:
            issue_data["milestone"] = milestone
        
        print(f"📝 Creating issue: {title}")
        return self.make_request("POST", f"repos/{self.repo}/issues", issue_data)
    
    def update_issue(self, issue_number: int, title: Optional[str] = None, 
                    body: Optional[str] = None, state: Optional[str] = None,
                    assignees: Optional[List[str]] = None, labels: Optional[List[str]] = None) -> Optional[Dict]:
        """Update an existing issue"""
        update_data = {}
        
        if title:
            update_data["title"] = title
        if body:
            update_data["body"] = body
        if state:
            update_data["state"] = state
        if assignees:
            update_data["assignees"] = assignees
        if labels:
            update_data["labels"] = labels
        
        print(f"✏️ Updating issue #{issue_number}")
        return self.make_request("PATCH", f"repos/{self.repo}/issues/{issue_number}", update_data)
    
    def create_comment(self, issue_number: int, body: str) -> Optional[Dict]:
        """Add a comment to an issue"""
        comment_data = {"body": body}
        print(f"💬 Adding comment to issue #{issue_number}")
        return self.make_request("POST", f"repos/{self.repo}/issues/{issue_number}/comments", comment_data)
    
    def get_milestones(self) -> Optional[List[Dict]]:
        """Get repository milestones"""
        return self.make_request("GET", f"repos/{self.repo}/milestones")
    
    def create_milestone(self, title: str, description: Optional[str] = None, 
                        due_on: Optional[str] = None) -> Optional[Dict]:
        """Create a new milestone"""
        milestone_data = {"title": title}
        
        if description:
            milestone_data["description"] = description
        if due_on:
            milestone_data["due_on"] = due_on
        
        print(f"🎯 Creating milestone: {title}")
        return self.make_request("POST", f"repos/{self.repo}/milestones", milestone_data)
    
    def get_labels(self) -> Optional[List[Dict]]:
        """Get repository labels"""
        return self.make_request("GET", f"repos/{self.repo}/labels")
    
    def create_label(self, name: str, color: str, description: Optional[str] = None) -> Optional[Dict]:
        """Create a new label"""
        label_data = {
            "name": name,
            "color": color.lstrip('#')  # Remove # if present
        }
        
        if description:
            label_data["description"] = description
        
        print(f"🏷️ Creating label: {name}")
        return self.make_request("POST", f"repos/{self.repo}/labels", label_data)
    
    def get_collaborators(self) -> Optional[List[Dict]]:
        """Get repository collaborators"""
        return self.make_request("GET", f"repos/{self.repo}/collaborators")
    
    def get_repository_content(self, path: str = "") -> Optional[Dict]:
        """Get repository content"""
        return self.make_request("GET", f"repos/{self.repo}/contents/{path}")
    
    def create_or_update_file(self, path: str, message: str, content: str, 
                             sha: Optional[str] = None, branch: str = "main") -> Optional[Dict]:
        """Create or update a file in the repository"""
        import base64
        
        file_data = {
            "message": message,
            "content": base64.b64encode(content.encode()).decode(),
            "branch": branch
        }
        
        if sha:  # Update existing file
            file_data["sha"] = sha
        
        print(f"📄 {'Updating' if sha else 'Creating'} file: {path}")
        return self.make_request("PUT", f"repos/{self.repo}/contents/{path}", file_data) 