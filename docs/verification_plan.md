# APB RAM Verification Plan

**Project:** APB RAM Verification using Cocotb and Verilator

**Author:** Andrew Abdi

**Document Version:** 3.0

**Date:** October 6, 2026

---

## 1. Purpose

This document defines the final verification plan and implemented verification strategy for the APB RAM design.

It describes:

- DUT functionality and verification scope
- Verification objectives
- Active Cocotb testbench architecture
- Directed, random, negative, corner-case, stress, and protocol-characterization testing
- Functional and code-coverage strategy
- Regression and reporting flow
- Pass criteria and final results
- Assumptions, risks, exclusions, and deliverables

The goal is to provide evidence that the APB RAM correctly performs legal read and write transactions, stores and retrieves data accurately, responds properly to reset, detects illegal addresses, recovers after errors, and remains reliable under randomized and sustained traffic.

---

## 2. Project Verification Progress

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Planning | Complete |
| Phase 2 | Repository setup | Complete |
| Phase 3 | RTL development | Complete |
| Phase 4 | Testbench development | Complete |
| Phase 5 | Basic verification | Complete |
| Phase 6 | Functional verification | Complete |
| Phase 7 | Coverage | Complete |
| Phase 8 | Regression and reporting | Complete |
| Phase 9 | Waveform debugging | Complete |
| Phase 10 | Documentation | In progress |
| Phase 11 | Final release | Planned |

---

## 3. Design Overview

The Device Under Test (DUT) is a synchronous APB slave containing a 32-word × 32-bit memory.

The design supports:

- APB write transactions
- APB read transactions
- Synchronous active-low reset
- Legal-address detection
- Illegal-address error reporting
- Ready signaling
- Data storage and retrieval
- Consecutive transfers

The memory contains:

```systemverilog
logic [31:0] mem [0:31];
```

This represents:

- 32 memory locations
- 32 bits per location
- 1,024 total bits
- 128 total bytes

Although `paddr` is 32 bits wide, the RTL interprets it directly as a RAM word index.

| Address | Classification | Behavior |
|---:|---|---|
| `0–31` | Legal | Accesses `mem[0]` through `mem[31]` |
| `32` or greater | Illegal | Asserts `pslverr` |

---

## 4. DUT Interface

### 4.1 Inputs

| Signal | Width | Description |
|---|---:|---|
| `pclk` | 1 | APB clock |
| `presetn` | 1 | Synchronous active-low reset |
| `psel` | 1 | APB slave select |
| `penable` | 1 | APB ACCESS-phase indicator |
| `pwrite` | 1 | Write when high and read when low |
| `paddr` | 32 | Direct RAM word index |
| `pwdata` | 32 | Write data |

### 4.2 Outputs

| Signal | Width | Description |
|---|---:|---|
| `prdata` | 32 | Read data |
| `pready` | 1 | Transfer-completion indication |
| `pslverr` | 1 | Illegal-access indication |

For detailed protocol and timing information, refer to:

```text
docs/apb_protocol.md
```

For design and testbench architecture, refer to:

```text
docs/architecture.md
```

---

## 5. Verification Scope

### 5.1 In Scope

The verification environment checks:

- Legal writes to every RAM address
- Legal reads from every RAM address
- Read-after-write behavior
- Default memory contents after reset
- Overwriting previously written locations
- Boundary addresses 0 and 31
- Important 32-bit data patterns
- Back-to-back transfers
- Repeated access to the same address
- Reset during a transaction
- First access after reset
- Illegal read addresses
- Illegal write addresses
- Error recovery
- Random legal read and write traffic
- Random illegal accesses
- Full-memory sweeps
- Sustained and mixed traffic
- Behavior under intentionally unstable APB master signals
- Functional coverage
- Verilator code coverage
- Automated regression and reporting
- Waveform-based debugging

### 5.2 Out of Scope

The following features are not implemented or verified:

- Multiple APB masters
- Multiple APB slaves
- Overlapping transfers
- Programmable wait-state insertion
- APB4 signals such as `PSTRB` and `PPROT`
- Byte-address translation
- Partial writes
- Clock-domain crossing
- Power-aware verification
- Formal verification
- FPGA or post-silicon validation
- Performance or bandwidth analysis

