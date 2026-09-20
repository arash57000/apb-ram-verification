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

TOPLEVEL := tb_top

# Default test (can override)
MODULE ?= tests.test_smoke

.PHONY: smoke reset addr0 addr31 read_default overwrite seqwrite seqread \
        writerd random data_patterns boundary_toggle same_address \
        reset_during_transaction post_reset_access illegal_write illegal_read \
        setup_no_enable write_data_change recovery_after_error \
        random_write_readback random_read_write random_memory_sweep \
        random_illegal_access stress stress_repeat stress_full_memory \
        stress_mixed enable_no_select address_change pwritechange pwdatachange \
        basic corner negative random_tests stress_tests protocol regress \
        regress-coverage coverage clean-all


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
# Coverage
# -----------------------------

COVERAGE_DIR := coverage_runs
COVERAGE_TEST_DIR := $(COVERAGE_DIR)/tests
COVERAGE_MERGED_DIR := $(COVERAGE_DIR)/merged

FUNCTIONAL_COVERAGE_DIR := functional_coverage
FUNCTIONAL_COVERAGE_TEST_DIR := $(FUNCTIONAL_COVERAGE_DIR)/tests
FUNCTIONAL_COVERAGE_MERGED_DIR := $(FUNCTIONAL_COVERAGE_DIR)/merged
define SAVE_COVERAGE
	mkdir -p $(COVERAGE_TEST_DIR)
	cp coverage.dat $(COVERAGE_TEST_DIR)/$(1).dat
endef


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
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_smoke
	$(call SAVE_COVERAGE,smoke)
reset:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_reset
	$(call SAVE_COVERAGE,reset)
addr0:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_addr0
	$(call SAVE_COVERAGE,addr0)

addr31:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_addr31
	$(call SAVE_COVERAGE,addr31)

read_default:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_read_default
	$(call SAVE_COVERAGE,read_default)

overwrite:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_overwrite
	$(call SAVE_COVERAGE,overwrite)

seqwrite:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_sequential_write
	$(call SAVE_COVERAGE,seqwrite)

seqread:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_sequential_read
	$(call SAVE_COVERAGE,seqread)

writerd:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_write_read_immediate
	$(call SAVE_COVERAGE,writerd)

random:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_random_basic
	$(call SAVE_COVERAGE,random)

# =====================================================
# Phase 6 — Functional Verification
# =====================================================

# -----------------------------
# Corner-Case Tests
# -----------------------------

data_patterns:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_data_patterns
	$(call SAVE_COVERAGE,data_patterns)

# Future Corner-Case Tests

boundary_toggle:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_boundary_toggle
	$(call SAVE_COVERAGE,boundary_toggle)

same_address:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_same_address_repeated
	$(call SAVE_COVERAGE,same_address)

reset_during_transaction:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_reset_during_transaction
	$(call SAVE_COVERAGE,reset_during_transaction)
post_reset_access:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_post_reset_access
	$(call SAVE_COVERAGE,post_reset_access)

# -----------------------------
# Negative Tests
# -----------------------------
illegal_write:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_illegal_write_address
	$(call SAVE_COVERAGE,illegal_write)
illegal_read:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_illegal_read_address
	$(call SAVE_COVERAGE,illegal_read)
setup_no_enable:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_setup_without_enable
	$(call SAVE_COVERAGE,setup_no_enable)

write_data_change:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_write_data_changes_during_access
	$(call SAVE_COVERAGE,write_data_change)
recovery_after_error:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_recovery_after_illegal_access
	$(call SAVE_COVERAGE,recovery_after_error)
# Future targets

# -----------------------------
# Random Tests
# -----------------------------
random_write_readback:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_random_write_readback
	$(call SAVE_COVERAGE,random_write_readback)
random_read_write:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_random_read_write
	$(call SAVE_COVERAGE,random_read_write)
random_memory_sweep:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_random_memory_sweep
	$(call SAVE_COVERAGE,random_memory_sweep)
random_illegal_access:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_random_illegal_access
	$(call SAVE_COVERAGE,random_illegal_access)
# Future targets

# -----------------------------
# Stress Tests
# -----------------------------
stress:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_stress_back2back
	$(call SAVE_COVERAGE,stress)
stress_repeat:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_stress_repeated_address
	$(call SAVE_COVERAGE,stress_repeat)
stress_full_memory:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_stress_full_memory
	$(call SAVE_COVERAGE,stress_full_memory)
