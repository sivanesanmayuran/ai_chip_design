#!/usr/bin/env bash
# Install the free EDA toolchain inside WSL2 Ubuntu. Run: bash tools/install_wsl.sh
set -e
sudo apt update
sudo apt install -y build-essential python3-dev python3-venv python3-pip git \
  verilator iverilog yosys nextpnr-ice40 fpga-icestorm gtkwave klayout magic netgen

# Keep the venv and a copy of the repo on the Linux filesystem (faster than /mnt/c)
python3 -m venv ~/venv
. ~/venv/bin/activate
pip install --upgrade pip wheel
pip install -r "$(dirname "$0")/../requirements-eda.txt"
echo "Done. Next time: source ~/venv/bin/activate"
