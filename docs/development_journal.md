w# APB RAM Verification Project

# Weekly Engineering Notes

---

# Week 1

**Date:** July 12, 2026

## Objectives

This week focused on building the foundation of the APB RAM verification project.

Major goals included:

* Repository setup
* RTL implementation
* Cocotb verification environment
* Directed verification
* Project documentation

---

## Accomplishments

### Project Setup

Completed:

* Git repository initialization
* Repository organization
* Makefile creation
* Documentation structure
* Linux development environment

---

### RTL Development

Implemented:

* APB RAM module
* APB interface
* Top-level testbench
* Finite State Machine (FSM)
* Reset logic
* Illegal address detection

---

### Verification Environment

Implemented:

* Driver
* Monitor
* Agent
* Environment
* Scoreboard
* Coverage infrastructure
* APB helper functions

---

### Directed Tests Completed

* Smoke Test
* Reset Test
* Address 0
* Address 31
* Default Read
* Overwrite
* Sequential Write
* Sequential Read
* Stress Back-to-Back

---

## Documentation

Created or updated:

* README.md
* verification_plan.md
* apb_protocol.md

---

## Technical Skills Practiced

* SystemVerilog RTL
* APB Protocol
* Cocotb
* Python
* Verilator
* GTKWave
* Linux
* Git
* GitHub

---

## Lessons Learned

This week reinforced several important verification concepts:

* Verification planning should begin before writing tests.
* Separating drivers, monitors, and scoreboards improves testbench organization.
* Directed tests provide confidence before introducing constrained-random verification.
* Clear documentation makes the project easier to maintain and explain.
* Git commits should represent meaningful engineering milestones.

---

## Challenges Encountered

Major debugging efforts included:

* APB transaction timing
* Cocotb coroutine synchronization
* Read/write sequencing
* Scoreboard verification
* Reset behavior
* Repository organization

Each issue improved understanding of both APB protocol behavior and Cocotb-based verification.

---

## Overall Progress

Completed

* Phase 1 — Planning
* Phase 2 — Repository Setup
* Phase 3 — RTL Development
* Phase 4 — Testbench Development
* Phase 5 — Basic Verification

Current Focus

➡️ Phase 6 — Functional Verification

---

# Week 2

**Date:** July 19, 2026

## Objectives

Expand the verification environment by improving regression quality, repository organization, and project documentation.

---

## Accomplishments

Completed:

* Repository cleanup
* Regression target improvements
* Documentation updates
* Makefile organization
* README improvements
* Verification plan updates

---

## Engineering Improvements

Improved the organization of the verification environment by:

* Cleaning repository structure
* Standardizing documentation
* Improving Makefile readability
* Simplifying regression execution
* Organizing project files for long-term maintenance

---

## Lessons Learned

This week's work reinforced that maintaining a clean repository is an important part of engineering. Well-organized documentation and consistent project structure make verification environments easier to understand, review, and extend.

---

## Overall Progress

Completed

* Repository cleanup
* Documentation improvements
* Regression organization

Current Focus

➡️ Expanding functional verification

---

# Week 3

**Date:** July 26, 2026

## Objectives

Expand functional verification through negative, random, and stress testing while improving verification helper functions.

---

## Accomplishments

Completed:

* Illegal read testing
* Illegal write testing
* Recovery after illegal access testing
* Random verification tests
* Stress testing
* Verification helper improvements

---

## Engineering Note — APB Transaction Timing

During stress testing, consecutive APB transactions occasionally began before the previous transaction had fully completed.

The original helper functions completed after the ACCESS phase, allowing the next transaction to start too early during back-to-back testing.

The helper functions were updated to include an additional clock cycle before beginning the next transaction, allowing the APB interface to cleanly return to the idle state.

Transaction flow became:

* Cycle 1 — SETUP
* Cycle 2 — ACCESS
* Cycle 3 — TRANSFER / Cleanup

This change improved transaction reliability during stress regression.

### Lesson Learned

Verification helper functions should accurately model protocol timing. Even when the DUT responds without wait states, helper functions should allow the interface to return to a clean idle condition before initiating another transaction.

---

