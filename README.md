<h1 align="center">
  MCP-123
  <br>
  <sub>The *easiest* way to run an MCP server & client (2 lines each)</sub>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11%2B-blue" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/fastmcp-powered-informational" alt="FastMCP">
  <img src="https://img.shields.io/badge/openai-ready-green" alt="OpenAI ready">
</p>

> **MCP-123** bundles a zero-boilerplate Model-Context-Protocol server *and* client.  
> Drop in your functions ➜ run ➜ profit.

---

## 🗂️ Table&nbsp;of&nbsp;Contents
1. [Quick start](#️-quickstart)
2. [Features](#-features)
3. [How it works](#-how-it-works)
4. [Example output](#️-example-output)
5. [Requirements](#-requirements)
6. [Why MCP-123?](#-why-mcp123)
7. [Credits](#-credits)
8. [Feedback](#-feedback--contributions)

---

## 🖥️ Quickstart

### 1. Install
```bash
pip install -r requirements.txt

2. Create your tools (tools.py)

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

3. Start the server (2 lines)

from mcp123 import server
server.run_server("tools.py", port=9999)

4. Spin up the client (2 lines)

from mcp123.client import McpClient
client = McpClient("http://localhost:9999", "sk-...your-OpenAI-key...")

5. Ask things

answer = client.ask("Add 15 and 14.")
print("Answer:", answer)  # ➜ 29

6. Close when done

client.close()

🚀 Features

    Ultra-minimal setup – server or client in two lines.

    Write plain functions – no decorators, schemas, or wrappers.

    Automatic tool discovery – every top-level function in tools.py becomes an MCP tool.

    OpenAI-aware client – sends prompts, calls tools, streams answers.

📝 How It Works
Component	Responsibility
Server	Imports tools.py, registers each top-level function as an MCP tool, serves over HTTP.
Client	Discovers available tools, sends your prompt to OpenAI, executes tool calls when the model requests them, then returns the final answer.
🛠️ Example Output

Tools discovered:
 [add, …]

Answer: 29

🔑 Requirements

    Python 3.11 or newer

    OpenAI API key (client only)

📢 Why MCP-123?

    Zero boilerplate – just write functions.

    LLM-native – built for OpenAI function-calling & friends.

    Extensible – add a new tool by adding a new function.

🤝 Credits

    Built with https://github.com/typpo/fastmcp

    Inspired by the Model Context Protocol (MCP)

📬 Feedback & Contributions

Issues welcome, and PULL REQUESTS IN ALL CAPS are extra welcome. 😉
