# GitHub Agent with Strands SDK

An intelligent AI-powered GitHub automation tool that uses the Strands Agents SDK to manage repositories, issues, and pull requests automatically.

## =€ Features

- **Intelligent Issue Management**: Automatically create, update, close, and comment on issues
- **Pull Request Automation**: Review, merge, comment, and track pull requests
- **GitHub API Integration**: Full support for both GraphQL and REST APIs
- **File Operations**: Read and write repository files programmatically
- **Workflow Automation**: Trigger other GitHub Actions workflows
- **Shell Command Execution**: Execute git and system commands
- **OpenAI Integration**: Uses GPT models for intelligent responses and analysis

## =Á Project Structure

- **`setup.py`** - Interactive setup script that configures the GitHub Agent
- **`agent.py`** - Main GitHub Agent with comprehensive repository management capabilities
- **`requirements.txt`** - Project dependencies including Strands SDK and tools

## =à Installation

1. **Run the setup script:**
   ```bash
   python setup.py
   ```

2. **For interactive setup with environment configuration:**
   ```bash
   python setup.py --interactive
   ```

3. **Quick setup (basic files only):**
   ```bash
   python setup.py --quick
   ```

4. **Check existing installation:**
   ```bash
   python setup.py --check
   ```

## ™ Configuration

### Required Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (starts with sk-)
- `GITHUB_TOKEN` - GitHub personal access token (automatically provided in Actions)
- `GITHUB_REPOSITORY` - Repository name (automatically set in Actions)

### Optional Configuration

- `OPENAI_MODEL_ID` - OpenAI model to use (default: gpt-4)
- `OPENAI_MAX_TOKENS` - Maximum tokens for responses (default: 4000)

## <¯ Agent Capabilities

### GitHub Management
- **Issues**: Create, update, close, comment, and organize issues
- **Pull Requests**: Review, merge, comment, and track PRs
- **Repository Files**: Read and write files in the repository
- **Git Operations**: Execute git commands through shell interface

### API Operations
- **GraphQL Queries**: Execute complex GitHub GraphQL operations
- **REST API Calls**: Make GitHub REST API requests
- **Workflow Dispatch**: Trigger other GitHub Actions workflows
- **Context Awareness**: Access GitHub Actions context and environment

### Intelligence Features
- **Code Analysis**: Analyze code and provide insights
- **Automated Responses**: Intelligent responses to repository events
- **Python REPL**: Execute Python code for analysis tasks
- **External API Calls**: Make HTTP requests to external services

## =¦ Usage

### GitHub Actions Integration

The agent automatically responds to these GitHub events:
- Issues (opened, edited, closed, reopened, assigned, labeled)
- Issue comments (created, edited, deleted)
- Pull requests (opened, closed, edited, synchronized)
- Pull request reviews and comments
- Manual workflow dispatch

### Manual Execution

```bash
python agent.py "Analyze the current repository status"
```

### Command Line Arguments

```bash
python agent.py "What are my active pull requests and issues?"
```

## =Ë Setup Steps

1. **Configure Repository Secrets:**
   - Go to Repository Settings ’ Secrets and variables ’ Actions
   - Add `OPENAI_API_KEY` secret with your OpenAI API key

2. **Set Workflow Permissions:**
   - Go to Repository Settings ’ Actions ’ General ’ Workflow permissions
   - Select "Read and write permissions"
   - Enable "Allow GitHub Actions to create and approve pull requests"

3. **Commit and Push Files:**
   ```bash
   git add .
   git commit -m "Add GitHub Agent with Strands SDK"
   git push
   ```

4. **Test the Agent:**
   - Go to Actions tab ’ GitHub Agent ’ Run workflow
   - Or create a new issue/PR to trigger automatic response

## =' Dependencies

- **strands-agents** - Core Strands Agents SDK
- **strands-agents-tools** - Additional tools for the agent
- **requests** - HTTP client for API interactions
- **colorama** - Terminal colors for setup script
- **rich** - Rich text formatting
- **python-dateutil** - Date/time utilities
- **jsonschema** - JSON validation
- **python-dotenv** - Environment variable management
- **GitPython** - Git operations
- **markdown** - Markdown processing
- **PyYAML** - YAML handling

##   Important Notes

- Never commit your `.env` file to the repository (it's in `.gitignore`)
- The agent requires Python 3.10+ to run
- Make sure your repository has proper workflow permissions configured
- Test the agent in a development repository before deploying to production

## > How It Works

1. **Event Trigger**: GitHub Actions triggers the workflow on repository events
2. **Agent Initialization**: The agent loads with OpenAI model and Strands tools
3. **Context Analysis**: Agent analyzes the GitHub event and repository context  
4. **Tool Execution**: Agent uses available tools to perform appropriate actions
5. **Response Generation**: Agent provides intelligent responses and takes automated actions

## =Ú Available Tools

- `use_github` - Execute GitHub GraphQL queries and mutations
- `github_rest_api` - Make GitHub REST API calls
- `get_github_context` - Get current GitHub context and environment
- `dispatch_workflow` - Trigger other GitHub Actions workflows
- `manage_issue` - Comprehensive issue management
- `manage_pull_request` - Comprehensive PR management
- `file_read/file_write` - Repository file operations
- `shell` - Execute git and system commands
- `http_request` - Make external API calls
- `python_repl` - Execute Python code for analysis
- `current_time` - Get current timestamp
- `environment` - Check environment variables

## <‰ Getting Started

Ready to add AI automation to your repository? Run the setup script and follow the interactive prompts:

```bash
python setup.py --interactive
```

The agent will be ready to help manage your GitHub repository intelligently!