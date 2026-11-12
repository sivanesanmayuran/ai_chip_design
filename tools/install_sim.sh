#!/usr/bin/env bash
# Minimal install for running cocotb simulations + waveforms in WSL2 Ubuntu.
# Run inside Ubuntu: bash tools/install_sim.sh
set -e
sudo apt update
sudo apt install -y build-essential python3-dev python3-venv python3-pip git \
  iverilog verilator gtkwave make

python3 -m venv ~/venv
. ~/venv/bin/activate
pip install --upgrade pip wheel
pip install pyyaml cocotb numpy mcp

echo
echo "Installed. Check:"
which iverilog cocotb-config
echo "Next: source ~/venv/bin/activate"
