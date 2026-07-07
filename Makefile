# =====================================================
# APB RAM Verification Makefile (cocotb + Verilator)
# =====================================================

# -----------------------------
# Simulator
# -----------------------------

SIM ?= verilator
TOPLEVEL_LANG ?= verilog

# -----------------------------
# DUT
# -----------------------------

TOPLEVEL = tb_top

# Default test (can override)
MODULE ?= tests.test_smoke

# -----------------------------
# RTL Sources
# -----------------------------

VERILOG_SOURCES = \
	rtl/apb_ram.sv \
	rtl/apb_if.sv \
	rtl/tb_top.sv

# -----------------------------
# Verilator options
# -----------------------------

EXTRA_ARGS += --trace --coverage --timing

# -----------------------------
# Python path
# -----------------------------

export PYTHONPATH := $(PWD)/tb/cocotb:$(PYTHONPATH)
# -----------------------------
# Export vars
# -----------------------------

export SIM
export TOPLEVEL
export TOPLEVEL_LANG
export MODULE
export VERILOG_SOURCES

# -----------------------------
# Cocotb build system
# -----------------------------

include /home/anddrew/cocotb-venv/lib/python3.12/site-packages/cocotb/share/makefiles/Makefile.sim

# =====================================================
# Regression Targets
# =====================================================

smoke:
	make clean
	make SIM=$(SIM) MODULE=tests.test_smoke

illegal:
	make clean
	make SIM=$(SIM) MODULE=tests.test_illegal_addr

random:
	make clean
	make SIM=$(SIM) MODULE=tests.test_random_basic

stress:
	make clean
	make SIM=$(SIM) MODULE=tests.test_stress_back2back

reset:
	make clean
	make SIM=$(SIM) MODULE=tests.test_reset

# =====================================================
# Run all tests
# =====================================================

regress:
	make smoke
	make illegal
	make random
	make stress
	make reset

# =====================================================
# Coverage report
# =====================================================

coverage:
	verilator_coverage --write-info coverage.info sim_build/coverage.dat
	genhtml coverage.info --output-directory coverage_report
	@echo "Coverage report generated in coverage_report/index.html"

# =====================================================
# Utility
# =====================================================

clean-all:
	rm -rf sim_build results.xml coverage* coverage_report
