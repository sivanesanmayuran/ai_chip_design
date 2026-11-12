# Agents
Put LLM glue here. Suggested loop: run `flow/orchestrator.py <step>`, read
`build/<step>.log` on failure, send log + RTL to the LLM, apply patch, retry
(bounded iterations). Candidate MCP servers: OpenROAD-MCP, verilator-mcp.
