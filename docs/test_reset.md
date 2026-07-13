APB RAM Verification – test_reset.py Summary
Purpose

The purpose of test_reset.py was to verify that the APB RAM DUT correctly initializes after an active-low reset (presetn) and can immediately resume normal APB communication.

This test ensures the DUT starts from a known, stable state before any functional testing is performed.

What We Did

During this test, we:

Started the APB clock using Cocotb.
Applied an active-low reset using the reset_dut() helper function.
Held the DUT in reset for several clock cycles.
Released the reset and allowed one additional clock cycle for stabilization.
Performed an APB write transaction to address 5.
Performed an APB read transaction from the same address.
Compared the read data with the written data using an assertion.

The simulation log confirmed that the value written (0x12345678) matched the value read after reset.

What We Accomplished

Successfully passing this test demonstrated that:

✅ The DUT exits reset correctly.
✅ The APB interface is functional immediately after reset.
✅ The internal control logic (FSM) resumes normal operation after reset.
✅ Read and write transactions operate correctly after reset.
✅ The verification environment can safely initialize the DUT before running more advanced tests.

This gives us confidence that every future test begins with the DUT in a known, reliable state.

Usage in a Verification Environment

test_reset.py is one of the most important sanity tests in any verification project.

Its main uses are:

Verify correct power-up behavior.
Confirm that reset initializes the DUT properly.
Ensure communication resumes normally after reset.
Provide a clean starting point for all subsequent verification tests.
Detect reset-related design bugs early before running more complex scenarios.

In a real ASIC or FPGA verification environment, reset testing is typically one of the first tests executed in every regression.

Difficulties We Had

Compared to the previous tests, this test was straightforward because we had already built reusable helper functions in tb_utils.py.

The main points we considered were:

Understanding that the purpose of the test is not to verify that RAM contents are cleared, since our RTL does not clear memory during reset.
Waiting one additional clock cycle after releasing reset to ensure the DUT had stabilized before starting APB transactions.
Reusing the existing reset_dut(), apb_write(), and apb_read() helper functions instead of rewriting the APB protocol.

As a result, no major debugging or RTL modifications were required, and the test passed on the first run.

Lessons Learned

From this test, we learned that:

Reset verification checks that the DUT can recover and operate normally after reset.
Helper functions make test creation much simpler and more consistent.
A passing reset test increases confidence that failures in later tests are caused by functional issues rather than incorrect DUT initialization.
Separating reset logic into tb_utils.py improves code reuse and makes the verification environment easier to maintain.
Outcome

Status: ✅ PASS

The test_reset.py successfully verified that the APB RAM DUT initializes correctly after reset and immediately supports normal APB read and write transactions. This establishes a reliable foundation for the remaining verification tests, beginning with test_illegal_addr.py, where we will validate the DUT's behavior when invalid APB addresses are accessed.