---

## 6. Verification Objectives

The verification objectives are:

1. Confirm that legal writes store the expected 32-bit data.
2. Confirm that legal reads return the most recently stored value.
3. Verify all 32 legal memory addresses.
4. Verify the lowest and highest legal addresses.
5. Confirm that reset clears memory and control outputs.
6. Confirm that the DUT accepts transfers after reset.
7. Confirm that illegal accesses assert `pslverr`.
8. Confirm that illegal writes do not corrupt legal memory.
9. Confirm that the DUT recovers after an illegal access.
10. Verify important data patterns.
11. Exercise back-to-back and repeated transactions.
12. Exercise randomized legal and illegal traffic.
13. Compare randomized behavior against a Python reference model.
14. Characterize RTL behavior when APB master signals are unstable.
15. Achieve functional coverage closure.
16. Analyze code-coverage holes and document justified exclusions.
17. Run all tests automatically and preserve machine-readable results.
18. Generate waveforms for failure analysis and debugging.

---

## 7. Verification Environment

The active verification environment contains:

| Component | Purpose |
|---|---|
| SystemVerilog DUT | Implements the APB RAM |
| `tb_top.sv` | Connects DUT signals to Cocotb |
| Cocotb tests | Generate stimulus and perform checking |
| `tb_utils.py` | Provides reset, read, write, and error-access helpers |
| `ApbMonitor` | Observes completed transfers |
| `ApbCoverage` | Collects functional coverage |
| Local reference models | Track expected memory contents |
| Verilator | Compiles and simulates the RTL |
| Makefile | Runs individual tests and regression groups |
| Regression report script | Summarizes saved XML results |
| GTKWave | Displays waveforms for debugging |

### 7.1 Active Data Flow

```text
Cocotb test
    ↓
APB helper function
    ↓
tb_top
    ↓
apb_ram DUT
    ↓
Assertions or reference-model comparison
```

The monitoring and coverage path is:

```text
apb_ram DUT
    ↓
ApbMonitor
    ↓
ApbCoverage
    ↓
Per-test functional-coverage JSON
```

### 7.2 Reusable Components

The repository also contains reusable components such as:

- `ApbDriver`
- `ApbAgent`
- `ApbScoreboard`
- `ApbEnv`
- `RegressionEnv`
- Sequence classes
- SystemVerilog `apb_if`

These components demonstrate a layered UVM-inspired structure, but they are not directly instantiated by the current 32-test regression.

The active regression uses helper functions, direct assertions, local reference models, the monitor, and the functional coverage collector.

---

## 8. Verification Strategy

The verification strategy combines multiple complementary methods:

| Method | Purpose |
|---|---|
| Directed tests | Verify specific features with deterministic stimulus |
| Boundary tests | Verify the lowest and highest legal addresses |
| Corner-case tests | Exercise reset timing, data patterns, and repeated operations |
| Negative tests | Verify illegal accesses and incomplete transfers |
| Random tests | Exercise varying legal and illegal transactions |
| Reference-model checking | Compare DUT state against expected Python memory state |
| Stress tests | Exercise sustained, repeated, and mixed traffic |
| Protocol characterization | Document behavior under invalid master signal sequences |
| Functional coverage | Measure whether important scenarios occurred |
| Code coverage | Measure executed RTL coverage points |
| Waveform debugging | Diagnose signal timing and state transitions |
| Regression automation | Run the entire suite consistently |

---

## 9. Directed Testing

Directed tests use known addresses, data values, and expected results.

The basic regression group contains:

| Test | Objective | Status |
|---|---|---|
| Smoke | Basic write and readback | Complete |
| Reset | Reset followed by legal access | Complete |
| Address 0 | Lowest legal address | Complete |
| Address 31 | Highest legal address | Complete |
| Default memory read | All locations contain zero after reset | Complete |
| Overwrite | Latest write replaces the previous value | Complete |
| Sequential write | Write every legal address | Complete |
| Sequential read | Read every legal address | Complete |
| Immediate write/read | Read an address immediately after writing it | Complete |
| Random basic | Basic randomized legal reads and writes | Complete |

