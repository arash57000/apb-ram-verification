test_sequential_write.py

Verification Objective

Verify that the DUT accepts writes to every valid address in the RAM.

Unlike the smoke test, which writes one location, this test exercises the entire address space.

Why do we need this test?

Suppose there is a bug in the address decoder.

Example:

Address 0  ✓
Address 1  ✓
Address 2  ✓
...
Address 15 ✓
Address 16 ✗
...
Address 31 ✓

A smoke test would never find that.

Writing all 32 addresses gives us confidence that every address can be accessed.

Test Flow

Reset DUT
      │
      ▼
Write Address 0
      │
      ▼
Write Address 1
      │
      ▼
Write Address 2
      │
      ▼
...
      │
      ▼
Write Address 31
      │
      ▼
PASS

Notice something important:

This test does not verify the data by reading it back.

It only verifies:

"Can I successfully perform a write transaction to every valid address?"

We'll verify the stored data in the next test (test_sequential_read.py).

This follows the single verification objective principle we've been using.

What did test_sequential_write.py actually verify?

The purpose of this test was:

Can the DUT successfully perform write transactions to every valid address?

Your simulation showed:

WRITE ADDR=00 DATA=0x00000001
WRITE ADDR=01 DATA=0x00000002
...
WRITE ADDR=31 DATA=0x00000020
PASS

This confirms:

✅ Every valid address (0–31) accepted a write transaction.
✅ The APB write path worked for the full address range.
✅ The address decoder accepted every valid address.
✅ No illegal address errors occurred.
What did this test not verify?

Notice that after each write, we never did:

rdata = await apb_read(...)

So we did not verify that the data was actually stored correctly.

Think of it like this:

CPU
 │
 ▼
Write data
 │
 ▼
RAM

We proved the write transaction reached the RAM.

We have not yet proven that the RAM remembers the data correctly.

Why split this into two tests?

A common verification principle is:

One test = One verification objective.

So:

test_sequential_write.py

Objective:

Can I write every address?
test_sequential_read.py

Objective:

Does every address return the expected data?

If something fails later, it's much easier to isolate the problem.

For example:

If test_sequential_write.py fails, you investigate the write path.
If test_sequential_write.py passes but test_sequential_read.py fails, you focus on the memory storage or read path.
Why did we use:
data = addr + 1

Instead of:

data = 0

or

data = 0xFFFFFFFF

Because each address gets a unique value.

Address	Data
0	     1
1	     2
2	     3
...	     ...
31	    32

Imagine we later read:

Address 17
Expected: 18
Received: 5

We immediately know:

Address 17 is wrong.
The wrong value matches what should have been at another address.
That can point to an addressing or indexing bug.

If every address contained 0, we wouldn't be able to detect those kinds of issues.


Why is this version better?( By using initialize_memory_pattern coroutine function in tb_utils.py)


Professional Verification Principle

A test should answer what is being verified.

The helper functions answer how to perform it.



A coroutine function is a specialized function that can pause its execution and yield control back to a caller or event loop, then resume exactly where it left off


Before

Your test contained all the implementation details:

await reset_dut(dut)

for addr in range(32):

    data = addr + 1

    ...

    await apb_write(...)

The test was doing two jobs:

Describing the verification objective.
Implementing the memory initialization.
Now

Your test simply says:

await reset_dut(dut)

await initialize_memory_pattern(dut)

Immediately, another engineer understands the intent.

The implementation details are hidden inside the helper.

This is called abstraction.

This is exactly how commercial DV code evolves

Instead of this:

Test
 ├── for loop
 ├── write
 ├── write
 ├── write
 ├── write
 └── write

It becomes

Test
 │
 ├── Reset DUT
 │
 ├── Initialize Memory
 │
 └── Verify Objective

The helper handles all the repetitive work.