## Additional Improvements

Completed:

* Improved APB utility functions
* Expanded regression coverage
* Improved negative testing
* Continued documentation updates

---

## Overall Progress

Completed

* Directed Testing
* Negative Testing
* Random Testing
* Stress Testing

Current Focus

➡️ Protocol compliance and repository polish

---

# Week 4

Date: August 2, 2026

## Objectives

Review the APB RAM verification repository from a software engineering perspective and improve overall code quality, documentation, and GitHub presentation without changing verified functionality.

## Accomplishments

Completed:

Reviewed the overall repository structure.
Reviewed .gitignore and verified generated files are excluded from version control.
Cleaned and refactored tb_utils.py.
Removed duplicate helper functions.
Removed development-only comments from production code.
Added documentation to utility functions.
Removed the obsolete test_illegal_addr.py after replacing it with dedicated illegal read and illegal write tests.
Removed local __pycache__ directories from the development workspace.
Reviewed the project README.md and identified future updates after Phase 6 completion.
Established a weekly engineering review workflow for repository maintenance, documentation, and GitHub updates.
## Repository Improvements

This week's work focused on improving repository maintainability and presentation.

Improvements included:

Eliminating duplicate code.
Improving helper function readability.
Removing obsolete files.
Improving documentation consistency.
Verifying repository organization.
Confirming Git hygiene through proper .gitignore configuration.

These changes improved the overall quality of the project while preserving existing verification functionality.

## Lessons Learned

Preparing a project for public review requires more than passing simulations.

Professional-quality repositories should also emphasize:

Clean code
Consistent documentation
Maintainable helper functions
Meaningful Git history
Readable project organization

Small improvements in readability can significantly improve the experience for reviewers and future contributors.

## Overall Progress

Completed

Phase 1 — Planning
Phase 2 — Repository Setup
Phase 3 — RTL Development
Phase 4 — Testbench Development
Phase 5 — Basic Verification
Phase 6 — Functional Verification (Directed, Boundary, Negative, Random, and Stress Testing)

## Current Focus

➡️ Phase 6 — Protocol Compliance Verification

---
# Week 5

Date: August 23, 2026

## Objectives

Expand APB protocol behavior verification, strengthen stress testing, improve regression organization, preserve per-test coverage results, and continue repository engineering polish.

## Accomplishments

Completed:

* Added `test_address_changes_during_access.py`.
* Added `test_pwrite_changes_during_access.py`.
* Added `test_pwdata_changes_during_access.py`.
* Added `test_stress_mixed_traffic.py`.
* Added deterministic mixed-traffic testing with 1,000 transactions and random seed `12345`.
* Organized Makefile targets into basic, corner, negative, random, stress, and protocol groups.
* Updated recursive Makefile commands to use `$(MAKE)`.
* Added `.PHONY` declarations for executable Makefile targets.
* Added per-test coverage preservation under `coverage_runs/tests/`.
* Added merged and annotated coverage report generation.
* Updated `.gitignore` to exclude generated coverage output and editor backup files.
* Improved formatting, documentation, and logging in `tb_utils.py`.
* Ran the complete APB RAM regression successfully.

## Protocol Behavior Characterization

The new protocol tests intentionally change APB control or data signals between SETUP and ACCESS.

These tests are not APB protocol-compliance tests. They document the current RTL behavior when the APB stability requirements are intentionally violated.

The characterization tests verify changes to:

* `PADDR` during ACCESS
* `PWRITE` during ACCESS
* `PWDATA` during ACCESS

The current RTL samples these signals when the transfer completes during ACCESS.

## Stress Verification

The mixed-traffic stress test performs 1,000 randomly selected reads and writes across all 32 RAM addresses.

A software reference model tracks the expected contents of every address. Every read is compared against the reference model immediately.

The fixed random seed makes the transaction sequence reproducible for debugging.

## Regression and Coverage

The regression is organized into these groups:

* Basic tests
* Corner-case tests
* Negative tests
* Random tests
* Stress tests
* Protocol tests

The complete regression passed successfully.

Merged Verilator code coverage reached:

* 54 of 60 coverage points
* 90% total code coverage

