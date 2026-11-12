SIM ?= icarus
TOPLEVEL_LANG = verilog
# Relative path: works for Linux and for Windows-native iverilog under Cygwin make
VERILOG_SOURCES = ../../../../rtl/cores/riscv/picorv32/picorv32.v
TOPLEVEL = picorv32
COCOTB_TEST_MODULES = test_picorv32
# For older cocotb (<2.0) use: MODULE = test_picorv32
MODULE = test_picorv32
# Dump waveforms by default (sim_build/picorv32.fst). Disable with: make WAVES=0
WAVES ?= 1
include $(shell cocotb-config --makefiles)/Makefile.sim

# Open the waveform in GTKWave (needs WSLg on Windows 11, or X server)
wave:
	gtkwave sim_build/$(TOPLEVEL).fst &
