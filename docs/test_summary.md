# APB RAM Test Summary

**Project:** APB RAM Verification using Cocotb and Verilator
**Author:** Andrew Abdi
**Document Version:** 1.0
**Date:** October 6, 2026

---

## 1. Overview

This document summarizes the Cocotb tests used to verify the APB RAM design.

The regression contains 32 tests organized into six Makefile groups:

- Basic tests
- Corner-case tests
- Negative tests
- Random tests
- Stress tests
- Protocol-behavior characterization tests

The tests verify normal read and write behavior, reset operation, legal and illegal addresses, boundary conditions, data integrity, randomized traffic, sustained traffic, error recovery, and DUT behavior when APB master signals violate stability requirements.

---

## 2. Final Regression Result

The final saved regression report contains the following result:

| Metric | Result |
|---|---:|
| Total tests | 32 |
| Passed | 32 |
| Failed | 0 |
| Skipped | 0 |
| Pass rate | 100% |

```text
Total: 32  Passed: 32  Failed: 0  Skipped: 0
```

---

## 3. Regression Organization

| Makefile group | Test count | Primary purpose |
|---|---:|---|
| `basic` | 10 | Basic directed operation and initial sanity checking |
| `corner` | 5 | Boundary conditions, reset timing, and repeated operations |
| `negative` | 5 | Invalid operations, error response, and recovery |
| `random_tests` | 4 | Random legal and illegal traffic |
| `stress_tests` | 4 | Sustained and repeated traffic |
| `protocol` | 4 | Characterization of unusual or invalid APB signal sequences |
| **Total** | **32** | |

---

## 4. Basic Tests

The basic group contains ten tests:

```makefile
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
```

| Make target | Cocotb module | Verification objective | Result |
|---|---|---|---|
| `smoke` | `tests.test_smoke` | Performs a basic write and readback at address 0 to confirm fundamental DUT operation | PASS |
| `reset` | `tests.test_reset` | Applies reset and confirms that normal write/read operation succeeds afterward | PASS |
| `addr0` | `tests.test_addr0` | Verifies write and read operation at the lowest legal address, address 0 | PASS |
| `addr31` | `tests.test_addr31` | Verifies write and read operation at the highest legal address, address 31 | PASS |
| `read_default` | `tests.test_read_default` | Reads all 32 locations after reset and verifies that every location contains zero | PASS |
| `overwrite` | `tests.test_overwrite` | Writes two different values to the same address and verifies that the latest value is retained | PASS |
| `seqwrite` | `tests.test_sequential_write` | Verifies successful write transactions at every legal address from 0 through 31 | PASS |
| `seqread` | `tests.test_sequential_read` | Verifies expected data at every legal address after memory initialization | PASS |
| `writerd` | `tests.test_write_read_immediate` | Writes to a legal address and reads the same address in the next transaction | PASS |
| `random` | `tests.test_random_basic` | Performs randomized legal writes and reads and compares each read against its expected value | PASS |

The `random` target uses randomized stimulus but remains in the basic group because it performs a straightforward legal write/read verification sequence.

---

## 5. Corner-Case Tests

The corner group contains five tests:

```makefile
corner:
        $(MAKE) data_patterns
        $(MAKE) boundary_toggle
        $(MAKE) same_address
        $(MAKE) reset_during_transaction
        $(MAKE) post_reset_access
```

| Make target | Cocotb module | Verification objective | Result |
|---|---|---|---|
| `data_patterns` | `tests.test_data_patterns` | Writes and reads important 32-bit data patterns to verify data-path integrity | PASS |
| `boundary_toggle` | `tests.test_boundary_toggle` | Alternates rapidly between addresses 0 and 31 to verify boundary decoding and memory independence | PASS |
| `same_address` | `tests.test_same_address_repeated` | Repeatedly overwrites one address and verifies that every read returns the most recent value | PASS |
| `reset_during_transaction` | `tests.test_reset_during_transaction` | Asserts reset during an active write and verifies that the DUT recovers and accepts later transfers | PASS |
| `post_reset_access` | `tests.test_post_reset_access` | Verifies that the first transaction immediately after reset release completes correctly | PASS |

The data-pattern testing contributes to functional coverage for the following patterns:

