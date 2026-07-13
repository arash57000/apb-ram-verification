APB RAM Verification — Test 1: test_smoke.py
Objective

The purpose of the smoke test is to answer one simple question:

"Does the APB RAM work at the most basic level?"

Instead of testing every feature, a smoke test verifies that the DUT is alive and that the most fundamental operation succeeds.

For an APB RAM this means:

Reset
      ↓
Write one location
      ↓
Read the same location
      ↓
Compare data

If this passes, we know the DUT is functioning before moving on to more advanced tests.

What we implemented

Our smoke test performs four steps.

Step 1 — Start the clock

Because our tb_top.sv intentionally contains no clock generator, Cocotb owns simulation time.

We added:

cocotb.start_soon(
    Clock(dut.pclk, 10, units="ns").start()
)

This creates a 10 ns APB clock.

Without a clock:

No RisingEdge
        ↓
No reset
        ↓
Simulation ends immediately
Step 2 — Reset the DUT

We reused our helper:

await reset_dut(dut)

Inside tb_utils.py this:

drives presetn = 0
clears APB signals
waits 5 clock cycles
releases reset

This guarantees every test starts from a known state.

Step 3 — Perform one APB write

We wrote

Address = 0
Data    = 0xA5

using

await apb_write(...)

The helper automatically performs the APB protocol:

SETUP
↓

ACCESS
↓

TRANSFER
↓

IDLE
Step 4 — Read the same location

We executed

rdata = await apb_read(...)

which performs another APB transaction and returns the value from memory.

Step 5 — Scoreboard check

Finally,

assert rdata == data

This is our simplest scoreboard.

Expected:

0xA5

Received:

0xA5

PASS.

Final simulation
WRITE ADDR=0 DATA=0xA5

↓

READ ADDR=0 DATA=0xA5

↓

Smoke test PASSED

Simulation finished successfully at

120 ns
Problems we encountered

This exercise was valuable because we solved several common verification issues.

1. Python couldn't find the tests

Initial error:

ModuleNotFoundError:
No module named 'tests'
Cause

PYTHONPATH pointed to the wrong directory.

Fix

Updated the Makefile so Python could locate the tests package.

2. Python couldn't find tb_utils

Next error:

No module named tb_utils
Cause

The import was

from tb_utils import ...

but tb_utils.py lives in the same package as test_smoke.py.

Fix

Used a relative import:

from .tb_utils import ...
3. Simulator shut down immediately

Error:

Simulator shut down prematurely

Simulation time:

0 ns
Cause

No clock was running.

tb_top.sv intentionally has

no clock
no initial block
no $finish

because Cocotb controls simulation.

Fix

Started the clock inside the test:

Clock(dut.pclk, 10, units="ns")
4. APB helper reuse

Instead of rewriting protocol code, we reused:

reset_dut()

↓

apb_write()

↓

apb_read()

This makes every future test much shorter and easier to maintain.

Why this smoke test is important

Every verification project begins with a smoke test because it confirms that:

✔ the simulator launches correctly
✔ Cocotb is configured correctly
✔ the DUT can be reset
✔ the clock is running
✔ APB transactions work
✔ memory can be written
✔ memory can be read
✔ the basic data path is correct

Only after this foundation is proven does it make sense to run more advanced tests.

Skills practiced

By completing this test, you practiced:

Cocotb test structure (@cocotb.test)
Starting a clock with Clock
Using await for asynchronous transactions
Reusing helper functions from tb_utils.py
APB write and read transactions
Basic scoreboard checking with assert
Python package management (PYTHONPATH and relative imports)
Debugging Cocotb import errors
Debugging simulation startup issues
Running individual tests through the Makefile

Current Verification Progress
Test	Purpose	Status
✅ test_smoke.py	Basic APB read/write functionality	PASS
⏳ test_reset.py	Verify reset behavior	Next
⏳ test_illegal_addr.py	Verify invalid address handling	Pending
⏳ test_random_basic.py	Random APB transactions	Pending
✅ test_stress_back2back.py	Consecutive APB transactions	PASS
