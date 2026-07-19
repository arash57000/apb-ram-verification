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
# Export variables
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
# Phase 5 — Basic Verification
# =====================================================

smoke:
	make clean
	make SIM=$(SIM) MODULE=tests.test_smoke

reset:
	make clean
	make SIM=$(SIM) MODULE=tests.test_reset

illegal:
	make clean
	make SIM=$(SIM) MODULE=tests.test_illegal_addr

addr0:
	make clean
	make SIM=$(SIM) MODULE=tests.test_addr0

addr31:
	make clean
	make SIM=$(SIM) MODULE=tests.test_addr31

read_default:
	make clean
	make SIM=$(SIM) MODULE=tests.test_read_default

overwrite:
	make clean
	make SIM=$(SIM) MODULE=tests.test_overwrite

seqwrite:
	make clean
	make SIM=$(SIM) MODULE=tests.test_sequential_write

seqread:
	make clean
	make SIM=$(SIM) MODULE=tests.test_sequential_read

writerd:
	make clean
	make SIM=$(SIM) MODULE=tests.test_write_read_immediate

stress:
	make clean
	make SIM=$(SIM) MODULE=tests.test_stress_back2back

random:
	make clean
	make SIM=$(SIM) MODULE=tests.test_random_basic

# =====================================================
# Phase 6 — Functional Verification
# =====================================================

# -----------------------------
# Corner-Case Tests
# -----------------------------

data_patterns:
	make clean
	make SIM=$(SIM) MODULE=tests.test_data_patterns

# Future Corner-Case Tests

boundary_toggle:
	make clean
	make SIM=$(SIM) MODULE=tests.test_boundary_toggle

 same_address:
	make clean
	make SIM=$(SIM) MODULE=tests.test_same_address_repeated

# reset_mid_transaction:
#	make clean
#	make SIM=$(SIM) MODULE=tests.test_reset_mid_transaction
#
# post_reset_access:
#	make clean
#	make SIM=$(SIM) MODULE=tests.test_post_reset_access

# -----------------------------
# Negative Tests
# -----------------------------

# Future targets

# -----------------------------
# Random Tests
# -----------------------------

# Future targets

# -----------------------------
# Stress Tests
# -----------------------------

# Future targets

# -----------------------------
# Protocol Compliance Tests
# -----------------------------

# Future targets

# =====================================================
# Run Full Regression
# =====================================================

regress:
	@echo ""
	@echo "======================================================"
	@echo "        APB RAM FULL REGRESSION STARTED"
	@echo "======================================================"
	@echo ""
    
	# Phase 5
	$(MAKE) smoke
	$(MAKE) reset
	$(MAKE) illegal
	$(MAKE) addr0
	$(MAKE) addr31
	$(MAKE) read_default
	$(MAKE) overwrite
	$(MAKE) seqwrite
	$(MAKE) seqread
	$(MAKE) writerd
	$(MAKE) stress
	$(MAKE) random

	# Phase 6
	$(MAKE) data_patterns
	$(MAKE) boundary_toggle
	$(MAKE) same_address

	@echo ""
	@echo "======================================================"
	@echo "          APB RAM REGRESSION PASSED"
	@echo "======================================================"
	@echo ""

# =====================================================
# Coverage Report
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