| Pattern | Description |
|---|---|
| `0x00000000` | All zeros |
| `0xFFFFFFFF` | All ones |
| `0xAAAAAAAA` | Alternating `1010` pattern |
| `0x55555555` | Alternating `0101` pattern |
| `0x80000000` | Most-significant bit set |
| `0x00000001` | Least-significant bit set |
| `0x7FFFFFFF` | All bits except the most-significant bit set |
| `0xFFFFFFFE` | All bits except the least-significant bit set |

---

## 6. Negative Tests

The negative group contains five tests:

```makefile
negative:
        $(MAKE) illegal_write
        $(MAKE) illegal_read
        $(MAKE) setup_no_enable
        $(MAKE) write_data_change
        $(MAKE) recovery_after_error
```

| Make target | Cocotb module | Verification objective | Result |
|---|---|---|---|
| `illegal_write` | `tests.test_illegal_write_address` | Sends writes to illegal addresses and verifies that `pslverr` is asserted without modifying RAM | PASS |
| `illegal_read` | `tests.test_illegal_read_address` | Sends reads to illegal addresses and verifies that `pslverr` is asserted without modifying RAM | PASS |
| `setup_no_enable` | `tests.test_setup_without_enable` | Holds the bus in SETUP without asserting `penable` and verifies that no transfer occurs | PASS |
| `write_data_change` | `tests.test_write_data_changes_during_access` | Intentionally changes `pwdata` between SETUP and ACCESS to characterize DUT behavior during an invalid master sequence | PASS |
| `recovery_after_error` | `tests.test_recovery_after_illegal_access` | Generates illegal accesses and confirms that later legal accesses complete successfully | PASS |

These tests verify that error conditions do not corrupt legal memory locations or leave the DUT stuck.

---

## 7. Random Tests

The random group contains four tests:

```makefile
random_tests:
        $(MAKE) random_write_readback
        $(MAKE) random_read_write
        $(MAKE) random_memory_sweep
        $(MAKE) random_illegal_access
```

| Make target | Cocotb module | Verification objective | Result |
|---|---|---|---|
| `random_write_readback` | `tests.test_random_write_readback` | Performs random legal writes followed immediately by reads from the same address | PASS |
| `random_read_write` | `tests.test_random_read_write` | Generates a random mixture of legal reads and writes using a software reference model | PASS |
| `random_memory_sweep` | `tests.test_random_memory_sweep` | Runs a long random sequence and then compares all 32 addresses against the reference model | PASS |
| `random_illegal_access` | `tests.test_random_illegal_access` | Generates random illegal reads and writes while periodically confirming that legal accesses still work | PASS |

### 7.1 Reference-Model Checking

The random tests maintain an expected software representation of the 32-word RAM.

For writes:

```text
DUT write → update expected memory model
```

For reads:

```text
DUT read → compare returned data with expected model value
```

This approach allows randomized transaction ordering while preserving deterministic pass/fail checking.

---

## 8. Stress Tests

The stress group contains four tests:

```makefile
stress_tests:
        $(MAKE) stress
        $(MAKE) stress_repeat
        $(MAKE) stress_full_memory
        $(MAKE) stress_mixed
```

| Make target | Cocotb module | Verification objective | Result |
|---|---|---|---|
| `stress` | `tests.test_stress_back2back` | Writes all 32 locations and reads all 32 locations during sustained back-to-back traffic | PASS |
| `stress_repeat` | `tests.test_stress_repeated_address` | Repeatedly writes and reads one address to verify stability under repeated updates | PASS |
| `stress_full_memory` | `tests.test_stress_full_memory` | Repeatedly writes and verifies the entire memory over multiple full-memory cycles | PASS |
| `stress_mixed` | `tests.test_stress_mixed_traffic` | Runs a long randomized mixture of reads and writes while checking a reference model | PASS |

The stress tests check for corruption, stale data, address-decoding problems, and failures that may appear only after repeated activity.

---

## 9. Protocol-Behavior Characterization Tests

The protocol group contains four tests:

```makefile
protocol:
        $(MAKE) enable_no_select
        $(MAKE) address_change
        $(MAKE) pwritechange
        $(MAKE) pwdatachange
```

