#!/usr/bin/env python3
"""
Streaming Multi-Agent GitHub Development System
Advanced system with streaming responses, callback handlers, and real-time monitoring

Features:
- Real-time streaming responses
- Advanced callback handling
- Multi-agent coordination with streaming
- Live progress monitoring
- Dynamic tool creation and loading
- Memory management and context awareness
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, AsyncIterator
from pathlib import Path

from strands import Agent, tool
from strands.models.openai import OpenAIModel
from strands_tools import (
    file_read, file_write, http_request, environment, shell,
    current_time, python_repl, calculator, load_tool, editor,
    mem0_memory, journal
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StreamingCallbackHandler:
    """Advanced callback handler for streaming and monitoring"""
    
    def __init__(self, agent_name: str = "Unknown"):
        self.agent_name = agent_name
        self.start_time = None
        self.tool_calls = []
        self.reasoning_steps = []
        self.current_phase = "initializing"
        
    def __call__(self, **kwargs):
        """Handle various callback events"""
        
        # Initialize timing
        if self.start_time is None:
            self.start_time = datetime.now()
        
        # Handle different event types
        if kwargs.get("reasoning", False):
            self._handle_reasoning(kwargs)
        elif "current_tool_use" in kwargs:
            self._handle_tool_use(kwargs)
        elif kwargs.get("complete", False):
            self._handle_completion(kwargs)
        elif "streaming_chunk" in kwargs:
            self._handle_streaming(kwargs)
        elif "error" in kwargs:
            self._handle_error(kwargs)
    
    def _handle_reasoning(self, kwargs):
        """Handle reasoning events"""
        reasoning_text = kwargs.get("reasoningText", "")
        self.reasoning_steps.append({
            "timestamp": datetime.now().isoformat(),
            "text": reasoning_text,
            "phase": self.current_phase
        })
        
        print(f"🧠 [{self.agent_name}] REASONING: {reasoning_text[:100]}...")
        logger.info(f"Agent {self.agent_name} reasoning: {reasoning_text}")
    
    def _handle_tool_use(self, kwargs):
        """Handle tool usage events"""
        tool = kwargs["current_tool_use"]
        tool_name = tool.get('name', 'unknown')
        tool_args = tool.get('arguments', {})
        
        self.tool_calls.append({
            "timestamp": datetime.now().isoformat(),
            "tool_name": tool_name,
            "arguments": tool_args,
            "phase": self.current_phase
        })
        
        print(f"🔧 [{self.agent_name}] USING TOOL: {tool_name}")
        if tool_args:
            print(f"   Arguments: {json.dumps(tool_args, indent=2)[:200]}...")
        
        logger.info(f"Agent {self.agent_name} using tool: {tool_name}")
    
    def _handle_completion(self, kwargs):
        """Handle completion events"""
        duration = datetime.now() - self.start_time if self.start_time else timedelta(0)
        
        print(f"✅ [{self.agent_name}] COMPLETED in {duration.total_seconds():.2f}s")
        print(f"   Tools used: {len(self.tool_calls)}")
        print(f"   Reasoning steps: {len(self.reasoning_steps)}")
        
        logger.info(f"Agent {self.agent_name} completed - Duration: {duration}, Tools: {len(self.tool_calls)}")
    
    def _handle_streaming(self, kwargs):
        """Handle streaming chunk events"""
        chunk = kwargs.get("streaming_chunk", "")
        if chunk.strip():
            print(f"📡 [{self.agent_name}] {chunk}", end="", flush=True)
    
    def _handle_error(self, kwargs):
        """Handle error events"""
        error = kwargs.get("error", "Unknown error")
        print(f"❌ [{self.agent_name}] ERROR: {error}")
        logger.error(f"Agent {self.agent_name} error: {error}")
    
    def get_summary(self) -> Dict:
        """Get execution summary"""
        duration = datetime.now() - self.start_time if self.start_time else timedelta(0)
        
        return {
            "agent_name": self.agent_name,
            "duration_seconds": duration.total_seconds(),
            "tool_calls_count": len(self.tool_calls),
            "reasoning_steps_count": len(self.reasoning_steps),
            "tool_calls": self.tool_calls,
            "reasoning_steps": self.reasoning_steps
        }

class StreamingMultiAgent:
    """Advanced Multi-Agent System with Streaming and Real-time Monitoring"""
    
    def __init__(self):
        self.repo = os.getenv('GITHUB_REPOSITORY', 'unknown/repo')
        self.token = os.getenv('GITHUB_TOKEN')
        self.actor = os.getenv('GITHUB_ACTOR', 'unknown')
        
        # Initialize model with streaming enabled
        self.model = OpenAIModel(
            client_args={'api_key': os.getenv('OPENAI_API_KEY')},
            model_id=os.getenv('OPENAI_MODEL_ID', 'gpt-4o-mini'),
            params={
                'max_completion_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '4000')),
                'stream': True  # Enable streaming
            }
        )
        
        # Callback handlers for each agent
        self.callbacks = {}
        
        # Initialize agents
        self._setup_streaming_agents()
    
    def _setup_streaming_agents(self):
        """Initialize all agents with streaming and callback handlers"""
        
        # Lead Orchestrator Agent with streaming
        lead_callback = StreamingCallbackHandler("Lead-Orchestrator")
        self.callbacks["lead"] = lead_callback
        
        lead_prompt = f"""You are the Lead Orchestrator Agent for repository {self.repo}.
