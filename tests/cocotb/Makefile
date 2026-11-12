SIM ?= icarus
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/../../rtl/peripherals/apb_gpio.sv
COMPILE_ARGS += -g2012
TOPLEVEL = apb_gpio
COCOTB_TEST_MODULES = test_apb_gpio
# For older cocotb (<2.0) use: MODULE = test_apb_gpio
MODULE = test_apb_gpio
include $(shell cocotb-config --makefiles)/Makefile.sim