---

## 10. Corner-Case Testing

The corner-case group contains:

| Test | Objective | Status |
|---|---|---|
| Data patterns | Verify important 32-bit patterns | Complete |
| Boundary toggle | Alternate between addresses 0 and 31 | Complete |
| Same address repeated | Repeatedly overwrite and read one address | Complete |
| Reset during transaction | Assert reset during an active write | Complete |
| Post-reset access | Execute the first transfer immediately after reset | Complete |

The important data patterns are:

- `0x00000000`
- `0xFFFFFFFF`
- `0xAAAAAAAA`
- `0x55555555`
- `0x80000000`
- `0x00000001`
- `0x7FFFFFFF`
- `0xFFFFFFFE`

---

## 11. Negative Testing

The negative-test group contains:

| Test | Objective | Status |
|---|---|---|
| Illegal write | Verify error response and prevent memory corruption | Complete |
| Illegal read | Verify error response for invalid read addresses | Complete |
| SETUP without enable | Confirm that no transfer occurs without ACCESS | Complete |
| Write-data change | Characterize behavior when write data changes during a transfer | Complete |
| Recovery after error | Verify legal operation immediately after an error | Complete |

Negative tests verify both the error response and the DUT’s ability to continue operating after the error condition.

---

## 12. Randomized Testing

Random tests select addresses, data, operation types, transaction order, and transaction count within explicit constraints.

### 12.1 Randomized Fields

The randomized fields include:

- Legal or illegal address
- 32-bit write data
- Read or write operation
- Transaction order
- Number of transactions

### 12.2 Legal-Traffic Constraints

Legal random traffic obeys the following constraints:

- Legal addresses range from 0 through 31.
- Write data is limited to 32 bits.
- SETUP and ACCESS phases follow the helper-driven sequence.
- Only one transfer occurs at a time.
- Transfers do not overlap.

### 12.3 Implemented Random Tests

| Test | Objective | Status |
|---|---|---|
| Random write/readback | Random write followed by same-address readback | Complete |
| Random read/write | Random legal mixture checked against a model | Complete |
| Random memory sweep | Long random sequence followed by full-memory checking | Complete |
| Random illegal access | Repeated illegal accesses with periodic legal checks | Complete |

The basic group also contains `test_random_basic`, which performs randomized legal reads and writes.

### 12.4 Reference Model

Random and stress tests use a Python memory model:

```text
Write:
    Drive DUT write
    Update expected model

Read:
    Read from DUT
    Compare against expected model
```

This allows the transaction sequence to vary while maintaining deterministic checking.

---

## 13. Stress Testing

The stress group contains:

| Test | Objective | Status |
|---|---|---|
| Back-to-back stress | Sustained writes and reads across all addresses | Complete |
| Repeated-address stress | Repeated write/read activity at one location | Complete |
| Full-memory stress | Multiple complete write/read memory cycles | Complete |
| Mixed-traffic stress | Long randomized mixture of reads and writes | Complete |

Stress tests look for:

- Data corruption
- Stale data
- Address-decoding failures
- State-machine recovery problems
- Failures caused by repeated activity

---

## 14. Protocol-Behavior Characterization

APB requires `paddr`, `pwrite`, and `pwdata` to remain stable from SETUP through ACCESS.

The following tests intentionally violate those master-side requirements:

| Test | Intent | Status |
|---|---|---|
| Enable without select | Assert `penable` without `psel` | Complete |
| Address changes during ACCESS | Change `paddr` after SETUP | Complete |
| Direction changes during ACCESS | Change `pwrite` after SETUP | Complete |
| Write data changes during ACCESS | Change `pwdata` after SETUP | Complete |

These tests are not protocol-compliance tests. They characterize the existing RTL behavior under invalid master stimulus.

The observed implementation samples the current address, direction, and write data when the transfer completes during ACCESS.

---

## 15. Functional Coverage Plan

The functional coverage model contains 119 bins:

| Coverage group | Bins | Purpose |
|---|---:|---|
| Operation | 2 | Read and write |
| Legal address | 32 | Every legal address |
| Address type | 2 | Legal and illegal |
| Boundary | 2 | Addresses 0 and 31 |
| Error | 2 | `pslverr=0` and `pslverr=1` |
| Data pattern | 8 | Important 32-bit patterns |
| Sequence | 2 | Back-to-back and write/read-same-address |
| Operation × address type | 4 | Legal and illegal reads and writes |
| Operation × legal address | 64 | Read and write at every legal address |
| Reset | 1 | Reset observed |
| **Total** | **119** | |

### 15.1 Functional Coverage Goal

Target:

```text
95% or higher
```

Final result:

```text
119/119 bins = 100%
```

Status:

```text
Goal exceeded
```

---

## 16. Code Coverage Plan

Verilator code coverage is collected for the RTL and merged across the full regression.

The coverage workflow includes:

- Per-test coverage data
- Merged regression coverage
- Annotated RTL coverage
- LCOV-format reporting
- Coverage-hole analysis
- Justified exclusion of structurally unreachable logic

### 16.1 Original Code Coverage Goal

The original planning target was:

```text
95% or higher
```

### 16.2 Final Code Coverage Result

```text
56/59 coverage points = 94%
```

The result is one percentage point below the original aspirational target.

Coverage closure was accepted at 94% after:

- Running all 32 tests
- Achieving 100% functional coverage
- Reviewing the remaining code-coverage holes
- Excluding the structurally unreachable defensive FSM default branch
- Confirming that no known critical functional bug remained

### 16.3 FSM Default Exclusion

The FSM state variable is two bits wide, and all four possible two-bit encodings are assigned:

```text
00 = IDLE
01 = SETUP
10 = ACCESS
11 = TRANSFER
```

Verilator uses two-state simulation for this design. Therefore, an unknown or high-impedance state cannot be injected to reach the defensive default branch.

The following branch is retained for defensive RTL coding but excluded from Verilator coverage:

```systemverilog
/* verilator coverage_off */
default: state <= IDLE;
/* verilator coverage_on */
```

---

## 17. Regression Strategy

The Makefile organizes the 32 tests into six groups:

| Group | Tests |
|---|---:|
| `basic` | 10 |
| `corner` | 5 |
| `negative` | 5 |
| `random_tests` | 4 |
| `stress_tests` | 4 |
| `protocol` | 4 |
| **Total** | **32** |

The full regression is launched with:

```bash
make regress
```

The regression:

1. Clears previous per-test results.
2. Runs all six groups.
3. Preserves individual XML result files.
4. Stops and reports failure if a group fails.
5. Generates the final regression report.

The final text report is stored at:

```text
results/regression_report.txt
```

For the complete test inventory, refer to:

```text
docs/test_summary.md
```

---

## 18. Debug Strategy

The debugging process uses:

- Cocotb log messages
- Assertion failure messages
- Saved XML results
- Verilator waveform tracing
- GTKWave signal inspection
- RTL state and APB phase analysis
- Focused single-test reruns
- Full regression reruns after a correction

The Phase 9 debugging exercise deliberately introduced an incorrect expected value, observed the assertion failure, inspected the waveform, restored the correct check, and reran the test and regression successfully.

Signals inspected during waveform debugging include:

- `pclk`
- `presetn`
- `psel`
- `penable`
- `pwrite`
- `paddr`
- `pwdata`
- `prdata`
- `pready`
- `pslverr`
- FSM state

---

## 19. Pass and Exit Criteria

Verification is accepted when:

- All 32 regression tests pass.
- No test is unexpectedly skipped.
- Legal read and write behavior is verified.
- Illegal-address behavior is verified.
- Reset behavior is verified.
- Reference-model comparisons pass.
- Functional coverage reaches at least 95%.
- Code coverage is reviewed and justified.
- No known critical functional bug remains.
- Regression reporting completes successfully.
- Documentation records the final architecture, strategy, tests, coverage, and lessons learned.

### 19.1 Final Exit-Criteria Status