You coordinate multiple specialized AI agents with real-time streaming capabilities.

STREAMING CAPABILITIES:
- Provide real-time progress updates
- Stream reasoning process to users
- Coordinate multiple agents simultaneously
- Monitor and report on agent activities

CORE RESPONSIBILITIES:
1. Analyze repository state with streaming feedback
2. Route tasks to appropriate specialist agents
3. Create custom tools dynamically using meta-tooling
4. Provide real-time status updates
5. Coordinate complex multi-agent workflows

AVAILABLE SPECIALIST AGENTS (all with streaming):
- code_analysis_agent: Real-time code quality analysis
- issue_resolution_agent: Live bug fixing and feature implementation
- pr_review_agent: Streaming code review process
- documentation_agent: Live documentation generation
- testing_agent: Real-time test creation and execution
- security_agent: Live security analysis and hardening

STREAMING INSTRUCTIONS:
- Always provide progress updates during long operations
- Stream your reasoning process
- Report on specialist agent activities
- Give real-time feedback on task completion

Current repository: {self.repo}
Current actor: {self.actor}"""
        
        self.lead_agent = Agent(
            model=self.model,
            system_prompt=lead_prompt,
            callback_handler=lead_callback,
            tools=[
                self._create_github_api_tool(),
                self._create_streaming_agent_tools(),
                # Meta-tooling with streaming
                load_tool, editor, shell, python_repl,
                # Memory and journaling
                mem0_memory, journal,
                # Standard tools
                file_read, file_write, http_request, current_time, calculator
            ]
        )
        
        # Create specialized streaming agents
        self._create_specialized_streaming_agents()
    
    def _create_github_api_tool(self):
        """Create GitHub API tool with enhanced error handling"""
        @tool
        def github_api(endpoint: str, method: str = 'GET', data: Optional[Dict] = None) -> Dict:
            """Make GitHub API calls with detailed logging"""
            if not self.token:
                return {"error": "GitHub token not available"}
            
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json'
            }
            
            url = f"https://api.github.com{endpoint}"
            
            try:
                print(f"🌐 Making GitHub API call: {method} {endpoint}")
                
                if method.upper() in ['POST', 'PUT', 'PATCH'] and data:
                    response = http_request(method=method, url=url, headers=headers, json=data)
                else:
                    response = http_request(method=method, url=url, headers=headers)
                
                print(f"✅ GitHub API call successful")
                return response
            except Exception as e:
                error_msg = f"GitHub API request failed: {str(e)}"
                print(f"❌ {error_msg}")
                return {"error": error_msg}
        
        return github_api
    
    def _create_streaming_agent_tools(self):
        """Create agent-as-tools with streaming support"""
        
        @tool
        def code_analysis_agent(query: str) -> str:
            """Specialized code analysis with real-time streaming"""
            try:
                print(f"🔍 Starting code analysis: {query[:50]}...")
                response = self.code_agent(query)
                return str(response)
            except Exception as e:
                return f"Error in code analysis: {str(e)}"
        
        @tool
        def issue_resolution_agent(query: str) -> str:
            """Specialized issue resolution with streaming progress"""
            try:
                print(f"🐛 Starting issue resolution: {query[:50]}...")
                response = self.issue_agent(query)
                return str(response)
            except Exception as e:
                return f"Error in issue resolution: {str(e)}"
        
        @tool
        def pr_review_agent(query: str) -> str:
            """Specialized PR review with streaming feedback"""
            try:
                print(f"📋 Starting PR review: {query[:50]}...")
                response = self.pr_agent(query)
                return str(response)
            except Exception as e:
                return f"Error in PR review: {str(e)}"
        
        @tool
        def documentation_agent(query: str) -> str:
            """Specialized documentation with live generation"""
            try:
                print(f"📚 Starting documentation work: {query[:50]}...")
                response = self.docs_agent(query)
                return str(response)
            except Exception as e:
                return f"Error in documentation: {str(e)}"
        
        @tool
        def testing_agent(query: str) -> str:
            """Specialized testing with real-time execution"""
            try:
                print(f"🧪 Starting testing work: {query[:50]}...")
                response = self.test_agent(query)
                return str(response)
            except Exception as e:
                return f"Error in testing: {str(e)}"
        
        @tool
        def security_agent(query: str) -> str:
            """Specialized security analysis with live scanning"""
            try:
                print(f"🔒 Starting security analysis: {query[:50]}...")
                response = self.security_agent(query)
                return str(response)
            except Exception as e:
                return f"Error in security analysis: {str(e)}"
        
        # Return all agent tools
        return [
            code_analysis_agent,
            issue_resolution_agent,
            pr_review_agent,
            documentation_agent,
            testing_agent,
            security_agent
        ]
    
    def _create_specialized_streaming_agents(self):
        """Create specialized agents with streaming capabilities"""
        
        # Code Analysis Agent
        code_callback = StreamingCallbackHandler("Code-Analyzer")
        self.callbacks["code"] = code_callback
        
        self.code_agent = Agent(
            model=self.model,
            system_prompt="""You are a specialized Code Analysis Agent with real-time streaming capabilities.

