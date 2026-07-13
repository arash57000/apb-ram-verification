Phase 5 Progress
✅ Directed Test #2 Complete

Test: test_addr31.py

Verification Objective:

✔ Start APB clock
✔ Reset DUT
✔ Write to the highest valid address (31)
✔ Read from address 31
✔ Verify the returned data matches the written data



Why these two tests matter

Together, test_addr0.py and test_addr31.py perform boundary value testing.

For a 32-entry RAM:

Valid Addresses

0 --------------------------------------------- 31
^                                               ^
|                                               |
Lowest valid address                    Highest valid address

Boundary tests are important because many RTL bugs occur at the edges of valid ranges, such as off-by-one errors, incorrect address decoding, or array indexing mistakes.
