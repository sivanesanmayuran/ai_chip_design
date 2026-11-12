#!/usr/bin/env python3
"""MCP server exposing the chip flow to an AI client (stdio transport).

Tools: list_files, read_file, write_file, run_step, read_log.
Writes are restricted to the writable_dirs in config.yaml.
"""
import subprocess
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

sys.path.insert(0, str(Path(__file__).parent))
from llm import CFG, ROOT  # noqa: E402

mcp = FastMCP("chip-flow")
STEPS = ("lint", "sim", "fpga", "asic", "all")


def _safe(rel, write=False):
    p = (ROOT / rel).resolve()
    if not p.is_relative_to(ROOT):
        raise ValueError("path outside repo")
    if write and not any(p.is_relative_to((ROOT / d).resolve())
                         for d in CFG["agent"]["writable_dirs"]):
        raise ValueError("path not writable")
    return p


@mcp.tool()
def list_files(subdir: str = ".") -> str:
    """List files under a repo subdirectory."""
    base = _safe(subdir)
    return "\n".join(str(p.relative_to(ROOT)) for p in sorted(base.rglob("*"))
                     if p.is_file() and ".git" not in p.parts
                     and "build" not in p.parts)[:20000]


@mcp.tool()
def read_file(path: str) -> str:
    """Read a text file in the repo."""
    return _safe(path).read_text()[:50000]


@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Write a file under rtl/, tests/, sdk/, firmware/ or applications/."""
    p = _safe(path, write=True)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return f"wrote {path}"


@mcp.tool()
def run_step(step: str) -> str:
    """Run a flow step (lint, sim, fpga, asic, all). Returns status and log tail."""
    if step not in STEPS:
        return f"unknown step; use one of {STEPS}"
    r = subprocess.run([sys.executable, str(ROOT / "flow" / "orchestrator.py"), step],
                       capture_output=True, text=True, cwd=ROOT)
    return (r.stdout + r.stderr)[-4000:] + f"\nexit={r.returncode}"


@mcp.tool()
def read_log(step: str) -> str:
    """Read the tail of build/<step>.log."""
    p = _safe(f"build/{step}.log")
    return p.read_text()[-8000:] if p.exists() else "no log"


if __name__ == "__main__":
    mcp.run()