| Criterion | Final status |
|---|---|
| All regression tests pass | Met — 32/32 |
| No skipped tests | Met — 0 skipped |
| Legal reads and writes verified | Met |
| All legal addresses verified | Met |
| Illegal accesses verified | Met |
| Reset behavior verified | Met |
| Error recovery verified | Met |
| Random and stress testing complete | Met |
| Functional coverage target | Met — 100% |
| Code coverage reviewed | Met — 94% with documented analysis |
| No known critical functional bugs | Met |
| Automated regression report | Met |
| Architecture documentation | Met |
| Test-summary documentation | Met |
| Phase 10 final documentation | In progress |

---

## 20. Assumptions

The verification plan uses the following assumptions:

- One APB master
- One APB slave
- One transfer at a time
- No overlapping transactions
- No programmable wait-state insertion
- Direct word-index addressing
- Fixed memory depth of 32 words
- Fixed data width of 32 bits
- Synchronous active-low reset
- APB master signals remain stable during legal transfers

---

## 21. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Missing address coverage | Read and write every legal address |
| Boundary-decoding error | Dedicated address 0, address 31, and boundary-toggle tests |
| Memory corruption | Reference-model comparisons and full-memory sweeps |
| Error response not exercised | Directed and randomized illegal accesses |
| DUT remains stuck after an error | Recovery-after-error testing |
| Reset timing issue | Reset and reset-during-transaction tests |
| Missing data-pattern behavior | Eight dedicated data-pattern bins |
| Random-only bug is not reproducible | Preserve deterministic test structure and logs |
| Long-traffic corruption | Stress and mixed-traffic tests |
| Protocol ambiguity | Separate legal testing from behavior-characterization tests |
| Coverage number hides a hole | Inspect uncovered points and annotated RTL |
| Structurally unreachable branch reduces coverage | Document and exclude the defensive FSM default branch |
| Regression result is lost | Preserve per-test XML and generate a text report |

---

## 22. Deliverables

The project deliverables include:

- SystemVerilog APB RAM RTL
- SystemVerilog simulation wrapper
- Reusable APB interface
- Cocotb testbench
- APB helper functions
- Transaction monitor
- Functional coverage model
- Directed tests
- Corner-case tests
- Negative tests
- Random tests
- Stress tests
- Protocol-characterization tests
- Python reference models
- Makefile regression automation
- XML test results
- Automated regression report
- Verilator code-coverage data
- Functional coverage JSON reports
- Waveform generation
- GTKWave debugging flow
- Verification plan
- APB protocol documentation
- Architecture documentation
- Test summary
- Development journal
- Phase summary documents
- Git repository and GitHub project

---

## 23. Final Verification Results

| Metric | Result |
|---|---:|
| Total tests | 32 |
| Passed tests | 32 |
| Failed tests | 0 |
| Skipped tests | 0 |
| Regression pass rate | 100% |
| Functional coverage | 119/119 bins, 100% |
| Verilator code coverage | 56/59 points, 94% |
| Known critical functional bugs | 0 |

---

## 24. Optional Future Enhancements

The following items are possible extensions and are not required for the current verification release:

- Integrate `ApbEnv`, `ApbDriver`, `ApbScoreboard`, and sequence classes into the active regression
- Add SystemVerilog Assertions for APB protocol properties
- Add a second-simulator regression
- Parameterize memory depth and data width
- Add programmable wait states
- Add APB4 `PSTRB` and `PPROT` support
- Add partial-write testing
- Add continuous-integration automation
- Add random-reset insertion
- Add formal property checking

---

## 25. Revision History

| Version | Date | Description |
|---|---|---|
| 1.0 | July 6, 2026 | Initial verification plan |
| 2.0 | July 12, 2026 | Updated after completing Phases 1–5 |
| 2.1 | July 13, 2026 | Added completed basic-verification tests and project progress |
| 3.0 | October 6, 2026 | Updated to final implemented strategy, 32-test regression, coverage results, debug flow, exit status, and Phase 10 documentation |

---

## 26. Current Project Status

Phases 1 through 9 are complete.

Phase 10 documentation is in progress. The architecture document and complete test summary are finished. The verification plan now reflects the implemented environment and verified final results.

Phase 11 will perform final cleanup, GitHub publication, release tagging, and portfolio preparation.

---

# End of Document
