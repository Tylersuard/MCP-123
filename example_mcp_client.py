from mcp123_client import McpClient

# 1️⃣ create client (auto-discovers tools)
client = McpClient(
    "http://localhost:9999",
    "sk-"   # your OpenAI key
)

print("Tools discovered:\n", client.tools, "\n")

# 2️⃣ high-level prompt
answer = client.ask("Add 15 and 14.")
print("Answer:", answer, "\n")

client.close()
