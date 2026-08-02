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

reset_during_transaction:
	make clean
	make SIM=$(SIM) MODULE=tests.test_reset_during_transaction
#
post_reset_access:
	make clean
	make SIM=$(SIM) MODULE=tests.test_post_reset_access

# -----------------------------
# Negative Tests
# -----------------------------
illegal_write:
	make clean
	make SIM=$(SIM) MODULE=tests.test_illegal_write_address
illegal_read:
	make clean
	make SIM=$(SIM) MODULE=tests.test_illegal_read_address
setup_no_enable:
	make clean
	make SIM=$(SIM) MODULE=tests.test_setup_without_enable	
enable_no_select:
	make clean
	make SIM=$(SIM) MODULE=tests.test_enable_without_select	
address_change:
	make clean
	make SIM=$(SIM) MODULE=tests.test_address_changes_during_access
write_data_change:
	make clean
	make SIM=$(SIM) MODULE=tests.test_write_data_changes_during_access
recovery_after_error:
	make clean
	make SIM=$(SIM) MODULE=tests.test_recovery_after_illegal_access
# Future targets

# -----------------------------
# Random Tests
# -----------------------------
random_write_readback:
	make clean
	make SIM=$(SIM) MODULE=tests.test_random_write_readback
random_read_write:
	make clean
	make SIM=$(SIM) MODULE=tests.test_random_read_write
random_memory_sweep:
	make clean
	make SIM=$(SIM) MODULE=tests.test_random_memory_sweep
random_illegal_access:
	make clean
	make SIM=$(SIM) MODULE=tests.test_random_illegal_access
# Future targets

# -----------------------------
# Stress Tests
# -----------------------------
stress:
	make clean
	make SIM=$(SIM) MODULE=tests.test_stress_back2back
stress_repeat:
	make clean
	make SIM=$(SIM) MODULE=tests.test_stress_repeated_address
stress_full_memory:
	make clean
	make SIM=$(SIM) MODULE=tests.test_stress_full_memory
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
	$(MAKE) reset_during_transaction
	$(MAKE) post_reset_access
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