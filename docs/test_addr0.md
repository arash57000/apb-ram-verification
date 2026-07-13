Phase 5 — Directed Test #1
test_addr0.py
Objective

Verify that the APB RAM correctly performs:

Write to the lowest valid address (0)
Read from address 0
Return the exact data written
Why do we need this test?

Even though the smoke test probably accessed address 0, this test has a single verification objective.

Professional verification follows the principle:

One test = One verification objective

The smoke test proves the environment works.

This test proves:

"Address 0 functions correctly."

If it fails in the future, you'll immediately know the issue is specific to the lowest address boundary—not the environment.

What we're verifying
          Write
            │
            ▼
      Address = 0
      Data    = 0xA5A50001
            │
            ▼
         APB RAM
            │
            ▼
          Read
            │
            ▼
Expected = 0xA5A50001


Test Flow
Reset DUT
      │
      ▼
Write Address 0
      │
      ▼
Read Address 0
      │
      ▼
Compare Data
      │
      ▼
PASS


Before writing code

I'd like to keep all directed tests looking consistent.

We'll use the same template for every test:

@cocotb.test()
async def test_xxx(dut):

    # Test description

    # Reset DUT

    # Apply stimulus

    # Check response

    # PASS

Every directed test in the project will follow this structure.
