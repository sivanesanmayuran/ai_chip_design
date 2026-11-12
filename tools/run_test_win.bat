@echo off
rem Run a cocotb test folder on native Windows (Icarus + Cygwin make) and open the waveform.
rem Usage: tools\run_test_win.bat tests\cores\riscv\picorv32 picorv32
rem        (second arg = toplevel name of the .fst file; omit to skip GTKWave)
set PATH=C:\iverilog\bin;C:\iverilog\gtkwave\bin;%PATH%
make -C %1 ICARUS_BIN_DIR=/cygdrive/c/iverilog/bin
if not "%2"=="" start "" gtkwave.exe %1\sim_build\%2.fst
