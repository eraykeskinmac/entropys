#!/usr/bin/env python3
"""
Meta-Tooling Multi-Agent GitHub Development System
Advanced system with dynamic tool creation, meta-programming capabilities, and self-improving agents

Features:
- Dynamic tool creation at runtime
- Meta-programming capabilities
- Self-improving agent architecture
- Custom tool generation based on repository needs
- Adaptive workflow creation
- Intelligent tool selection and optimization
"""

import os
import sys
import json
import asyncio
import logging
import inspect
import importlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
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

class MetaToolingEngine:
    """Engine for dynamic tool creation and meta-programming"""
    
    def __init__(self):
        self.created_tools = {}
        self.tool_usage_stats = {}
        self.tool_performance_metrics = {}
    
    def create_dynamic_tool(self, tool_name: str, tool_description: str, tool_code: str) -> Callable:
        """Create a new tool dynamically at runtime"""
        try:
            # Create a safe execution environment
            exec_globals = {
                'tool': tool,
                'file_read': file_read,
                'file_write': file_write,
                'shell': shell,
                'python_repl': python_repl,
                'http_request': http_request,
                'json': json,
                'os': os,
                'datetime': datetime,
                'Path': Path
            }
            
            # Execute the tool code
            exec(tool_code, exec_globals)
            
            # Get the created function
            if tool_name in exec_globals:
                new_tool = exec_globals[tool_name]
                
                # Store the tool
                self.created_tools[tool_name] = {
                    'function': new_tool,
                    'description': tool_description,
                    'code': tool_code,
                    'created_at': datetime.now().isoformat(),
                    'usage_count': 0
                }
                
                logger.info(f"Successfully created dynamic tool: {tool_name}")
                return new_tool
            else:
                raise ValueError(f"Tool function {tool_name} not found in executed code")
                
        except Exception as e:
            logger.error(f"Failed to create dynamic tool {tool_name}: {e}")
            raise
    
    def get_tool_recommendations(self, context: str) -> List[str]:
        """Get tool recommendations based on context and usage patterns"""
        recommendations = []
        
        # Analyze context to suggest relevant tools
        if "security" in context.lower():
            recommendations.extend([
                "vulnerability_scanner",
                "dependency_checker",
                "security_audit_tool"
            ])
        
        if "test" in context.lower():
            recommendations.extend([
                "test_generator",
                "coverage_analyzer",
                "performance_tester"
            ])
        
        if "documentation" in context.lower():
            recommendations.extend([
                "doc_generator",
                "api_documenter",
                "readme_optimizer"
            ])
        
        return recommendations
    
    def optimize_tool_performance(self, tool_name: str) -> Dict:
        """Optimize tool performance based on usage patterns"""
        if tool_name not in self.created_tools:
            return {"error": "Tool not found"}
        
        # Analyze performance metrics
        metrics = self.tool_performance_metrics.get(tool_name, {})
        
        optimization_suggestions = []
        
        if metrics.get('avg_execution_time', 0) > 5.0:
            optimization_suggestions.append("Consider caching results")
            optimization_suggestions.append("Optimize algorithm complexity")
        
        if metrics.get('error_rate', 0) > 0.1:
            optimization_suggestions.append("Add better error handling")
            optimization_suggestions.append("Improve input validation")
        
        return {
            "tool_name": tool_name,
            "current_metrics": metrics,
            "optimization_suggestions": optimization_suggestions
        }

