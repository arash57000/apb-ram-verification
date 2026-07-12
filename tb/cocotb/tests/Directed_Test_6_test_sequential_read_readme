test_sequential_read.py
Verification Objective

Verify that every valid memory location returns the expected data after the RAM has been initialized with a known pattern.

Test Flow
Start Clock
      │
      ▼
Reset DUT
      │
      ▼
Initialize Memory Pattern
      │
      ▼
Read Address 0  → Expect 1
      │
Read Address 1  → Expect 2
      │
Read Address 2  → Expect 3
      │
...
      │
Read Address 31 → Expect 32
      │
PASS

Notice we're not testing the write path here.

We're assuming initialize_memory_pattern() already performs the writes.

This test focuses on:

Can I correctly read every memory location?

Summary — test_sequential_read.py
Verification Objective

Verify that every valid RAM address (0–31) returns the correct data after the RAM has been initialized with a known pattern.

Unlike test_sequential_write.py, this test focuses on the read path.

Test Flow
Start Clock
      │
      ▼
Reset DUT
      │
      ▼
Initialize Memory Pattern
      │
      ▼
Read Address 0  → Expect 1
Read Address 1  → Expect 2
...
Read Address 31 → Expect 32
      │
      ▼
PASS
What did we verify?

During initialization, the helper wrote:

Address	Data Written
0	0x00000001
1	0x00000002
2	0x00000003
...	...
31	0x00000020

Then the test read every address and verified that the returned value matched the expected pattern.

Your log confirms:

READ ADDR=0  DATA=0x01
READ ADDR=1  DATA=0x02
...
READ ADDR=31 DATA=0x20

Every read matched the expected value, so the test passed.

What does this prove?

This single test gives confidence in several parts of the DUT:

✅ Memory retains written values.
✅ APB read transactions work correctly.
✅ Address decoding is correct for all valid addresses.
✅ The RAM array stores independent values at each location.
✅ No address aliasing was observed (for example, writing one address did not corrupt another).
Why use a unique pattern?

Instead of writing the same value everywhere, you used:

data = addr + 1

That creates this mapping:

Address 00 → 1
Address 01 → 2
...
Address 31 → 32

This is much more powerful than writing all zeros because if one address returns the wrong value, you can immediately identify the mismatch.

For example:

Expected:
Address 17 → 18

Actual:
Address 17 → 5

That points directly to a problem rather than simply reporting "incorrect data."
