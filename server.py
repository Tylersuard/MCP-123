from __future__ import annotations
import importlib.util, inspect, asyncio
from pathlib import Path
from typing import Callable, Any

from fastmcp import FastMCP                     # FastMCP v2 server core
from fastmcp.tools.tool import Tool
import uvicorn

class McpServer:
    def __init__(self, tools_path: str | Path, *, host="0.0.0.0", port=8000):
        self.host, self.port = host, port
        self.mcp = FastMCP(Path(tools_path).stem.capitalize())   # server name
        self._load_tools(Path(tools_path))

    def _load_tools(self, path: Path) -> None:
        """Import module by path and register every top-level function."""
        spec = importlib.util.spec_from_file_location(path.stem, str(path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)                               # type: ignore

        for name, func in inspect.getmembers(mod, inspect.isfunction):
            if name.startswith("_"):           # private helper, skip
                continue
            self._register(func)

    def _register(self, fn: Callable[..., Any]) -> None:
        """Turn a function into an MCP Tool using FastMCP's helper."""
   # Convert the plain function to a Tool and register it
        tool = Tool.from_function(fn)                 # auto-builds schema & description
        self.mcp.add_tool(tool)

    # ---------- public API ---------- #
    def run(self, reload: bool = False) -> None:
        """Block and serve over HTTP."""
        uvicorn.run(self.mcp.http_app(), host=self.host, port=self.port, reload=reload)

def run_server(tools_filepath: str | Path, **kwargs):
    """Convenience one-liner."""
    McpServer(tools_filepath, **kwargs).run()