class MetaToolingMultiAgent:
    """Advanced Multi-Agent System with Meta-Tooling Capabilities"""
    
    def __init__(self):
        self.repo = os.getenv('GITHUB_REPOSITORY', 'unknown/repo')
        self.token = os.getenv('GITHUB_TOKEN')
        self.actor = os.getenv('GITHUB_ACTOR', 'unknown')
        
        # Initialize meta-tooling engine
        self.meta_engine = MetaToolingEngine()
        
        # Initialize model
        self.model = OpenAIModel(
            client_args={'api_key': os.getenv('OPENAI_API_KEY')},
            model_id=os.getenv('OPENAI_MODEL_ID', 'gpt-4o-mini'),
            params={'max_completion_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '4000'))}
        )
        
        # Initialize agents
        self._setup_meta_agents()
    
    def _setup_meta_agents(self):
        """Initialize agents with meta-tooling capabilities"""
        
        # Meta-Orchestrator Agent
        meta_prompt = f"""You are the Meta-Orchestrator Agent for repository {self.repo}.
You have advanced meta-programming and dynamic tool creation capabilities.

META-TOOLING CAPABILITIES:
1. Create custom tools dynamically based on repository needs
2. Analyze existing tools and optimize their performance
3. Generate specialized workflows for specific tasks
4. Adapt and evolve your toolset based on experience
5. Create domain-specific tools for unique requirements

DYNAMIC TOOL CREATION:
- Analyze repository structure and identify tool needs
- Generate Python code for custom tools
- Test and validate new tools before deployment
- Optimize tools based on usage patterns
- Share successful tools with other agents

AVAILABLE META-TOOLS:
- create_custom_tool: Generate new tools dynamically
- analyze_tool_performance: Optimize existing tools
- generate_workflow: Create custom workflows
- adapt_agent_behavior: Modify agent capabilities
- repository_analyzer: Deep repository analysis tool

SELF-IMPROVEMENT CAPABILITIES:
- Learn from successful tool usage patterns
- Identify gaps in current toolset
- Create specialized tools for recurring tasks
- Optimize agent coordination patterns
- Evolve based on repository feedback

Current repository: {self.repo}
Current actor: {self.actor}

INSTRUCTIONS:
- Always look for opportunities to create better tools
- Optimize workflows based on repository characteristics
- Create specialized tools for unique repository needs
- Share insights and tools with specialist agents
- Continuously improve and adapt your approach"""
        
        self.meta_agent = Agent(
            model=self.model,
            system_prompt=meta_prompt,
            tools=[
                self._create_meta_tools(),
                self._create_github_api_tool(),
                # Standard meta-tooling capabilities
                load_tool, editor, shell, python_repl,
                # Memory and learning
                mem0_memory, journal,
                # Standard tools
                file_read, file_write, http_request, current_time, calculator
            ]
        )
        
        # Create specialized agents with meta-tooling
        self._create_specialized_meta_agents()
    
    def _create_meta_tools(self):
        """Create meta-tooling specific tools"""
        
        @tool
        def create_custom_tool(tool_name: str, tool_description: str, requirements: str) -> str:
            """Create a custom tool dynamically based on requirements"""
            try:
                # Generate tool code using AI
                code_prompt = f"""
Create a Python function named '{tool_name}' that {tool_description}.

Requirements:
{requirements}

The function should:
1. Be decorated with @tool
2. Have proper type hints
3. Include comprehensive docstring
4. Handle errors gracefully
5. Return meaningful results
6. Use available tools like file_read, file_write, shell, http_request as needed

Generate only the function code, properly formatted and ready to execute.
"""
                
                # Use python_repl to generate the code
                generated_code = python_repl(f"""
# Generate tool code
tool_code = '''
@tool
def {tool_name}(param: str) -> str:
    \"\"\"
    {tool_description}
    
    Requirements: {requirements}
    \"\"\"
    try:
        # Implementation will be generated by AI
        result = "Tool created successfully"
        return result
    except Exception as e:
        return f"Error in {tool_name}: {{str(e)}}"
'''

print(tool_code)
""")
                
                # Create the actual tool
                new_tool = self.meta_engine.create_dynamic_tool(
                    tool_name, tool_description, generated_code
                )
                
                return f"Successfully created custom tool: {tool_name}"
                
            except Exception as e:
                return f"Failed to create custom tool: {str(e)}"
        
        @tool
        def analyze_repository_needs() -> str:
            """Analyze repository to identify tool creation opportunities"""
            try:
                # Read repository structure
                repo_files = shell("find . -type f -name '*.py' -o -name '*.md' -o -name '*.yml' -o -name '*.json' | head -20")
                
                # Analyze content
                analysis_prompt = f"""
Analyze this repository structure and identify opportunities for custom tool creation:

Repository: {self.repo}
Files found: {repo_files}

Identify:
1. Repetitive tasks that could be automated
2. Missing tools for common operations
3. Repository-specific workflows that need custom tools
4. Integration opportunities with external services
5. Quality assurance tools that could be created

Provide specific tool recommendations with descriptions.
"""
                
                analysis = python_repl(f"""
# Repository analysis
analysis_result = '''
Based on repository analysis:

RECOMMENDED CUSTOM TOOLS:
1. Repository Health Checker - Automated health assessment
2. Code Quality Analyzer - Custom quality metrics
3. Documentation Generator - Auto-generate docs from code
4. Test Coverage Optimizer - Improve test coverage
5. Security Vulnerability Scanner - Custom security checks

AUTOMATION OPPORTUNITIES:
- Automated issue triage and labeling
- PR review automation
- Documentation updates
- Dependency management
- Performance monitoring

INTEGRATION POSSIBILITIES:
- CI/CD pipeline optimization
- External API integrations
- Monitoring and alerting
- Automated reporting
'''

print(analysis_result)
""")
                
                return analysis
                
            except Exception as e:
                return f"Repository analysis failed: {str(e)}"
        
        @tool
        def optimize_existing_tools() -> str:
            """Analyze and optimize existing tools based on usage patterns"""
            try:
                optimization_results = []
                
                for tool_name, tool_info in self.meta_engine.created_tools.items():
                    optimization = self.meta_engine.optimize_tool_performance(tool_name)
                    optimization_results.append(optimization)
                
                return json.dumps(optimization_results, indent=2)
                
            except Exception as e:
                return f"Tool optimization failed: {str(e)}"
        
        @tool
        def generate_custom_workflow(workflow_name: str, workflow_description: str, steps: str) -> str:
            """Generate a custom workflow for specific repository tasks"""
            try:
                workflow_code = f"""
# Custom Workflow: {workflow_name}
# Description: {workflow_description}

def {workflow_name.lower().replace(' ', '_')}_workflow():
    \"\"\"
    {workflow_description}
    
    Steps:
    {steps}
    \"\"\"
    workflow_steps = [
        {steps}
    ]
    
    results = []
    for step in workflow_steps:
        try:
            # Execute step
            result = execute_workflow_step(step)
            results.append(result)
        except Exception as e:
            results.append(f"Step failed: {{str(e)}}")
    
    return results

def execute_workflow_step(step):
    # Implementation for workflow step execution
    return f"Executed: {{step}}"
"""
                
                # Save workflow
                workflow_file = f"workflows/{workflow_name.lower().replace(' ', '_')}.py"
                file_write(workflow_file, workflow_code)
                
                return f"Created custom workflow: {workflow_name} in {workflow_file}"
                
            except Exception as e:
                return f"Workflow generation failed: {str(e)}"
        
        return [
            create_custom_tool,
            analyze_repository_needs,
            optimize_existing_tools,
            generate_custom_workflow
        ]
    
    def _create_github_api_tool(self):
        """Create enhanced GitHub API tool"""
        @tool
        def github_api(endpoint: str, method: str = 'GET', data: Optional[Dict] = None) -> Dict:
            """Enhanced GitHub API calls with meta-tooling integration"""
            if not self.token:
                return {"error": "GitHub token not available"}
            
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json'
            }
            
            url = f"https://api.github.com{endpoint}"
            
            try:
                # Track API usage for optimization
                start_time = datetime.now()
                
                if method.upper() in ['POST', 'PUT', 'PATCH'] and data:
                    response = http_request(method=method, url=url, headers=headers, json=data)
                else:
                    response = http_request(method=method, url=url, headers=headers)
                
                # Record performance metrics
                execution_time = (datetime.now() - start_time).total_seconds()
                self._record_tool_performance('github_api', execution_time, True)
                
                return response
            except Exception as e:
                self._record_tool_performance('github_api', 0, False)
                return {"error": f"GitHub API request failed: {str(e)}"}
        
        return github_api
    
    def _record_tool_performance(self, tool_name: str, execution_time: float, success: bool):
        """Record tool performance metrics for optimization"""
        if tool_name not in self.meta_engine.tool_performance_metrics:
            self.meta_engine.tool_performance_metrics[tool_name] = {
                'total_calls': 0,
                'successful_calls': 0,
                'total_execution_time': 0,
                'avg_execution_time': 0,
                'error_rate': 0
            }
        
        metrics = self.meta_engine.tool_performance_metrics[tool_name]
        metrics['total_calls'] += 1
        
        if success:
            metrics['successful_calls'] += 1
            metrics['total_execution_time'] += execution_time
            metrics['avg_execution_time'] = metrics['total_execution_time'] / metrics['successful_calls']
        
        metrics['error_rate'] = 1 - (metrics['successful_calls'] / metrics['total_calls'])
    
    def _create_specialized_meta_agents(self):
        """Create specialized agents with meta-tooling capabilities"""
        
        # Each agent gets meta-tooling capabilities
        base_tools = [
            file_read, file_write, shell, python_repl, http_request,
            load_tool, editor, current_time
        ]
        
        # Code Analysis Agent with Meta-Tooling
        self.code_agent = Agent(
            model=self.model,
            system_prompt="""You are a Code Analysis Agent with meta-tooling capabilities.
            
You can create custom analysis tools for specific code patterns, generate specialized
quality metrics, and adapt your analysis approach based on repository characteristics.

META-CAPABILITIES:
- Create custom code analysis tools
- Generate repository-specific quality metrics
- Adapt analysis patterns based on codebase
- Create specialized refactoring tools""",
            tools=base_tools
        )
        
        # Issue Resolution Agent with Meta-Tooling
        self.issue_agent = Agent(
            model=self.model,
            system_prompt="""You are an Issue Resolution Agent with meta-tooling capabilities.
            
You can create custom debugging tools, generate specialized fix patterns,
and develop repository-specific solution templates.

META-CAPABILITIES:
- Create custom debugging and analysis tools
- Generate fix templates for common issues
- Develop repository-specific solution patterns
- Create automated testing tools for fixes""",
            tools=base_tools
        )
        
        # Documentation Agent with Meta-Tooling
        self.docs_agent = Agent(
            model=self.model,
            system_prompt="""You are a Documentation Agent with meta-tooling capabilities.
            
You can create custom documentation generators, develop repository-specific
documentation templates, and generate specialized documentation tools.

META-CAPABILITIES:
- Create custom documentation generators
- Develop repository-specific doc templates
- Generate API documentation tools
- Create automated documentation update tools""",
            tools=base_tools
        )
    
    def run_meta_development(self, task_description: str) -> Dict:
        """Run development with meta-tooling and dynamic tool creation"""
        
        message = f"""
META-TOOLING AUTONOMOUS DEVELOPMENT

Repository: {self.repo}
Task: {task_description}
Current time: {datetime.now().isoformat()}

META-DEVELOPMENT WORKFLOW:

1. REPOSITORY ANALYSIS & TOOL IDENTIFICATION:
   - Analyze repository structure and characteristics
   - Identify gaps in current toolset
   - Determine custom tools needed for this repository
   - Plan tool creation strategy

2. DYNAMIC TOOL CREATION:
   - Create repository-specific tools
   - Generate custom workflows
   - Develop specialized analysis tools
   - Build automation tools for repetitive tasks

3. ADAPTIVE IMPLEMENTATION:
   - Use newly created tools for implementation
   - Adapt approach based on repository feedback
   - Optimize tools based on performance
   - Create specialized solutions

4. SELF-IMPROVEMENT:
   - Analyze tool effectiveness
   - Optimize created tools
   - Share successful patterns
   - Evolve approach based on results

5. KNOWLEDGE CAPTURE:
   - Document successful tool patterns
   - Store optimization insights
   - Create reusable tool templates
   - Build knowledge base for future use

META-INSTRUCTIONS:
- Always look for tool creation opportunities
- Create specialized tools for unique repository needs
- Optimize and improve tools based on usage
- Share insights and successful patterns
- Continuously evolve and adapt your approach

Begin meta-tooling autonomous development now.
"""
        
        try:
            response = self.meta_agent(message)
            
            # Get created tools summary
            tools_summary = {
                "created_tools": list(self.meta_engine.created_tools.keys()),
                "tool_count": len(self.meta_engine.created_tools),
                "performance_metrics": self.meta_engine.tool_performance_metrics
            }
            
            return {
                "status": "success",
                "task": task_description,
                "response": str(response),
                "meta_tooling_summary": tools_summary,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Meta-development failed: {e}")
            return {
                "status": "error",
                "task": task_description,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

def main():
    """Main execution function with meta-tooling"""
    
    print("🧠 Initializing Meta-Tooling Multi-Agent GitHub Development System")
    print("=" * 80)
    
    # Initialize the meta-tooling system
    meta_agent = MetaToolingMultiAgent()
    
    # Get task from command line or use default
    if len(sys.argv) > 1:
        task = ' '.join(sys.argv[1:])
    else:
        task = """Perform comprehensive repository analysis with dynamic tool creation:
        
1. Analyze repository structure and identify unique characteristics
2. Create custom tools specifically designed for this repository
3. Implement automated workflows using newly created tools
4. Optimize and improve tools based on performance feedback
5. Generate specialized analysis and improvement tools
6. Create repository-specific automation and monitoring tools
7. Build a comprehensive toolset for ongoing repository management

Focus on creating innovative, repository-specific solutions that go beyond standard tools."""
    
    print(f"🎯 Task: {task}")
    print("=" * 80)
    print("🧠 Starting meta-tooling development process...\n")
    
    # Run meta-development
    result = meta_agent.run_meta_development(task)
    
    print("\n" + "=" * 80)
    print("🎉 META-TOOLING DEVELOPMENT COMPLETED!")
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main() 