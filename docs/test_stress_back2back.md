Goal of test_stress_back2back.py

Verify the APB RAM can handle:

Write
Write
Write
Write
Write
...

with no extra idle clocks inserted by the test.

Then:

Read
Read
Read
Read
Read
...

and confirm all data is correct.

What Are We Stressing?

Normal smoke test:

Write addr 0
Read addr 0

Write addr 1
Read addr 1

Stress test:

Write addr 0
Write addr 1
Write addr 2
Write addr 3
...
Write addr 15

Read addr 0
Read addr 1
Read addr 2
Read addr 3
...
Read addr 15

This exercises:

Continuous APB transactions
Address decoding
RAM storage
No transaction corruption
test_stress_back2back.py
import cocotb

from tb_utils import (
    reset_dut,
    apb_write,
    apb_read
)


@cocotb.test()
async def test_stress_back2back(dut):

    await reset_dut(dut)

    # -------------------------
    # Back-to-back writes

    for addr in range(16):

        data = (addr * 3) & 0xFF

        await apb_write(
            dut,
            addr,
            data
        )

    # -------------------------
    # Back-to-back reads

    for addr in range(16):

        expected = (addr * 3) & 0xFF

        actual = await apb_read(
            dut,
            addr
        )

        assert actual == expected, (
            f"Address {addr}: "
            f"Expected {expected:#04x}, "
            f"Got {actual:#04x}"
        )

    cocotb.log.info(
        "Back-to-back stress test PASSED"
    )
Example Data Pattern

Using:

data = (addr * 3) & 0xFF

gives:

Address	Data
0	0
1	3
2	6
3	9
4	12
5	15
...	...

This is better than:

data = addr

because it's less trivial and catches more mistakes.

Expected Waveform Conceptually

Writes:

Addr 0 -> 0
Addr 1 -> 3
Addr 2 -> 6
Addr 3 -> 9
...
Addr15 ->45

Reads:

Read Addr0 -> 0
Read Addr1 -> 3
Read Addr2 -> 6
Read Addr3 -> 9
...
Read Addr15 ->45

Every comparison should pass.

Contribution Level

For this test, try to write it yourself first and only use the checklist:

1. Import cocotb
2. Import tb_utils functions
3. Reset DUT
4. Loop over addresses and write data
5. Loop over addresses and read data
6. Compare expected vs actual
7. Print PASS message

That's about 60–70% of what a junior DV engineer would write for a simple APB stress test.



Very Brief APB RAM Operation Summary

Think of the APB RAM as a small memory connected to an APB bus.

What the RAM Does
Address 0  -> Data
Address 1  -> Data
Address 2  -> Data
...
Address 15 -> Data

Example:

RAM[0] = 0x11
RAM[1] = 0x22
RAM[2] = 0x33
APB Write Operation

When the master wants to write:

Address = 5
Data    = 0x55
Setup Phase
PSEL    = 1
PENABLE = 0
PWRITE  = 1
PADDR   = 5
PWDATA  = 0x55
Access Phase
PENABLE = 1

RAM performs:

RAM[5] = 0x55
APB Read Operation

Want to read:

Address = 5
Setup Phase
PSEL    = 1
PENABLE = 0
PWRITE  = 0
PADDR   = 5
Access Phase
PENABLE = 1

RAM performs:

PRDATA = RAM[5]

returns:

PRDATA = 0x55
Illegal Address

Suppose RAM depth is 16:

Valid:
0 - 15

Invalid:
16+

If we access:

Address = 100

RAM asserts:

PSLVERR = 1

This is what test_illegal_addr.py verifies.

How Your Tests Map to the RAM
Test	What it checks
test_smoke.py	Can write and read one location
test_illegal_addr.py	Invalid address generates PSLVERR
test_random_basic.py	Many random addresses/data work
test_stress_back2back.py	Continuous APB transactions work
test_reset.py	Reset clears RAM correctly
Verification View
Test
  ↓
tb_utils.py
  ↓
APB Signals
  ↓
APB RAM
  ↓
Memory Array

Example from your stress test:

Write:
RAM[0]  = 0
RAM[1]  = 3
RAM[2]  = 6
...
RAM[15] = 45

Read:
RAM[0]  -> 0
RAM[1]  -> 3
RAM[2]  -> 6
...
RAM[15] -> 45


=================================RESULT==============================================



