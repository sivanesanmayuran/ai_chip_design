"""Minimal OpenAI-compatible chat client (stdlib only) for local LLM servers."""
import json
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((Path(__file__).parent / "config.yaml").read_text())


def chat(messages, **over):
    c = {**CFG["llm"], **over}
    body = json.dumps({
        "model": c["model"],
        "messages": messages,
        "temperature": c["temperature"],
    }).encode()
    req = urllib.request.Request(
        c["base_url"].rstrip("/") + "/chat/completions", data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {c['api_key']}"})
    with urllib.request.urlopen(req, timeout=c["timeout_s"]) as r:
        return json.load(r)["choices"][0]["message"]["content"]
