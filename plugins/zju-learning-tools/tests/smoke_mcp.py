"""Start the bundled stdio MCP and verify its read-only tool surface."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PLUGIN_ROOT = Path(__file__).resolve().parents[1]


async def run() -> dict[str, object]:
    params = StdioServerParameters(
        command="uv",
        args=["run", "--project", "./runtime", "--frozen", "python", "./scripts/start_mcp.py"],
        cwd=str(PLUGIN_ROOT),
        env=dict(os.environ),
    )
    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            names = sorted(tool.name for tool in tools.tools)
            if len(names) != 23:
                raise RuntimeError(f"Expected 23 tools, got {len(names)}")
            forbidden = ("submit", "answer", "signin", "post", "upload", "delete", "remove", "complete")
            bad = [name for name in names if any(word in name for word in forbidden)]
            if bad:
                raise RuntimeError(f"Remote-write-like tools were exposed: {bad}")
            doctor = await session.call_tool("zju_doctor", {})
            return {"ok": not doctor.isError, "tool_count": len(names), "tools": names}


if __name__ == "__main__":
    print(json.dumps(asyncio.run(asyncio.wait_for(run(), timeout=60)), ensure_ascii=False, indent=2))
