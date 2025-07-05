from __future__ import annotations
import asyncio, json
from typing import Any, Dict, List

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from openai import OpenAI


class McpError(RuntimeError):
    pass


class McpClient:
    def __init__(self, server_url: str, openai_key: str,
                 *, model: str = "gpt-4o") -> None:
        self._url = server_url.rstrip("/")
        self._oa = OpenAI(api_key=openai_key)
        self._model = model
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        self._transport_ctx = None
        self._session: ClientSession | None = None
        self.tools: List[Dict[str, Any]] = []

        self._loop.run_until_complete(self._bootstrap())

    async def _bootstrap(self):
        self._transport_ctx = streamablehttp_client(f"{self._url}/mcp")
        read, write, _ = await self._transport_ctx.__aenter__()
        cm = ClientSession(read, write)
        self._session = await cm.__aenter__()
        await self._session.initialize()

        resp = await self._session.list_tools()
        self.tools = [t.model_dump(exclude_none=True) for t in resp.tools]

    async def aclose(self):
        # Properly close async resources if they exist
        if self._session:
            try:
                await self._session.__aexit__(None, None, None)
            except Exception:
                pass
        if self._transport_ctx:
            try:
                await self._transport_ctx.__aexit__(None, None, None)
            except Exception:
                pass

    def close(self):
        # Run async cleanup before closing the event loop
        self._loop.run_until_complete(self.aclose())
        self._loop.close()

    def ask(self, prompt: str) -> str:
        return self._loop.run_until_complete(self._ask_async(prompt))

    async def _ask_async(self, prompt: str) -> str:
        if not self._session:
            raise McpError("Session not initialised.")

        tool_json = json.dumps({"tools": self.tools}, ensure_ascii=False)
        first = self._oa.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system",
                 "content": "If a tool is useful, reply ONLY with "
                            '{"tool": "<name>", "arguments": {...}}'},
                {"role": "system", "content": f"TOOLS:\n{tool_json}"},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        ).choices[0].message.content or ""

        try:
            spec = json.loads(first)
            tool, args = spec["tool"], spec["arguments"]
        except Exception:                       # model didn't pick a tool
            return first

        raw = await self._session.call_tool(tool, args)
        result = raw.structuredContent or raw.content or str(raw)

        if isinstance(result, (dict, list)):
            tool_result_msg = json.dumps(result, ensure_ascii=False)
        else:
            tool_result_msg = str(result)

        final = self._oa.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "assistant", "content": first},
                {"role": "system",
                 "content": "TOOL RESULT:\n" + tool_result_msg},
                {"role": "user", "content": "Answer the original question."},
            ],
            temperature=0,
        ).choices[0].message.content or ""
        return final
