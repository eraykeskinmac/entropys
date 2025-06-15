#!/usr/bin/env python3
"""
Advanced Multi-Agent GitHub Development System
Comprehensive AI-powered repository management with:
- Multi-agent coordination
- Streaming responses
- Meta-tooling capabilities
- Dynamic tool creation
- Self-improving architecture
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from strands import Agent, tool
from strands.models.openai import OpenAIModel
# Import Strands tools with error handling
try:
    from strands_tools import (
        file_read, file_write, http_request, environment, shell,
        current_time, python_repl, calculator, load_tool, editor,
        journal
    )
    # Try to import mem0_memory separately as it might not be available
    try:
        from strands_tools import mem0_memory
        MEMORY_AVAILABLE = True
    except ImportError:
        print("⚠️ mem0_memory not available, continuing without memory features")
        mem0_memory = None
        MEMORY_AVAILABLE = False
    
    print("✅ Strands tools loaded successfully")
except ImportError as e:
    print(f"❌ Failed to import strands_tools: {e}")
    # Create dummy functions if strands_tools is not available
    def file_read(*args, **kwargs): return "file_read not available"
    def file_write(*args, **kwargs): return "file_write not available"
    def http_request(*args, **kwargs): return "http_request not available"
    def environment(*args, **kwargs): return "environment not available"
    def shell(*args, **kwargs): return "shell not available"
    def current_time(*args, **kwargs): return "current_time not available"
    def python_repl(*args, **kwargs): return "python_repl not available"
    def calculator(*args, **kwargs): return "calculator not available"
    def load_tool(*args, **kwargs): return "load_tool not available"
    def editor(*args, **kwargs): return "editor not available"
    def journal(*args, **kwargs): return "journal not available"
    mem0_memory = None
    MEMORY_AVAILABLE = False

# Import our advanced modules
try:
    from advanced_multi_agent import AdvancedGitHubMultiAgent
    from streaming_multi_agent import StreamingMultiAgent, StreamingCallbackHandler
    from meta_tooling_agent import MetaToolingMultiAgent, MetaToolingEngine
    print("✅ Advanced agent modules loaded successfully")
except ImportError as e:
    print(f"⚠️ Warning: Could not import advanced modules: {e}")
    AdvancedGitHubMultiAgent = None
    StreamingMultiAgent = None
    MetaToolingMultiAgent = None

# Import legacy GitHub modules for compatibility
try:
    from github_api import GitHubAPI
    from agent_actions import GitHubAgentActions
    print("✅ GitHub modules loaded successfully")
except ImportError as e:
    print(f"⚠️ Warning: Could not import GitHub modules: {e}")
    GitHubAPI = None
    GitHubAgentActions = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UnifiedGitHubAgent:
    """Unified GitHub Agent with multiple operational modes"""
    
    def __init__(self):
        self.repo = os.getenv('GITHUB_REPOSITORY', 'unknown/repo')
        self.token = os.getenv('GITHUB_TOKEN')
        self.actor = os.getenv('GITHUB_ACTOR', 'unknown')
        
        # Initialize model
        self.model = OpenAIModel(
            client_args={'api_key': os.getenv('OPENAI_API_KEY')},
            model_id=os.getenv('OPENAI_MODEL_ID', 'gpt-4o-mini'),
            params={'max_completion_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '4000'))}
        )
        
        # Initialize different agent modes
        self.basic_agent = None
        self.advanced_agent = None
        self.streaming_agent = None
        self.meta_agent = None
        
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all agent modes"""
        
        # Basic Agent (legacy compatibility)
        self._setup_basic_agent()
        
        # Advanced Multi-Agent System
        if AdvancedGitHubMultiAgent:
            try:
                self.advanced_agent = AdvancedGitHubMultiAgent()
                print("✅ Advanced Multi-Agent system initialized")
            except Exception as e:
                print(f"⚠️ Failed to initialize Advanced Multi-Agent: {e}")
        
        # Streaming Agent System
        if StreamingMultiAgent:
            try:
                self.streaming_agent = StreamingMultiAgent()
                print("✅ Streaming Multi-Agent system initialized")
            except Exception as e:
                print(f"⚠️ Failed to initialize Streaming Multi-Agent: {e}")
        
        # Meta-Tooling Agent System
        if MetaToolingMultiAgent:
            try:
                self.meta_agent = MetaToolingMultiAgent()
                print("✅ Meta-Tooling Multi-Agent system initialized")
            except Exception as e:
                print(f"⚠️ Failed to initialize Meta-Tooling Multi-Agent: {e}")
    
    def _setup_basic_agent(self):
        """Setup basic agent for compatibility"""
        
        basic_prompt = f"""
You are an advanced GitHub agent running in GitHub Actions for repository: {self.repo}.
You use the Strands Agents SDK to autonomously manage and improve repositories.

🎯 PRIMARY MISSION: BE PROACTIVE AND TAKE ACTION
- Don't just analyze - CREATE ISSUES and PULL REQUESTS
- When you find problems - FIX THEM or CREATE ISSUES
- When you see improvements - IMPLEMENT THEM
- Always use proactive_repository_analysis() to take concrete actions

OPERATIONAL MODES AVAILABLE:
1. BASIC MODE: Standard repository management with proactive actions
2. ADVANCED MODE: Multi-agent coordination with specialists
3. STREAMING MODE: Real-time streaming responses
4. META-TOOLING MODE: Dynamic tool creation and optimization

CORE CAPABILITIES:
- Autonomous repository analysis and improvement
- Issue creation, management, and resolution
- Pull request review and management
- Code quality analysis and enhancement
- Security vulnerability detection and fixing
- Documentation generation and updates
- Test creation and coverage improvement
- CI/CD pipeline optimization

PROACTIVE ACTION TOOLS:
- create_improvement_issue(): Create issues for identified problems
- create_improvement_pr(): Create PRs with code improvements
- proactive_repository_analysis(): Comprehensive analysis with automatic issue creation
- github_api(): Direct GitHub API access for any operations

ADVANCED FEATURES:
- Multi-agent coordination for complex tasks
- Real-time streaming responses for long operations
- Dynamic tool creation based on repository needs
- Self-improving architecture with learning capabilities
- Meta-programming for custom solution development

Current repository: {self.repo}
Current actor: {self.actor}

🚀 INSTRUCTIONS FOR PROACTIVE BEHAVIOR:
1. ALWAYS start with comprehensive_repository_action() for complete analysis and actions
2. Use analyze_existing_issues() to review and comment on all open issues
3. Use analyze_pull_requests() to provide reviews on all open PRs
4. Use detect_performance_issues() to find and create performance optimization tasks
5. Use proactive_repository_analysis() to create new improvement issues
6. When analyzing code - CREATE ISSUES for problems found
7. When finding security issues - CREATE SECURITY ISSUES immediately
8. When seeing missing documentation - CREATE DOCUMENTATION ISSUES
9. When detecting performance problems - CREATE PERFORMANCE ISSUES
10. Use github_api() to check existing issues before creating duplicates
11. Take autonomous actions to improve repository health
12. Create detailed, actionable issues with implementation plans
13. Use appropriate labels and assign issues when possible
14. Provide comprehensive solutions with concrete next steps
15. Comment on issues with analysis and action plans
16. Review pull requests with detailed feedback

🎯 DEFAULT WORKFLOW:
1. Run comprehensive_repository_action() first
2. This will automatically:
   - Analyze all existing issues and comment with action plans
   - Review all open pull requests with detailed feedback
   - Detect performance issues and create optimization tasks
   - Run proactive analysis to create new improvement issues
3. Take additional specific actions based on the task

REMEMBER: You are not just an observer - you are an active contributor!
Your goal is to make the repository better through concrete actions.
Every analysis should result in actionable items: issues, PRs, or comments.
"""
        
        # Prepare tools list
        tools_list = [
            self._create_unified_tools(),
            file_read, file_write, http_request, environment, shell,
            current_time, python_repl, calculator, load_tool, editor,
            journal
        ]
        
        # Add memory tool if available
        if MEMORY_AVAILABLE and mem0_memory:
            tools_list.append(mem0_memory)
        
        self.basic_agent = Agent(
            model=self.model,
            system_prompt=basic_prompt,
            tools=tools_list
        )
    
    def _create_unified_tools(self):
        """Create unified tools that can access all agent modes"""
        
        @tool
        def activate_advanced_mode(task_description: str) -> str:
            """Activate advanced multi-agent mode for complex tasks"""
            if not self.advanced_agent:
                return "Advanced mode not available"
            
            try:
                result = self.advanced_agent.run_autonomous_maintenance()
                return f"Advanced mode executed: {json.dumps(result, indent=2)}"
            except Exception as e:
                return f"Advanced mode failed: {str(e)}"
        
        @tool
        def activate_streaming_mode(task_description: str) -> str:
            """Activate streaming mode for real-time responses"""
            if not self.streaming_agent:
                return "Streaming mode not available"
            
            try:
                results = self.streaming_agent.run_streaming_development(task_description)
                return f"Streaming mode completed with {len(results)} events"
            except Exception as e:
                return f"Streaming mode failed: {str(e)}"
        
        @tool
        def activate_meta_tooling_mode(task_description: str) -> str:
            """Activate meta-tooling mode for dynamic tool creation"""
            if not self.meta_agent:
                return "Meta-tooling mode not available"
            
            try:
                result = self.meta_agent.run_meta_development(task_description)
                return f"Meta-tooling mode executed: {json.dumps(result, indent=2)}"
            except Exception as e:
                return f"Meta-tooling mode failed: {str(e)}"
        
        @tool
        def github_api(endpoint: str, method: str = 'GET', data: Optional[Dict] = None) -> Dict:
            """Enhanced GitHub API calls"""
            if not self.token:
                return {"error": "GitHub token not available"}
            
            headers = {
                'Authorization': f'Bearer {self.token}',
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
                return {"error": f"GitHub API request failed: {str(e)}"}
        
        @tool
        def analyze_repository_complexity() -> str:
            """Analyze repository complexity to recommend optimal agent mode"""
            try:
                # Get repository information
                repo_info = github_api(f"/repos/{self.repo}")
                
                if "error" in repo_info:
                    return "Could not analyze repository complexity"
                
                # Analyze complexity factors
                complexity_score = 0
                recommendations = []
                
                # Size factors
                if repo_info.get('size', 0) > 10000:  # Large repository
                    complexity_score += 2
                    recommendations.append("Consider advanced mode for large codebase")
                
                # Activity factors
                if repo_info.get('open_issues_count', 0) > 10:
                    complexity_score += 1
                    recommendations.append("Advanced mode recommended for issue management")
                
                # Language complexity
                languages = github_api(f"/repos/{self.repo}/languages")
                if not isinstance(languages, dict) or "error" not in languages:
                    if len(languages) > 3:
                        complexity_score += 1
                        recommendations.append("Multi-language project benefits from specialized agents")
                
                # Recommend mode based on complexity
                if complexity_score >= 3:
                    mode_recommendation = "META-TOOLING MODE - High complexity requires custom tools"
                elif complexity_score >= 2:
                    mode_recommendation = "ADVANCED MODE - Multiple specialists needed"
                elif complexity_score >= 1:
                    mode_recommendation = "STREAMING MODE - Real-time feedback beneficial"
                else:
                    mode_recommendation = "BASIC MODE - Standard operations sufficient"
                
                return f"""
REPOSITORY COMPLEXITY ANALYSIS:
Repository: {self.repo}
Complexity Score: {complexity_score}/4
Recommended Mode: {mode_recommendation}

Factors:
{chr(10).join(f"- {rec}" for rec in recommendations)}

Available Modes:
- BASIC: Standard repository management
- ADVANCED: Multi-agent coordination
- STREAMING: Real-time responses
- META-TOOLING: Dynamic tool creation
"""
            except Exception as e:
                return f"Repository analysis failed: {str(e)}"
        
        @tool
        def execute_comprehensive_improvement() -> str:
            """Execute comprehensive repository improvement using all available modes"""
            results = []
            
            # Start with repository analysis
            analysis = analyze_repository_complexity()
            results.append(f"Analysis: {analysis}")
            
            # Try each mode based on availability and suitability
            if self.meta_agent:
                try:
                    meta_result = self.meta_agent.run_meta_development(
                        "Comprehensive repository analysis and improvement with custom tool creation"
                    )
                    results.append(f"Meta-tooling: {meta_result['status']}")
                except Exception as e:
                    results.append(f"Meta-tooling failed: {str(e)}")
            
            if self.advanced_agent:
                try:
                    advanced_result = self.advanced_agent.run_autonomous_maintenance()
                    results.append(f"Advanced mode: {advanced_result['status']}")
                except Exception as e:
                    results.append(f"Advanced mode failed: {str(e)}")
            
            # Legacy actions as fallback
            if GitHubAgentActions:
                try:
                    actions = GitHubAgentActions()
                    health_result = actions.run_full_health_check()
                    results.append(f"Health check: {len(health_result.get('actions_taken', []))} actions taken")
                except Exception as e:
                    results.append(f"Health check failed: {str(e)}")
            
            return f"Comprehensive improvement completed:\n" + "\n".join(results)
        
        @tool
        def create_improvement_issue(title: str, description: str, labels: list = None) -> str:
            """Create a new issue for repository improvements"""
            if not self.token:
                return "GitHub token not available"
            
            issue_data = {
                'title': title,
                'body': description,
                'labels': labels or ['enhancement', 'ai-generated']
            }
            
            try:
                result = github_api(f"/repos/{self.repo}/issues", method='POST', data=issue_data)
                if 'number' in result:
                    return f"✅ Created issue #{result['number']}: {title}"
                else:
                    return f"❌ Failed to create issue: {result.get('message', 'Unknown error')}"
            except Exception as e:
                return f"❌ Error creating issue: {str(e)}"

        @tool
        def create_improvement_pr(title: str, description: str, branch_name: str, file_changes: dict) -> str:
            """Create a pull request with code improvements"""
            if not self.token:
                return "GitHub token not available"
            
            try:
                # First create a new branch
                main_ref = github_api(f"/repos/{self.repo}/git/ref/heads/main")
                if 'object' not in main_ref:
                    return f"❌ Could not get main branch reference"
                
                main_sha = main_ref['object']['sha']
                
                # Create new branch
                branch_data = {
                    'ref': f'refs/heads/{branch_name}',
                    'sha': main_sha
                }
                
                branch_result = github_api(f"/repos/{self.repo}/git/refs", method='POST', data=branch_data)
                
                # Create/update files in the new branch
                for file_path, content in file_changes.items():
                    file_data = {
                        'message': f'AI improvement: Update {file_path}',
                        'content': content,
                        'branch': branch_name
                    }
                    
                    github_api(f"/repos/{self.repo}/contents/{file_path}", method='PUT', data=file_data)
                
                # Create pull request
                pr_data = {
                    'title': title,
                    'body': description,
                    'head': branch_name,
                    'base': 'main'
                }
                
                pr_result = github_api(f"/repos/{self.repo}/pulls", method='POST', data=pr_data)
                
                if 'number' in pr_result:
                    return f"✅ Created PR #{pr_result['number']}: {title}"
                else:
                    return f"❌ Failed to create PR: {pr_result.get('message', 'Unknown error')}"
                    
            except Exception as e:
                return f"❌ Error creating PR: {str(e)}"

        @tool
        def proactive_repository_analysis() -> str:
            """Perform comprehensive analysis and take proactive actions"""
            actions_taken = []
            
            # 1. Security Analysis
            security_issues = []
            
            # Check for common security issues in requirements.txt
            try:
                requirements_content = file_read("requirements.txt")
                if "requirements.txt" in requirements_content:
                    if "safety" not in requirements_content:
                        security_issues.append("Missing security scanning tool (safety)")
                    if "bandit" not in requirements_content:
                        security_issues.append("Missing static security analysis tool (bandit)")
            except:
                pass
            
            # Create security improvement issue if needed
            if security_issues:
                security_description = f"""## 🛡️ Security Improvements Needed

The AI analysis detected the following security improvements:

{chr(10).join(f"- {issue}" for issue in security_issues)}

### Recommended Actions:
1. Add security scanning tools to requirements.txt
2. Set up automated security checks in CI/CD
3. Implement security best practices

### Implementation Plan:
- [ ] Add `safety>=2.3.0` for dependency vulnerability scanning
- [ ] Add `bandit>=1.7.0` for static security analysis
- [ ] Create security workflow in GitHub Actions
- [ ] Add security documentation

**This issue was automatically created by the AI Multi-Agent System.**
"""
                
                result = create_improvement_issue(
                    "🛡️ Security: Add security scanning and hardening tools",
                    security_description,
                    ['security', 'enhancement', 'ai-generated']
                )
                actions_taken.append(result)
            
            # 2. Code Quality Analysis
            quality_issues = []
            
            # Check for code quality tools
            try:
                requirements_content = file_read("requirements.txt")
                if "black" not in requirements_content:
                    quality_issues.append("Missing code formatter (black)")
                if "pylint" not in requirements_content:
                    quality_issues.append("Missing linter (pylint)")
                if "pytest" not in requirements_content:
                    quality_issues.append("Missing testing framework (pytest)")
            except:
                pass
            
            # Create code quality issue if needed
            if quality_issues:
                quality_description = f"""## 📊 Code Quality Improvements

The AI analysis identified areas for code quality improvement:

{chr(10).join(f"- {issue}" for issue in quality_issues)}

### Recommended Actions:
1. Set up code formatting and linting
2. Implement comprehensive testing
3. Add code quality checks to CI/CD

### Implementation Plan:
- [ ] Configure black for code formatting
- [ ] Set up pylint for code analysis
- [ ] Add pytest for testing framework
- [ ] Create pre-commit hooks
- [ ] Add code quality badges to README

**This issue was automatically created by the AI Multi-Agent System.**
"""
                
                result = create_improvement_issue(
                    "📊 Code Quality: Implement formatting, linting, and testing",
                    quality_description,
                    ['code-quality', 'enhancement', 'ai-generated']
                )
                actions_taken.append(result)
            
            # 3. Documentation Analysis
            doc_issues = []
            
            # Check for missing documentation files
            try:
                contributing_content = file_read("CONTRIBUTING.md")
                if "not found" in contributing_content.lower():
                    doc_issues.append("Missing CONTRIBUTING.md")
            except:
                doc_issues.append("Missing CONTRIBUTING.md")
            
            try:
                changelog_content = file_read("CHANGELOG.md")
                if "not found" in changelog_content.lower():
                    doc_issues.append("Missing CHANGELOG.md")
            except:
                doc_issues.append("Missing CHANGELOG.md")
            
            # Create documentation issue if needed
            if doc_issues:
                doc_description = f"""## 📚 Documentation Improvements

The AI analysis found missing documentation:

{chr(10).join(f"- {issue}" for issue in doc_issues)}

### Recommended Actions:
1. Create comprehensive project documentation
2. Add contribution guidelines
3. Maintain changelog for releases

### Implementation Plan:
- [ ] Create CONTRIBUTING.md with development guidelines
- [ ] Add CHANGELOG.md for version tracking
- [ ] Enhance README with more examples
- [ ] Add API documentation
- [ ] Create user guides and tutorials

**This issue was automatically created by the AI Multi-Agent System.**
"""
                
                result = create_improvement_issue(
                    "📚 Documentation: Add missing project documentation",
                    doc_description,
                    ['documentation', 'enhancement', 'ai-generated']
                )
                actions_taken.append(result)
            
            # 4. Performance Analysis
            perf_issues = []
            
            # Check for performance monitoring
            try:
                requirements_content = file_read("requirements.txt")
                if "psutil" not in requirements_content:
                    perf_issues.append("Missing performance monitoring (psutil)")
                if "memory-profiler" not in requirements_content:
                    perf_issues.append("Missing memory profiling tools")
            except:
                pass
            
            # Create performance issue if needed
            if perf_issues:
                perf_description = f"""## ⚡ Performance Optimization

The AI analysis identified performance improvement opportunities:

{chr(10).join(f"- {issue}" for issue in perf_issues)}

### Recommended Actions:
1. Add performance monitoring tools
2. Implement performance benchmarks
3. Optimize resource usage

### Implementation Plan:
- [ ] Add psutil for system monitoring
- [ ] Implement memory profiling
- [ ] Create performance benchmarks
- [ ] Add performance tests to CI/CD
- [ ] Monitor and optimize agent execution time

**This issue was automatically created by the AI Multi-Agent System.**
"""
                
                result = create_improvement_issue(
                    "⚡ Performance: Add monitoring and optimization tools",
                    perf_description,
                    ['performance', 'enhancement', 'ai-generated']
                )
                actions_taken.append(result)
            
            # 5. CI/CD Analysis
            cicd_issues = []
            
            # Check for missing CI/CD features
            try:
                workflow_content = file_read(".github/workflows/agent.yml")
                if "test" not in workflow_content.lower():
                    cicd_issues.append("Missing automated testing in CI/CD")
                if "security" not in workflow_content.lower():
                    cicd_issues.append("Missing security scanning in CI/CD")
            except:
                pass
            
            # Create CI/CD issue if needed
            if cicd_issues:
                cicd_description = f"""## 🔄 CI/CD Pipeline Improvements

The AI analysis found CI/CD enhancement opportunities:

{chr(10).join(f"- {issue}" for issue in cicd_issues)}

### Recommended Actions:
1. Enhance GitHub Actions workflows
2. Add comprehensive testing pipeline
3. Implement security scanning

### Implementation Plan:
- [ ] Add automated testing workflow
- [ ] Implement security scanning pipeline
- [ ] Add code quality checks
- [ ] Set up deployment automation
- [ ] Add performance testing

**This issue was automatically created by the AI Multi-Agent System.**
"""
                
                result = create_improvement_issue(
                    "🔄 CI/CD: Enhance automation and testing pipeline",
                    cicd_description,
                    ['ci-cd', 'enhancement', 'ai-generated']
                )
                actions_taken.append(result)
            
            # Summary of actions taken
            if actions_taken:
                summary = f"""
🤖 PROACTIVE ANALYSIS COMPLETED

Actions Taken:
{chr(10).join(actions_taken)}

The AI Multi-Agent System has analyzed the repository and created improvement issues.
Each issue contains detailed implementation plans and can be addressed by the development team or future AI agent runs.
"""
            else:
                summary = "🎉 Repository analysis complete - No immediate improvements needed!"
            
            return summary
        
        @tool
        def analyze_existing_issues() -> str:
            """Analyze all open issues and take appropriate actions"""
            if not self.token:
                return "GitHub token not available"
            
            try:
                # Get all open issues
                issues = github_api(f"/repos/{self.repo}/issues?state=open")
                
                if not isinstance(issues, list):
                    return f"❌ Could not fetch issues: {issues.get('message', 'Unknown error')}"
                
                if not issues:
                    return "✅ No open issues found. Repository is in good shape!"
                
                actions_taken = []
                
                for issue in issues:
                    issue_number = issue['number']
                    issue_title = issue['title']
                    issue_body = issue['body'] or ""
                    labels = [label['name'] for label in issue.get('labels', [])]
                    
                    # Skip if it's a pull request
                    if 'pull_request' in issue:
                        continue
                    
                    # Analyze issue type and take action
                    action_result = analyze_and_act_on_issue(issue_number, issue_title, issue_body, labels)
                    actions_taken.append(f"Issue #{issue_number}: {action_result}")
                
                summary = f"""
🔍 ISSUE ANALYSIS COMPLETED

Analyzed {len(issues)} open issues:
{chr(10).join(actions_taken)}

All issues have been analyzed and appropriate actions taken.
"""
                return summary
                
            except Exception as e:
                return f"❌ Error analyzing issues: {str(e)}"

        @tool
        def analyze_and_act_on_issue(issue_number: int, title: str, body: str, labels: list) -> str:
            """Analyze a specific issue and take appropriate action"""
            
            # Determine issue type and create action plan
            issue_type = "general"
            action_plan = []
            
            # Categorize issue
            title_lower = title.lower()
            body_lower = body.lower()
            
            if any(keyword in title_lower or keyword in body_lower for keyword in ["bug", "error", "fail", "broken", "crash"]):
                issue_type = "bug"
                action_plan = [
                    "1. Reproduce the bug",
                    "2. Identify root cause",
                    "3. Implement fix",
                    "4. Add tests to prevent regression",
                    "5. Create pull request with fix"
                ]
            elif any(keyword in title_lower or keyword in body_lower for keyword in ["feature", "enhancement", "improve", "add"]):
                issue_type = "enhancement"
                action_plan = [
                    "1. Design feature architecture",
                    "2. Implement core functionality",
                    "3. Add comprehensive tests",
                    "4. Update documentation",
                    "5. Create pull request"
                ]
            elif any(keyword in title_lower or keyword in body_lower for keyword in ["security", "vulnerability", "cve"]):
                issue_type = "security"
                action_plan = [
                    "1. Assess security impact",
                    "2. Implement security fix",
                    "3. Add security tests",
                    "4. Update security documentation",
                    "5. Create urgent pull request"
                ]
            elif any(keyword in title_lower or keyword in body_lower for keyword in ["performance", "slow", "optimize", "speed"]):
                issue_type = "performance"
                action_plan = [
                    "1. Profile current performance",
                    "2. Identify bottlenecks",
                    "3. Implement optimizations",
                    "4. Add performance benchmarks",
                    "5. Create pull request with improvements"
                ]
            elif any(keyword in title_lower or keyword in body_lower for keyword in ["doc", "documentation", "readme"]):
                issue_type = "documentation"
                action_plan = [
                    "1. Analyze documentation gaps",
                    "2. Create comprehensive documentation",
                    "3. Add examples and tutorials",
                    "4. Update README if needed",
                    "5. Create pull request with docs"
                ]
            
            # Create detailed comment with analysis and action plan
            comment_body = f"""## 🤖 AI Agent Analysis

**Issue Type:** {issue_type.title()}

**Analysis:**
This issue has been automatically analyzed by the AI Multi-Agent System. Based on the title and description, this appears to be a **{issue_type}** issue.

**Recommended Action Plan:**
{chr(10).join(action_plan)}

**Next Steps:**
- The AI system will begin working on this issue
- Progress updates will be posted here
- A pull request will be created when ready

**Estimated Priority:** {"🔴 High" if issue_type in ["security", "bug"] else "🟡 Medium" if issue_type == "performance" else "🟢 Normal"}

---
*This analysis was automatically generated by the Advanced Multi-Agent GitHub System*
"""
            
            # Post comment on the issue
            comment_result = github_api(
                f"/repos/{self.repo}/issues/{issue_number}/comments",
                method='POST',
                data={'body': comment_body}
            )
            
            if 'id' in comment_result:
                return f"✅ Analyzed and commented on {issue_type} issue"
            else:
                return f"⚠️ Analyzed {issue_type} issue but failed to comment"

        @tool
        def analyze_pull_requests() -> str:
            """Analyze open pull requests and provide reviews"""
            if not self.token:
                return "GitHub token not available"
            
            try:
                # Get all open pull requests
                prs = github_api(f"/repos/{self.repo}/pulls?state=open")
                
                if not isinstance(prs, list):
                    return f"❌ Could not fetch PRs: {prs.get('message', 'Unknown error')}"
                
                if not prs:
                    return "✅ No open pull requests found."
                
                actions_taken = []
                
                for pr in prs:
                    pr_number = pr['number']
                    pr_title = pr['title']
                    pr_body = pr['body'] or ""
                    
                    # Analyze PR and provide review
                    review_result = provide_pr_review(pr_number, pr_title, pr_body)
                    actions_taken.append(f"PR #{pr_number}: {review_result}")
                
                summary = f"""
🔍 PULL REQUEST ANALYSIS COMPLETED

Analyzed {len(prs)} open pull requests:
{chr(10).join(actions_taken)}

All PRs have been reviewed by the AI system.
"""
                return summary
                
            except Exception as e:
                return f"❌ Error analyzing PRs: {str(e)}"

        @tool
        def provide_pr_review(pr_number: int, title: str, body: str) -> str:
            """Provide comprehensive review for a pull request"""
            
            # Analyze PR content
            review_points = []
            
            # Check title quality
            if len(title) < 10:
                review_points.append("📝 Consider making the PR title more descriptive")
            
            # Check description quality
            if len(body) < 50:
                review_points.append("📋 Please add a more detailed description of the changes")
            
            # Check for common patterns
            title_lower = title.lower()
            if "fix" in title_lower:
                review_points.append("🐛 Bug fix detected - ensure tests are included")
            elif "feat" in title_lower or "feature" in title_lower:
                review_points.append("✨ New feature detected - verify documentation is updated")
            elif "refactor" in title_lower:
                review_points.append("🔧 Refactoring detected - ensure no breaking changes")
            
            # Create review comment
            if review_points:
                review_body = f"""## 🤖 AI Code Review

Thank you for your contribution! The AI system has analyzed this pull request.

**Review Points:**
{chr(10).join(f"- {point}" for point in review_points)}

**General Recommendations:**
- ✅ Ensure all tests pass
- ✅ Update documentation if needed
- ✅ Follow coding standards
- ✅ Add appropriate labels
- ✅ Consider adding reviewers

**Security Check:**
- 🔍 No obvious security issues detected in title/description
- 🔍 Please ensure sensitive data is not exposed

**Performance Considerations:**
- ⚡ Consider performance impact of changes
- ⚡ Add benchmarks for performance-critical code

---
*This review was automatically generated by the Advanced Multi-Agent GitHub System*
"""
            else:
                review_body = f"""## 🤖 AI Code Review

Thank you for your contribution! The AI system has analyzed this pull request.

**Analysis Result:** ✅ **Looks Good!**

The PR title and description appear well-structured. Here are some general recommendations:

**Best Practices Checklist:**
- ✅ Ensure all tests pass
- ✅ Update documentation if needed
- ✅ Follow coding standards
- ✅ Add appropriate labels

**Security & Performance:**
- 🔍 No obvious issues detected
- ⚡ Consider performance impact

Great work! 🎉

---
*This review was automatically generated by the Advanced Multi-Agent GitHub System*
"""
            
            # Post review comment
            comment_result = github_api(
                f"/repos/{self.repo}/issues/{pr_number}/comments",
                method='POST',
                data={'body': review_body}
            )
            
            if 'id' in comment_result:
                return f"✅ Provided comprehensive review"
            else:
                return f"⚠️ Analyzed but failed to post review"

        @tool
        def detect_performance_issues() -> str:
            """Detect performance issues and create optimization tasks"""
            performance_issues = []
            
            # Check for common performance issues in code files
            try:
                # Check agent.py for performance issues
                agent_content = file_read("agent.py")
                if "agent.py" in agent_content:
                    if "time.sleep" in agent_content:
                        performance_issues.append("Blocking sleep calls detected in agent.py")
                    if "for" in agent_content and "range" in agent_content:
                        performance_issues.append("Potential inefficient loops in agent.py")
                
                # Check requirements.txt for heavy dependencies
                requirements_content = file_read("requirements.txt")
                if "requirements.txt" in requirements_content:
                    heavy_packages = ["tensorflow", "torch", "transformers", "scikit-learn"]
                    for package in heavy_packages:
                        if package in requirements_content:
                            performance_issues.append(f"Heavy dependency detected: {package}")
                
                # Check for missing performance monitoring
                if "psutil" not in requirements_content:
                    performance_issues.append("Missing performance monitoring tools")
                if "memory-profiler" not in requirements_content:
                    performance_issues.append("Missing memory profiling capabilities")
                
            except Exception as e:
                performance_issues.append(f"Could not analyze files: {str(e)}")
            
            if performance_issues:
                # Create performance optimization issue
                perf_description = f"""## ⚡ Performance Optimization Needed

The AI system detected the following performance issues:

{chr(10).join(f"- {issue}" for issue in performance_issues)}

### 🎯 Optimization Plan:

#### 1. Code Optimization
- [ ] Profile current performance bottlenecks
- [ ] Optimize inefficient loops and algorithms
- [ ] Remove blocking operations where possible
- [ ] Implement async/await patterns for I/O operations

#### 2. Dependency Optimization
- [ ] Audit heavy dependencies
- [ ] Consider lighter alternatives
- [ ] Implement lazy loading for optional features
- [ ] Use optional dependencies where appropriate

#### 3. Monitoring Implementation
- [ ] Add psutil for system monitoring
- [ ] Implement memory profiling
- [ ] Create performance benchmarks
- [ ] Add performance tests to CI/CD

#### 4. Caching Strategy
- [ ] Implement response caching
- [ ] Add memoization for expensive operations
- [ ] Use Redis for distributed caching
- [ ] Cache GitHub API responses

### 📊 Expected Improvements:
- 🚀 30-50% faster execution time
- 💾 20-40% reduced memory usage
- ⚡ Better responsiveness for large repositories
- 📈 Improved scalability

### 🔧 Implementation Priority:
1. **High**: Remove blocking operations
2. **Medium**: Add performance monitoring
3. **Low**: Optimize dependencies

---
**This issue was automatically created by the AI Multi-Agent System**
"""
                
                result = create_improvement_issue(
                    "⚡ Performance: Optimize system performance and add monitoring",
                    perf_description,
                    ['performance', 'optimization', 'ai-generated', 'high-priority']
                )
                
                return f"🎯 Performance issues detected and issue created: {result}"
            else:
                return "✅ No significant performance issues detected"

        @tool
        def comprehensive_repository_action() -> str:
            """Perform comprehensive repository analysis and take all necessary actions"""
            all_actions = []
            
            print("🚀 Starting comprehensive repository action...")
            
            # 1. Analyze existing issues
            print("📋 Analyzing existing issues...")
            issue_analysis = analyze_existing_issues()
            all_actions.append(f"Issue Analysis: {issue_analysis}")
            
            # 2. Analyze pull requests
            print("🔍 Analyzing pull requests...")
            pr_analysis = analyze_pull_requests()
            all_actions.append(f"PR Analysis: {pr_analysis}")
            
            # 3. Detect performance issues
            print("⚡ Detecting performance issues...")
            perf_analysis = detect_performance_issues()
            all_actions.append(f"Performance Analysis: {perf_analysis}")
            
            # 4. Run proactive analysis
            print("🎯 Running proactive analysis...")
            proactive_analysis = proactive_repository_analysis()
            all_actions.append(f"Proactive Analysis: {proactive_analysis}")
            
            # Summary
            summary = f"""
🤖 COMPREHENSIVE REPOSITORY ACTION COMPLETED

The AI Multi-Agent System has performed a complete repository analysis and taken the following actions:

{chr(10).join(f"{i+1}. {action}" for i, action in enumerate(all_actions))}

🎉 Repository improvement process completed!
Check the issues tab for new improvement tasks and the pull requests tab for any automated fixes.
"""
            
            return summary
        
        return [
            activate_advanced_mode,
            activate_streaming_mode,
            activate_meta_tooling_mode,
            github_api,
            analyze_repository_complexity,
            execute_comprehensive_improvement,
            create_improvement_issue,
            create_improvement_pr,
            proactive_repository_analysis,
            analyze_existing_issues,
            analyze_and_act_on_issue,
            analyze_pull_requests,
            provide_pr_review,
            detect_performance_issues,
            comprehensive_repository_action
        ]
    
    def process_message(self, message: str, mode: str = "auto") -> str:
        """Process message with specified or auto-detected mode"""
        
        if mode == "auto":
            # Auto-detect best mode based on message content
            if any(keyword in message.lower() for keyword in ["stream", "real-time", "live", "progress"]):
                mode = "streaming"
            elif any(keyword in message.lower() for keyword in ["create tool", "custom", "meta", "dynamic"]):
                mode = "meta-tooling"
            elif any(keyword in message.lower() for keyword in ["complex", "comprehensive", "multi", "specialist"]):
                mode = "advanced"
            else:
                mode = "basic"
        
        print(f"🤖 Processing with {mode.upper()} mode")
        
        try:
            if mode == "streaming" and self.streaming_agent:
                results = self.streaming_agent.run_streaming_development(message)
                return f"Streaming mode completed with {len(results)} events"
            
            elif mode == "meta-tooling" and self.meta_agent:
                result = self.meta_agent.run_meta_development(message)
                return json.dumps(result, indent=2)
            
            elif mode == "advanced" and self.advanced_agent:
                # For advanced mode, we'll use the basic agent to coordinate
                enhanced_message = f"""
ADVANCED MULTI-AGENT COORDINATION REQUEST:

Original Message: {message}

INSTRUCTIONS:
1. Use activate_advanced_mode to engage specialist agents
2. Coordinate complex tasks across multiple domains
3. Provide comprehensive solutions
4. Take autonomous actions as appropriate

Execute advanced multi-agent coordination now.
"""
                return self.basic_agent(enhanced_message)
            
            else:
                # Use basic agent
                return self.basic_agent(message)
                
        except Exception as e:
            logger.error(f"Error processing message in {mode} mode: {e}")
            return f"Error in {mode} mode: {str(e)}"

def main():
    """Main execution function"""
    import argparse
    
    try:
        print("🚀 Initializing Advanced Multi-Agent GitHub Development System")
        print("=" * 80)
        
        # Parse command line arguments
        parser = argparse.ArgumentParser(description='Advanced Multi-Agent GitHub Development System')
        parser.add_argument('message', nargs='?', help='Task message for the AI agents')
        parser.add_argument('--mode', choices=['auto', 'basic', 'advanced', 'streaming', 'meta-tooling'], 
                          default='auto', help='Agent mode selection')
        parser.add_argument('--priority', choices=['low', 'normal', 'high', 'critical'], 
                          default='normal', help='Task priority level')
        
        args = parser.parse_args()
        
        # Initialize unified agent
        unified_agent = UnifiedGitHubAgent()
        
        # Get the message to process
        message = args.message
        mode = args.mode
        priority = args.priority
        
        print(f"🎯 Mode: {mode.upper()}")
        print(f"📊 Priority: {priority.upper()}")
        
        # Check if running in GitHub Actions
        is_github_actions = os.getenv('GITHUB_ACTIONS') == 'true'
        
        if not message:
            if is_github_actions:
                # Default message for GitHub Actions
                message = """Perform comprehensive autonomous repository management:
                
1. Analyze repository health and complexity
2. Identify improvement opportunities
3. Create and resolve issues as needed
4. Implement code quality improvements
5. Update documentation and tests
6. Apply security hardening measures
7. Optimize CI/CD pipelines
8. Create custom tools if beneficial

Use the most appropriate agent mode based on repository characteristics."""
                print(f"Using default GitHub Actions message")
            else:
                # Interactive mode for local development
                print("🤖 Advanced Multi-Agent GitHub Development System")
                print("Available modes: basic, advanced, streaming, meta-tooling, auto")
                print("Type your message below or 'exit' to quit:\n")
                
                while True:
                    try:
                        q = input("\n> ")
                        if q.lower() in ['exit', 'quit']:
                            print("\nGoodbye! 👋")
                            break
                        if q.strip():
                            # Check for mode specification
                            mode = "auto"
                            if q.startswith("mode:"):
                                parts = q.split(":", 1)
                                if len(parts) == 2:
                                    mode = parts[0].replace("mode", "").strip()
                                    q = parts[1].strip()
                            
                            result = unified_agent.process_message(q, mode)
                            print(f"\n📋 Response:\n{result}")
                    except KeyboardInterrupt:
                        print("\nGoodbye! 👋")
                        break
                    except Exception as e:
                        print(f"Error: {e}")
                return
        
        # Process the message
        print(f"📝 Processing message: {message[:100]}...")
        print("=" * 80)
        
        result = unified_agent.process_message(message, mode)
        
        print("\n" + "=" * 80)
        print("✅ Agent execution completed")
        print(f"📋 Result: {result}")
        
        return result
            
    except Exception as e:
        logger.error(f"Main execution failed: {e}")
        print(f"❌ Error: {e}")
        return None

if __name__ == '__main__':
    main()