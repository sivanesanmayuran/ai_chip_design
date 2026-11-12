# AI-Aided Chip Design (single repo)

Free/open-source flow: spec -> RTL -> lint -> cocotb -> FPGA (Yosys/nextpnr) -> ASIC (LibreLane -> GDSII).

## Layout
| Folder | Purpose |
|---|---|
| spec/ | YAML SoC spec (cores, peripherals, bus, memory map) |
| rtl/ | HDL: peripherals/, bus/, dsp/, ai/, top/ |
| tests/ | cocotb / pyuvm tests (tests/cocotb) |
| flow/ | Python orchestrator, FPGA and LibreLane configs |
| python/ai_training/ | ML model training / quantization for AI blocks |
| python/agents/ | LLM agent prompts and glue |
| tools/ | Installed/vendored tools and helper scripts |
| sdk/ | Headers (generated register maps), drivers |
| firmware/ | Boot code, linker scripts |
| applications/ | Example apps built on the SDK |
| docs/ | Documentation |
| build/ | Generated outputs (git-ignored) |

## Free tools
Verilator, Icarus Verilog, cocotb, pyuvm, Yosys, nextpnr, IceStorm/Trellis,
LibreLane (OpenROAD, Magic, Netgen, KLayout), Sky130/GF180/IHP PDKs, LiteX/FuseSoC.
Easiest on Linux/WSL2 (or the IIC-OSIC-TOOLS docker image). Tools are not
installed by this scaffold.

## Usage
```
pip install -r requirements.txt
python flow/orchestrator.py lint
python flow/orchestrator.py sim
python flow/orchestrator.py fpga
python flow/orchestrator.py asic
python flow/orchestrator.py all
```
Each step runs a free tool, writes logs to build/, and stops on failure so an
AI agent can read the log and patch RTL (see python/agents/).