STREAMING FEATURES:
- Stream code analysis progress in real-time
- Provide live feedback on code quality issues
- Report findings as they are discovered

EXPERTISE: Code quality assessment, architecture analysis, performance optimization, refactoring.

ACTIONS: Analyze codebase, identify issues, suggest improvements, create quality reports.

Always stream your analysis process and provide real-time updates.""",
            callback_handler=code_callback,
            tools=[file_read, file_write, shell, python_repl, http_request]
        )
        
        # Issue Resolution Agent
        issue_callback = StreamingCallbackHandler("Issue-Resolver")
        self.callbacks["issue"] = issue_callback
        
        self.issue_agent = Agent(
            model=self.model,
            system_prompt="""You are a specialized Issue Resolution Agent with streaming implementation.

STREAMING FEATURES:
- Stream bug fixing progress in real-time
- Provide live updates on feature implementation
- Report testing results as they happen

EXPERTISE: Bug analysis, feature implementation, issue triage, root cause analysis.

ACTIONS: Analyze issues, implement fixes, develop features, create tests, generate PRs.

Always stream your implementation process and provide progress updates.""",
            callback_handler=issue_callback,
            tools=[file_read, file_write, shell, python_repl, http_request]
        )
        
        # PR Review Agent
        pr_callback = StreamingCallbackHandler("PR-Reviewer")
        self.callbacks["pr"] = pr_callback
        
        self.pr_agent = Agent(
            model=self.model,
            system_prompt="""You are a specialized PR Review Agent with streaming review process.

STREAMING FEATURES:
- Stream code review progress in real-time
- Provide live feedback on code changes
- Report security and quality issues as found

EXPERTISE: Code review, security detection, performance analysis, testing assessment.

ACTIONS: Review changes, provide feedback, approve/request changes, merge PRs.

Always stream your review process and provide real-time feedback.""",
            callback_handler=pr_callback,
            tools=[file_read, file_write, shell, python_repl, http_request]
        )
        
        # Documentation Agent
        docs_callback = StreamingCallbackHandler("Documentation-Writer")
        self.callbacks["docs"] = docs_callback
        
        self.docs_agent = Agent(
            model=self.model,
            system_prompt="""You are a specialized Documentation Agent with live generation capabilities.

STREAMING FEATURES:
- Stream documentation creation in real-time
- Provide live updates on writing progress
- Show documentation structure as it's built

EXPERTISE: Technical writing, API documentation, user guides, code comments.

ACTIONS: Create README files, generate API docs, write guides, add comments.

