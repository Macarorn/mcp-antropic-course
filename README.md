# MCP Chat

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models through OpenRouter API. The application supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Context Protocol) architecture.

**Note**: This project has been migrated from Anthropic API to OpenRouter API for free access to AI models.

## Prerequisites

- Python 3.10+
- OpenRouter API Key (free at [openrouter.ai](https://openrouter.ai))

## Setup

### Step 1: Configure the environment variables

1. Create or edit the `.env` file in the project root and verify that the following variables are set correctly:

```
OPENROUTER_API_KEY=""  # Enter your OpenRouter API key
CLAUDE_MODEL=poolside/laguna-m.1:free  # Free model with tool calling support
USE_UV=1
```

### Step 2: Install dependencies

#### Option 1: Setup with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

```bash
pip install uv
```

2. Install dependencies:

```bash
uv sync
```

3. Run the project

```bash
uv run main.py
```

#### Option 2: Setup without uv

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install openai python-dotenv prompt-toolkit "mcp[cli]>=1.8.0"
```

3. Run the project

```bash
python main.py
```

## Usage

### Basic Interaction

Simply type your message and press Enter to chat with the model.

### Document Retrieval

Use the @ symbol followed by a document ID to include document content in your query:

```
> Tell me about @deposition.md
```

### Commands

Use the / prefix to execute commands defined in the MCP server:

```
> /summarize deposition.md
```

Commands will auto-complete when you press Tab.

## Development

### MCP Inspector

Use the MCP Inspector to test and debug your MCP server locally:

```bash
uv run mcp dev -- python mcp_server.py
```

This will open the MCP Inspector in your browser at `http://127.0.0.1:6274` (or similar port). In the inspector:

1. Configure the connection:
   - Command: `python`
   - Args: `mcp_server.py`
2. Click "Connect"
3. Use "List Tools" to see available tools
4. Test tools interactively

### Testing MCP Client

To test the MCP client independently:

```bash
uv run mcp_client.py
```

This will list all available tools from the MCP server.

### Adding New Documents

Edit the `mcp_server.py` file to add new documents to the `docs` dictionary.

### Implementing MCP Features

To fully implement the MCP features:

1. Complete the TODOs in `mcp_server.py`
2. Implement the missing functionality in `mcp_client.py`

### Linting and Typing Check

There are no lint or type checks implemented.
