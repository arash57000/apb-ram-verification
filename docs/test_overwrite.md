test_overwrite.py
Verification Objective

Verify that writing to the same memory address twice correctly replaces the old value with the new value.

Why is this test important?

Imagine the RAM behaves like this:

Write Address 10 = 0x11111111

Memory becomes

Address 10
──────────────
0x11111111

Now write again:

Write Address 10 = 0xAAAAAAAA

The RAM must replace the previous value.

Final memory should be

Address 10
──────────────
0xAAAAAAAA

If the RTL still returns

0x11111111

then there is a bug.

Test Flow

Reset DUT
      │
      ▼
Write Address 10 = 0x11111111
      │
      ▼
Write Address 10 = 0xAAAAAAAA
      │
      ▼
Read Address 10
      │
      ▼
Expected = 0xAAAAAAAA


Summary — test_overwrite.py
Objective

Verify that writing to the same memory address twice correctly replaces the old data with the new data.

Test Flow
Reset DUT
      │
      ▼
Write Address 10 = 0x11111111
      │
      ▼
Write Address 10 = 0xAAAAAAAA
      │
      ▼
Read Address 10
      │
      ▼
Expect 0xAAAAAAAA
What happened?
First write
WRITE1 ADDR=10 DATA=0x11111111

Memory became:

Address 10
──────────────
0x11111111
Second write
WRITE2 ADDR=10 DATA=0xAAAAAAAA

The DUT executed:

mem[10] <= 32'hAAAAAAAA;

So the memory contents changed to:

Address 10
──────────────
0xAAAAAAAA

The previous value should no longer exist.

Read
READ ADDR=10 DATA=0xAAAAAAAA

The RAM returned the second value, which confirms the overwrite worked correctly.

What did we verify?

This test confirms several things:

✅ A memory location can be written more than once.
✅ The latest write replaces the previous value.
✅ The write path updates memory correctly.
✅ The read path returns the updated value.
✅ There is no stale or cached data being returned.

Why is this test important?

Many hardware blocks update configuration registers or memory locations multiple times during normal operation.

For example:

CPU
 │
 ▼
Write Register = 5

Later...

Write Register = 8

If the second write doesn't overwrite the first, the hardware would continue using outdated data, leading to incorrect behavior.

Although your DUT is a RAM rather than a register block, the verification principle is the same: the most recent write must be the value that is stored and read back.


