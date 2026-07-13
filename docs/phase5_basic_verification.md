# Phase 5 – Basic Verification Report

**Project:** APB RAM Verification using cocotb + Verilator  
**Author:** Andrew Abdi  
**Phase:** Phase 5 – Basic Verification  
**Date:** July 13, 2026

---

# 1. Overview

Phase 5 focused on verifying the fundamental functionality of the APB RAM design using directed test cases.

The objective was to confirm that the DUT correctly performs APB read and write transactions, properly initializes memory after reset, handles valid and invalid address accesses, and behaves correctly under common operating scenarios before proceeding to constrained-random verification.

All directed tests completed successfully.

---

# 2. Verification Objectives

The following verification objectives were defined for Phase 5:

- Verify basic APB write transactions
- Verify basic APB read transactions
- Verify reset behavior
- Verify memory initialization after reset
- Verify valid boundary addresses
- Verify illegal address handling
- Verify overwrite behavior
- Verify sequential memory accesses
- Verify immediate read-after-write behavior

---

# 3. Test Environment

The verification environment consisted of:

- cocotb Python testbench
- Verilator simulator
- SystemVerilog RTL
- APB helper functions
- Python utility library (`tb_utils.py`)
- Makefile automation
- GTKWave waveform generation

---

# 4. Directed Test Suite

| Test ID | Test | Verification Objective | Result |
|----------|------|------------------------|--------|
| DT001 | Smoke Test | Basic APB write/read operation | ✅ PASS |
| DT002 | Reset Test | Verify DUT reset functionality | ✅ PASS |
| DT003 | Address 0 Test | Verify lowest valid memory address | ✅ PASS |
| DT004 | Address 31 Test | Verify highest valid memory address | ✅ PASS |
| DT005 | Default Memory Test | Verify memory initializes to zero after reset | ✅ PASS |
| DT006 | Overwrite Test | Verify new writes replace previous data | ✅ PASS |
| DT007 | Sequential Write Test | Verify writes to every valid address | ✅ PASS |
| DT008 | Sequential Read Test | Verify reads from every valid address | ✅ PASS |
| DT009 | Illegal Address Test | Verify PSLVERR generation for invalid addresses | ✅ PASS |
| DT010 | Immediate Write/Read Test | Verify read-after-write functionality | ✅ PASS |
| DT011 | Stress Back-to-Back Test | Verify consecutive APB transactions | ✅ PASS |

---

# 5. Verification Results

The directed verification suite successfully exercised all major functional requirements of the APB RAM.

The following features were verified:

## Reset

- Active-low reset
- Memory initialization
- Output signal reset

## Write Path

- Single write
- Sequential writes
- Memory overwrite
- Boundary addresses

## Read Path

- Single read
- Sequential reads
- Immediate read-after-write

## Addressing

- Address 0
- Address 31
- Illegal addresses

## APB Protocol

- Setup phase
- Access phase
- Read transactions
- Write transactions
- Back-to-back transfers

---

# 6. Testbench Improvements

Several improvements were made during Phase 5.

## Reusable Helper Functions

The helper library (`tb_utils.py`) was expanded to include reusable APB transaction utilities.

Implemented helper functions include:

- `reset_dut()`
- `apb_write()`
- `apb_read()`
- `initialize_memory_pattern()`
- `apb_write_expect_error()`
- `apb_read_expect_error()`

These utilities significantly reduced duplicated code across the directed test suite.

---

# 7. Challenges Encountered

Several issues were identified and resolved during Phase 5.

### APB Transaction Timing

Additional clock cycles were added after APB transactions to correctly model the TRANSFER state of the DUT.

### Test Reusability

Common APB transaction code was consolidated into reusable helper functions to improve maintainability.

### Memory Initialization

A reusable initialization routine was created to generate a consistent memory pattern for multiple tests.

---

# 8. Lessons Learned

During Phase 5, several important verification concepts were reinforced:

- Directed tests should verify a single objective whenever possible.
- Reusable helper functions simplify test development.
- Boundary testing is essential for memory verification.
- Clear logging simplifies debugging.
- Deterministic tests provide a stable foundation before constrained-random verification.

---

# 9. Phase 5 Summary

Phase 5 was completed successfully.

Achievements include:

- 11 directed tests implemented
- All directed tests passing
- Reusable cocotb verification utilities developed
- APB helper library established
- Verification plan updated
- Project documentation expanded

Phase 5 provides a solid verification baseline for moving into constrained-random verification.

---

# 10. Next Phase

The next project milestone is **Phase 6 – Functional Verification**.

Upcoming work includes:

- Randomized APB transactions
- Corner-case testing
- Protocol compliance testing
- Stress testing
- Additional negative testing

The directed verification suite completed in Phase 5 will serve as the regression baseline for all future verification work.

---

# End of Report