Merged functional coverage reached:

* 119 of 119 coverage bins
* 100% total functional coverage
* Zero uncovered functional-coverage bins

## Coverage-Hole Analysis

The annotated Verilator report identified one zero-hit RTL statement:

```systemverilog
default: state <= IDLE;
```

This defensive FSM branch cannot be exercised through normal APB stimulus. The state variable is two bits wide, and all four possible binary encodings are assigned to valid states: `IDLE`, `SETUP`, `ACCESS`, and `TRANSFER`.

Verilator uses two-state simulation, so an unknown or high-impedance state value cannot be injected to reach the branch. Therefore, this statement is classified as structurally unreachable in the current simulation environment rather than as a missing functional test.

The remaining code-coverage hole is accepted with justification. No additional APB test is required to close it.

## Lessons Learned

Protocol violations should be clearly separated from protocol-compliance testing. A characterization test documents how the current RTL responds to an invalid stimulus without claiming that the stimulus is legal APB behavior.

Deterministic random seeds are important because they allow stress-test failures to be reproduced.

Grouped regression targets make large verification suites easier to run, understand, debug, and maintain.

Generated coverage artifacts and temporary editor files should remain outside version control.

## Overall Progress

Completed:

* Phase 1 — Planning
* Phase 2 — Repository Setup
* Phase 3 — RTL Development
* Phase 4 — Testbench Development
* Phase 5 — Basic Verification
* Phase 6 — Functional and Protocol Verification
* Phase 7 — Coverage

Infrastructure established:

* Initial automated regression foundation for Phase 8


## Current Focus

➡️ Phase 8 — Regression automation and reporting

---

# Week 6

Date: September 22–October 12, 2026

## Objectives

Complete regression reporting, perform waveform-based debugging, rerun the final verification flow, close Phase 10 documentation, and prepare the project for final release.

## Regression Automation and Reporting

Completed:

* Added `scripts/regression_report.py`.
* Updated the Makefile to preserve individual Cocotb XML result files.
* Added the `regression-report` target.
* Added grouped error handling to the full regression.
* Generated `results/regression_report.txt`.
* Confirmed that all 32 tests appear in the final report.
* Confirmed zero failed and zero skipped tests.

Final regression result:

```text
Total: 32  Passed: 32  Failed: 0  Skipped: 0
```

The regression is organized into:

* 10 basic tests
* 5 corner-case tests
* 5 negative tests
* 4 random tests
* 4 stress tests
* 4 protocol-characterization tests

## Waveform Debugging

Performed a controlled debugging exercise using the smoke test.

The exercise:

1. Deliberately changed the expected read value so the test would fail.
2. Ran the focused Cocotb test.
3. Observed the assertion failure and simulation log.
4. Opened the generated VCD waveform in GTKWave.
5. Inspected the APB clock, reset, control, address, data, ready, error, and state signals.
6. Confirmed that the DUT returned the correct value and that the expected value was intentionally wrong.
7. Restored the correct test expectation.
8. Reran the focused test successfully.
9. Reran the regression and coverage flow successfully.

This exercise demonstrated how logs, assertions, and waveforms work together during failure diagnosis.

## Final Coverage Results

Final merged functional coverage:

```text
119/119 bins = 100%
```

Final merged Verilator code coverage:

```text
56/59 coverage points = 94%
```

The original code-coverage goal was 95%. The final result was accepted after coverage-hole analysis, full regression success, 100% functional coverage, and documented exclusion of the structurally unreachable defensive FSM default branch.

The default FSM branch is structurally unreachable in the current Verilator environment because:

* The state variable is two bits wide.
* All four possible two-bit encodings are assigned to valid states.
* Verilator uses two-state simulation.
* An unknown or high-impedance state cannot be injected to reach the branch.

## Phase 10 Documentation

Completed and verified:

* `docs/architecture.md`
* `docs/test_summary.md`
* Version 3.0 of `docs/verification_plan.md`
* Final portfolio-facing `README.md`
* Final development-journal entry

The architecture document records:

