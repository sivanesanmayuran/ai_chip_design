#!/usr/bin/env python3
"""Spec-driven flow runner: lint -> sim -> fpga -> asic.

Each step logs to build/<step>.log and exits non-zero on failure so that an
AI agent can read the log and patch the RTL.
"""
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
SPEC = yaml.safe_load((ROOT / "spec" / "soc_spec.yaml").read_text())


def run(step, cmd, cwd=ROOT):
    BUILD.mkdir(exist_ok=True)
    log = BUILD / f"{step}.log"
    print(f"[{step}] {' '.join(map(str, cmd))}")
    with open(log, "w") as f:
        rc = subprocess.call(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT)
    print(f"[{step}] {'OK' if rc == 0 else 'FAIL'} (log: {log})")
    if rc:
        sys.exit(rc)


def srcs():
    return [str(ROOT / s) for s in SPEC["rtl_sources"]]


def lint():
    run("lint", ["verilator", "--lint-only", "-Wall", "--top-module",
                 SPEC["top_module"], *srcs()])


def sim():
    """Run every cocotb testbench (any tests/**/Makefile)."""
    for mk in sorted((ROOT / "tests").rglob("Makefile")):
        name = "sim_" + "_".join(mk.parent.relative_to(ROOT / "tests").parts)
        run(name, ["make"], cwd=mk.parent)


def fpga():
    top = SPEC["top_module"]
    f = SPEC["fpga"]
    json_out = BUILD / f"{top}.json"
    asc = BUILD / f"{top}.asc"
    run("yosys", ["yosys", "-q", "-p",
                  f"read_verilog -sv {' '.join(srcs())}; synth_ice40 -top {top} -json {json_out}"])
    run("nextpnr", ["nextpnr-ice40", f"--{f['device']}", "--package", f["package"],
                    "--json", str(json_out), "--pcf", str(ROOT / f["constraints"]),
                    "--asc", str(asc)])
    run("icepack", ["icepack", str(asc), str(BUILD / f"{top}.bin")])


def asic():
    run("librelane", ["librelane", str(ROOT / SPEC["asic"]["config"])])


STEPS = {"lint": lint, "sim": sim, "fpga": fpga, "asic": asic}

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    if arg == "all":
        for fn in STEPS.values():
            fn()
    elif arg in STEPS:
        STEPS[arg]()
    else:
        sys.exit(f"usage: orchestrator.py [{'|'.join(STEPS)}|all]")