stress_mixed:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_stress_mixed_traffic
	$(call SAVE_COVERAGE,stress_mixed)
# Future targets

# =====================================================
# Protocol Verification
# =====================================================

# Protocol Robustness Tests

enable_no_select:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_enable_without_select
	$(call SAVE_COVERAGE,enable_no_select)

# Protocol Behavior Characterization Tests

address_change:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_address_changes_during_access
	$(call SAVE_COVERAGE,address_change)

pwritechange:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_pwrite_changes_during_access
	$(call SAVE_COVERAGE,pwritechange)

pwdatachange:
	$(MAKE) clean
	$(MAKE) SIM=$(SIM) MODULE=tests.test_pwdata_changes_during_access
	$(call SAVE_COVERAGE,pwdatachange)
# =====================================================
# Test Groups
# =====================================================

basic:
	$(MAKE) smoke
	$(MAKE) reset
	$(MAKE) addr0
	$(MAKE) addr31
	$(MAKE) read_default
	$(MAKE) overwrite
	$(MAKE) seqwrite
	$(MAKE) seqread
	$(MAKE) writerd
	$(MAKE) random

corner:
	$(MAKE) data_patterns
	$(MAKE) boundary_toggle
	$(MAKE) same_address
	$(MAKE) reset_during_transaction
	$(MAKE) post_reset_access

negative:
	$(MAKE) illegal_write
	$(MAKE) illegal_read
	$(MAKE) setup_no_enable
	$(MAKE) write_data_change
	$(MAKE) recovery_after_error

random_tests:
	$(MAKE) random_write_readback
	$(MAKE) random_read_write
	$(MAKE) random_memory_sweep
	$(MAKE) random_illegal_access

stress_tests:
	$(MAKE) stress
	$(MAKE) stress_repeat
	$(MAKE) stress_full_memory
	$(MAKE) stress_mixed

protocol:
	$(MAKE) enable_no_select
	$(MAKE) address_change
	$(MAKE) pwritechange
	$(MAKE) pwdatachange
# =====================================================
# Run Full Regression
# =====================================================

regress:
	@echo ""
	@echo "======================================================"
	@echo "        APB RAM FULL REGRESSION STARTED"
	@echo "======================================================"
	@echo ""

	$(MAKE) basic
	$(MAKE) corner
	$(MAKE) negative
	$(MAKE) random_tests
	$(MAKE) stress_tests
	$(MAKE) protocol

	@echo ""
	@echo "======================================================"
	@echo "          APB RAM REGRESSION PASSED"
	@echo "======================================================"

# =====================================================
# Full Regression + Coverage
# =====================================================

regress-coverage:
	$(MAKE) regress
	$(MAKE) coverage

# =====================================================
# Coverage Report
# =====================================================

coverage:
	rm -rf $(COVERAGE_DIR)/annotated
	mkdir -p $(COVERAGE_MERGED_DIR)
	mkdir -p $(COVERAGE_DIR)/annotated
	verilator_coverage --write $(COVERAGE_MERGED_DIR)/regression.dat $(COVERAGE_TEST_DIR)/*.dat
	verilator_coverage --annotate $(COVERAGE_DIR)/annotated --annotate-all $(COVERAGE_MERGED_DIR)/regression.dat
	@echo ""
	@echo "======================================================"
	@echo "        APB RAM COVERAGE REPORT COMPLETE"
	@echo "======================================================"
# =====================================================
# Functional Coverage Report
# =====================================================

functional-coverage:
	python scripts/merge_functional_coverage.py \
		--input-dir $(FUNCTIONAL_COVERAGE_TEST_DIR) \
		--output $(FUNCTIONAL_COVERAGE_MERGED_DIR)/regression.json

# =====================================================
# Full Regression + Functional Coverage
# =====================================================

regress-functional-coverage:
	$(MAKE) clean-functional-coverage
	rm -rf $(COVERAGE_DIR)
	$(MAKE) regress
	$(MAKE) coverage
	$(MAKE) functional-coverage
# =====================================================
# Clean Functional Coverage
# =====================================================

clean-functional-coverage:
	rm -rf $(FUNCTIONAL_COVERAGE_DIR)
# =====================================================
# Utility
# =====================================================

clean-all:
	$(MAKE) clean
	rm -rf coverage_runs
	rm -rf functional_coverage
	rm -f coverage.dat
	rm -f results.xml
