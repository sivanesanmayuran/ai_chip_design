# Setup

Native Windows: only `pip install -r requirements.txt` (agent + MCP server).
The EDA tools (LibreLane, OpenROAD, Magic, Yosys, nextpnr) need Linux.

## WSL2 (recommended)
```
wsl --install -d Ubuntu          # in admin PowerShell, then reboot
sudo apt update
sudo apt install -y build-essential python3-venv python3-pip git \
  verilator iverilog yosys nextpnr-ice40 fpga-icestorm gtkwave klayout magic netgen
cd /mnt/c/Users/nxh00777/Desktop/JOB/startup/ai_chip_design
python3 -m venv ~/venv && source ~/venv/bin/activate
pip install -r requirements-eda.txt
```
Copying the repo into the WSL filesystem (~/ai_chip_design) is faster than /mnt/c.
LibreLane also needs Nix or Docker; see https://librelane.readthedocs.io.
Ollama can stay on Windows; WSL2 reaches it at http://localhost:11434
(or set base_url in python/agents/config.yaml).

## Alternative
Docker image iic-osic-tools bundles all the tools.

## Windows-only option
Install "Microsoft C++ Build Tools" (Desktop development with C++) to fix
wheel build errors, but the EDA tools will still not run natively.
