# Running tests and viewing waveforms

Run everything inside Ubuntu (WSL), after `bash tools/install_wsl.sh`.

## 1. Run one testbench
```
source ~/venv/bin/activate
cd /mnt/c/Users/nxh00777/Desktop/JOB/startup/ai_chip_design/tests/cores/riscv/picorv32
make            # runs the tests, prints PASS/FAIL table, writes results.xml
```
Waveform is written to `sim_build/picorv32.fst` (WAVES=1 is the default here).

## 2. Run all testbenches via the flow
```
cd /mnt/c/Users/nxh00777/Desktop/JOB/startup/ai_chip_design
python flow/orchestrator.py sim      # logs in build/sim_*.log
```

## 3. View waveforms
- GTKWave in WSL (Windows 11 has WSLg built in): `make wave` in the test folder,
  or `gtkwave sim_build/picorv32.fst`. Drag signals (clk, mem_valid, mem_addr,
  mem_wdata, mem_rdata, mem_ready, trap) from the left tree into the signal pane.
- VS Code: install the "Surfer" or "WaveTrace" extension and open the .fst/.vcd file
  (via the "WSL" remote window).
- Because the repo is on C:, you can also open `sim_build\picorv32.fst` from
  Windows with a Windows build of GTKWave or Surfer.

## 4. Results
- Console table of tests with PASS/FAIL and sim time.
- `results.xml` (JUnit format) in the test folder, usable by CI.
- Add `dut._log.info(...)` in tests for extra prints (run `make COCOTB_LOG_LEVEL=DEBUG`).

## Clean
`make clean` in the test folder removes sim_build and results.xml.
