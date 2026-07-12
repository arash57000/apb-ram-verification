# APB RAM Verification Plan

**Project:** APB RAM Verification using cocotb + Verilator  
**Author:** Andrew Abdi  
**Version:** 2.0  
**Date:** July 12, 2026

---

# 1. Introduction

## 1.1 Purpose

This document defines the verification strategy for the APB RAM design. It identifies the design functionality, verification objectives, planned test cases, coverage goals, and overall verification methodology.

The goal is to verify that the APB RAM correctly implements APB transactions, stores and retrieves memory data accurately, handles reset conditions, and properly detects illegal accesses.

---

# 2. Design Overview

The Device Under Test (DUT) is a simple APB slave implementing a 32-word memory.

The design supports:

- APB write transactions
- APB read transactions
- synchronous operation
- active-low reset
- illegal address detection
- ready signaling

---

# 3. DUT Features

| Feature | Description |
|----------|-------------|
| Memory depth | 32 words |
| Memory width | 32 bits |
| Interface | APB |
| Clock | pclk |
| Reset | Active-low (presetn) |
| Ready signal | pready |
| Error signal | pslverr |

---

# 4. Interface Description

## Inputs

| Signal | Width | Description |
|---------|------:|-------------|
| pclk | 1 | APB clock |
| presetn | 1 | Active-low reset |
| psel | 1 | Slave select |
| penable | 1 | Enable phase |
| pwrite | 1 | Write enable |
| paddr | 32 | Address |
| pwdata | 32 | Write data |

---

## Outputs

| Signal | Width | Description |
|---------|------:|-------------|
| prdata | 32 | Read data |
| pready | 1 | Ready signal |
| pslverr | 1 | Error indication |

---

# 5. APB Transaction Flow

This verification plan assumes standard ARM AMBA APB transaction behavior.

For a detailed explanation of:

- APB timing
- Bus phases
- Signal descriptions
- Read/write transactions
- Error handling
- Reset behavior

refer to:

docs/apb_protocol.md

# 6. Verification Objectives

The verification environment shall verify:

- Correct write operation
- Correct read operation
- Read-after-write functionality
- Reset behavior
- Illegal address handling
- Consecutive APB transactions
- Random memory accesses
- APB protocol timing

---

# 7. Verification Environment

The verification environment consists of:

- cocotb Python testbench
- Verilator simulator
- APB helper functions
- Directed tests
- Randomized tests
- Regression automation (Makefile + scripts)
- GTKWave waveform generation

---

# 8. Verification Strategy

The APB RAM verification environment uses both directed and constrained-random testing.

Directed tests verify specific known features with deterministic stimulus.  
Constrained-random tests generate legal APB transactions with randomized addresses, data, and read/write operations.

---

## 8.1 Directed Tests

Test ID	Test	Status
DT001	Smoke	✅ Complete
DT002	Reset	✅ Complete
DT003	Address 0	✅ Complete
DT004	Address 31	✅ Complete
DT005	Default Read	✅ Complete
DT006	Overwrite	✅ Complete
DT007	Sequential Write	✅ Complete
DT008	Sequential Read	✅ Complete
DT009	Illegal Address	🚧 Planned / In Progress
DT010	Stress Back-to-Back	✅ Complete
---

## 8.2 Constrained-Random Tests

| Test ID | Test Name | Objective | Status |
|----------|-----------|-----------|--------|
| CR001 | Random Basic Test | Random legal APB read/write operations | 🚧 In Progress |
| CR002 | Random Address Test | Random valid address access | Planned |
| CR003 | Random Data Pattern Test | Randomized write data patterns | Planned |
| CR004 | Random Read/Write Mix | Random read and write sequence mix | Planned |
| CR005 | Long Random Regression | Large number of randomized transactions | Planned |

---


## 8.3 Randomized Fields

The constrained-random tests may randomize:

- Address
- Write data
- Read/write operation
- Transaction order
- Number of transactions

---