* DUT structure
* APB interface
* Memory organization
* Four-state FSM
* Reset, read, write, and error behavior
* Active verification flow
* Monitor-to-coverage flow
* Functional coverage model
* Reusable but inactive framework components
* Code-coverage exclusion rationale

The test summary records:

* All 32 tests
* Six regression groups
* Test objectives
* Final pass status
* Functional coverage relationship
* Regression and reporting flow

The verification plan was updated from an early planning document to an accurate as-built verification plan containing the final strategy, environment, test categories, coverage results, exit criteria, risks, limitations, and deliverables.

The README was rewritten as the final project report and portfolio entry. Outdated planned-work sections were removed and replaced with verified final results, correct run commands, architecture, coverage, debugging, lessons learned, documentation links, limitations, and optional future enhancements.

## Lessons Learned

### Sample Outputs After RTL Updates

Cocotb checks must sample DUT outputs after nonblocking assignments and other simulator updates have settled. Using the `ReadOnly` trigger avoids race conditions and prevents checks from reading stale output values.

### Separate Legal Protocol Tests from Characterization

Tests that intentionally change `PADDR`, `PWRITE`, or `PWDATA` between SETUP and ACCESS violate APB master requirements.

These tests are useful for documenting the current RTL response, but they should be classified as behavior-characterization tests rather than protocol-compliance tests.

### Functional Coverage and Code Coverage Measure Different Things

One hundred percent functional coverage confirms that every planned functional bin was observed. It does not imply that every RTL coverage point is reachable or executed.

Functional coverage answers whether planned scenarios occurred. Code coverage identifies which RTL structures executed.

### Coverage Holes Require Engineering Analysis

A coverage hole should not automatically cause another test to be added.

The engineer must determine whether the hole represents:

* Missing stimulus
* Missing checking
* An untested functional path
* Structurally unreachable logic
* A simulator limitation
* A justified exclusion

### Deterministic Random Testing Improves Debugging

Fixed random seeds make long randomized and stress-test failures reproducible. Reproducibility allows the same sequence to be rerun while examining logs and waveforms.

### Regression Results Must Be Preserved

Saving per-test XML files provides an auditable record of the regression. It also allows a separate reporting script to summarize results after all tests complete.

### Documentation Must Match the Active Implementation

The repository contains reusable driver, agent, environment, scoreboard, interface, and sequence components. However, the active regression uses APB helper functions, direct assertions, local reference models, the transaction monitor, and the functional coverage collector.

Documentation must clearly distinguish implemented reusable infrastructure from the path actually exercised by the regression.

### Historical Results Should Remain Historical

Earlier weekly coverage numbers and project status remain in the journal because they accurately record the project at that time. Final documents separately report the completed results.

### Version Control Supports Safe Documentation Rework

Git made it safe to replace outdated verification-plan and README content because every earlier version remained recoverable through commit history.

## Final Verification Status

| Metric | Final result |
|---|---:|
| Regression tests | 32 |
| Passed | 32 |
| Failed | 0 |
| Skipped | 0 |
| Functional coverage | 119/119 bins, 100% |
| Verilator code coverage | 56/59 points, 94% |
| Known critical functional bugs | 0 |

## Overall Progress

Completed:

* Phase 1 — Planning
* Phase 2 — Repository Setup
* Phase 3 — RTL Development
* Phase 4 — Testbench Development
* Phase 5 — Basic Verification
* Phase 6 — Functional and Protocol Verification
* Phase 7 — Coverage
* Phase 8 — Regression and Reporting
* Phase 9 — Waveform Debugging
* Phase 10 — Documentation

## Current Focus

➡️ Phase 11 — Final cleanup, GitHub release, release tagging, and portfolio screenshots

---

# Project Evolution

The APB RAM Verification Project has evolved from a basic directed-test environment into a layered Cocotb-based verification environment featuring directed, boundary, negative, random, and stress testing.

Throughout development, emphasis has been placed on:

* Verification planning
* Clean repository organization
* Incremental engineering improvements
* Comprehensive documentation
* Git version control
* Maintainable verification infrastructure

Weekly engineering reviews are used to continuously improve code quality, documentation, repository organization, and overall project maintainability as the project progresses toward completion.


