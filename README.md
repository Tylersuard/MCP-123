# MCP-123
The easiest possible implementation of an MCP server and client.  Set up a server or a client in 2 lines of code.

## 🧩 Minimal MCP Server & Client

This project is the **simplest possible way** to set up a Model Context Protocol (MCP) Server and Client in Python. With just **2 lines of code**, you can launch a server that exposes your Python functions as tools, or a client that can discover and use them powered by OpenAI models.

---

## 🚀 Features
- **Ultra-minimal setup**: Start a server or client in 2 lines.
- **Easy tool creation**: Write normal functions in your `tools.py` file—**no decorators or special wrappers needed**—and they get included as tools that your MCP server can use automatically.
- **OpenAI integration**: The client uses your OpenAI API key to answer questions, calling tools as needed.
- **FastMCP v2**: Built on the FastMCP server core for speed and reliability.

---

## 🖥️ Quickstart

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Create Your Tools

Define your functions in `tools.py`. For example:

```python
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
```

### 3. Start the MCP Server (2 lines)

```python
from mcp123 import server
server.run_server("tools.py", port=9999)
```


### 4. Set up the MCP Client (2 lines)

```python
from mcp123.client import McpClient
client = McpClient("http://localhost:9999", "sk-...your OpenAI key...")

### 5. Use the MCP Client
answer = client.ask("Add 15 and 14.")
print("Answer:", answer)

### 6. Close the MCP Client when you are done
client.close()
```

---

## 📝 How It Works

- **Server**: Loads all top-level functions from `tools.py` and exposes them as MCP tools via HTTP.
- **Client**: Discovers available tools, sends prompts to OpenAI, and automatically calls tools if needed.

---

## 🛠️ Example Output

When you run the client, you’ll see:

```
Tools discovered:
 [ ...list of tools... ]

Answer: 29
```

---

## 🔑 Requirements
- Python 3.11+
- OpenAI API key (for the client)

---

## 📢 Why MCP123?
- **Zero boilerplate**: No need to write schemas or wrappers—just write functions.
- **LLM-native**: Designed for seamless LLM tool use.
- **Extensible**: Add more tools by simply adding functions.

---

## 🤝 Credits
- Built with [FastMCP](https://github.com/typpo/fastmcp)
- Inspired by the Model Context Protocol (MCP)

---

## 📬 Feedback & Contributions
Pull requests and issues are welcome, as long as Pull Requests are in all-caps.