## 8.4 Constraints

The constrained-random tests shall obey the following constraints:

- Valid addresses are from 0 to 31
- Data width is 32 bits
- APB setup and access phases must be legal
- Only one APB transfer occurs at a time
- No overlapping transactions are allowed

---

## 8.5 Negative and Corner-Case Tests

| Test | Purpose | Status |
|------|---------|--------|
| Boundary Address Test | Verify address 0 and address 31 | Complete |
| Invalid Address Repeat Test | Repeated illegal address accesses | Planned |
| Reset During Transaction | Reset asserted during APB transfer | Planned |
| Random Reset Test | Reset inserted randomly between transactions | Planned |
| Data Pattern Test | Verify 0x0, 0xFFFFFFFF, 0xAAAAAAAA, 0x55555555 | Planned |

---

## 8.6 Regression Strategy

The regression suite shall run all directed and constrained-random tests automatically.

Regression passes when:

- All tests pass
- No unexpected DUT errors occur
- No scoreboard mismatches occur
- Functional coverage target is reached
- Code coverage target is reached

## 8.7 Exit Criteria

Verification is considered complete when:

- All directed tests pass.
- All planned random tests pass.
- Illegal address behavior is verified.
- Functional coverage goals are met.
- No known critical functional bugs remain.

# 9. Planned Future Tests

The following tests may be added in future project phases.

| Test | Purpose |
|------|---------|
| Long Random Regression | Extended random verification |
| Protocol Violation Test | Illegal APB sequences |
| Error Injection | Corner-case verification |
| Timing Stress Test | High-frequency transaction sequences |
| Functional Coverage Closure Tests | Cover uncovered scenarios |

---

# 10. Functional Coverage Goals

The verification environment should exercise:

- All valid addresses
- Reads
- Writes
- Read-after-write
- Reset
- Illegal addresses
- Consecutive transactions
- FSM transitions

Target Functional Coverage:

> 95% or higher

---

# 11. Code Coverage Goals

Code coverage should include:

- Statement coverage
- Branch coverage
- Toggle coverage
- FSM state coverage

Target Code Coverage:

> 95% or higher

---

# 12. Pass Criteria

Verification is considered complete when:

- All directed tests pass
- All regression tests pass
- No unexpected assertions occur
- Functional coverage reaches target
- Code coverage reaches target
- No unresolved bugs remain

---

# 13. Assumptions

The following assumptions apply:

- Single APB master
- Single APB slave
- One transaction at a time
- No wait-state insertion
- Word-aligned addressing
- 32 valid memory locations

---

# 14. Risks

Potential verification risks include:

- Incomplete functional coverage
- Missing corner-case scenarios
- APB protocol violations not exercised
- Reset timing edge cases
- Address boundary conditions

These risks will be mitigated through directed tests, randomized testing, and coverage analysis.

---

# 15. Deliverables

The completed project shall include:

- RTL
- cocotb testbench
- Directed tests
- Random tests
- Regression scripts
- Waveform generation
- Coverage reports
- Documentation
- GitHub repository
-Verification Plan
-README
-APB Protocol Documentation
-Weekly Notes

---

# 16. Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | July 6, 2026 | Initial verification plan |
| 2.0 | July 12, 2026 | Updated after completing Phases 1–5, expanded directed tests, added coverage goals, exit criteria, risks, deliverables, and project status |

---

# 17. Project Status

| Item | Status |
|------|--------|
| DUT RTL | Complete |
| cocotb Environment | Complete |
| Directed Tests | Complete |
| Smoke Test | Complete |
| Reset Test | Complete |
| Illegal Address Test | In Progress |
| Stress Back-to-Back Test | Complete |
| Constrained-Random Tests | In Progress |
| Random Basic Test | In Progress |
| Long Random Regression | Planned |
| Functional Coverage | Planned |
| Code Coverage | Planned |
| Regression Script | Planned |
| Verification Plan | Complete |
---

# End of Document
