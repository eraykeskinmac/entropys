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

OPERATIONAL MODES AVAILABLE:
1. BASIC MODE: Standard repository management
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

ADVANCED FEATURES:
- Multi-agent coordination for complex tasks
- Real-time streaming responses for long operations
- Dynamic tool creation based on repository needs
- Self-improving architecture with learning capabilities
- Meta-programming for custom solution development

Current repository: {self.repo}
Current actor: {self.actor}

INSTRUCTIONS:
- Analyze the task and choose the most appropriate operational mode
- Use advanced features when beneficial
- Provide comprehensive solutions
- Take autonomous actions to improve repository health
- Create issues, PRs, and documentation as needed
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
        
        return [
            activate_advanced_mode,
            activate_streaming_mode,
            activate_meta_tooling_mode,
            github_api,
            analyze_repository_complexity,
            execute_comprehensive_improvement
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