| Make target | Cocotb module | Verification objective | Result |
|---|---|---|---|
| `enable_no_select` | `tests.test_enable_without_select` | Asserts `penable` without `psel` and verifies that no transfer or memory update occurs | PASS |
| `address_change` | `tests.test_address_changes_during_access` | Changes `paddr` between SETUP and ACCESS and documents which value the RTL uses | PASS |
| `pwritechange` | `tests.test_pwrite_changes_during_access` | Changes `pwrite` between SETUP and ACCESS and documents which operation the RTL performs | PASS |
| `pwdatachange` | `tests.test_pwdata_changes_during_access` | Changes `pwdata` between SETUP and ACCESS and documents which data value the RTL writes | PASS |

### 9.1 Important Interpretation

APB requires address, direction, and write data to remain stable from SETUP through ACCESS.

The following tests intentionally violate that master-side requirement:

- `address_change`
- `pwritechange`
- `pwdatachange`

They are not tests proving APB protocol compliance. They characterize the current RTL behavior when the master supplies an invalid signal sequence.

The observed RTL behavior is that `paddr`, `pwrite`, and `pwdata` are sampled when the transfer completes during ACCESS.

---

## 10. Common Test Flow

Most tests use the following sequence:

1. Start a 10 ns APB clock.
2. Apply synchronous active-low reset.
3. Drive one or more APB transfers.
4. Wait for transfer completion.
5. Sample DUT outputs during Cocotb’s read-only simulation phase.
6. Compare actual behavior against expected behavior.
7. Report pass or raise an assertion failure.

A typical legal transfer follows:

```text
SETUP:
    psel = 1
    penable = 0
    address, direction, and data are driven

ACCESS:
    psel = 1
    penable = 1
    DUT asserts pready and completes the transfer

CLEANUP:
    helper deasserts the APB control signals
    DUT clears completion and error outputs
```

---

## 11. Verification Techniques

| Technique | Application |
|---|---|
| Directed testing | Known addresses, values, reset sequences, and expected outcomes |
| Boundary testing | Addresses 0 and 31 |
| Negative testing | Illegal addresses and incomplete or invalid transfers |
| Random testing | Random addresses, data, and read/write operation selection |
| Reference modeling | Expected RAM contents maintained in Python |
| Stress testing | Long, repeated, back-to-back, and full-memory activity |
| Protocol characterization | Observation of RTL behavior under intentionally unstable APB inputs |
| Assertions | Immediate comparison of expected and actual behavior |
| Functional coverage | Measurement of operation, address, data, sequence, error, and reset scenarios |
| Waveform debugging | Inspection of APB timing and RTL state transitions |

---

## 12. Relationship to Functional Coverage

The 32 tests collectively cover the following functional categories:

| Coverage category | Covered behavior |
|---|---|
| Boundaries | Addresses 0 and 31 |
| Error response | `pslverr=0` and `pslverr=1` |
| Data patterns | Eight important 32-bit patterns |
| Sequences | Back-to-back transfers and write/read-same-address |
| Operation × address type | Legal and illegal reads and writes |
| Operation × legal address | Read and write at every legal address |
| Reset | Reset observation |

Final merged functional coverage:

```text
119/119 bins = 100%
```

Final merged Verilator code coverage:

```text
56/59 coverage points = 94%
```

---

## 13. Regression Execution and Reporting

The six groups are executed by the full regression target:

```bash
make regress
```

The regression runs the following groups in sequence:

```text
basic
corner
negative
random_tests
stress_tests
protocol
```

The automated reporting flow reads the saved per-test XML results and produces:

```text
results/regression_report.txt
```

The final report lists:

- Makefile target name
- Pass, fail, or skipped status
- Cocotb test-function name
- Overall totals

---

## 14. Final Test Inventory

| Category | Tests | Passed |
|---|---:|---:|
| Basic | 10 | 10 |
| Corner | 5 | 5 |
| Negative | 5 | 5 |
| Random | 4 | 4 |
| Stress | 4 | 4 |
| Protocol characterization | 4 | 4 |
| **Total** | **32** | **32** |

---

## 15. Summary

The APB RAM regression verifies the complete 32-word memory across normal, boundary, invalid, random, sustained, reset, and protocol-characterization scenarios.

All 32 tests pass with no failures or skipped tests. The test suite achieves 100% functional coverage and 94% Verilator code coverage.

The combined use of directed tests, randomized traffic, reference models, negative testing, stress testing, transaction monitoring, coverage collection, regression reporting, and waveform debugging provides strong evidence that the DUT behaves consistently with its implemented specification.
