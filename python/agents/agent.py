#!/usr/bin/env python3
"""Prompt -> RTL -> lint (-> sim) self-correcting loop using a local LLM.

Usage:
  python python/agents/agent.py "Create an APB UART with 16-byte TX/RX FIFOs" \
      --top apb_uart --steps lint
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from llm import CFG, ROOT, chat  # noqa: E402

SYSTEM = (Path(__file__).parent / "prompts" / "system.md").read_text()
FILE_RE = re.compile(r"```[a-zA-Z]*\n(?://|#) FILE: (\S+)\n(.*?)```", re.S)


def save_files(reply):
    written = []
    allowed = CFG["agent"]["writable_dirs"]
    for rel, body in FILE_RE.findall(reply):
        p = (ROOT / rel).resolve()
        if not any(p.is_relative_to((ROOT / d).resolve()) for d in allowed):
            print(f"skip (not writable): {rel}")
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        content = body if body.startswith(("//", "#")) else body
        # keep the FILE marker line out of the file
        p.write_text(content)
        written.append(rel)
    return written


def run_verilator(top, files):
    rtl = [str(ROOT / f) for f in files if f.endswith((".sv", ".v"))]
    cmd = ["verilator", "--lint-only", "-Wall", "--top-module", top, *rtl]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    return r.returncode, r.stdout + r.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("--top", required=True, help="top module name")
    ap.add_argument("--steps", default="lint", choices=["lint"])
    a = ap.parse_args()

    msgs = [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": a.prompt +
             f"\nTop module name must be {a.top}."}]
    files = []
    for i in range(1, CFG["agent"]["max_iterations"] + 1):
        reply = chat(msgs)
        files = save_files(reply) or files
        print(f"[iter {i}] wrote: {files}")
        rc, log = run_verilator(a.top, files)
        if rc == 0:
            print("lint clean")
            return 0
        print(log[-2000:])
        msgs += [{"role": "assistant", "content": reply},
                 {"role": "user", "content":
                  "Verilator reported:\n" + log[-4000:] +
                  "\nReturn complete corrected files."}]
    print("giving up after max iterations")
    return 1


if __name__ == "__main__":
    sys.exit(main())
