Final Phase 5 Test Summary
test_write_read_immediate.py
Verification Objective

Verify that data written to a valid RAM address can be read back immediately in the next APB transaction.

Test Flow
Reset DUT
      │
      ▼
Write Address 20 = 0xDEADBEEF
      │
      ▼
Immediately Read Address 20
      │
      ▼
Compare Data
      │
      ▼
PASS
Why is this test important?

This models a very common software/firmware access pattern:

write_register(...);
value = read_register(...);

Firmware often writes a configuration value and immediately reads it back to confirm the write succeeded.

Your test confirms that the APB RAM supports this expected behavior.

What did this test verify?
✅ APB write transaction
✅ APB read transaction
✅ Memory update
✅ Immediate data availability
✅ Correct read-after-write behavior

Phase 5 Final Test Suite



Total Directed Tests: 10 / 10 ✅