DULE=tests.test_stress_back2back TESTCASE= TOPLEVEL=tb_top TOPLEVEL_LANG=verilog \
         sim_build/Vtop  --trace --coverage --timing  
     -.--ns INFO     gpi                                ..mbed/gpi_embed.cpp:108  in set_program_name_in_venv        Using Python virtual environment interpreter at /home/anddrew/cocotb-venv/bin/python
     -.--ns INFO     gpi                                ../gpi/GpiCommon.cpp:101  in gpi_print_registered_impl       VPI registered
     0.00ns INFO     cocotb                             Running on Verilator version 5.040 2025-08-30
     0.00ns INFO     cocotb                             Running tests with cocotb v1.9.2 from /home/anddrew/cocotb-venv/lib/python3.12/site-packages/cocotb
     0.00ns INFO     cocotb                             Seeding Python random module with 1781890343
     0.00ns INFO     cocotb.regression                  Found test tests.test_stress_back2back.test_stress_back2back
     0.00ns INFO     cocotb.regression                  running test_stress_back2back (1/1)
                                                          Stress test:
                                                          - No idle cycles between APB transactions
                                                          - Write all locations
                                                          - Read all locations
                                                          - Verify data integrity
   100.00ns INFO     cocotb                             MEM0=0 MEM1=0 MEM2=0
   130.00ns INFO     cocotb                             MEM0=0 MEM1=3 MEM2=0
   160.00ns INFO     cocotb                             MEM0=0 MEM1=3 MEM2=6
   190.00ns INFO     cocotb                             MEM0=0 MEM1=3 MEM2=6
   220.00ns INFO     cocotb                             MEM0=0 MEM1=3 MEM2=6
   250.00ns INFO     cocotb                             MEM0=0 MEM1=3 MEM2=6
   280.00ns INFO     cocotb                             MEM0=0 MEM1=3 MEM2=6
   310.00ns INFO     cocotb                             MEM0=0 MEM1=3 MEM2=6
   340.00ns INFO     cocotb                             MEM0=0 MEM1=3 MEM2=6
   370.00ns INFO     cocotb                             MEM0=0 MEM1=3 MEM2=6
   400.00ns INFO     cocotb                             MEM0=0 MEM1=3 MEM2=6
   430.00ns INFO     cocotb                             MEM0=0 MEM1=3 MEM2=6
   460.00ns INFO     cocotb                             MEM0=0 MEM1=3 MEM2=6
   490.00ns INFO     cocotb                             MEM0=0 MEM1=3 MEM2=6
   520.00ns INFO     cocotb                             MEM0=0 MEM1=3 MEM2=6
   550.00ns INFO     cocotb                             MEM0=0 MEM1=3 MEM2=6
   590.00ns INFO     cocotb                             READ ADDR=0 DATA=0x00
   630.00ns INFO     cocotb                             READ ADDR=1 DATA=0x03
   670.00ns INFO     cocotb                             READ ADDR=2 DATA=0x06
   710.00ns INFO     cocotb                             READ ADDR=3 DATA=0x09
   750.00ns INFO     cocotb                             READ ADDR=4 DATA=0x0C
   790.00ns INFO     cocotb                             READ ADDR=5 DATA=0x0F
   830.00ns INFO     cocotb                             READ ADDR=6 DATA=0x12
   870.00ns INFO     cocotb                             READ ADDR=7 DATA=0x15
   910.00ns INFO     cocotb                             READ ADDR=8 DATA=0x18
   950.00ns INFO     cocotb                             READ ADDR=9 DATA=0x1B
   990.00ns INFO     cocotb                             READ ADDR=10 DATA=0x1E
  1030.00ns INFO     cocotb                             READ ADDR=11 DATA=0x21
  1070.00ns INFO     cocotb                             READ ADDR=12 DATA=0x24
  1110.00ns INFO     cocotb                             READ ADDR=13 DATA=0x27
  1150.00ns INFO     cocotb                             READ ADDR=14 DATA=0x2A
  1190.00ns INFO     cocotb                             READ ADDR=15 DATA=0x2D
  1190.00ns INFO     cocotb                             test_stress_back2back PASSED
  1190.00ns INFO     cocotb.regression                  test_stress_back2back passed
  1190.00ns INFO     cocotb.regression                  ***********************************************************************************************************
                                                        ** TEST                                               STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
                                                        ***********************************************************************************************************
                                                        ** tests.test_stress_back2back.test_stress_back2back   PASS        1190.00           0.13       9252.59  **
                                                        ***********************************************************************************************************
                                                        ** TESTS=1 PASS=1 FAIL=0 SKIP=0                                    1190.00           0.23       5245.25  **
                                                        ***********************************************************************************************************
                                                        
- :0: Verilog $finish
make[2]: Leaving directory '/home/anddrew/dv_projects/apb-ram-verification'
make[1]: Leaving directory '/home/anddrew/dv_projects/apb-ram-verification'

🎉 Excellent! You just got your first real stress test PASS.

The important part is:

READ ADDR=0 DATA=0x00
READ ADDR=1 DATA=0x03
READ ADDR=2 DATA=0x06
...
READ ADDR=15 DATA=0x2D

test_stress_back2back PASSED

and finally:

TESTS=1 PASS=1 FAIL=0
What We Learned During Debug
1. Python Packaging Issue

Started with:

No module named 'tests'

Fixed imports and PYTHONPATH.

2. Signal Name Mismatch

Started with:

tb_top contains no object named PRESETn

Your RTL uses:

pclk
presetn
psel
penable
...

not uppercase APB names.

3. No Clock Running

Your tb_top.sv intentionally had:

// No clock generation here

so Cocotb had to start:

Clock(dut.pclk, 10, units="ns")
4. Read Timing Issue

This was the real bug.

Your RTL updates:

prdata <= mem[paddr];

inside an always_ff.

Therefore the helper needed to wait until the value was actually visible before sampling.

Verification Result
Writes

Proved by:

MEM1=3
MEM2=6

inside DUT memory.

Reads

Proved by:

READ ADDR=1 DATA=0x03
READ ADDR=2 DATA=0x06
...
Stress Scenario
16 writes
followed by
16 reads

with continuous traffic.

Current Project Status
Test	Status
test_smoke.py	?
test_illegal_addr.py	?
test_random_basic.py	?
test_stress_back2back.py	✅ PASS
test_reset.py	?
Next Recommendation

Run:

make smoke

Then:

make illegal

Then:

make random

Then:

make reset

After all individual tests pass:

make regress



