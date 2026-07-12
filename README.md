# APB RAM Verification Project

**ASIC / SoC Design Verification Project**

SystemVerilog • APB • Cocotb • Python • Verilator • GTKWave • Linux

---

# Project Status

## Current Phase

- ✅ Phase 1 – Planning
- ✅ Phase 2 – Repository Setup
- ✅ Phase 3 – RTL Development
- ✅ Phase 4 – Testbench Development
- ✅ Phase 5 – Basic Verification

### Verification Progress

| Test | Status |
|------|--------|
| Smoke Test | ✅ PASS |
| Reset Test | ✅ PASS |
| Address 0 | ✅ PASS |
| Address 31 | ✅ PASS |
| Read Default | ✅ PASS |
| Overwrite | ✅ PASS |
| Sequential Write | ✅ PASS |
| Sequential Read | ✅ PASS |

### Next Phase

➡️ Phase 6 – Random & Negative Testing

---

# Project Overview

This project implements and verifies an APB RAM peripheral using an open-source verification flow.

The objective is to demonstrate a professional ASIC/SoC Design Verification workflow including:

- RTL verification
- APB protocol verification
- Cocotb-based verification environment
- Directed testing
- Functional coverage
- Scoreboard checking
- Regression-ready test structure
- Waveform debugging

The DUT is a 32-word × 32-bit APB RAM supporting:

- Read
- Write
- Reset
- Illegal address detection
- PSLVERR generation

---

---

# APB Protocol

This project verifies an **Advanced Peripheral Bus (APB)** slave implementing a
32 × 32-bit RAM peripheral.

For a detailed explanation of the APB protocol, including:

- Bus architecture
- APB timing
- Bus signals
- Read transactions
- Write transactions
- Error handling (PSLVERR)
- Reset behavior
- APB state machine

see:

```
docs/apb_protocol.md
``` 

# Repository Structure

```
apb-ram-verification/

├── docs/
│   ├── verification_plan.md
│   └── weekly_notes.md
│
├── rtl/
│   ├── apb_ram.sv
│   ├── apb_if.sv
│   └── tb_top.sv
│
├── tb/
│   └── cocotb/
│       ├── agents/
│       ├── env/
│       ├── sequences/
│       └── tests/
│
├── scripts/
├── coverage/
├── results/
├── Makefile
└── README.md
```

---

# Current Repository Status

| Item | Status |
|------|--------|
| RTL | ✅ Complete |
| Cocotb Environment | ✅ Complete |
| Driver | ✅ Complete |
| Monitor | ✅ Complete |
| Scoreboard | ✅ Complete |
| Coverage Collector | ✅ Complete |
| Directed Tests | ✅ Complete |
| Random Tests | 🚧 In Progress |
| Regression | 🚧 Planned |

# Design Under Test

APB RAM

Features

- 32 × 32-bit memory
- APB slave interface
- FSM implementation
- Active-low reset
- Illegal address detection
- PSLVERR support
- Synchronous operation

---

# Verification Environment

The verification environment follows a layered, UVM-inspired architecture implemented in Cocotb.

Components

- Driver
- Monitor
- Agent
- Environment
- Scoreboard
- Coverage
- Directed Tests

---

# Completed Verification

## Smoke

- DUT boots correctly

## Reset

- Reset initializes outputs
- Memory reset verified

## Directed Tests

- Address 0
- Address 31
- Default Read
- Overwrite
- Sequential Write
- Sequential Read

---

# Planned Verification

Phase 6

- Random transactions
- Random read/write sequences
- Illegal address tests
- Back-to-back transactions

Phase 7

- Functional coverage closure
- Code coverage improvements

Phase 8

- Automated regression
- CI integration

---

# Coverage Goals

Functional coverage includes:

- Read operations
- Write operations
- Boundary addresses
- Illegal addresses
- Reset behavior
- Sequential accesses

Code coverage includes:

- FSM states
- Error paths
- Normal paths

---

# Running the Project

Compile and run

```bash
make
```

Run a specific test

```bash
make MODULE=tests.test_smoke
```

View waveforms

```bash
gtkwave waves/dump.vcd
```

Generate coverage

```bash
make coverage
```

---

# Tools Used

| Category | Tool |
|----------|------|
| RTL | SystemVerilog |
| Verification | Cocotb |
| Language | Python |
| Simulator | Verilator |
| Waveforms | GTKWave |
| OS | Ubuntu Linux |
| Version Control | Git & GitHub |

---

# Skills Demonstrated

- APB Protocol Verification
- SystemVerilog RTL
- Cocotb Verification
- Python Test Development
- Scoreboard Design
- Driver Development
- Monitor Development
- Functional Coverage
- Linux Workflow
- Git Version Control
- Waveform Debugging

---

# Future Work

- Random verification
- Constrained-random testing
- Functional coverage closure
- Coverage reports
- Regression automation
- GitHub Actions CI

---

# Documentation

Project documentation is available in the `docs/` directory.

| Document | Description |
|----------|-------------|
| apb_protocol.md | APB protocol overview, timing, signals, and transactions |
| verification_plan.md | Verification objectives, test plan, and coverage goals |
| weekly_notes.md | Weekly engineering progress and lessons learned |

# Author

**Andrew Abdi**

ASIC / SoC Design Verification Engineer

SystemVerilog • UVM • Cocotb • Python • APB • Verilator • Linux