Always stream your writing process and show documentation as it's created.""",
            callback_handler=docs_callback,
            tools=[file_read, file_write, shell, python_repl, http_request]
        )
        
        # Testing Agent
        test_callback = StreamingCallbackHandler("Test-Engineer")
        self.callbacks["test"] = test_callback
        
        self.test_agent = Agent(
            model=self.model,
            system_prompt="""You are a specialized Testing Agent with real-time test execution.

STREAMING FEATURES:
- Stream test creation and execution in real-time
- Provide live coverage reports
- Show CI/CD setup progress

EXPERTISE: Unit testing, integration testing, test coverage, CI/CD setup.

ACTIONS: Create test suites, improve coverage, set up CI/CD, implement automation.

Always stream your testing process and provide real-time execution results.""",
            callback_handler=test_callback,
            tools=[file_read, file_write, shell, python_repl, http_request]
        )
        
        # Security Agent
        security_callback = StreamingCallbackHandler("Security-Analyst")
        self.callbacks["security"] = security_callback
        
        self.security_agent = Agent(
            model=self.model,
            system_prompt="""You are a specialized Security Agent with live vulnerability scanning.

STREAMING FEATURES:
- Stream security analysis in real-time
- Provide live vulnerability reports
- Show security hardening progress

EXPERTISE: Vulnerability detection, dependency analysis, security best practices.

ACTIONS: Scan vulnerabilities, analyze dependencies, implement patches, create security docs.

Always stream your security analysis and provide real-time threat assessment.""",
            callback_handler=security_callback,
            tools=[file_read, file_write, shell, python_repl, http_request]
        )
    
    async def stream_autonomous_development(self, task_description: str) -> AsyncIterator[Dict]:
        """Stream autonomous development process with real-time updates"""
        
        print(f"🚀 Starting Streaming Autonomous Development")
        print(f"Repository: {self.repo}")
        print(f"Task: {task_description}")
        print("=" * 80)
        
        message = f"""
STREAMING AUTONOMOUS DEVELOPMENT MODE

Repository: {self.repo}
Task: {task_description}
Current time: {datetime.now().isoformat()}

REAL-TIME DEVELOPMENT WORKFLOW:

1. STREAMING ANALYSIS PHASE:
   - Stream repository analysis in real-time
   - Provide live updates on task understanding
   - Show component identification progress
   - Stream implementation strategy planning

2. LIVE IMPLEMENTATION PHASE:
   - Use specialist agents with streaming
   - Stream code changes as they happen
   - Provide real-time test creation updates
   - Show documentation updates live

3. STREAMING QUALITY ASSURANCE:
   - Stream security analysis progress
   - Provide live test coverage reports
   - Show code quality improvements in real-time
   - Stream review process

4. REAL-TIME INTEGRATION:
   - Stream PR creation process
   - Show labeling and assignment in real-time
   - Provide live project tracking updates
   - Stream change documentation

5. LIVE MONITORING SETUP:
   - Stream monitoring configuration
   - Show improvement planning in real-time
   - Provide live maintenance schedule updates

STREAMING INSTRUCTIONS:
- Use all specialist agents with streaming enabled
- Provide continuous real-time updates
- Stream all reasoning and decision-making
- Show progress on all tasks
- Provide live status reports

Begin streaming autonomous development now.
"""
        
        try:
            # Stream the response from lead agent
            async for chunk in self.lead_agent.stream_async(message):
                yield {
                    "type": "stream_chunk",
                    "agent": "lead",
                    "content": chunk,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Get final summary from all agents
            summary = self._get_execution_summary()
            yield {
                "type": "summary",
                "content": summary,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Streaming development failed: {e}")
            yield {
                "type": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_execution_summary(self) -> Dict:
        """Get comprehensive execution summary from all agents"""
        summary = {
            "total_agents": len(self.callbacks),
            "execution_time": datetime.now().isoformat(),
            "agent_summaries": {}
        }
        
        for agent_name, callback in self.callbacks.items():
            summary["agent_summaries"][agent_name] = callback.get_summary()
        
        return summary
    
    def run_streaming_development(self, task_description: str) -> Dict:
        """Run streaming development (synchronous wrapper)"""
        
        async def _run():
            results = []
            async for chunk in self.stream_autonomous_development(task_description):
                results.append(chunk)
                
                # Print real-time updates
                if chunk["type"] == "stream_chunk":
                    print(chunk["content"], end="", flush=True)
                elif chunk["type"] == "summary":
                    print(f"\n\n📊 EXECUTION SUMMARY:")
                    print(json.dumps(chunk["content"], indent=2))
                elif chunk["type"] == "error":
                    print(f"\n❌ ERROR: {chunk['error']}")
            
            return results
        
        # Run the async function
        return asyncio.run(_run())

def main():
    """Main execution function with streaming support"""
    
    print("🌊 Initializing Streaming Multi-Agent GitHub Development System")
    print("=" * 80)
    
    # Initialize the streaming multi-agent system
    streaming_agent = StreamingMultiAgent()
    
    # Get task from command line or use default
    if len(sys.argv) > 1:
        task = ' '.join(sys.argv[1:])
    else:
        task = """Perform comprehensive repository analysis and autonomous improvements:
        
1. Analyze current codebase quality and architecture
2. Identify and resolve any existing issues
3. Implement security hardening measures
4. Improve test coverage and CI/CD pipeline
5. Update and enhance documentation
6. Create improvement roadmap for future development

Provide real-time streaming updates throughout the entire process."""
    
    print(f"🎯 Task: {task}")
    print("=" * 80)
    print("🌊 Starting streaming development process...\n")
    
    # Run streaming development
    results = streaming_agent.run_streaming_development(task)
    
    print("\n" + "=" * 80)
    print("🎉 STREAMING DEVELOPMENT COMPLETED!")
    print(f"Total events processed: {len(results)}")

if __name__ == '__main__':
    main() 